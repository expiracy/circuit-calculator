from circuit.Current import Current
from components.ComponentType import ComponentType
from components.Grouping import Grouping


class SeriesGroup(Grouping):
    def __init__(self, nodes=None, edge=None, components=None):
        super().__init__(edge, components)

        self.component = ComponentType.SERIES_GROUP
        self.nodes = nodes

    def FindComponentWithEdge(self, edge):
        for component in self.components:
            component_edge = component.edge[:2]

            if component_edge == edge or tuple(reversed(component_edge)) == edge:
                return component

    def Reverse(self):
        self.edge = tuple(reversed(self.edge[:2])) + self.edge[2:]
        self.nodes = list(reversed(self.nodes))

        self.components = list(reversed(self.components))
        
        reversed_paths = [list(reversed(path)) for path in self.paths]
        self.paths = reversed_paths

        return self

    def GetAllNodes(self):
        return [self.edge[0]] + self.nodes + [self.edge[1]]

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Nodes: {self.nodes} Edge: {self.edge} Current ID: {self.current.id})"
