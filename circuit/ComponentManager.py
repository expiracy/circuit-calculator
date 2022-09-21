from components.ComponentType import ComponentType
from components.Resistor import Resistor
from components.Cell import Cell


class ComponentManager:
    def __init__(self, circuit=None):
        self.circuit = circuit
        self.grouping_types = [ComponentType.SERIES_GROUP, ComponentType.PARALLEL_BRANCH]

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

    def CreateComponent(self, component_type, value, id):
        components = {
            ComponentType.RESISTOR: Resistor(id=id, resistance=value),
            ComponentType.CELL: Cell(id=id, potential_difference=value)
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

    def CalculatePotentialDifferences(self):
        for component in self.GetComponents():
            if component.potential_difference is None:
                component.potential_difference = component.current.value * component.resistance

        return self

    def GetComponents(self):
        components = []

        for edge in self.circuit.GetEdges():
            component = self.GetComponentForEdgeAndID(edge)

            components.append(component)

        return components

    def IsGrouping(self, component):
        if component.component in self.grouping_types:
            return True

        else:
            return False

    def IsParallelBranch(self, component):
        if component.component is ComponentType.PARALLEL_BRANCH:
            return True

        else:
            return False

    def IsSeriesGroup(self, component):
        if component.component is ComponentType.SERIES_GROUP:
            return True

        else:
            return False

    def IsCell(self, component):
        if component.component is ComponentType.CELL:
            return True

        else:
            return False

    def IsResistor(self, component):
        if component.component is ComponentType.RESISTOR:
            return True

        else:
            return False
