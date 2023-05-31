import sys

sys.path.append('../chapter02')
from TokenType import TokenType


class Test:
    def __init__(self, value):
        self.value = value
        self.value += 1

    def getValue(self):
        return self.value


if __name__ == '__main__':
    test = Test(5)
    print(test.getValue())
    test1 = Test(7)
    print(test1.getValue())