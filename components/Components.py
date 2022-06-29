from enum import Enum


class Components(Enum):
    CELL = 1
    RESISTOR = 2
    LAMP = 3

    def __str__(self):
        return self.name
