from components.Resistance import Resistance
from components.ComponentType import ComponentType


class Resistor(Resistance):
    def __init__(self, resistance=None, potential_difference=None):
        super().__init__(potential_difference, resistance)

        self.component = ComponentType.RESISTOR

    def __str__(self):
        return f"({self.component} {self.resistance} Edge: {self.edge} Current ID: {self.current.id} {str(self.current.symbol)})"
