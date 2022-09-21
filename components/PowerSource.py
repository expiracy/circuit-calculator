from circuit.Current import Current
from components.ComponentType import ComponentType
from components.Component import Component

class PowerSource(Component):
    def __init__(self, id=None, potential_difference=None, internal_resistance=None, edge=None):
        super().__init__(id, potential_difference, internal_resistance, edge)

    def __str__(self):
        return __name__
