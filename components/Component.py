from circuit.Current import Current


class Component:
    def __init__(self, id=None, potential_difference=None, resistance=None, edge=None):
        self.id = id
        self.potential_difference = potential_difference
        self.resistance = resistance
        self.current = Current()
        self.edge = edge

    def __str__(self):
        return __name__