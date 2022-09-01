from components.COMPONENT import COMPONENT
from components.Resistor import Resistor
from components.Cell import Cell


class ComponentManager:
    def __init__(self, circuit=None):
        self.circuit = circuit
        self.grouping_types = [COMPONENT.SERIES_GROUP, COMPONENT.PARALLEL_BRANCH]

    def GetComponentsForEdge(self, edge):
        components = []

        components_for_edges = self.GetEdgesForComponents()

        for edge_and_id in components_for_edges.keys():
            if edge == edge_and_id[:-1] or tuple(reversed(edge)) == edge_and_id[:-1]:
                components.append(components_for_edges[edge_and_id])

        return components

    def GetComponentForEdgeAndID(self, edge):
        components_for_edges = self.GetEdgesForComponents()

        if edge not in components_for_edges:
            edge = tuple(reversed(edge[:-1])) + (edge[2],)

        component = components_for_edges[edge]

        return component

    def CreateComponent(self, component_type, value):
        components = {
            COMPONENT.RESISTOR: Resistor(resistance=value),
            COMPONENT.CELL: Cell(potential_difference=value)
        }

        component_class = components[component_type]

        return component_class

    def GetEdgesForComponents(self):
        edges_and_components = self.circuit.GetEdgeAttributes('component')

        return edges_and_components

    def SetComponentEdges(self):
        edges_and_components = self.GetEdgesForComponents()

        for edge, component in edges_and_components.items():
            component.edge = edge

    def GetComponents(self):
        components = []

        for edge in self.circuit.GetEdges():
            component = self.GetComponentForEdgeAndID(edge)

            components.append(component)

        return components

    def AssignCurrent(self, flow):
        pass

    def IsGrouping(self, component):
        if component.component in self.grouping_types:
            return True

        else:
            return False

    def IsParallelBranch(self, component):
        if component.component is COMPONENT.PARALLEL_BRANCH:
            return True

        else:
            return False

    def IsSeriesGroup(self, component):
        if component.component is COMPONENT.SERIES_GROUP:
            return True

        else:
            return False
