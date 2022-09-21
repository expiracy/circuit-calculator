from sympy import Eq, solve
from solver.EquationManager import EquationManager


class Solver:
    def __init__(self, equations=None, components=None):
        self.equations = equations
        self.components = components

    def Solve(self):
        solutions = solve(self.equations)

        solutions_dict = {}

        for symbol, value in solutions.items():
            solutions_dict[str(symbol)] = value

        return solutions_dict