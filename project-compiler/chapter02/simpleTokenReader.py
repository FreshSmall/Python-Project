class SimpleTokenReader:
    pos = 0

    def __init__(self, tokens):
        self.tokens = tokens

    def read(self):
        if self.pos < len(self.tokens):
            tempToken = self.tokens[self.pos]
            self.pos += 1
            return tempToken
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
