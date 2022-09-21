from circuit.Current import Current
from components.ComponentType import ComponentType
from components.Component import Component


class Resistance(Component):
    def __init__(self, id=None, potential_difference=None, resistance=None, edge=None):
        super().__init__(id, potential_difference, resistance, edge)

    def Reverse(self):
        #self.edge = tuple(reversed(self.edge[:2])) + self.edge[2:]

        return self

    def __str__(self):
        return __name__
