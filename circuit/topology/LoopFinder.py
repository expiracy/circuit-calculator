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
        self.SortLoops()

        return self.loops

    def SortLoops(self):
        self.loops = list(sorted(self.loops, key=len))

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

                    if edge not in component_ids_for_edges.keys():
                        edge = tuple(reversed(edge))

                    component_ids_for_edge = component_ids_for_edges[edge]

                    if len(component_ids_for_edge) < 2:
                        self.loops.remove(loop)

                        break

        return self

    def GetSimpleLoops(self, series_group_nodes):
        sorted_simple_loops = []
        simple_loops = []

        loops = LoopFinder(self.circuit).FindLoops()

        series_nodes = [node for nodes in series_group_nodes for node in nodes]

        for loop in loops:
            simple_loop = []

            for node in loop:
                if node not in series_nodes:
                    simple_loop.append(node)

            sorted_simple_loop = list(sorted(simple_loop))

            if sorted_simple_loop not in sorted_simple_loops:
                simple_loops.append(simple_loop)
                sorted_simple_loops.append(sorted_simple_loop)

        return simple_loops
