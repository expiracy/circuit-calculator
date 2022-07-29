from graph.Graph import Graph
from graph.DiGraph import DiGraph
from graph.MultiGraph import MultiGraph
from graph.MultiDiGraph import MultiDiGraph
from solver.LoopFinder import LoopFinder
from circuit.NetList import NetList
from components.COMPONENT import COMPONENT
from components.Resistor import Resistor
from components.Cell import Cell
from solver.CurrentManager import CurrentManager


class CircuitManager:
    def __init__(self, circuit=None):
        self.circuit = circuit
        self._component_id = 0

    def Main(self):
        pass

    def CreateCircuitFromNetListFile(self, net_list_file):
        net_list = NetList(net_list_file)

        components = net_list.GetComponents()
        left_nodes = net_list.GetLeftNodes()
        right_nodes = net_list.GetRightNodes()
        values = net_list.GetValues()

        max_node = max(max(left_nodes), max(right_nodes))

        for node in range(max_node + 1):
            self.circuit.AddNode(node)

        for index in range(len(left_nodes)):
            component_type = components[index][0]
            component_class = None

            if component_type == COMPONENT.RESISTOR.value:
                component_class = Resistor(resistance=values[index])

            elif component_type == COMPONENT.CELL.value:
                component_class = Cell(potential_difference=values[index])

            self.circuit.AddEdge(left_nodes[index], right_nodes[index], component_class)

    def GetComponentForEdgeAndID(self, edge, component_id):
        components_for_edge_and_id = self.circuit.GetEdgeAttributes('value')

        edge_and_id = edge + (component_id,)

        try:
            component = components_for_edge_and_id[edge_and_id]
        except KeyError:
            edge_and_id = tuple(reversed(edge)) + (component_id,)
            component = components_for_edge_and_id[edge_and_id]

        return component

    def GetComponentIDsForEdge(self, edge):
        component_ids_for_edges = self.circuit.GetEdgeIDsForEdges()

        try:
            component_ids_for_edge = component_ids_for_edges[edge]
        except KeyError:
            edge = tuple(reversed(edge))
            component_ids_for_edge = component_ids_for_edges[edge]

        return component_ids_for_edge

    def GetComponentsOnLoop(self, loop):
        components_for_loop = []

        for node in range(len(loop) - 1):
            edge = (loop[node], loop[node + 1])

            component_ids_for_edge = self.GetComponentIDsForEdge(edge)

            components = []

            for component_id in component_ids_for_edge:
                component = self.GetComponentForEdgeAndID(edge, component_id)

                components.append(str(component))

            components_for_loop.append(components)

        return components_for_loop

    def AssignCurrentDirections(self):
        loops = LoopFinder(self.circuit).FindLoops()

        current_manager = CurrentManager(self.circuit, loops).Main()

        '''
        for loop in loops:
            for index in range(len(loop) - 1):
                edge = (loop[index], loop[index + 1])

                component_ids_for_edge = self.GetComponentIDsForEdge(edge)

                for component_id in component_ids_for_edge:
                    component = self.GetComponentForEdgeAndID(edge, component_id)

                    current_direction = component.current.GetDirection()

                    if current_direction is None:
        
                        component.current.SetDirection(*edge)
                        circuit.AddEdge(*edge)


        for edge in circuit.GetEdges():
            component = self.GetComponentForEdgeAndID(edge[:-1], edge[2])
            print(f"{component}, {component.current.GetDirection()}")


        circuit.Show()



            #nodes
        '''


if __name__ == "__main__":
    circuit_manager = CircuitManager(MultiGraph())
    circuit_manager.CreateCircuitFromNetListFile("../testing/Circuit2.txt")
    circuit_manager.AssignCurrentDirections()
