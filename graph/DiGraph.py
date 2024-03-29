from graph.Graph import Graph
import networkx as nx


class DiGraph(Graph):
    def __init__(self, graph=None):
        super().__init__()

        if graph is None:
            self._graph = nx.DiGraph()
        else:
            self._graph = graph
