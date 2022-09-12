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
                    self.FindPaths([], [component])

                self.equations[loop_index].append(component)

    def FindPaths(self, paths, stack):
        pass









