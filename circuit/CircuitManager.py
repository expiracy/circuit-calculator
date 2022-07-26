from graph.Graph import Graph
from graph.DiGraph import DiGraph
from graph.MultiGraph import MultiGraph
from graph.MultiDiGraph import MultiDiGraph
# from solver.LoopFinder import LoopFinder
from circuit.NetList import NetList
from components.COMPONENT import COMPONENT
from components.Resistor import Resistor
from components.Cell import Cell


class CircuitManager:
    def __init__(self, circuit=None):
        self.circuit = circuit
        self._component_id = 0

    def Main(self):
        pass

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

    def AssignCurrentDirections(self):
        loop_finder = LoopFinder(self.circuit)

        self.circuit.Show()

        circuit = MultiDiGraph()
        print(loop_finder.loops)

        for loop in loop_finder.loops:
            for index in range(len(loop) - 1):
                component = (loop[index], loop[index + 1])

                components = circuit.GetEdges()

                if not (component in components or component[::-1] in components):
                    circuit.AddEdge(*component)

        print("Test")

    def GetComponents(self):
        return self.circuit.GetEdgeAttributes('value')

    def AddComponent(self, component):
        pass


if __name__ == "__main__":
    circuit_manager = CircuitManager(MultiGraph())
    circuit_manager.CreateCircuitFromNetListFile("../testing/Circuit2.txt")
    circuit_manager.AssignCurrentDirections()
