from components.Resistance import Resistance
from components.ComponentType import ComponentType


class Resistor(Resistance):
    def __init__(self, id=None, resistance=None, potential_difference=None):
        super().__init__(id, potential_difference, resistance)

        self.component = ComponentType.RESISTOR

    def __str__(self):
        return f"(({self.component} {self.id}) R: {self.resistance}, I: {self.current.value}, V: {self.potential_difference}, Symbol: {self.current.symbol}, Edge: {self.edge})"