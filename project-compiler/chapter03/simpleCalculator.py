import sys

sys.path.append("../chapter02")
from TokenType import TokenType
from ast import ASTNodeType
from simpleLexer import tokenize


class SimpleASTNode:

    def __init__(self, nodeType, text):
        self.nodeType = nodeType
        self.text = text
        self.children = []
        self.parent = None

    def getParent(self):
        return self.parent

    def getChildren(self):
        return self.children

    def getType(self):
        return self.nodeType

    def getText(self):
        return self.text

    def addChild(self, child):
        self.children.append(child)
        child.parent = self


def intDeclare(tokens):
    node = None
    token = tokens.peek()  # 预读
    # 匹配Int
    if token is not None and token.getType() == TokenType.Int:
        # 消耗掉int
        token = tokens.read()
        # 匹配标识符
        if tokens.peek().getType() == TokenType.Identifier:
            # 消耗掉标识符
            token = tokens.read()
            # 创建当前节点，并把变量名记到AST节点的文本值中，这里新建一个变量子节点也是可以的
            node = SimpleASTNode(ASTNodeType.IntDeclaration, token.getText())
            # 预读
            token = tokens.peek()
            if token is not None and token.getType() == TokenType.Assignment:
                # 消耗掉等号
                tokens.read()
                # 匹配一个表达式
                child = additive(tokens)
                if child is None:
                    raise Exception("invalid variable initialization, exception an expression")
                else:
                    node.addChild(child)
        else:
            raise Exception("variable name excepted")

        if node is not None:
            token = tokens.peek()
            if token is not None and token.getType() == TokenType.SemiColon:
                tokens.read()
            else:
                raise Exception("invalid statement,excepting semicolon")
    return node


'''
 语法解析：加法表达式
'''


def additive(tokens):
    child1 = multiplicative(tokens)
    node = child1
    token = tokens.peek()
    if child1 is not None and token is not None:
        if token.getType() == TokenType.Plus or token.getType() == TokenType.Minus:
            token = tokens.read()
            child2 = additive(tokens)
            if child2 is not None:
                node = SimpleASTNode(ASTNodeType.Additive, token.getText())
                node.addChild(child1)
                node.addChild(child2)
            else:
                raise Exception("invalid additive expression, excepting the right part.")
    return node


'''
语法解析：乘法表达式
'''


def multiplicative(tokens):
    child1 = primary(tokens)
    node = child1

    token = tokens.peek()
    if child1 is not None and token is not None:
        if token.getType() == TokenType.Star or token.getType() == TokenType.Slash:
            token = tokens.read()
            child2 = multiplicative(tokens)
            if child2 is not None:
                node = SimpleASTNode(ASTNodeType.Multiplicative, token.getText())
                node.addChild(child1)
                node.addChild(child2)
            else:
                raise Exception("invalid multiplicative expression, exception the right part.")

    return node


'''
语法解析：基础表达式
'''


def primary(tokens):
    node = None
    token = tokens.peek()
    if token is not None:
        if token.getType() == TokenType.IntLiteral:
            token = tokens.read()
            node = SimpleASTNode(ASTNodeType.IntLiteral, token.getText())
        elif token.getType() == TokenType.Identifier:
            token = tokens.read()
            node = SimpleASTNode(ASTNodeType.Identifier, token.getText())
        elif token.getType() == TokenType.LeftParen:
            tokens.read()
            node = additive(tokens)
            if node is not None:
                token = tokens.peek()
                if token is not None and token.getType() == TokenType.RightParen:
                    tokens.read()
                else:
                    raise Exception("excepting right parenthesis")
            else:
                raise Exception("excepting an additive expression inside parenthesis")
    # 这个方法也做了AST的简化，就是不用构造一个primary节点，直接返回子节点。因为它只有一个子节点
    return node


'''
打印输出AST的树状结构
'''


def dumpAST(node, indent):
    print(indent + node.getType().name + " " + node.getText())
    children = node.children
    for child in children:
        dumpAST(child, indent + "\t")


'''
执行脚本，并打印输出AST和求值过程
'''


def evaluate1(script):
    try:
        tree = parse(script)
        dumpAST(tree, "")
        evaluate(tree, "")
    except Exception as e:
        print(e)


def evaluate(node, indent):
    result = 0
    print(indent + "Calculating:" + node.getType().name)
    if node.getType() == ASTNodeType.Programm:
        children = node.getChildren()
        for child in children:
            result = evaluate(child, indent + "\t")
    elif node.getType() == ASTNodeType.Additive:
        child1 = node.getChildren()[0]
        value1 = evaluate(child1, indent + "\t")
        child2 = node.getChildren()[1]
        value2 = evaluate(child2, indent + "\t")
        if node.getText() == "+":
            result = int(value1) + int(value2)
        else:
            result = int(value1) - int(value2)
    elif node.getType() == ASTNodeType.Multiplicative:
        child1 = node.getChildren()[0]
        value1 = evaluate(child1, indent + "\t")
        child2 = node.getChildren()[1]
        value2 = evaluate(child2, indent + "\t")
        if node.getText() == "*":
            result = int(value1) * int(value2)
        else:
            result = int(value1) / int(value2)
    elif node.getType() == ASTNodeType.IntLiteral:
        result = node.getText()
    print(indent + "Result:" + str(result))
    return result


'''
解析脚本，并返回根节点
'''


def parse(code):
    tokens = tokenize(code)
    rootNode = prog(tokens)
    return rootNode


'''
语法解析：根节点
'''


def prog(tokens):
    node = SimpleASTNode(ASTNodeType.Programm, "Calculator")
    child = additive(tokens)
    if child is not None:
        node.addChild(child)
    return node


if __name__ == '__main__':
    script = "int a = b +3;"
    print("解析变量声明语句：" + script)
    tokens = tokenize(script)
    try:
        node = intDeclare(tokens)
        dumpAST(node, "")
    except Exception as e:
        print(e)

    # 测试表达式2
    script = "2+3*5"
    print("\n计算：" + script + "，看上去一切正常。")
    evaluate1(script)
