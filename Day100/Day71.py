import pandas as pd
import numpy as np
import openpyxl


def run1():
    scores = np.random.randint(60, 101, (5, 3))
    courses = ['语文', '数学', '英语', ]
    ids = [1001, 1002, 1003, 1004, 1005]
    df1 = pd.DataFrame(data=scores, columns=courses, index=ids)
    print(df1)


def run2():
    scores = {
        '语文': [62, 72, 93, 88, 93],
        '数学': [95, 65, 86, 66, 87],
        '英语': [66, 75, 82, 69, 82],
    }
    ids = [1001, 1002, 1003, 1004, 1005]
    df2 = pd.DataFrame(data=scores, index=ids)
    print(df2)


def readCsv():
    df3 = pd.read_csv('/Users/yinchao/account.csv', index_col='id')
    print(df3)


def readExcel():
    df4 = pd.read_excel('/Users/yinchao/account.xlsx')
    group = df4.groupby('隶属部门路径')
    listObj = list(group)
    for obj in listObj:
        print(obj)


if __name__ == '__main__':
    readCsv()
