from enum import Enum
from TokenType import TokenType


class DfaState(Enum):
    # 初始化状态
    Initial = 1
    # 标识符状态
    Id = 2
    # 大于操作符状态
    GT = 3
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
    # Token类型
    type = None
    # 文本值
    text = None

    def getType(self):
        return self.type

    def getText(self):
        return self.text


class SimpleTokenReader:
    pos = 0

    def __init__(self, tokens):
        self.tokens = tokens

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


tokenText = []  # 临时保存token的文本
tokens = []  # 保存解析出来的Token
token = None  # 当前正在解析的Toke


def initToken(ch):
    global tokenText
    global token
    if len(tokenText) > 0:
        token.text = "".join(tokenText)
        tokens.append(token)
        tokenText = []
        token = SimpleToken()
    if ch.isalpha():
        if ch == 'i':
            newState = DfaState.Id_int1
        else:
            newState = DfaState.Id  # 进入Id状态
        token.type = TokenType.Identifier
        tokenText.append(ch)
    elif ch.isdigit():  # 第一个字符是数字
        newState = DfaState.IntLiteral
        token.type = TokenType.IntLiteral
        tokenText.append(ch)
    elif ch == '>':  # 第一个字符是>
        newState = DfaState.GT
        token.type = TokenType.GT
        tokenText.append(ch)
    elif ch == '+':
        newState = DfaState.Plus
        token.type = TokenType.Plus
        tokenText.append(ch)
    elif ch == '-':
        newState = DfaState.Minus
        token.type = TokenType.Minus
        tokenText.append(ch)
    elif ch == '*':
        newState = DfaState.Star
        token.type = TokenType.Star
        tokenText.append(ch)
    elif ch == '/':
        newState = DfaState.Slash
        token.type = TokenType.Slash
        tokenText.append(ch)
    elif ch == ';':
        newState = DfaState.SemiColon
        token.type = TokenType.SemiColon
        tokenText.append(ch)
    elif ch == '(':
        newState = DfaState.LeftParen
        token.type = TokenType.LeftParen
        tokenText.append(ch)
    elif ch == ')':
        newState = DfaState.RightParen
        token.type = TokenType.RightParen
        tokenText.append(ch)
    elif ch == '=':
        newState = DfaState.Assignment
        token.type = TokenType.Assignment
        tokenText.append(ch)
    else:
        newState = DfaState.Initial  # skip all unknown patterns
    return newState


def tokenize(code):
    global token
    global tokenText
    token = SimpleToken()
    tokenText = []
    codes = list(code)
    state = DfaState.Initial
    try:
        for code in codes:
            if state == DfaState.Initial:
                state = initToken(code)
            elif state == DfaState.Id:
                if code.isdigit() or code.isalpha():
                    tokenText.append(code)
                else:
                    state = initToken(code)
            elif state == DfaState.GT:
                if code == '=':
                    token.type = TokenType.GE
                    state = DfaState.GE
                    tokenText.append(code)
                else:
                    state = initToken(code)
            elif state == DfaState.GE:
                state = initToken(code)
            elif state == DfaState.Assignment:
                state = initToken(code)
            elif state == DfaState.Plus:
                state = initToken(code)
            elif state == DfaState.Minus:
                state = initToken(code)
            elif state == DfaState.Star:
                state = initToken(code)
            elif state == DfaState.Slash:
                state = initToken(code)
            elif state == DfaState.SemiColon:
                state = initToken(code)
            elif state == DfaState.LeftParen:
                state = initToken(code)
            elif state == DfaState.RightParen:
                state = initToken(code)
            elif state == DfaState.IntLiteral:
                if code.isdigit():
                    tokenText.append(code)
                else:
                    state = initToken(code)
            elif state == DfaState.Id_int1:
                if code == 'n':
                    state = DfaState.Id_int2
                    tokenText.append(code)
                elif code.isDigit or code.isalpha:
                    state = DfaState.Id  # 切换回Id状态
                    tokenText.append(code)
                else:
                    state = initToken(code)
            elif state == DfaState.Id_int2:
                if code == 't':
                    state = DfaState.Id_int3
                    tokenText.append(code)
                elif code.isdigit() or code.isalpha():
                    state = DfaState.Id
                    tokenText.append(code)
                else:
                    state = initToken(code)
            elif state == DfaState.Id_int3:
                if code == ' ' or code == '\t' or code == '\n':
                    token.type = TokenType.Int
                    state = initToken(code)
                else:
                    state = DfaState.Id  # 切换回Id状态
                    tokenText.append(code)

        if len(tokenText) > 0:
            initToken(code)
    except Exception as ex:
        print("something is error。error:%s" % ex)
    return tokens


if __name__ == '__main__':
    script = "int age = 45;"
    print("parse :" + script)
    tokens = tokenize(script)
    for token in tokens:
        print(token.getText() + "\t\t" + str(token.getType()))
