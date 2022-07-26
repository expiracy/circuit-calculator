from components.Resistance import Resistance
from components.COMPONENT import COMPONENT


class Resistor(Resistance):
    def __init__(self, resistance=0, potential_difference=0, current=0):
        super().__init__(resistance, potential_difference, current)

        self._component = COMPONENT.RESISTOR

    def __str__(self):
        return f"{self._component} {self._resistance}"
