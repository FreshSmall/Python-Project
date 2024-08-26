import pandas as pd
import numpy as np
import requests
import json


dic ={}
def getUser(list):
    list_param = list.tolist()
    url = 'https://api-medusa.baijia.com/employ/employInfo/search.json'
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
    data = {
        'displayNumbers': list_param
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    dataList = result.get('data')
    for item in dataList:
        dic[item.get('displayNumber')] = item






if __name__ == '__main__':
    list =[]
    df = pd.read_excel('/Users/bjhl/tmk_crm_user.xlsx')
    splits = np.array_split(df['员工工号'].tolist(), 10)
    for array in splits:
        getUser(array)

    for key in dic:
        itemDic = {}
        itemDic['员工工号'] = key
        itemDic['域账号'] = dic[key].get('domain')
        itemDic['姓名'] = dic[key].get('name')
        employMap = dic[key].get('employType')
        itemDic['员工性质'] = employMap.get('name')
        itemDic['隶属部门'] = dic[key].get('departmentPathName')
        itemDic['员工是否生效'] = dic[key].get('hrStatus')
        list.append(itemDic)
    df = pd.DataFrame(list)
    df.to_csv('/Users/bjhl/tmk_crm_user_result.csv', index=False)
