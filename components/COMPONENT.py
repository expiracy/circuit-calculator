from enum import Enum


class COMPONENT(Enum):
    CELL = "V"
    RESISTOR = "R"

    def __str__(self):
        return self.name
