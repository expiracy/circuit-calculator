from components.PowerSource import PowerSource
from components.ComponentType import ComponentType


class Cell(PowerSource):
    def __init__(self, id=None, potential_difference=None, internal_resistance=None):
        super().__init__(id, potential_difference, internal_resistance)

        self.component = ComponentType.CELL
        self.positive_terminal = None

    def Reverse(self):
        #self.edge = tuple(reversed(self.edge)[:2]) + self.edge[2:]

        return self

    def __str__(self):
        return f"(({self.component} {self.id}) R: {self.resistance}, I: {self.current.value}, V: {self.potential_difference}, Symbol: {self.current.symbol}, Edge: {self.edge})"
