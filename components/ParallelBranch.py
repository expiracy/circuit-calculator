class ParallelBranch:
    def __init__(self, edge=None, components=None):
        self.edge = edge
        self.components = components

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Edge: {self.edge})"
