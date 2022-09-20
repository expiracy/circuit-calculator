import sympy as sym

class Current:
    def __init__(self, id=-1, symbol=None, value=None, flow=None):
        self.id = id
        self.symbol = symbol
        self.direction = ''
        self.value = value
        self.flow = flow

    def ChangeDirection(self):
        if self.symbol == '':
            self.symbol = '-'

        else:
            self.symbol = ''

    def SetSymbol(self, symbol):
        self.symbol = sym.symbols(f"{self.direction}{symbol}")

        return self

    def __str__(self):
        return f"ID: {self.id}, Symbol: {self.symbol}, Value: {self.value}"
