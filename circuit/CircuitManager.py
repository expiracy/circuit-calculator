from graph.MultiGraph import MultiGraph
from circuit.NetList import NetList
from circuit.CurrentManager import CurrentManager
from circuit.ComponentManager import ComponentManager
from circuit.topology.JunctionsManager import JunctionsManager
from circuit.topology.TopologyManager import TopologyManager
from solver.EquationManager import EquationManager


class CircuitManager:
    def __init__(self, circuit=None):
        self.circuit = circuit
        self.loops = []

        self.component_manager = ComponentManager(self.circuit)

        self.junction_manager = JunctionsManager(self.circuit)

        self.topology_manager = TopologyManager(self.circuit,
                                                JunctionsManager(self.circuit),
                                                ComponentManager(self.circuit))

        self.current_manager = CurrentManager(self.circuit,
                                              self.topology_manager,
                                              self.junction_manager,
                                              self.component_manager)

    def Main(self, file):
        self.CreateCircuitFromNetListFile(file)

        self.topology_manager.SimplifyTopology()

        self.current_manager.AssignCurrents(self.topology_manager.components)
        #self.current_manager.SimplifyCurrents(self.topology_manager.components)

        equation_manager = EquationManager(self.topology_manager.circuit,
                                           ComponentManager(self.topology_manager.circuit),
                                           self.topology_manager,
                                           self.junction_manager)

        equations = equation_manager.FindEquations()

        return self

    def AddComponentToCircuit(self, left_node, right_node, component_type, value):
        component_class = self.component_manager.CreateComponent(component_type, value)

        if left_node[-1] == '+':
            left_node = int(left_node[:-1])
            component_class.positive_terminal = left_node

        elif right_node[-1] == '+':
            right_node = int(right_node[:-1])
            component_class.positive_terminal = right_node

        attribute = {'component': component_class}

        self.circuit.AddEdge(int(left_node), int(right_node), **attribute)

    def CreateCircuitFromNetListFile(self, net_list_file):
        net_list = NetList().LoadFile(net_list_file)

        components_details = net_list.GetComponentsDetails()

        for component_details in components_details:
            self.AddComponentToCircuit(**component_details)

        self.component_manager.SetComponentEdges()

        test = self.circuit.GetEdgeAttributes('component')

        return self

    def GetComponentsOnLoop(self, loop):
        components_on_loop = []

        for node_index in range(len(loop) - 1):
            edge = (loop[node_index], loop[node_index + 1])

            components_for_edge = self.component_manager.GetComponentsForEdge(edge)

            components_on_loop.append(components_for_edge)

        return components_on_loop

    def CreateCircuitFromComponents(self, components):
        for component in components:
            print(component)


if __name__ == "__main__":
    circuit = MultiGraph()
    file = "../testing/Circuit9.txt"
    circuit_manager = CircuitManager(circuit).Main(file)
