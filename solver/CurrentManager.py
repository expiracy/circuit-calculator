from solver.JunctionsManager import JunctionsManager


class CurrentManager:
    def __init__(self, circuit=None, loops=None):
        self.circuit = circuit
        self.junctions_manager = JunctionsManager(circuit)
        self.loops = loops

    def Main(self):
        for edge in self.circuit.GetEdges():
            pass

        self.CheckJunctionValid()

    def CheckJunctionValid(self):
        for junction, directions in self.junctions_manager.junctions.items():
            print(self.circuit.GetEdgesForNode(junction))

    def AssignCurrentDirections(self):
        pass
