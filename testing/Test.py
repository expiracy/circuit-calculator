import sympy as sym

class Test:
    def __init__(self):
        self.symbol = sym.symbols('a')
        self.symbol2 = sym.symbols('b')

if __name__ == '__main__':
    test = Test()

    eq1 = sym.Eq(test.symbol + test.symbol2, 5)
    eq2 = sym.Eq(test.symbol ** 2 + test.symbol2 ** 2, 17)

    restult = sym.solve([eq1, eq2], (test.symbol, test.symbol2))

    print(restult)