import requests
import openpyxl as op


def queryData(url, userName, cookie):
    # 添加请求头
    header = {
        "Content-Type": "application/json"
    }
    # 请求参数
    param = {
        "current": 1,
        "pageSize": 50,
        "subTeacherName": userName
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
        queryDataImpl(url, userName, cookie, i, agingCallList)
    # create_xl(agingCallList, "测试.xlsx")
    # print(agingCallList)
    return agingCallList


def queryDataImpl(url, userName, cookie, i, agingCallListTotal):
    # 添加请求头
    header = {
        "Content-Type": "application/json"
    }
    # 请求参数
    param = {
        "current": i,
        "pageSize": 50,
        "subTeacherName": userName
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
    {'id': 1938729, 'city': '北京', 'subTeacherName': '张正冉', 'subTeacherNumber': '10144734920049984', 'studentName': '',
     'studentNumber': '6186151', 'subClazzName': '张正冉1072', 'subClazzNumber': '20974415209956352',
     'firstDistTime': '2023-01-09 13:05:05', 'callCount': 0, 'callStandard': 0, 'level1Code': 85, 'level1Name': '大学',
     'level2Code': 811068, 'level2Name': '考研', 'level3Code': 4134, 'level3Name': '规划课', 'entryDate': '2021-10-14',
     'callRecordSaveTime': None, 'directSuperiorName': '郝丹', 'directSuperiorNumber': '10082121', 'agingCallTag': 0,
     'subTeacherDomain': 'zhangzhengran'}

    ws.append(['城市', '二讲老师', '二讲老师id', '学生名称', '学生编号', '班级名称', '班级id', '首次分配时间', '外呼次数', '是否达标', '一级品类', '二级品类', '三级品类',
               '直属上级'])  # 添加表头
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
                "level3Name"], data[i]["directSuperiorName"]
        ws.append(d)  # 每次写入一行
    wb.save(fileName)


if __name__ == '__main__':
    url = "https://a-be-api.baijia.com/duke/aging_call/list"
    cookie = {
        "cookie": 'fp=35e5966eab3d1fbc58ce3cca3ef1f35c; OUTFOX_SEARCH_USER_ID_NCOO=855479571.6146568; qingzhou_cas_login_cookie="um:gateway:qingzhouCasLogin:8A9A9D909B929C"; prod_portal_gateway_sessionid_2=28124973b60b439587d5338988043fde; GrafanaAuthProxyToken=eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJjYWxsY2VudGVyIn0.eyJpYXQiOjE2NzMzMjA4ODEzODUsImdyb3VwcyI6ImNhbGxjZW50ZXIiLCJ1c2VybmFtZSI6InlpbmNoYW8ifQ.MuUvij5MsqalUkifa5LulOiJFiV1p-a-CY_V8KVZunh2T7s_jRC_Coon4aZJu00sfI5LAvSw37AipedZvW_FPIDK-uVRDYYHf4ZnyX04d8hfV3JLc_SjypjEdMN1Db5dvaQcOhHhEDhpZ7DchBL6O-ycHprKNzROhEsf8_SFWvEJIA8RflIFsU_A7dDGVGTCv8yM8kqX-OaXXAF-3HBayljZRnJNp_252lIt-j5jyHTt74h4lRi60mh0MfNKYWrDmtuGTL6ZuFasGzI1UeCaf6LxNCbDHzwEydzXoyl8ndflAk6O1hzc5j59j9tf7D95FjqU3U2CyeVwusPP1TqPCQ; _const_d_jsession_id_=4eaf8b25c6ee494d8a2f55e80e2ecba9.a-be-api.baijia.com/auth/login?next=a.baijia.com; CAS_AC_CURRENT_ROLE=%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86%E5%91%98-tag; a_be_api_sessionid=6D178E41168151722F14AB3FE0C2B95B'
    }
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
    # names = ["张正冉", "张秀文"]
    totalList = []
    for name in names:
        agingcallList = queryData(url, name, cookie)
        for callList in agingcallList:
            totalList.append(callList)
    create_xl(totalList, "时效质检1.xlsx")
