from components.PowerSource import PowerSource
from components.COMPONENT import COMPONENT


class Cell(PowerSource):
    def __init__(self, potential_difference=0, internal_resistance=0, current=0):
        super().__init__(potential_difference, internal_resistance, current)

        self.component = COMPONENT.CELL

    def __str__(self):
        return f"({self.component} {self.potential_difference} Edge: {self.edge} Current ID: {self.current.id})"
