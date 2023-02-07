import requests
import openpyxl as op
import time
import calendar


def queryData(url, time, cookie):
    # 添加请求头
    header = {
        "Content-Type": "application/json"
    }
    # 请求参数
    param = {
        "current": 1,
        "pageSize": 50,
        "level1Code": [85],
        "firstDistStartTime": time,
        "firstDistEndTime": time+86399999
    }
    # 发送 post 请求
    response = requests.post(url=url, json=param, headers=header, cookies=cookie)
    # print(response.json())
    data = response.json().get('data')
    pagination = data.get('pagination')
    agingCallList = data.get('list')
    # 多次请求
    total = pagination.get('total')
    totalPage = int(total / 50) + 2
    for i in range(2, totalPage):
        queryDataImpl(url, time, cookie, i, agingCallList)
    # create_xl(agingCallList, "测试.xlsx")
    # print(agingCallList)
    return agingCallList


def queryDataImpl(url, time, cookie, i, agingCallListTotal):
    # 添加请求头
    header = {
        "Content-Type": "application/json"
    }
    # 请求参数
    param = {
        "current": i,
        "pageSize": 50,
        "level1Code": [85],
        "firstDistStartTime": time,
        "firstDistEndTime": time+86399999
    }
    # 发送 post 请求
    response = requests.post(url=url, json=param, headers=header, cookies=cookie)
    # print(response.json())
    data = response.json().get('data')
    agingCallList = data.get('list')
    for element in agingCallList:
        agingCallListTotal.append(element)


def create_xl(data, fileName):
    # 创建工作簿对象
    wb = op.Workbook()
    # 创建子表
    ws = wb['Sheet']
    # {'id': 1938729, 'city': '北京', 'subTeacherName': '张正冉', 'subTeacherNumber': '10144734920049984', 'studentName': '',
    #  'studentNumber': '6186151', 'subClazzName': '张正冉1072', 'subClazzNumber': '20974415209956352',
    #  'firstDistTime': '2023-01-09 13:05:05', 'callCount': 0, 'callStandard': 0, 'level1Code': 85, 'level1Name': '大学',
    #  'level2Code': 811068, 'level2Name': '考研', 'level3Code': 4134, 'level3Name': '规划课', 'entryDate': '2021-10-14',
    #  'callRecordSaveTime': None, 'directSuperiorName': '郝丹', 'directSuperiorNumber': '10082121', 'agingCallTag': 0,
    #  'subTeacherDomain': 'zhangzhengran'}

    ws.append(['城市', '二讲老师', '二讲老师id', '学生名称', '学生编号', '班级名称', '班级id', '首次分配时间', '外呼次数', '是否达标', '一级品类', '二级品类', '三级品类',
               '直属上级', '电话记录时间'])  # 添加表头
    for i in range(len(data)):
        if data[i]["callStandard"] == 0:
            data[i]["callStandard"] = "--"
        elif data[i]["callStandard"] == 1:
            data[i]["callStandard"] = "未达成"
        elif data[i]["callStandard"] == 2:
            data[i]["callStandard"] = "达成"
        d = data[i]["city"], data[i]["subTeacherName"], data[i]["subTeacherNumber"], data[i]["studentName"], data[i][
            "studentNumber"], data[i]["subClazzName"], data[i]["subClazzNumber"], data[i]["firstDistTime"], \
            data[i]["callCount"], data[i]["callStandard"], data[i]["level1Name"], data[i]["level2Name"], data[i][
                "level3Name"], data[i]["directSuperiorName"], data[i]["callRecordSaveTime"]
        ws.append(d)  # 每次写入一行
    wb.save(fileName)


