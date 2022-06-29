import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self._graph = nx.Graph()

    def Show(self, node_size=1000, with_labels=True):
        # add colours
        nx.draw(self._graph, node_size=node_size, with_labels=with_labels)
        plt.show()

    def AddNode(self, node):
        self._graph.add_node(node)

    def AddNodes(self, node_list):
        self._graph.add_nodes_from(node_list)

    def AddEdge(self, start, end):
        self._graph.add_edge(start, end)

    def AddEdgesFrom(self, edge_list):
        self._graph.add_edges_from(edge_list)


graph = Graph()
graph.AddNodes(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
graph.AddEdgesFrom(
    [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'), ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])
graph.Show()
print("test")
