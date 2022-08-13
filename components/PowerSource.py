from circuit.Current import Current


class PowerSource:
    def __init__(self, potential_difference=0, internal_resistance=0, edge=None):
        self.potential_difference = potential_difference
        self.internal_resistance = internal_resistance
        self.current = Current()
        self.edge = edge

    def __str__(self):
        return __name__
