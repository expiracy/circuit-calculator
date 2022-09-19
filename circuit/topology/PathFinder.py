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

    def FindPathsThroughComponent(self, current_component):
        outer_series_group = self.component_manager.IsSeriesGroup(current_component)
        outer_parallel_branch = self.component_manager.IsParallelBranch(current_component)

        if not current_component.GetGroupings():
            if outer_parallel_branch:
                current_component.paths = [[component] for component in current_component.components]

            elif outer_series_group:
                current_component.paths = [current_component.components]

            return current_component

        components = current_component.components

        components_with_paths = []

        for component in components:
            if self.component_manager.IsGrouping(component):
                component_with_path = self.FindPathsThroughComponent(component)

                components_with_paths.append(component_with_path)

            else:
                components_with_paths.append(component)

        current_component.components = components_with_paths

        paths = []

        for component in components:
            inner_series_group = self.component_manager.IsSeriesGroup(component)
            inner_parallel_branch = self.component_manager.IsParallelBranch(component)

            if outer_series_group:
                if inner_series_group:

                    for component_path in component.paths:
                        if paths:
                            for path in paths:
                                path += component_path

                        else:
                            paths.append(component_path)

                elif inner_parallel_branch:
                    old_paths = paths.copy()
                    paths = []

                    for component_path in component.paths:
                        if old_paths:
                            for old_path in old_paths:
                                new_path = old_path + component_path
                                paths.append(new_path)

                        else:
                            paths.append(component_path)

                else:
                    if paths:
                        for path in paths:
                            path += [component]

                    else:
                        paths.append([component])

            elif outer_parallel_branch:
                if inner_series_group or inner_parallel_branch:
                    for path in component.paths:
                        paths.append(path)

                else:
                    paths.append([component])

        current_component.paths = paths

        return current_component

