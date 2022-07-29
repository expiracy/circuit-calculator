from graph.Graph import Graph
from graph.MultiGraph import MultiGraph


class LoopFinder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.loops = []

    def FindLoops(self):
        self.FindAllLoops()
        self.RemoveDuplicateLoops()
        self.RemoveInvalidLoops()

        return self.loops

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

    def RemoveInvalidLoops(self):
        component_ids_for_edges = self.circuit.GetEdgeIDsForEdges()

        for loop in self.loops[:]:
            if len(loop) == 3:
                for node in range(len(loop) - 1):
                    edge = (loop[node], loop[node + 1])

                    try:
                        component_ids_for_edge = component_ids_for_edges[edge]
                    except KeyError:
                        edge = tuple(reversed(edge))
                        component_ids_for_edge = component_ids_for_edges[edge]

                    if len(component_ids_for_edge) < 2:
                        self.loops.remove(loop)

                        break

        return self



