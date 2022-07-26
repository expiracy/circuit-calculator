from graph.Graph import Graph
from circuit.CircuitManager import CircuitManager
from graph.MultiGraph import MultiGraph


class LoopFinder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.loops = []
        self.FindLoops()

    def FindLoops(self):
        self.FindAllLoops()
        self.RemoveDuplicateLoops()
        self.RemoveInvalidLoops()

    def FindAllLoops(self):
        self.loops = [[0] + path for path in self.circuit.DFS(0, 0)]

        return self

    def RemoveDuplicateLoops(self):
        loops_copy = self.loops.copy()
        self.loops = []

        for loop in loops_copy:
            if loop[::-1] not in self.loops:
                self.loops.append(loop)

        return self

    # check if goes through 2 different components

    def RemoveInvalidLoops(self):
        components_for_edge_and_id = self.circuit.GetEdgeAttributes('value')
        component_ids_for_edges = {}

        for u, v, d in self.circuit.GetEdges():
            try:
                component_ids_for_edges[(u, v)]
            except KeyError:
                component_ids_for_edges[(u, v)] = []

            component_ids_for_edges[(u, v)].append(d)

        invalid_loops = []

        for loop in self.loops:
            if len(loop) == 3:
                components_for_loop = []
                print(loop)
                for node in range(len(loop) - 1):
                    edge = (loop[node], loop[node + 1])

                    try:
                        component_ids_for_edge = component_ids_for_edges[edge]
                    except KeyError:
                        edge = tuple(reversed(edge))
                        component_ids_for_edge = component_ids_for_edges[edge]

                    components = []

                    for component_id in component_ids_for_edge:
                        edge_and_id = edge + (component_id,)

                        try:
                            component = components_for_edge_and_id[edge_and_id]
                        except KeyError:
                            edge_and_id = edge + (component_id,)
                            component = components_for_edge_and_id[edge_and_id]

                        components.append(str(component))

                    components_for_loop.append(components)

                    if len(components) < 2:
                        invalid_loops.append(loop)

                print(components_for_loop)


if __name__ == "__main__":
    circuit_manager = CircuitManager(MultiGraph())
    circuit_manager.CreateCircuitFromNetListFile("./testing/Circuit1.txt")
    loop_finder = LoopFinder(circuit_manager.circuit)
