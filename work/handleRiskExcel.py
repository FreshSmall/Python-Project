import json

import pandas as pd
import requests


# 定义调用API接口的函数
def request_department_info(department_number):
    url = 'https://api-medusa.baijia.com/department/listSearch.json'
    headers = {
        'appId': 'ticket-access-token',
        'time': '1638344398',
        'sign': '42020b5c0fff5bf7c96273a5240eaf97',
        'Content-Type': 'application/json'
    }
    data = {
        "numbers": [department_number]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        api_response = response.json()
        # Process the API response here
        print(api_response)
        return api_response
    else:
        print(f"Error: {response.status_code} - {response.text}")


def request_employ_info(display_number):
    url = 'https://api-medusa.baijia.com/employ/employInfo/search.json'
    headers = {
        'appId': 'ticket-access-token',
        'time': '1638344398',
        'sign': '42020b5c0fff5bf7c96273a5240eaf97',
        'Content-Type': 'application/json'
    }
    data = {
        "displayNumbers": [display_number]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        api_response = response.json()
        # Process the API response here
        print(api_response)
        return api_response
    else:
        print(f"Error: {response.status_code} - {response.text}")


dttype = {
    '账号平台': str,
    '管理部门编号': str
}

# 读取原始Excel数据
input_file = '/Users/bjhl/commonAccount.xlsx'  # 替换为你的原始Excel文件名
df = pd.read_excel(input_file, sheet_name='Sheet1', dtype=dttype)


# 定义获取部门管理员信息的函数
def get_department_manager(department_number):
    # 替换为你的API接口URL和需要的参数
    if pd.isna(department_number):
        return ""
    depart_info = request_department_info(str(department_number))
    if depart_info.get('data') != None:
        list = depart_info.get('data').get('list')
        if len(list) > 0:
            display_number = depart_info.get('data').get('list')[0].get('owner')
            employ_info = request_employ_info(display_number)
            numbers = ''.join(filter(str.isdigit, employ_info.get('data')[0].get('domain')))
            return employ_info.get('data')[0].get('name') + numbers
        else:
            return ""


# 直属上级
def get_employ_info(display_number):
    if pd.isna(display_number):
        return ""
    list_employ = display_number.split('-')
    employ_info = request_employ_info(list_employ[-1])
    numbers = ''.join(filter(str.isdigit, employ_info.get('data')[0].get('domain')))
    return employ_info.get('data')[0].get('name') + numbers


# 直属上上级
def get_employ_info1(display_number):
    if pd.isna(display_number):
        return ""
    list_employ = display_number.split('-')
    employ_info = request_employ_info(list_employ[-2])
    numbers = ''.join(filter(str.isdigit, employ_info.get('data')[0].get('domain')))
    return employ_info.get('data')[0].get('name') + numbers


# 对每个部门编号调用接口获取部门管理员信息
df['部门管理员'] = df['管理员部门编号'].apply(get_department_manager)

#df['直属上级'] = df['管理员路径'].apply(get_employ_info)

# 直属上上级
#df['直属上上级'] = df['管理员路径'].apply(get_employ_info1)

# 输出新的Excel文件
output_file = '通用账号.xlsx'  # 新的Excel文件名
df.to_excel(output_file, index=False)
print(df)

if __name__ == '__main__':
    pass
