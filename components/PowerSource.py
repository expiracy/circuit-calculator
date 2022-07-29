from components.Current import Current


class PowerSource:
    def __init__(self, potential_difference=0, internal_resistance=0, current=0):
        self.potential_difference = potential_difference
        self.internal_resistance = internal_resistance
        self.current = Current(current)

    def __str__(self):
        return __name__
