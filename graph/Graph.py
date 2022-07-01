import networkx as nx
import matplotlib.pyplot as plt
from components.Resistor import Resistor
from components.COMPONENT import COMPONENT


class Graph:
    def __init__(self):
        self._graph = nx.Graph()

    def Show(self, node_size=1000, labels=None):

        nx.draw(self._graph, node_size=node_size, labels=labels)

        plt.show()

    def AddNode(self, node):
        self._graph.add_node(node)

    def AddNodes(self, node_list):
        self._graph.add_nodes_from(node_list)

    def AddEdge(self, start, end, attribute):
        self._graph.add_edge(start, end, value=attribute)

    def AddEdgesFrom(self, edge_list):
        self._graph.add_edges_from(edge_list)

    def GetEdgeAttributes(self, name):
        return nx.get_edge_attributes(self._graph, name)

    def SetEdgeAttributes(self, attributes_for_edges):
        nx.set_edge_attributes(self._graph, attributes_for_edges)

    def SetNodeAttributes(self, attributes_for_nodes, name):
        nx.set_node_attributes(self._graph, attributes_for_nodes, name)

    def GetNodeAttributes(self, name):
        return nx.get_node_attributes(self._graph, name)

if __name__ == "__main__":
    graph = Graph()
    graph.AddNodes([1, 2, 3, 4, 5, 6, 7])
    graph.AddEdgesFrom([(1, 2), (1, 4), (1, 6), (2, 3), (4, 5), (4, 6), (6, 7), (5, 7), (3, 5), (3, 7)])

    # adding attributes
    components = {
        1: COMPONENT.CELL,
        2: COMPONENT.RESISTOR,
        3: COMPONENT.RESISTOR,
        4: COMPONENT.LAMP,
        5: COMPONENT.RESISTOR,
        6: COMPONENT.RESISTOR,
        7: COMPONENT.RESISTOR,
    }

    graph.SetNodeAttributes(components, COMPONENT)
    epic = graph.GetNodeAttributes(COMPONENT)

    graph.Show()

    print("test")
