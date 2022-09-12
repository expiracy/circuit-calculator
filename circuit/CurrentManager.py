from circuit.topology.PathFinder import PathFinder
from circuit.Current import Current


class CurrentManager:
    def __init__(self, circuit=None, topology_manager=None, junction_manager=None, component_manager=None):
        self.circuit = circuit

        self.topology_manager = topology_manager
        self.junction_manager = junction_manager
        self.component_manager = component_manager

        self.current_id = 0

    def GenerateNewCurrent(self):
        self.current_id += 1
        current = Current(self.current_id)

        return current

    def AssignCurrentDirections(self, components, current=None, is_parallel_branch=False):
        if current is None and is_parallel_branch is False:
            current = self.GenerateNewCurrent()

        for component in components:
            if is_parallel_branch:
                current = self.GenerateNewCurrent()

            component.current = current

            if self.component_manager.IsParallelBranch(component):
                self.AssignCurrentDirections(component.components, None, True)

            elif self.component_manager.IsSeriesGroup(component):
                self.AssignCurrentDirections(component.components, current, False)

        return self
