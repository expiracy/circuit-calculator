class Current:
    def __init__(self, current=0):
        self.current = current
        self.left_node = None
        self.right_node = None

    def SetDirection(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

        return self

    def GetDirection(self):
        if self.left_node is None and self.right_node is None:
            return None

        else:
            return self.left_node, self.right_node
