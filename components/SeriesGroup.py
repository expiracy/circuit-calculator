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
            component_edge = component.edge[:2]

            if component_edge == edge or tuple(reversed(component_edge)) == edge:
                return component

    def GetGroupings(self):
        groupings = []

        for component in self.components:
            component_type = component.component
            if component_type is COMPONENT.PARALLEL_BRANCH or component_type is COMPONENT.SERIES_GROUP:
                groupings.append(component)

        return groupings

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
