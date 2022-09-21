from circuit.Current import Current

class Component:
    def __init__(self, potential_difference=None, resistance=None, edge=None):
        self.potential_difference = potential_difference
        self.resistance = resistance
        self.current = Current()
        self.edge = edge

    def __str__(self):
        return __name__