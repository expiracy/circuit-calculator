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

        return self.paths.copy()

    def SortLoops(self):
        self.paths = list(sorted(self.paths, key=len))

    def FindAllLoops(self):
        nodes = list(self.circuit.GetNodes())
        start_and_end_node = nodes[0]
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

    def FindPathsThroughComponent(self, current_component, next_start_node):
        if not current_component.edge[0] == next_start_node:
            current_component = current_component.Reverse()

            if current_component.paths:
                return current_component

        outer_series_group = self.component_manager.IsSeriesGroup(current_component)
        outer_parallel_branch = self.component_manager.IsParallelBranch(current_component)

        if not current_component.GetGroupings():
            if outer_parallel_branch:
                current_component.paths = [[component] for component in current_component.components]

            elif outer_series_group:
                current_component.paths = [current_component.components]

            return current_component

        current_component_with_inner_paths = self.FindAllInnerPathsOfGrouping(current_component,
                                                                              outer_series_group,
                                                                              outer_parallel_branch,
                                                                              next_start_node)

        current_component_with_paths = self.SetComponentPaths(current_component_with_inner_paths,
                                                              outer_series_group,
                                                              outer_parallel_branch)

        return current_component_with_paths

    def FindAllInnerPathsOfGrouping(self, current_component, outer_series_group, outer_parallel_branch, last_start_node):
        components_with_paths = []

        if outer_series_group:
            all_nodes = current_component.GetAllNodes()

            for node_index in range(len(all_nodes) - 1):
                edge = (all_nodes[node_index], all_nodes[node_index + 1])

                component = current_component.FindComponentWithEdge(edge)

                if self.component_manager.IsGrouping(component):
                    component_with_paths = self.FindPathsThroughComponent(component, edge[0])

                    components_with_paths.append(component_with_paths)

                else:
                    components_with_paths.append(component)

        else:
            for component in current_component.components:
                if self.component_manager.IsGrouping(component):
                    if outer_parallel_branch:
                        component_with_paths = self.FindPathsThroughComponent(component, last_start_node)

                    else:
                        edge = current_component.edge[:2]

                        if edge[0] != last_start_node:
                            next_start_node = edge[0]

                        else:
                            next_start_node = edge[1]

                        component_with_paths = self.FindPathsThroughComponent(component, next_start_node)

                    components_with_paths.append(component_with_paths)

                else:
                    components_with_paths.append(component)

        current_component.components = components_with_paths

        return current_component

    def SetComponentPaths(self, current_component, outer_series_group, outer_parallel_branch):
        self.paths = []
        components = current_component.components

        for component in components:
            inner_series_group = self.component_manager.IsSeriesGroup(component)
            inner_parallel_branch = self.component_manager.IsParallelBranch(component)

            if outer_series_group:
                if inner_series_group:
                    self.ExtendSeriesPathsWithSeriesGroup(component)

                elif inner_parallel_branch:
                    self.ExtendSeriesPathsWithParallelBranch(component)

                else:
                    self.ExtendSeriesPathsWithComponent(component)

            elif outer_parallel_branch:
                if inner_series_group or inner_parallel_branch:
                    self.ExtendParallelPathsWithGrouping(component)

                else:
                    self.ExtendParallelPathsWithComponent(component)

        current_component.paths = self.paths

        return current_component

    def ExtendSeriesPathsWithSeriesGroup(self, component):
        for component_path in component.paths:
            if self.paths:
                for path in self.paths:
                    path += component_path

            else:
                self.paths.append(component_path)

        return self

    def ExtendSeriesPathsWithParallelBranch(self, component):
        old_paths = self.paths.copy()
        self.paths = []

        for component_path in component.paths:

            if old_paths:
                for old_path in old_paths:
                    new_path = old_path + component_path
                    self.paths.append(new_path)

            else:
                self.paths.append(component_path)

        return self

    def ExtendSeriesPathsWithComponent(self, component):
        if self.paths:
            for path in self.paths:
                path += [component]

        else:
            self.paths.append([component])

        return self

    def ExtendParallelPathsWithGrouping(self, component):
        for component_path in component.paths:
            self.paths.append(component_path)

        return self

    def ExtendParallelPathsWithComponent(self, component):
        self.paths.append([component])

        return self

    def GetPathsForLoops(self):
        loops = self.FindLoops()

        loop_paths = {}

        for loop_index in range(len(loops)):
            loop = loops[loop_index]
            loop_paths[tuple(loop)] = {}

            for node_index in range(len(loop) - 1):
                edge = (loop[node_index], loop[node_index + 1])
                loop_paths[tuple(loop)][edge] = []

                edge_paths = loop_paths[tuple(loop)][edge]

                component = self.component_manager.GetComponentsForEdge(edge)[0]

                if self.component_manager.IsGrouping(component):
                    component_with_paths = self.FindPathsThroughComponent(component, edge[0])

                    #self.OutputPathsForComponent(component_with_paths)

                    edge_paths += component_with_paths.paths

                else:
                    edge_paths.append([component])

        return loop_paths

    def OutputPathsForComponent(self, component):
        paths = []

        for path in component.paths:
            string_path = []

            for path_component in path:
                if self.component_manager.IsCell(path_component):
                    string_path.append(path_component.potential_difference)

                else:
                    string_path.append(path_component.resistance)

            paths.append(string_path)

        for path in paths:
            print(f"EDGE: {component.edge} PATH: {path}\n")


