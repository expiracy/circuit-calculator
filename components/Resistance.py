from circuit.Current import Current


class Resistance:
    def __init__(self, resistance=0, potential_difference=0, edge=None):
        self.resistance = resistance
        self.potential_difference = potential_difference
        self.current = Current()
        self.edge = edge

    def __str__(self):
        return __name__
