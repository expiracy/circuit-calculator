from components.PowerSource import PowerSource
from components.COMPONENT import COMPONENT


class Cell(PowerSource):
    def __init__(self, potential_difference=0, internal_resistance=0, current=0):
        super().__init__(potential_difference, internal_resistance, current)

        self.component = COMPONENT.CELL
        self.positive_terminal = None

    def Reverse(self):
        #self.edge = tuple(reversed(self.edge)[:2]) + self.edge[2:]

        return self

    def __str__(self):
        return f"({self.component} {self.potential_difference} Edge: {self.edge} Current ID: {self.current.id})"
