import components.ParallelBranch
from circuit.topology.PathFinder import PathFinder
from circuit.topology.TopologyManager import TopologyManager


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
                    component = self.path_finder.FindPathsThroughComponent(component, edge[0])

                    self.OutputPathsForComponent(component)

                self.equations[loop_index].append(component)

        print("test")

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
