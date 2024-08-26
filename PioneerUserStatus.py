import requests
import pandas as pd
import json


def getMedusaResponse(userNumberList):
    url = "https://api-medusa.baijia.com/employ/employInfo/search.json"
    payload = {
        "displayNumbers": userNumberList
    }
    headers = {
        'appId': 'ticket-access-token',
        'time': '1638344398',
        'sign': '42020b5c0fff5bf7c96273a5240eaf97',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'api-medusa.baijia.com',
        'Connection': 'keep-alive'
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    listObj = data.get("data")
    dic = {}
    for obj in listObj:
        dic[obj.get("displayNumber")] = obj.get("hrStatus")
    return dic


def isMedusa(userNumber):
    return userNumber > 10000000


def convertUser(userNumberList):
    list = []
    for number in userNumberList:
        list.append(str(int(number)))
    return list


def getCasResponse():
    dic = {}
    df = pd.read_excel("~/cas数据.xlsx", sheet_name="Sheet1")
    for row in df.iterrows():
        dic[str(row[1].get("id"))] = row[1].get("status")
    return dic


if __name__ == '__main__':
    list = []
    df = pd.read_excel("~/坐席元数据.xlsx", sheet_name="Sheet1")
    threshold = 10000000
    query_df = df.query("user_number > @threshold")
    userList = query_df["user_number"].unique()
    userList_str = convertUser(userList)
    userMap = getMedusaResponse(userList_str)
    casMap = getCasResponse()
    grouped = df.groupby("scene_id")
    for group in grouped:
        dic = {}
        dic["scene_id"] = group[0]
        group_userList = group[1]["user_number"]
        dic["用户数"] = group_userList.size
        c1 = 0
        c2 = 0
        for user in group_userList:
            if user > 10000000:
                c1 = c1 + 1
            else:
                c2 = c2 + 1
        dic["用户数（内部）"] = c1
        dic["用户数（外包）"] = c2
        # 坐席数
        c3 = 0
        # 坐席数内部
        c4 = 0
        # 坐席数外包
        c5 = 0
        # 用户数内部在职
        c6 = 0
        # 坐席数内部在职
        c7 = 0
        # 用户数外包在职
        c8 = 0
        # 坐席数外包在职
        c9 = 0
        for i in range(group_userList.size):
            obj = group[1].iloc[i]
            user_number = obj["user_number"]
            user_number_str = str(int(user_number))
            cno = obj["cno"]
            if cno is not None:
                c3 = c3 + 1
            if user_number > 10000000 and cno is not None:
                c4 = c4 + 1
                if userMap.get(user_number_str) == "A":
                    c7 = c7 + 1
            if user_number < 10000000 and cno is not None:
                c5 = c5 + 1
                if casMap.get(user_number_str) == 0:
                    c9 = c9 + 1
            if user_number > 10000000:
                if userMap.get(user_number_str) == "A":
                    c6 = c6 + 1
            if user_number < 10000000:
                # print('scene_id:{},user_number:{},status:{}'.format(group[0], user_number_str,casMap.get(user_number_str)))
                if casMap.get(user_number_str) == 0:
                    c8 = c8 + 1

        dic["坐席数"] = c3
        dic["坐席数（内部）"] = c4
        dic["坐席数（外包）"] = c5
        dic["用户数（内部在职）"] = c6
        dic["坐席数（外包在职）"] = c9
        dic["用户数（外包在职）"] = c8
        list.append(dic)
    out_df = pd.DataFrame(list)
    out_df.to_excel('~/坐席.xlsx', index=False)
