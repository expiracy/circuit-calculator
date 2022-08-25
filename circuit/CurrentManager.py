from circuit.topology.PathFinder import PathFinder


class CurrentManager:
    def __init__(self, circuit=None, topology_manager=None, junction_manager=None, component_manager=None):
        self.circuit = circuit

        self.topology_manager = topology_manager
        self.junction_manager = junction_manager
        self.component_manager = component_manager

    def AssignCurrentDirections(self, components):
        groupings = ["S", "P"]

        for component in components:
            if self.component_manager.IsGrouping(component):
                self.AssignCurrentDirections(component.components)

    def AssignCurrentDirections(self):
        loop_finder = PathFinder(self.circuit)

        components = self.topology_manager.components

        for component in components:
            for branch in component.components:
                if branch.component.value == "S":
                    path = loop_finder.FindPathBetweenAndThrough(branch.edge[0], branch.edge[1], branch.nodes)

                    print(path)

    def AssignParallelBranchCurrent(self, parallel_branch):
        pass

    def AssignSeriesGroupCurrent(self):
        pass
