from enum import Enum


class DIRECTION(Enum):
    NULL = -1
    IN = 1
    OUT = 0

    def __str__(self):
        return self.name
