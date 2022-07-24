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

    def GetAdjacencyList(self):
        return self._graph.adj

    def GetAdjacencyMatrix(self):
        return nx.to_scipy_sparse_matrix(self._graph).todense()

    def DFS(self, start, end):
        fringe = [(start, [])]

        while fringe:
            state, path = fringe.pop()
            if path and state == end:
                yield path
                continue

            for next_state in self.GetAdjacencyList()[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path + [next_state]))
