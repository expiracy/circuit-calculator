import matplotlib.pyplot as plt
from graph.Graph import Graph
import networkx as nx


class MultiDiGraph(Graph):
    def __init__(self, graph=None):
        super().__init__()

        if graph is None:
            self._graph = nx.MultiDiGraph()
        else:
            self._graph = graph
