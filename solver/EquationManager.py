import components.ParallelBranch
from circuit.topology.PathFinder import PathFinder
from circuit.topology.TopologyManager import TopologyManager
import sympy as sym
from sympy.parsing.sympy_parser import parse_expr

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

            for path_component in loops_paths[path_index]:
                component = path_component.component

                symbol = component.current.symbol
                direction = path_component.direction

                if self.component_manager.IsCell(component):
                    potential_difference = sym.symbols(f"{direction}{component.potential_difference}")

                else:
                    potential_difference = component.resistance * sym.symbols(f"{direction}{symbol}")

                self.equations[path_index].append(potential_difference)

        for equation in self.equations:
            print(equation)











