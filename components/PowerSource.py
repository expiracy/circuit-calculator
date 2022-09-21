from circuit.Current import Current
from components.ComponentType import ComponentType
from components.Component import Component

class PowerSource(Component):
    def __init__(self, potential_difference=0, internal_resistance=0, edge=None):
        super().__init__(potential_difference, internal_resistance, edge)

    def __str__(self):
        return __name__
