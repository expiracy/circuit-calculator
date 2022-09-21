class PathCell:
    def __init__(self, cell, sign):
        self.component = cell
        self.sign = sign

    def __str__(self):
        return f"{str(self.component)}"
