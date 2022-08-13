class CurrentManager:
    def __init__(self, circuit=None, junction_manager=None, component_manager=None):
        self.circuit = circuit
        self.junction_manager = junction_manager
        self.component_manager = component_manager

    def AssignCurrentDirections(self, loops):

        for loop_number in range(len(loops)):
            loop = loops[loop_number]

            specific_paths = self.FindSpecificPathsForLoop(loop)

            print(loop)

            for node_index in range(len(loop) - 1):
                edge = (loop[node_index], loop[node_index + 1])

                junction = self.junction_manager.GetJunctionForNode(loop[node_index])
                connected_components = junction.connected_components

                if loop_number == 0:

                    for connected_component in connected_components:

                        component_edge = connected_component.edge

                        if edge == component_edge[:-1] or tuple(reversed(edge)) == component_edge[:-1]:
                            if connected_component.current.flow is None:
                                connected_component.current.flow = edge

                                print(connected_component)

                                break

                else:

                    components_with_set_flows = self.GetComponentsWithSetFlowsOnLoop(loop)
                    print(f"set flows {components_with_set_flows}")

        for junction, connected_components in self.junction_manager.junctions.items():
            print(junction, connected_components)

        print(loops)

    def FindPossibleComponentsOnLoop(self, loop):
        possible_components_on_loop = []

        for node_index in range(len(loop) - 1):
            possible_components_on_loop.append([])

            edge = (loop[node_index], loop[node_index + 1])

            components = self.component_manager.GetComponentsForEdge(edge)

            for component in components:
                possible_components_on_loop[node_index].append(component)

        return possible_components_on_loop

    def FindSpecificPathsForLoop(self, loop):
        specific_paths = []
        possible_components_on_loop = self.FindPossibleComponentsOnLoop(loop)

        for components in possible_components_on_loop:
            pass

        return specific_paths

    def GetComponentsWithSetFlowsOnLoop(self, loop):
        set_flows = []

        for node_index in range(len(loop) - 1):
            edge = (loop[node_index], loop[node_index + 1])

            components = self.component_manager.GetComponentsForEdge(edge)

            for component in components:
                flow = component.current.flow

                if flow is not None:
                    set_flows.append(component)

        return set_flows

    def GetFlowForEdge(self, edge):
        component = self.component_manager.GetComponentForEdgeAndID(edge)
        flow = component.current.flow

        return flow

    def SetFlowForEdge(self, edge, flow):
        component = self.component_manager.GetComponentForEdgeAndID(edge)
        component.current.flow = flow
