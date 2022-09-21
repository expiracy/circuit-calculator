from circuit.path.PathFinder import PathFinder
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

            for path_component in loops_paths[path_index]:
                component = path_component.component

                symbol = component.current.symbol
                sign = path_component.sign

                if self.component_manager.IsCell(component):
                    potential_difference = sym.symbols(f"{sign}{component.potential_difference}")

                else:
                    potential_difference = component.resistance * sym.symbols(f"{sign}{symbol}")

                self.equations[path_index].append(potential_difference)

        for equation in self.equations:
            print(equation)











