import json

import pandas as pd
import requests

accountType = []
platform = []
accountName = []
accountId = []
accountManagerName = []
accountManagerDept = []
accountProblem = []
accountSolve = []


def read_risk_warn():
    df = pd.read_excel("~/账号问题详情（10.12）.xlsx")
    # print(df.items)
    # print(len(df))

    for i in range(0, len(df)):
        str = df.iloc[i][6]
        str2 = df.iloc[i][7]
        problemList = str.split("\n")
        solveList = str2.split("\n")
        for j in range(0, len(problemList) - 1):
            accountType.append(df.iloc[i][0])
            platform.append(df.iloc[i][1])
            accountName.append(df.iloc[i][2])
            accountId.append(df.iloc[i][3])
            accountManagerName.append(df.iloc[i][4])
            accountManagerDept.append(df.iloc[i][5])
            accountProblem.append(problemList[j][2:len(problemList[j])])
            accountSolve.append(solveList[j][2:len(problemList[j])])


def write_risk_warn():
    # 字典
    dict = {'账号分类': accountType, '账号平台': platform, '账号名称': accountName, '账号ID': accountId, '账号管理者': accountManagerName,
            '账号隶属部门': accountManagerDept, '存在的问题': accountProblem, '处理方式': accountSolve}

    df = pd.DataFrame(dict)

    # 保存 dataframe
    df.to_csv('账号问题详情（10.12）.csv', index=False)


if __name__ == '__main__':
    read_risk_warn()
    write_risk_warn()
