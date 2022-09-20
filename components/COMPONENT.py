from enum import Enum


class COMPONENT(Enum):
    CELL = "V"
    RESISTOR = "R"
    PARALLEL_BRANCH = "P"
    SERIES_GROUP = "S"

    def __str__(self):
        return self.name


class Component:
    def __init__(self):
        pass
