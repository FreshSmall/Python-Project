from enum import Enum


class ASTNodeType(Enum):
    # 程序入口，根节点
    Programm = 1
    # 整型变量声明
    IntDeclaration = 2
    # 表达式语句，即表达式后面跟个分号
    ExpressionStmt = 3
    # 赋值语句
    AssignmentStmt = 4
    # 基础表达式
    Primary = 5
    # 乘法表达式
    Multiplicative = 6
    # 加法表达式
    Additive = 7
    # 标识符
    Identifier = 8
    # 整型字面量
    IntLiteral = 9
