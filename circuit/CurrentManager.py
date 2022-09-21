from circuit.Current import Current


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

        current.symbol = symbol

        return current

    def AssignCurrents(self, components, current=None, outer_parallel_branch=False):
        if current is None and outer_parallel_branch is False:
            current = self.GenerateNewCurrent()

        for component in components:
            if outer_parallel_branch:
                new_current = self.GenerateNewCurrent()
                component.current = new_current

                current.components.append(new_current)

            else:
                component.current = current

            inner_series_group = self.component_manager.IsSeriesGroup(component)
            inner_parallel_branch = self.component_manager.IsParallelBranch(component)

            if inner_parallel_branch:
                self.AssignCurrents(component.components, component.current, True)

            elif inner_series_group:
                self.AssignCurrents(component.components, component.current, False)

        return self

    def SetCurrentValues(self, solutions):
        print(solutions)
        components = self.component_manager.GetComponents()

        for component in components:
            symbol = str(component.current.symbol)

            if symbol in solutions.keys():
                component.current.value = solutions[symbol]

            else:
                component.current.value = 0

        return self







