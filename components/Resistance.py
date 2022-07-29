from components.Current import Current


class Resistance:
    def __init__(self, resistance=0, potential_difference=0, current=0):
        self.resistance = resistance
        self.potential_difference = potential_difference
        self.current = Current(current)

    def __str__(self):
        return __name__
