from circuit.topology.PathFinder import PathFinder


class EquationManager:
    def __init__(self, circuit, component_manager=None, topology_manager=None, junction_manager=None):
        self.circuit = circuit

        self.component_manager = component_manager
        self.topology_manager = topology_manager
        self.junction_manager = junction_manager
        self.path_finder = PathFinder(circuit)

        self.equations = []

    def FindEquations(self):
        loops = self.path_finder.FindLoops()

        for loop_index in range(len(loops)):
            self.equations.append([])

            loop = loops[loop_index]

            for node_index in range(len(loop) - 1):
                edge = (loop[node_index], loop[node_index + 1])

                component = self.component_manager.GetComponentsForEdge(edge)[0]

                if self.component_manager.IsGrouping(component):
                    component = self.FindPath(component)

                self.equations[loop_index].append(component)

        print("test")

    def FindPath(self, current_component):
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
                component_with_path = self.FindPath(component)

                components_with_paths.append(component_with_path)

            else:
                components_with_paths.append(component)

        current_component.components = components_with_paths

        paths = current_component.paths

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

                    for component_path in component.paths:
                        if paths:
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

        return current_component

    def FindPaths(self, component, paths, stack, finished):
        if self.component_manager.IsSeriesGroup(component):
            groupings = component.GetGroupings()

            if not groupings:
                component.paths = [[component.components]]

                finished.append(component)

            else:
                stack.append(groupings)

                self.FindPaths(component, paths, stack, finished)

        elif self.component_manager.IsParallelBranch(component):
            groupings = component.GetSeriesGroups()

            if not groupings:
                component.paths = [[component] for component in component.components]

                finished.append(component)

            else:
                stack.append(groupings)


        next_component = stack.pop()
        self.FindPaths(next_component, paths, stack, finished)











