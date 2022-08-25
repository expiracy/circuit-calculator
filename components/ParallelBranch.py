from components.COMPONENT import COMPONENT


class ParallelBranch:
    def __init__(self, edge=None, components=None, flow=None):
        self.component = COMPONENT.PARALLEL_BRANCH
        self.edge = edge
        self.components = components
        self.flow = flow

    def __str__(self):
        return f"(No. Comp: {len(self.components)} Edge: {self.edge})"
