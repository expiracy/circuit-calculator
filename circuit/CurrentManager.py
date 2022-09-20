from circuit.topology.PathFinder import PathFinder
from circuit.Current import Current
import sympy as sym

class CurrentManager:
    def __init__(self, circuit=None, topology_manager=None, junction_manager=None, component_manager=None):
        self.circuit = circuit

        self.topology_manager = topology_manager
        self.junction_manager = junction_manager
        self.component_manager = component_manager

        self.available_current_symbols = list(map(chr, range(97, 123)))

        self.current_id = 0

    def GenerateNewCurrent(self):
        self.current_id += 1
        symbol = self.available_current_symbols[self.current_id - 1]
        current = Current(self.current_id)

        current.SetSymbol(symbol)

        return current

    def AssignCurrents(self, components, current=None, outer_parallel_branch=False):
        if current is None and outer_parallel_branch is False:
            current = self.GenerateNewCurrent()

        for component in components:
            if outer_parallel_branch:
                current = self.GenerateNewCurrent()

            component.current = current

            inner_series_group = self.component_manager.IsSeriesGroup(component)
            inner_parallel_branch = self.component_manager.IsParallelBranch(component)

            if inner_parallel_branch:
                self.AssignCurrents(component.components, None, True)

            elif inner_series_group:
                self.AssignCurrents(component.components, current, False)

        return self




