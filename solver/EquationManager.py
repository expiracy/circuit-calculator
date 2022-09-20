import components.ParallelBranch
from circuit.topology.PathFinder import PathFinder
from circuit.topology.TopologyManager import TopologyManager
import sympy as sym


class EquationManager:
    def __init__(self, circuit, component_manager=None, topology_manager=None, junction_manager=None):
        self.circuit = circuit

        self.component_manager = component_manager
        self.topology_manager = topology_manager
        self.junction_manager = junction_manager
        self.path_finder = PathFinder(circuit)

        self.equations = []

    def FindEquations(self):
        loops_paths = self.path_finder.GetLoopsPaths()

        for path_index in range(len(loops_paths)):
            self.equations.append([])

            for component in loops_paths[path_index]:
                if self.component_manager.IsCell(component):
                    self.equations[path_index].append(component.potential_difference)

                else:
                    self.equations[path_index].append(component.resistance * component.current.symbol)

        print(self.equations)











