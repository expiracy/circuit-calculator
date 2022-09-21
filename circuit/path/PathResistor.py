class PathResistor:
    def __init__(self, resistor, sign):
        self.component = resistor
        self.sign = sign

    def __str__(self):
        return f"{str(self.component)}"
