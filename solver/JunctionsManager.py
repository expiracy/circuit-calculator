from enum import Enum


class DIRECTION(Enum):
    NULL = -1
    IN = 1
    OUT = 0

    def __str__(self):
        return self.name


class JunctionsManager:
    def __init__(self, circuit):
        self.junctions = self.InitialiseJunctions(circuit)

    def InitialiseJunctions(self, circuit):

        print(circuit.GetEdges())

        junctions = {}

        for node in circuit.GetNodes():
            try:
                junctions[node]

            except KeyError:
                junctions[node] = {}

            edges_for_node = circuit.GetEdgesForNode(node)

            edges_and_count = self.GetEdgeAndCountForNode(edges_for_node)

            for edge, count in edges_and_count.items():
                for connected_node in edge:

                    if connected_node != node:

                        for edge_id in range(count):

                            try:
                                junctions[node][connected_node]

                            except KeyError:
                                junctions[node][connected_node] = {}

                            junctions[node][connected_node][edge_id] = DIRECTION.NULL

        circuit.SetNodesAttributes(junctions, 'current_direction')

        print(circuit.GetNodes()[1]['current_direction'])

        print(junctions)

        return junctions

    def GetEdgeAndCountForNode(self, edges_for_node):
        edges_and_counts = {}

        for edge in edges_for_node:
            try:
                edges_and_counts[edge] += 1

            except KeyError:
                edges_and_counts[edge] = 1

        return edges_and_counts

    def SetIntoNodeFrom(self, into_node, from_node):
        self.junctions[into_node][DIRECTION.IN].append(from_node)

        return self
