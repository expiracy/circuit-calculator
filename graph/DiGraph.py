import Graph
import networkx as nx


class DiGraph(Graph):
    def __init__(self):
        super().__init__()
        self._Graph = nx.DiGraph()
