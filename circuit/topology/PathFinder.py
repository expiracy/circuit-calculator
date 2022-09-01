from graph.Graph import Graph
from graph.MultiGraph import MultiGraph


class PathFinder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.paths = []

    def FindPathBetweenAndThrough(self, node_1, node_2, through_nodes):
        self.paths = []

        all_paths = [[node_1] + path for path in self.circuit.DFS(node_1, node_2)]

        through_nodes = list(sorted(through_nodes))
        sorted_paths = []

        for path in all_paths:
            sorted_paths.append(list(sorted(path)))

        for path in sorted_paths:
            if through_nodes in path:
                index = sorted_paths.index(path)
                self.paths.append(all_paths[index])

        return self.paths

    def GetComponentsBetweenNodes(self, node_1, node_2):
        all_paths = [[node_1] + path for path in self.circuit.DFS(node_1, node_2)]

        return all_paths

    def FindLoops(self):
        self.FindAllLoops()
        self.RemoveDuplicateLoops()
        self.RemoveInvalidLoops()

        return self.paths

    def SortLoops(self):
        self.paths = list(sorted(self.paths, key=len))

    def FindAllLoops(self):
        self.paths = [[0] + path for path in self.circuit.DFS(0, 0)]

        self.RemoveDuplicateLoops()

        return self.paths

    def RemoveDuplicateLoops(self):
        loops_copy = self.paths.copy()

        self.paths = []

        for loop in loops_copy:
            if loop[::-1] not in self.paths:
                self.paths.append(loop)

        return self

    def RemoveInvalidLoops(self):
        component_ids_for_edges = self.circuit.GetEdgeIDsForEdges()

        for loop in self.paths[:]:
            if len(loop) == 3:
                for node in range(len(loop) - 1):
                    edge = (loop[node], loop[node + 1])

                    if edge not in component_ids_for_edges.keys():
                        edge = tuple(reversed(edge))

                    component_ids_for_edge = component_ids_for_edges[edge]

                    if len(component_ids_for_edge) < 2:
                        self.paths.remove(loop)

                        break

        return self

    def GetSimpleLoops(self, series_group_nodes):
        sorted_simple_loops = []
        simple_loops = []

        loops = PathFinder(self.circuit).FindLoops()

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
