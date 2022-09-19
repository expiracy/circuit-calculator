from circuit.Current import Current
from components.COMPONENT import COMPONENT


class ParallelBranch:
    def __init__(self, edge=None, components=None, flow=None):
        self.component = COMPONENT.PARALLEL_BRANCH
        self.edge = edge
        self.components = components
        self.current = Current()
        self.paths = []

    def GetGroupings(self):
        groupings = []

        for component in self.components:
            component_type = component.component
            if component_type is COMPONENT.PARALLEL_BRANCH or component_type is COMPONENT.SERIES_GROUP:
                groupings.append(component)

        return groupings

    def Reverse(self):
        self.edge = tuple(reversed(self.edge[:2])) + self.edge[2:]

        return self

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Edge: {self.edge} Current ID: {self.current.id})"
