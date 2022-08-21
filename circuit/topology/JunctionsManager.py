from circuit.topology.Junction import Junction


class JunctionsManager:
    def __init__(self, circuit):
        self.circuit = circuit
        self.junctions = {}

    def InitialiseJunctions(self):
        self.junctions = {}

        for node in self.circuit.GetNodes():
            junction = Junction(node)

            if node not in self.junctions.keys():
                self.junctions[node] = []

            edges_for_node = self.circuit.GetEdgesWithIDForNode(node)
            edges_for_components = self.circuit.GetEdgeAttributes('component')

            for edge in edges_for_node:

                if edge not in edges_for_components.keys():
                    edge = tuple(reversed(edge[:-1])) + (edge[2],)

                component = edges_for_components[edge]
                junction.connected_components.append(component)

            self.junctions[node] = junction

        self.circuit.SetNodesAttributes(self.junctions, 'connected_components')

        return self

    def GetJunctionForNode(self, junction):
        return self.circuit.GetNodeAttributes('connected_components')[junction]

    def GetNeighboursOfJunction(self, junction):
        return self.circuit.GetNeighbourNodes(junction)
