from circuit.topology.ParallelGroup import ParallelGroup
from circuit.topology.SeriesGroup import SeriesGroup


class TopologyManager:
    def __init__(self, circuit=None, junction_manager=None):
        self.circuit = circuit

        self.junction_manager = junction_manager

        self.series_groups = []
        self.parallel_groups = []

    def GroupSeriesComponents(self):
        sorted_series_groups_nodes = []
        series_groups_nodes = []

        junctions = self.junction_manager.junctions

        for junction_number in junctions.keys():
            series_group_nodes = self.GetSeriesJunctions([junction_number], [])

            if series_group_nodes:
                if sorted(series_group_nodes) not in sorted_series_groups_nodes:
                    series_groups_nodes.append(series_group_nodes)
                    sorted_series_groups_nodes.append(sorted(series_group_nodes))

        print(series_groups_nodes)

    def GetSeriesJunctions(self, nodes_to_check, series_nodes):
        junction_number = nodes_to_check.pop()
        junction = self.junction_manager.GetJunctionForNode(junction_number)
        connected_components = junction.connected_components

        if len(connected_components) == 2:
            series_nodes.append(junction_number)

            for component in connected_components:
                for node in component.edge[:-1]:
                    if node not in series_nodes and node not in nodes_to_check:
                        nodes_to_check.append(node)

            return self.GetSeriesJunctions(nodes_to_check, series_nodes)

        else:
            if not nodes_to_check:
                return series_nodes

            else:
                return self.GetSeriesJunctions(nodes_to_check, series_nodes)
