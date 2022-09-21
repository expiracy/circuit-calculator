from circuit.path.PathFinder import PathFinder
from circuit.CurrentManager import CurrentManager
from sympy import *


class EquationManager:
    def __init__(self, circuit, component_manager=None, topology_manager=None, junction_manager=None):
        self.circuit = circuit

        self.component_manager = component_manager
        self.topology_manager = topology_manager
        self.junction_manager = junction_manager

        self.path_finder = PathFinder(circuit)
        self.current_manager = CurrentManager(circuit)

        self.equations = []

    def FindEquations(self):
        loops_paths = self.path_finder.GetLoopsPaths()

        for path_index in range(len(loops_paths)):
            terms = []

            for path_component in loops_paths[path_index]:
                component = path_component.component

                symbol = component.current.symbol
                sign = path_component.sign

                if self.component_manager.IsCell(component):
                    potential_difference = symbols(f"{sign}{component.potential_difference}")

                else:
                    potential_difference = component.resistance * symbols(f"{sign}{symbol}")

                terms.append(potential_difference)

            simplified_equation = self.CreateEquation(terms)

            self.equations.append(simplified_equation)

        components = self.component_manager.GetComponents()
        k1_equations = self.FindK1Equations(components, [], True)

        self.equations += k1_equations

        return self.equations

    def FindK1Equations(self, components, k1_equations, first_iteration):
        for component in components:
            if self.component_manager.IsParallelBranch(component):
                current = component.current

                if first_iteration:
                    expression = "-"

                else:
                    expression = f"{current.symbol}-"

                # may need to recurse deeper
                for current_component in current.components:

                    expression += f"{current_component.symbol}-"

                expression = expression[:-1]

                simplified_expression = simplify(expression)
                simplified_equation = Eq(simplified_expression, 0)

                k1_equations.append(simplified_equation)

                self.FindK1Equations(component.components, k1_equations, False)

            elif self.component_manager.IsSeriesGroup(component):
                self.FindK1Equations(component.components, k1_equations, False)

        return k1_equations

    def CreateEquation(self, terms):
        expression = ""

        for term in terms:
            expression += f"{term}+"

        expression = expression[:-1]

        simplified_expression = simplify(expression)
        simplified_equation = Eq(simplified_expression, 0)


        return simplified_equation
