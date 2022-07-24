from graph.Graph import Graph
from circuit.NetList import NetList
from components.COMPONENT import COMPONENT
from components.Resistor import Resistor
from components.Cell import Cell


class CircuitManager:
    def __init__(self, circuit=None):
        self.circuit = circuit
        self._component_id = 0

    def CreateCircuitFromNetListFile(self, net_list_file):
        net_list = NetList(net_list_file)

        components = net_list.GetComponents()
        left_nodes = net_list.GetLeftNodes()
        right_nodes = net_list.GetRightNodes()
        values = net_list.GetValues()

        max_node = max(max(left_nodes), max(right_nodes))

        for node in range(max_node + 1):
            self.circuit.AddNode(node)

        for index in range(len(left_nodes)):
            component_type = components[index][0]
            component_class = None

            if component_type == COMPONENT.RESISTOR.value:
                component_class = Resistor(resistance=values[index])

            elif component_type == COMPONENT.CELL.value:
                component_class = Cell(potential_difference=values[index])

            self.circuit.AddEdge(left_nodes[index], right_nodes[index], component_class)

    def GetComponents(self):
        return self.circuit.GetEdgeAttributes('value')

    def AddComponent(self, component):
        pass


if __name__ == "__main__":
    circuit = Graph()
    circuit_manager = CircuitManager(circuit)
    circuit_manager.CreateCircuitFromNetListFile("../testing/Circuit1.txt")
    circuit_manager.circuit.Show()