if __name__ == '__main__':
    url = "https://a-be-api.baijia.com/duke/aging_call/list"
    cookie = {
        "cookie": 'fp=35e5966eab3d1fbc58ce3cca3ef1f35c; OUTFOX_SEARCH_USER_ID_NCOO=855479571.6146568; gr_user_id=2867ff51-4a72-46db-911d-393a1e44c9fc; _gaotu_track_id_=a06fa012-1572-f228-de4f-d2e8c8445cbf; be26a9c1d6166354_gr_last_sent_cs1=24686; be26a9c1d6166354_gr_cs1=24686; qingzhou_cas_login_cookie="um:gateway:qingzhouCasLogin:8A9A9D909B929C"; CAS_AC_CURRENT_ROLE=%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86%E5%91%98-tag; GrafanaAuthProxyToken=eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJkZW1vIn0.eyJpYXQiOjE2NzU3MzM3NzMwMzksImdyb3VwcyI6InNtcyIsInVzZXJuYW1lIjoieWluY2hhbyJ9.Jfjx9Ohatc-fUEdV0b0fqnPUusEQ3JPd3evefBhgpkJ5dwE0ouf0CLOzS35eciZp-TqS0rGkdJWHfu2_uR5yUcll2EInB2FTPMykhJS1-cOJwZ6o6UlBdQdNTzbSFeKM7aH_Yu2H2lalef8J3BBpBxCXNaJPTcAgC_q9AnBn9Pc5L6lTIoPoQj-K_xa-Af3Rgqm0M1FyakteUwRXPcnLYmevnvLT_Da7lF3oBZu0hwNyZg84mbZ0bv3d1pS_XQhDbYNwEQetAljYzaCFQ-b9H6NrnQI1xgd5jqf--2F484ABxMlMgVHNvLFyZtXSaGesXdBdMWZUXBqTNe4UfapXjQ; _const_d_jsession_id_=c751d24c4a30418aa9e4bca856eb4b05.a-be-api.baijia.com/auth/login?next=a.baijia.com; a_be_api_sessionid=F11E7FA5F99C836540D8EBDB2C608D43'}
    names = ["张正冉",
             "张秀文",
             "胡楠",
             "张廷廷",
             "郭文慧",
             "夏业凤",
             "孟鑫",
             "廉莹莹",
             "黄遵煜",
             "张明月",
             "万新玲",
             "刘丹妮",
             "朴鑫",
             "王依婷",
             "杨彩娟",
             "高霞丽",
             "喻婷",
             "刘贤明",
             "刘贝贝",
             "李云阳",
             "周玄",
             "蔺雪薇",
             "赵雪言",
             "张凯娣",
             "康清",
             "张泽明",
             "李茸茸",
             "李娜",
             "陈新宇",
             "靖晓维",
             "李敏",
             "张志聪",
             "薄静茹",
             "王静静",
             "朱宇",
             "孙玥",
             "李玉梅",
             "张淑晴",
             "冯保乐",
             "杨梦馨",
             "付雨田",
             "郎辰雨",
             "刘江帆",
             "王庆华",
             "赵静霞",
             "郝静文",
             "杨光",
             "刘妍",
             "罗梦霞",
             "段亚男",
             "翟梦娜",
             "吴静",
             "王文杰",
             "王佳梁",
             "高洋",
             "方文江",
             "李静",
             "祁欣",
             "周雨欣",
             "王东丽",
             "刘路路",
             "谭照盈",
             "武晓晓",
             "王茂林",
             "张越",
             "罗瑛",
             "范程雪",
             "张炜哲",
             "刘金"]
    totalList = []
    times = [
        1674403200000,
        1674489600000,
        1674576000000,
        1674662400000,
        1674748800000,
        1674835200000,
        1674921600000,
        1675008000000,
        1675094400000,
        1675180800000,
        1675267200000,
        1675353600000,
        1675440000000,
        1675526400000
    ]
    for time in times:
        agingCallList = queryData(url, time, cookie)
        for callList in agingCallList:
            totalList.append(callList)
            #callCount = callList.get("callCount")
            #firstDistTime = callList.get("firstDistTime")
            #callRecordTime = callList.get("callRecordSaveTime")
            # if callRecordTime is not None:
            #     distTimestamp = calendar.timegm(time.strptime(firstDistTime, "%Y-%m-%d %H:%M:%S"))
            #     callRecordTimestamp = calendar.timegm(time.strptime(callRecordTime, "%Y-%m-%d %H:%M:%S"))
            #     if callRecordTimestamp - distTimestamp < 604800:
            #         totalList.append(callList)
    create_xl(totalList, "时效质检2.xlsx")
    # print(len(totalList))
