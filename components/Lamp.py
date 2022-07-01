from components.Resistance import Resistance
from components.COMPONENT import Component


class Lamp(Resistance):
    def __init__(self, resistance=0, potential_difference=0, current=0):
        super().__init__(resistance, potential_difference, current)

        self._component = Component.LAMP
