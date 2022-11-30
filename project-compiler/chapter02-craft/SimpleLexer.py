from enum import Enum
import TokenType


class DfaState(Enum):
    # 初始化状态
    Initial = 1
    # 标识符状态
    Id = 2
    # 大于操作符状态
    Gt = 3
    # 大于等于操作符
    GE = 4
    # 数字字面量
    IntLiteral = 5
    If = 6
    Id_if1 = 7
    Id_if2 = 8
    Else = 9
    Id_else1 = 10
    Id_else2 = 11
    Id_else3 = 12
    Id_else4 = 13
    Int = 14
    Id_int1 = 15
    Id_int2 = 16
    Id_int3 = 17
    Assignment = 18
    Plus = 19
    Minus = 20
    Star = 21
    Slash = 22
    SemiColon = 23
    LeftParen = 24
    RightParen = 25


class SimpleToken:
    def __init__(self, token, type):
        self.token = token
        self.type = type

    def getType(self):
        return self.type

    def getToken(self):
        return self.token


class SimpleTokenReader:
    def __init__(self, tokens, pos):
        self.tokens = tokens
        self.pos = pos

    def read(self):
        if self.pos < len(self.tokens):
            self.pos += 1
            return self.tokens[self.pos]
        return None

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def unread(self):
        if self.pos > 0:
            self.pos -= 1

    def getPosition(self):
        return self.pos

    def setPosition(self, position):
        if 0 <= position < len(self.tokens):
            self.pos = position

