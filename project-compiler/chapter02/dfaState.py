from enum import Enum


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
