import matplotlib.pyplot as plt
from graph.MultiGraph import MultiGraph
from graph.DiGraph import DiGraph
import networkx as nx


class MultiDiGraph(MultiGraph, DiGraph):
    def __init__(self, graph=None):
        super(MultiDiGraph).__init__()

        if graph is None:
            self._graph = nx.MultiDiGraph()
        else:
            self._graph = graph
