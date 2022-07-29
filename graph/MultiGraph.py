import matplotlib.pyplot as plt
from graph.Graph import Graph
import networkx as nx


class MultiGraph(Graph):
    def __init__(self, graph=None):
        super().__init__()

        if graph is None:
            self._graph = nx.MultiGraph()
        else:
            self._graph = graph

    def Show(self):
        pos = nx.spring_layout(self._graph)
        nx.draw(self._graph, pos, with_labels=True)

        edge_and_count = {}
        edge_ids_for_edges = self.GetEdgeIDsForEdges()

        for edge, edge_ids in edge_ids_for_edges.items():
            edge_and_count[edge] = len(edge_ids)

        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=edge_and_count)

        plt.show()

    def GetEdgeIDsForEdges(self):
        edge_ids_for_edges = {}

        for u, v, d in self.GetEdges():
            try:
                edge_ids_for_edges[(u, v)]
            except KeyError:
                edge_ids_for_edges[(u, v)] = []

            edge_ids_for_edges[(u, v)].append(d)

        return edge_ids_for_edges
