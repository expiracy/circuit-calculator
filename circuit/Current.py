class Current:
    def __init__(self, value=None, flow=None):
        self.value = value
        self.flow = flow

    def __str__(self):
        return f"Flow: {self.flow}, Value: {self.value}"
