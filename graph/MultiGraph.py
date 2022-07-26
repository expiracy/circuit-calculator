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

        edge_count = {}

        for u, v, d in self._graph.edges:
            try:
                edge_count[(u, v)] += 1

            except:
                edge_count[(u, v)] = 1

        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=edge_count)

        plt.show()
