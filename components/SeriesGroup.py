from circuit.Current import Current


class SeriesGroup:
    def __init__(self, nodes=None, edge=None, components=None):
        self.nodes = nodes
        self.edge = edge
        self.components = components
        self.current = Current()

    def SetFlow(self, flow):
        pass

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Nodes: {self.nodes} Edge: {self.edge} Flow: {self.current.flow})"
