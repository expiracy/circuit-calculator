class Junction:
    def __init__(self, number=None):
        self.number = number
        self.connected_components = []

    def __str__(self):
        return f"(Junc: {self.number}, No. Conns: {len(self.connected_components)})"
