from components.ParallelBranch import ParallelBranch
from components.SeriesGroup import SeriesGroup
from circuit.topology.LoopFinder import LoopFinder
from graph.MultiGraph import MultiGraph


class TopologyManager:
    def __init__(self, circuit=None, junction_manager=None, component_manager=None):
        self.circuit = circuit

        self.junction_manager = junction_manager
        self.component_manager = component_manager

        self.components = []

    def UpdateCircuit(self):
        self.circuit = MultiGraph()

        for component in self.components:
            attributes = {'component': component}

            edge = component.edge[:2]
            self.circuit.AddEdge(edge[0], edge[1], **attributes)

        self.component_manager.circuit = self.circuit
        self.junction_manager.circuit = self.circuit

        self.junction_manager.InitialiseJunctions()

        return self

    def SimplifyTopology(self):

        self.circuit.Show()
        # bug on other iterations

        old_circuit_nodes = list(self.circuit.GetNodes())

        # recursive redo series group and parallel
        series_groups_nodes = self.IdentitySeriesGroupsNodes()
        self.CreateSeriesGroups(series_groups_nodes)

        components_for_edges = self.GetComponentsForEdges()
        self.GroupParallelBranches(components_for_edges)

        self.UpdateCircuit()
        new_circuit_nodes = list(self.circuit.GetNodes())

        if new_circuit_nodes == old_circuit_nodes:
            return self

        else:
            self.SimplifyTopology()

    def IdentitySeriesGroupsNodes(self):
        sorted_series_groups_nodes = []
        series_groups_nodes = []

        junction_numbers = self.junction_manager.junctions.keys()

        for node in junction_numbers:
            series_group_nodes = self.IdentifySeriesGroupNodes([node], [])

            if series_group_nodes:
                if sorted(series_group_nodes) not in sorted_series_groups_nodes:
                    series_groups_nodes.append(series_group_nodes)
                    sorted_series_groups_nodes.append(sorted(series_group_nodes))

        return series_groups_nodes

    def IdentifySeriesGroupNodes(self, nodes_to_check, series_group_nodes):
        junction_number = nodes_to_check.pop()
        junction = self.junction_manager.GetJunctionForNode(junction_number)
        connected_components = junction.connected_components

        if len(connected_components) == 2:
            series_group_nodes.append(junction_number)

            for component in connected_components:

                for node in component.edge[:2]:

                    if node not in series_group_nodes and node not in nodes_to_check:
                        nodes_to_check.append(node)

            return self.IdentifySeriesGroupNodes(nodes_to_check, series_group_nodes)

        else:
            if not nodes_to_check:
                return series_group_nodes

            else:
                return self.IdentifySeriesGroupNodes(nodes_to_check, series_group_nodes)

    def FindEdgeFromSeriesGroupNodes(self, series_group_nodes):
        edge = ()

        first_neighbour_nodes = list(self.junction_manager.GetNeighboursOfJunction(series_group_nodes[0]))
        last_neighbour_nodes = list(self.junction_manager.GetNeighboursOfJunction(series_group_nodes[-1]))

        for node in first_neighbour_nodes:
            if node not in series_group_nodes:
                edge += (node,)

        for node in last_neighbour_nodes:
            if node not in series_group_nodes and node not in edge:
                edge += (node,)

        return edge

    def GetComponentsForSeriesGroupNodes(self, series_group_nodes):
        components = []

        for node in series_group_nodes:
            junction = self.junction_manager.GetJunctionForNode(node)

            connected_components = junction.connected_components

            for component in connected_components:
                if component not in components:
                    components.append(component)

        return components

    def CreateSeriesGroups(self, series_groups_nodes):
        self.components = []
        added_components = []

        for series_group_nodes in series_groups_nodes:
            edge = self.FindEdgeFromSeriesGroupNodes(series_group_nodes)
            components = self.GetComponentsForSeriesGroupNodes(series_group_nodes)

            added_components += components

            series_group = SeriesGroup(series_group_nodes, edge, components)

            self.components.append(series_group)

        components = self.component_manager.GetComponents()

        for component in components:
            if component not in added_components:
                self.components.append(component)

    def GroupParallelBranches(self, components_for_edges):
        new_components = []

        for edge, components in components_for_edges.items():
            if len(components) >= 2:

                parallel_branch = ParallelBranch(edge, components)

                new_components.append(parallel_branch)

            else:
                new_components += components

        self.components = new_components

        return self

    def GetComponentsForNode(self, node):
        components = []

        for component in self.components:
            if node in component.edge[:2] and component not in components:
                components.append(component)

        return components

    def GetComponentsForEdges(self):
        components_for_edges = {}

        for component in self.components:
            edge = component.edge[:2]

            keys = components_for_edges.keys()

            if edge not in keys and tuple(reversed(edge)) not in keys:
                components_for_edges[edge] = []

            if edge not in keys:
                edge = tuple(reversed(edge))

            components_for_edges[edge].append(component)

        return components_for_edges

    '''
    def IdentifyParallelJunctionsAndNeighbours(self):
        parallel_junctions_and_connections= {}

        for node in self.junction_manager.junctions.keys():
            connections = list(self.GetComponentsForNode(node))

            if len(connections) > 2:
                parallel_junctions_and_connections[node] = connections

        return parallel_junctions_and_connections
    '''
