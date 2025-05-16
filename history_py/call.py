import pandas as pd
import concurrent.futures
import requests
import json


# 假设这是你的上传函数
def upload_call_record(param):
    #param_str = str(param)
    url = "https://k8s-call-center-api.baijia.com/zhongtian/push/call-event"
    headers = {'Content-Type': 'application/json'}
    #param_data = json.loads(param_str)
    response = requests.request("POST", url, headers=headers, json=param)
    response_data = response.json()
    print(response_data)


def process_row(row):
    message = row['message']
    data = message.split('payload=')[1]
    length = len(data)
    param = data[:length - 1]
    upload_call_record(param)


# 读取CSV文件
df = pd.read_csv('/Users/bjhl/Downloads/openapi_log_58.csv')
dic = {}

# if __name__ == '__main__':
#     # 使用线程池并行处理每一行
#     with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
#         futures = [executor.submit(process_row, row) for index, row in df.iterrows()]
#
#         # 等待所有任务完成
#         for future in concurrent.futures.as_completed(futures):
#             try:
#                 future.result()  # 获取结果以捕获可能的异常
#             except Exception as e:
#                 print(f"Error occurred: {e}")

import http.client
import json

def run(cno):
    conn = http.client.HTTPSConnection("k8s-call-center-web.baijia.com")
    payload = json.dumps({
        "businessId": "fc3e",
        "cno": cno
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'k8s-call-center-web.baijia.com',
        'Connection': 'keep-alive'
    }
    conn.request("POST", "/agent/logout", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


if __name__ == '__main__':
    # for index, row in df.iterrows():
    #     message = row['message']
    #     data = message.split('payload=')[1]
    #     length = len(data)
    #     param = data[:length - 1]
    #     param_json = json.loads(param)
    #     call_id = param_json['data']['callid']
    #     if dic.get(call_id) is None:
    #         dic[call_id] = param_json
    #
    # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    #     # 提交任务并获取Future对象
    #     futures = [executor.submit(upload_call_record, dic[key]) for key in dic.keys()]
    #
    #     # 等待所有任务完成
    #     for future in concurrent.futures.as_completed(futures):
    #         try:
    #             future.result()  # 获取结果以捕获可能的异常
    #         except Exception as e:
    #             print(f"Error occurred: {e}")
    for i in range(300):
        run(i)