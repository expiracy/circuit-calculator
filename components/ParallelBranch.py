from circuit.Current import Current
from components.ComponentType import ComponentType
from components.Grouping import Grouping


class ParallelBranch(Grouping):
    def __init__(self, edge=None, components=None):
        super().__init__(edge, components)

        self.component = ComponentType.PARALLEL_BRANCH

    def Reverse(self):
        self.edge = tuple(reversed(self.edge[:2])) + self.edge[2:]

        reversed_paths = [list(reversed(path)) for path in self.paths]
        self.paths = reversed_paths

        return self

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Edge: {self.edge} Current ID: {self.current.id})"
