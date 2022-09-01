from circuit.Current import Current
from components.COMPONENT import COMPONENT


class SeriesGroup:
    def __init__(self, nodes=None, edge=None, components=None):
        self.component = COMPONENT.SERIES_GROUP
        self.nodes = nodes
        self.edge = edge
        self.components = components
        self.current = Current()

    def SetFlow(self, flow):
        for node_index in range(len(flow)):
            edge = (flow[node_index], flow[node_index + 1])

            for component in self.components:
                component_edge = component.edge[:2]

                if component_edge == edge or tuple(reversed(component_edge)) == edge:
                    component.current.flow = edge

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Nodes: {self.nodes} Edge: {self.edge} Current ID: {self.current.id})"
