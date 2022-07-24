from graph.Graph import Graph
from circuit.CircuitManager import CircuitManager


class LoopFinder:
    def __init__(self, circuit):
        self.loops = self.FindLoops(circuit)

    def FindLoops(self, circuit):
        cycles = [[0] + path for path in circuit.DFS(0, 0)]

        loops = []

        for loop in cycles:
            if loop[::-1] not in loops and len(loop) > 3:
                loops.append(loop)

        return loops


if __name__ == "__main__":
    circuit_manager = CircuitManager(Graph())
    circuit_manager.CreateCircuitFromNetListFile("./testing/Circuit1.txt")
    loop_finder = LoopFinder(circuit_manager.circuit)
