class PathComponent:
    def __init__(self, component, direction):
        self.component = component
        self.direction = direction

    def __str__(self):
        return f"{str(self.component)}"
