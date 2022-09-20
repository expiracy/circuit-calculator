from graph.Graph import Graph
from graph.MultiGraph import MultiGraph
from circuit.ComponentManager import ComponentManager
from components.PathComponent import PathComponent
from components.Paths import Paths
import random as rd


class PathFinder:
    def __init__(self, circuit):
        self.circuit = circuit
        self.component_manager = ComponentManager(circuit)

        paths = Paths()
        self.paths = paths.paths

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

        node = nodes[0]

        loops_for_node = [[node] + path for path in self.circuit.DFS(node, node)]

        self.paths += loops_for_node

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

    def GetEdgePathsForLoop(self):
        loops = self.FindLoops()

        edge_paths_for_loops = {}

        for loop_index in range(len(loops)):
            loop = loops[loop_index]
            loop_tuple = tuple(loop)

            edge_paths_for_loops[loop_tuple] = {}

            for node_index in range(len(loop) - 1):
                edge = (loop[node_index], loop[node_index + 1])

                paths = Paths()

                if tuple(reversed(edge)) in edge_paths_for_loops[loop_tuple].keys():
                    paths.direction = '-'

                edge_paths_for_loops[loop_tuple][edge] = paths
                edge_paths = edge_paths_for_loops[loop_tuple][edge].paths

                component = self.component_manager.GetComponentsForEdge(edge)[0]

                if self.component_manager.IsGrouping(component):
                    component_with_paths = self.FindPathsThroughComponent(component, edge[0])

                    #self.OutputPathsForComponent(component_with_paths)

                    edge_paths += component_with_paths.paths

                else:
                    edge_paths.append([component])

        return edge_paths_for_loops

    def RemoveInvalidLoopsPaths(self, loops_paths):
        valid_loops_paths = []

        for loop_path in loops_paths:
            component_and_count = {}

            valid = True

            for path_component in loop_path:
                component = path_component.component

                if component not in component_and_count.keys():
                    component_and_count[component] = 1

                else:
                    valid = False

            if valid and list(reversed(loop_path)) not in valid_loops_paths:
                valid_loops_paths.append(loop_path)

        return valid_loops_paths

    def GetLoopsPaths(self):
        edge_paths_for_loops = self.GetEdgePathsForLoop()
        self.OutputEdgePathsForLoops(edge_paths_for_loops)

        loops_paths = []

        for loop, edge_and_paths in edge_paths_for_loops.items():
            loop_paths = []

            for edge, paths in edge_and_paths.items():
                direction = paths.direction
                paths = paths.paths

                loop_paths = self.CreateLoopPaths(paths, loop_paths, direction)

            loops_paths += loop_paths

        loops_paths = self.RemoveInvalidLoopsPaths(loops_paths)

        self.OutputLoopsPaths(loops_paths)

        return loops_paths

    def CreateLoopPaths(self, paths, loop_paths, direction):
        path_component_paths = []

        for path_index in range(len(paths)):
            path_component_paths.append([])

            for component in paths[path_index]:
                path_component = PathComponent(component, direction)
                path_component_paths[path_index].append(path_component)

        if loop_paths:
            old_loop_paths = loop_paths.copy()
            loop_paths = []

            for old_loop_path in old_loop_paths:
                for path_component_path in path_component_paths:
                    extended_path = old_loop_path + path_component_path

                    loop_paths.append(extended_path)

        else:
            loop_paths += path_component_paths

        return loop_paths

    def OutputPathsForComponent(self, component):
        paths = []

        for path in component.paths:
            value_path = self.GetValueListFromComponentList(path)

            paths.append(value_path)

        for path in paths:
            print(f"EDGE: {component.edge} PATH: {path}\n")

    def OutputEdgePathsForLoops(self, loop_paths):
        print("--------------------------------------------------------------------")

        for loop, edge_and_paths in loop_paths.items():
            print(f"LOOP: {loop}:")

            for edge, paths in edge_and_paths.items():
                print(f"EDGE: {edge} DIRECTION: {paths.direction}")

                value_paths = []

                for path in paths.paths:
                    value_path = self.GetValueListFromComponentList(path)

                    value_paths.append(value_path)

                print(value_paths)

            print("--------------------------------------------------------------------")

    def OutputLoopsPaths(self, loops_paths):
        for loop_path in loops_paths:
            value_list = []

            for component in loop_path:
                if self.component_manager.IsCell(component.component):
                    value_list.append(component.component.potential_difference)

                else:
                    value_list.append(component.component.resistance)

            print(value_list)

    def GetValueListFromComponentList(self, component_list):
        value_list = []

        for component in component_list:
            if self.component_manager.IsCell(component):
                value_list.append(component.potential_difference)

            else:
                value_list.append(component.resistance)

        return value_list




