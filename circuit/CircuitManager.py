from graph.MultiGraph import MultiGraph
from circuit.NetList import NetList
from circuit.CurrentManager import CurrentManager
from circuit.ComponentManager import ComponentManager
from circuit.topology.JunctionsManager import JunctionsManager
from circuit.topology.TopologyManager import TopologyManager
from solver.EquationManager import EquationManager
from solver.Solver import Solver
import json


class CircuitManager:
    def __init__(self, circuit=None):
        if circuit is None:
            self.circuit = MultiGraph()

        else:
            self.circuit = circuit

        self.component_manager = ComponentManager(self.circuit)

        self.junction_manager = JunctionsManager(self.circuit)

        self.topology_manager = TopologyManager(self.circuit,
                                                JunctionsManager(self.circuit),
                                                ComponentManager(self.circuit))

        self.current_manager = CurrentManager(self.circuit,
                                              self.topology_manager,
                                              self.junction_manager,
                                              self.component_manager)

    def Solve(self):
        self.ConfigureCircuit()

        solutions = self.FindSolutions()

        self.SetComponentValues(solutions)

        json_result = self.GetJSONResults()

        return json_result

    def GetJSONResults(self):
        result = {}

        for component in self.component_manager.GetComponents():
            values = {
                    'potential_difference': str(component.potential_difference),
                    'resistance': str(component.resistance),
                    'current': str(component.current.value)
                      }

            component_name_and_id = f"{component.component} {component.id}"
            result[component_name_and_id] = json.dumps(values)

        return json.dumps(result)

    def ConfigureCircuit(self):
        self.topology_manager.SimplifyTopology()

        self.current_manager.AssignCurrents(self.topology_manager.components)

        return self

    def FindSolutions(self):
        equation_manager = EquationManager(self.topology_manager.circuit,
                                           ComponentManager(self.topology_manager.circuit),
                                           self.topology_manager,
                                           self.junction_manager)

        equations = equation_manager.FindEquations()
        solutions = Solver(equations).Solve()

        return solutions

    def SetComponentValues(self, solutions):
        self.current_manager.SetCurrentValues(solutions)
        self.component_manager.CalculatePotentialDifferences()

        return self

    def AddComponentToCircuit(self, id, left_node, right_node, component_type, value):
        component_class = self.component_manager.CreateComponent(component_type, value, id)

        if left_node[-1] == '+':
            left_node = int(left_node[:-1])
            component_class.positive_terminal = left_node

        elif right_node[-1] == '+':
            right_node = int(right_node[:-1])
            component_class.positive_terminal = right_node

        else:
            component_class.positive_terminal = int(right_node)

        attribute = {'component': component_class}

        self.circuit.AddEdge(int(left_node), int(right_node), **attribute)

    def CreateCircuitFromNetListFile(self, net_list_file):

        net_list = NetList().LoadFile(net_list_file)

        components_details = net_list.GetComponentsDetails()

        for component_details in components_details:
            self.AddComponentToCircuit(**component_details)

        self.component_manager.SetComponentEdges()

        return self

    def CreateCircuitFromComponents(self, components):
        for component in components:
            print(component)


if __name__ == "__main__":
    file = "../data/testing/Circuit10.txt"

    circuit_manager = CircuitManager()
    circuit_manager.CreateCircuitFromNetListFile(file)
    circuit_manager.Solve()