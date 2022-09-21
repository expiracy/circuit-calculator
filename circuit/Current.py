import sympy as sym

class Current:
    def __init__(self, id=-1, symbol=None, value=None):
        self.id = id
        self.symbol = symbol
        self.value = value
        self.components = []

    def IsPositive(self):
        sign = str(self.symbol)[0]

        if sign == '-':
            return False

        else:
            return True

    def __str__(self):
        return f"ID: {self.id}, Symbol: {self.symbol}, Value: {self.value}"
