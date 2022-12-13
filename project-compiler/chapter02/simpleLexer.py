from TokenType import TokenType
from simpleToken import SimpleToken
from dfaState import DfaState
from simpleTokenReader import SimpleTokenReader
import logging


class SimpleLexer:

    def __init__(self, tokenText, tokens, token):
        # 临时保存token的文本
        self.tokenText = tokenText
        # 保存解析出来的Token
        self.tokens = tokens
        # 当前正在解析的Token
        self.token = token

    def initToken(self, ch):
        if len(self.tokenText) > 0:
            self.token.text = "".join(self.tokenText)
            self.tokens.append(self.token)
            self.tokenText = []
            self.token = SimpleToken()
        if ch.isalpha():
            if ch == 'i':
                newState = DfaState.Id_int1
            else:
                newState = DfaState.Id  # 进入Id状态
            self.token.type = TokenType.Identifier
            self.tokenText.append(ch)
        elif ch.isdigit():  # 第一个字符是数字
            newState = DfaState.IntLiteral
            self.token.type = TokenType.IntLiteral
            self.tokenText.append(ch)
        elif ch == '>':  # 第一个字符是>
            newState = DfaState.GT
            self.token.type = TokenType.GT
            self.tokenText.append(ch)
        elif ch == '+':
            newState = DfaState.Plus
            self.token.type = TokenType.Plus
            self.tokenText.append(ch)
        elif ch == '-':
            newState = DfaState.Minus
            self.token.type = TokenType.Minus
            self.tokenText.append(ch)
        elif ch == '*':
            newState = DfaState.Star
            self.token.type = TokenType.Star
            self.tokenText.append(ch)
        elif ch == '/':
            newState = DfaState.Slash
            self.token.type = TokenType.Slash
            self.tokenText.append(ch)
        elif ch == ';':
            newState = DfaState.SemiColon
            self.token.type = TokenType.SemiColon
            self.tokenText.append(ch)
        elif ch == '(':
            newState = DfaState.LeftParen
            self.token.type = TokenType.LeftParen
            self.tokenText.append(ch)
        elif ch == ')':
            newState = DfaState.RightParen
            self.token.type = TokenType.RightParen
            self.tokenText.append(ch)
        elif ch == '=':
            newState = DfaState.Assignment
            self.token.type = TokenType.Assignment
            self.tokenText.append(ch)
        else:
            newState = DfaState.Initial  # skip all unknown patterns
        return newState

    def tokenize(self, code):
        token = SimpleToken()
        codes = list(code)
        state = DfaState.Initial
        try:
            for code in codes:
                if state == DfaState.Initial:
                    state = self.initToken(code)
                elif state == DfaState.Id:
                    if code.isdigit() or code.isalpha():
                        self.tokenText.append(code)
                    else:
                        state = self.initToken(code)
                elif state == DfaState.GT:
                    if code == '=':
                        token.type = TokenType.GE
                        state = DfaState.GE
                        self.tokenText.append(code)
                    else:
                        state = self.initToken(code)
                elif state == DfaState.GE:
                    state = self.initToken(code)
                elif state == DfaState.Assignment:
                    state = self.initToken(code)
                elif state == DfaState.Plus:
                    state = self.initToken(code)
                elif state == DfaState.Minus:
                    state = self.initToken(code)
                elif state == DfaState.Star:
                    state = self.initToken(code)
                elif state == DfaState.Slash:
                    state = self.initToken(code)
                elif state == DfaState.SemiColon:
                    state = self.initToken(code)
                elif state == DfaState.LeftParen:
                    state = self.initToken(code)
                elif state == DfaState.RightParen:
                    state = self.initToken(code)
                elif state == DfaState.IntLiteral:
                    if code.isdigit():
                        self.tokenText.append(code)
                    else:
                        state = self.initToken(code)
                elif state == DfaState.Id_int1:
                    if code == 'n':
                        state = DfaState.Id_int2
                        self.tokenText.append(code)
                    elif code.isDigit or code.isalpha:
                        state = DfaState.Id  # 切换回Id状态
                        self.tokenText.append(code)
                    else:
                        state = self.initToken(code)
                elif state == DfaState.Id_int2:
                    if code == 't':
                        state = DfaState.Id_int3
                        self.tokenText.append(code)
                    elif code.isdigit() or code.isalpha():
                        state = DfaState.Id
                        self.tokenText.append(code)
                    else:
                        state = self.initToken(code)
                elif state == DfaState.Id_int3:
                    if code == ' ' or code == '\t' or code == '\n':
                        token.type = TokenType.Int
                        state = self.initToken(code)
                    else:
                        state = DfaState.Id  # 切换回Id状态
                        self.tokenText.append(code)

            if len(tokenText) > 0:
                self.initToken(code)
        except Exception as ex:
            logging.exception(ex)
        return SimpleTokenReader(self.tokens)


if __name__ == '__main__':
    script = "int age = 45;"
    print("parse :" + script)
    tokenText = []  # 临时保存token的文本
    tokens = []  # 保存解析出来的Token
    token = SimpleToken()  # 当前正在解析的Toke
    lexer = SimpleLexer(tokenText, tokens, token)
    tokenReader = lexer.tokenize(script)
    token = tokenReader.read()
    while token is not None:
        print(token.getText() + "  " + str(token.getType().name))
        token = tokenReader.read()
