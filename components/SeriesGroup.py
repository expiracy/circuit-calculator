from circuit.Current import Current
from components.COMPONENT import COMPONENT


class SeriesGroup:
    def __init__(self, nodes=None, edge=None, components=None):
        self.component = COMPONENT.SERIES_GROUP
        self.nodes = nodes
        self.edge = edge
        self.components = components
        self.current = Current()
        self.paths = []

    def FindComponentWithEdge(self, edge):
        for component in self.components:
            if component.edge == edge or tuple(reversed(component.edge)) == edge:
                return component

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Nodes: {self.nodes} Edge: {self.edge} Current ID: {self.current.id})"
