import requests
import hashlib
import pandas as pd
import math
import ssl
import os
import json


# -*- coding : utf-8 -*-
# coding: utf-8
def getSign(roomNumber):
    str = "roomId={}&sessionId={}&format={}&expire={}".format(roomNumber, 0, "mp4", 2592000)
    hs = hashlib.md5()
    hs.update(str.encode('utf-8'))  # 进行MD5加密
    keyRes = hs.hexdigest()
    return keyRes


def getPlaybackUrl(row):
    roomNumber = row["room_number"]
    if math.isnan(roomNumber):
        return ""
    print(roomNumber)
    roomNumber = str(roomNumber)
    if len(roomNumber) == 0:
        return ""
    urlformat = "http://backend-api.wenzaizhibo.com/playback/getVideoUrlByRoomId?roomId={}&sign={}&sessionId=0&format=mp4&expire=2592000"
    sign = getSign(roomNumber)
    url = urlformat.format(roomNumber, sign)
    response = requests.get(url)
    data = response.json()
    if data.get("code") != 0:
        return ""
    return data.get('data').get('url')


def test(roomNumber):
    print(getSign(roomNumber))


def containMobile(listCol):
    for mobile in listCol:
        if mobile == "手机号":
            return True
    return False


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_excel('/Users/bjhl/1v1.xlsx')
    df["回放链接"] = df.apply(getPlaybackUrl, axis=1)
    df["room_number"] = df["room_number"].astype(str)
    df["clazz_lesson_number"] = df["clazz_lesson_number"].astype(str)
    output_file_path = "/Users/bjhl/1v1_play_1213.xlsx"  # 替换为您想要保存的文件路径
    df.to_excel(output_file_path, index=False)
#
#     # df = pd.read_excel('/Users/bjhl/v-v-jiaxiaofeng.xlsx')
#     # print(df.groupby(["_requestBody"], as_index=False).count())
#
# #     df = pd.read_csv('/Users/bjhl/data_mobile.csv')
# #     uploadUrl = df['upload_url'].tolist()
# #     clue = dict()
# #     totalCount = 0
# #     for row in df.iterrows():
# #         scene_id = row[1]['scene_id']
# #         uploadUrl = row[1]['upload_url']
# #         item = pd.read_excel(uploadUrl, keep_default_na=False)
# #         rowCount = item.shape[0]
# #         existCount = clue.get(scene_id)
# #         if existCount is None:
# #             clue[scene_id] = rowCount
# #         else:
# #             clue[scene_id] = existCount + rowCount
# # print(clue)
# if __name__ == '__main__':
#     # list = []
#     # df = pd.read_csv('/Users/bjhl/1221-0513.csv', delimiter='\t')
#     #
#     # callMap = {}
#     # #
#     # for row in df.iterrows():
#     #     userId = row[1]['user_id']
#     #     callId = row[1]['id']
#     #     callMap[callId] = userId
#     #
#     # df1 = pd.read_csv('/Users/bjhl/log_0507-0514.csv')
#     # list = []
#     # for row in df1.iterrows():
#     #     dic = {}
#     #     mapStr = row[1]['_requestBody']
#     #     domain = row[1]['_userDomain']
#     #     dict_result = json.loads(mapStr)
#     #     callId = dict_result.get('callId')
#     #     sceneId = dict_result.get('sceneId')
#     #     if callMap.get(callId) is not None:
#     #         dic['call_id'] = callId
#     #         dic['user_id'] = callMap[callId]
#     #         list.append(dic)
#     # out_df = pd.DataFrame(list)
#     # out_df.to_csv('~/user_id-1221-0513.csv', index=False)
#     df = pd.read_csv('/Users/bjhl/log-0507-0514.csv')
#     list = []
#     for row in df.iterrows():
#         dic = {}
#         mapStr = row[1]['_requestBody']
#         domain = row[1]['_userDomain']
#         datetime = row[1]['_time_']
#         dict_result = json.loads(mapStr)
#         callId = dict_result.get('callId')
#         datetime_str = str(datetime)
#         timeList = datetime_str.split('T')
#         dic['userDomain'] = domain
#         dic['callId'] = callId
#         dic['time'] = timeList[0]
#         list.append(dic)
#
#     out_df = pd.DataFrame(list)
#     out_df.to_csv('~/user-call-detail.csv', index=False)
