from components.ComponentType import ComponentType
from components.Component import Component


class Grouping(Component):
    def __init__(self, edge, components):
        super().__init__(edge=edge)
        self.edge = edge
        self.components = components
        self.paths = []

    def GetGroupings(self):
        groupings = []

        for component in self.components:
            component_type = component.component
            if component_type is ComponentType.PARALLEL_BRANCH or component_type is ComponentType.SERIES_GROUP:
                groupings.append(component)

        return groupings
