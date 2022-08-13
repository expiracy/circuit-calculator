from graph.MultiGraph import MultiGraph
from circuit.NetList import NetList
from circuit.CurrentManager import CurrentManager
from circuit.topology.JunctionsManager import JunctionsManager
from circuit.ComponentManager import ComponentManager
from circuit.topology.TopologyManager import TopologyManager


class CircuitManager:
    def __init__(self, circuit=None):
        self.circuit = circuit
        self.loops = []

        self.component_manager = ComponentManager(self.circuit)
        self.junction_manager = JunctionsManager(self.circuit)
        self.current_manager = CurrentManager(self.circuit, self.junction_manager, self.component_manager)
        self.topology_manager = TopologyManager(self.circuit, self.junction_manager)

    def Main(self, file):
        self.CreateCircuitFromNetListFile(file)
        self.junction_manager.InitialiseJunctions()

        # self.loops = LoopFinder(self.circuit).FindLoops()
        # self.current_manager.AssignCurrentDirections(self.loops)

        self.topology_manager.GroupSeriesComponents()

        return self

    def AddComponentToCircuit(self, left_node, right_node, component_type, value):
        component_class = self.component_manager.CreateComponent(component_type, value)

        attribute = {'component': component_class}

        self.circuit.AddEdge(left_node, right_node, **attribute)

    def CreateCircuitFromNetListFile(self, net_list_file):
        net_list = NetList().LoadFile(net_list_file)

        components_details = net_list.GetComponentsDetails()

        for component_details in components_details:
            self.AddComponentToCircuit(**component_details)

        self.component_manager.SetComponentEdges()

        return self


if __name__ == "__main__":
    circuit = MultiGraph()
    file = "../testing/Circuit6.txt"
    circuit_manager = CircuitManager(circuit).Main(file)
