from sympy import Eq, solve
from solver.EquationManager import EquationManager

class Solver:
    def __init__(self, equations=None):
        self.equations = equations

    def Solve(self):
        solutions = solve(self.equations)

        print(solutions)