from graph.Graph import Graph
from graph.MultiGraph import MultiGraph
from circuit.ComponentManager import ComponentManager
import random as rd


class PathFinder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.component_manager = ComponentManager(circuit)
        self.paths = []

    def FindPathsBetween(self, node_1, node_2):
        paths = [[] + path[:-1] for path in self.circuit.DFS(node_1, node_2)]

        return paths

    def FindLoops(self):
        self.FindAllLoops()
        self.RemoveDuplicateLoops()
        self.RemoveInvalidLoops()

        return self.paths

    def SortLoops(self):
        self.paths = list(sorted(self.paths, key=len))

    def FindAllLoops(self):
        nodes = list(self.circuit.GetNodes())
        random_index = rd.randint(0, len(nodes) - 1)
        start_and_end_node = nodes[random_index]

        self.paths = [[start_and_end_node] + path for path in self.circuit.DFS(start_and_end_node, start_and_end_node)]

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
        for loop in self.paths[:]:
            if len(loop) == 3:
                if self.IsShortLoopValid(loop) is False:
                    self.paths.remove(loop)

        return self

    def IsShortLoopValid(self, loop):
        edge = (loop[0], loop[1])

        component_ids_for_edges = self.circuit.GetEdgeIDsForEdges()

        if edge not in component_ids_for_edges.keys():
            edge = tuple(reversed(edge))

        component_ids_for_edge = component_ids_for_edges[edge]

        if len(component_ids_for_edge) < 2:
            component = self.component_manager.GetComponentsForEdge(edge)[0]

            if not self.component_manager.IsParallelBranch(component):
                return False

        return True

