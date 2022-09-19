from components.ParallelBranch import ParallelBranch
from components.SeriesGroup import SeriesGroup
from circuit.topology.PathFinder import PathFinder
from graph.MultiGraph import MultiGraph


class TopologyManager:
    def __init__(self, circuit=None, junction_manager=None, component_manager=None):
        self.circuit = circuit

        self.junction_manager = junction_manager
        self.component_manager = component_manager
        self.path_finder = PathFinder(circuit)

        self.components = []

    def AddRemainingComponents(self, added_components):
        for component in self.component_manager.GetComponents():
            if component not in added_components:
                self.components.append(component)

        return self

    def SimplifyTopology(self):
        self.junction_manager.InitialiseJunctions()

        old_circuit_nodes = list(self.circuit.GetNodes())

        series_groups_nodes = self.IdentitySeriesGroupsNodes()

        all_in_series = self.CheckIfAllInSeries(series_groups_nodes, old_circuit_nodes)

        if not all_in_series:
            added_components = self.CreateSeriesGroups(series_groups_nodes)
            self.AddRemainingComponents(added_components)

            components_for_edges = self.GetComponentsForEdges()
            self.GroupParallelBranches(components_for_edges)

            self.UpdateCircuit()

        new_circuit_nodes = list(self.circuit.GetNodes())

        if new_circuit_nodes == old_circuit_nodes:
            self.circuit.Show()

            return self

        else:
            self.SimplifyTopology()

    def FindPossibleSeriesGroupPath(self, component):
        possible_path = []

        edge = component.edge

        paths = self.path_finder.FindPathsBetween(edge[0], edge[1])

        sorted_nodes = list(sorted(component.nodes))
        sorted_paths = [list(sorted(path)) for path in paths]

        for path_index in range(len(sorted_paths)):

            if sorted_paths[path_index] == sorted_nodes:
                possible_path = paths[path_index]

                break

        return possible_path

    def OrderSeriesGroup(self, series_group):
        series_group_components = []

        possible_path = self.FindPossibleSeriesGroupPath(series_group)
        series_group_path = [series_group.edge[0]] + possible_path + [series_group.edge[1]]

        for node_index in range(len(series_group_path) - 1):
            edge = (series_group_path[node_index], series_group_path[node_index + 1])

            component_to_add = series_group.FindComponentWithEdge(edge)

            series_group_components.append(component_to_add)

        series_group.components = series_group_components
        series_group.nodes = possible_path

        return series_group

    def UpdateCircuit(self):
        self.circuit = MultiGraph()

        for component in self.components:
            attributes = {'component': component}

            edge = component.edge[:2]
            self.circuit.AddEdge(edge[0], edge[1], **attributes)

        self.component_manager.circuit = self.circuit
        self.junction_manager.circuit = self.circuit
        self.path_finder.circuit = self.circuit

        return self

    def CheckIfAllInSeries(self, series_groups_nodes, circuit_nodes):
        all_in_series = False

        for series_group_nodes in series_groups_nodes:
            if sorted(series_group_nodes) == sorted(circuit_nodes):
                all_in_series = True

        return all_in_series

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
        if nodes_to_check:
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
            return series_group_nodes

    def FindEdgeFromSeriesGroupNodes(self, series_group_nodes):
        edge = ()

        for node in series_group_nodes:
            neighbour_nodes = self.circuit.GetNeighbourNodes(node)

            for neighbour_node in neighbour_nodes:
                if neighbour_node not in edge and neighbour_node not in series_group_nodes:
                    edge += (neighbour_node,)

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

            ordered_series_group = self.OrderSeriesGroup(series_group)

            self.components.append(ordered_series_group)

        return added_components

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

    def GetComponentForEdge(self, edge, components):
        for component in components:
            component_edge = component.edge

            if component_edge == edge or tuple(reversed(component_edge)) == edge:
                return component

            return self.GetComponentForEdge(edge, component.components)
