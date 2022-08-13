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
            if not (u, v) in edge_ids_for_edges.keys():
                edge_ids_for_edges[(u, v)] = []

            edge_ids_for_edges[(u, v)].append(d)

        return edge_ids_for_edges

    def GetEdgesWithIDForNode(self, node):
        edges_for_node_with_id = []

        edges_and_counts = self.GetEdgesAndCountsForNode(node)

        for edge, count in edges_and_counts.items():

            for edge_id in range(count):
                full_edge = edge + (edge_id,)
                edges_for_node_with_id.append(full_edge)

        return edges_for_node_with_id

    def GetEdgesAndCountsForNode(self, node):
        edges_and_counts = {}

        for edge in self.GetEdgesForNode(node):
            if edge in edges_and_counts.keys():
                edges_and_counts[edge] += 1

            else:
                edges_and_counts[edge] = 1

        return edges_and_counts
