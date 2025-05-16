import json

import pandas as pd
import requests

secondDepart = []
thirdDepart = []


def read_depart():
    df = pd.read_excel("~/depart.xlsx")
    for i in range(0, len(df)):
        str1 = str(df.iloc[i][0])

        if str1 != None:
            if str1.__contains__("-"):
                strList = str1.split("-")
                if len(strList) >= 3:
                    secondDepart.append(strList[2])
                if len(strList) >= 4:
                    thirdDepart.append(strList[3])

    print("二级部门列表")
    print(set(secondDepart))
    print("三级部门列表")
    print(set(thirdDepart))


if __name__ == '__main__':
    read_depart()
