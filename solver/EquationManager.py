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
        loop_paths = self.path_finder.GetPathsForLoops()

        self.OutputLoopPaths(loop_paths)

    def OutputLoopPaths(self, loop_paths):
        for loop, edge_and_paths in loop_paths.items():
            print("----------------------------------------------")
            print(f"LOOP: {loop}")

            for edge, paths in edge_and_paths.items():
                print(f"EDGE: {edge}")

                value_paths = []

                for path in paths:
                    value_path = []

                    for component in path:
                        if self.component_manager.IsCell(component):
                            value_path.append(component.potential_difference)

                        else:
                            value_path.append(component.resistance)

                    value_paths.append(value_path)

                print(value_paths)




