import requests
import openpyxl as op


def queryData(url):
    # 添加请求头
    header = {
        "Content-Type": "application/json"
    }
    # 请求参数
    param = {
        "businessType": [],
        "lessonBeginTime": "",
        "lessonEndTime": "",
        "lessonName": "",
        "illegalStatus": ["1"],
        "aiCheckStatus": [
            "3"
        ],
        "assignorName": "",
        "teacherNumber": "",
        "teacherName": "",
        "clazzNumber": "",
        "clazzName": "",
        "playbackStatus": [],
        "assignStatus": [],
        "liveStatus": [],
        "courseType": [],
        "level1Code": [],
        "level2Code": [],
        "level3Code": [],
        "lessonTag": [],
        "grade": [],
        "subject": [],
        "term": [],
        "schoolYear": [],
        "clazzLabel": [],
        "courseLabel": [],
        "type": 20,
        "pageSize": 63,
        "current": 1,
        "size": 10,
        "page": 1,
        "sortType": "",
        "sortOrder": "",
        "expanded": "true",
        "total": 10000,
        "noAssignTotal": 0,
        "showSizeChanger": "true",
        "pageSizeOptions": [
            "10",
            "20",
            "50",
            "100"
        ],
        "pageTotal": 0
    }
    cookie = {
        "cookie": 'CAS_AC_CURRENT_ROLE=%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86%E5%91%98-tag; OUTFOX_SEARCH_USER_ID_NCOO=1695596982.777571; fp=f154971e8762e73ed2a42337c8102c0f; kefu_chat_web_sessionid=OWU2ZTllNzYtZmQwMS00Y2I4LWI4NzUtMjhiZWIxYjhlOThk; GrafanaAuthProxyToken=eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJjYWxsY2VudGVyIn0.eyJpYXQiOjE2Njg2Nzk4NTQzOTcsImdyb3VwcyI6ImNhbGxjZW50ZXIiLCJ1c2VybmFtZSI6InlpbmNoYW8ifQ.I-g62CYX4hhrGMIKM5LuwHFQ2t91ooLMImSwV42N6WWTQokBgY7rf9XEPj4rXKX3Bma-44Vhqgr_qJyjxpSeXj3RsP8l1MlfoQ7ukQv2RFkjdER3k3RWTTYFW4MiWOfHGvkmqI9weFIj4tz0ZDi8jyG3gJAdU2H0oyIzZ69_nZWBSDSpY_nP9GZyYLMd2ZRd0p0uRqaIEuzoInccqBVa7NXAunookom-d3b8JlrA-wG8-5VlpkmB6DjmpDIwlGWofVxIaQMiU509J6yS6eQETpJhFPRn0_gPon5Q5tWbGvwykjR79l5fUBUgFieA4Bj7FjOav_MuO62nuxkoHLcOTw; _const_d_jsession_id_=4278e184afc3462ea55fb2fa03176566.a-be-api.baijia.com/auth/login?next=a.baijia.com; qingzhou_cas_login_cookie="um:gateway:qingzhouCasLogin:8A9A9D909B929C"; a_be_api_sessionid=CF8272E254F00EAC81FA5D0109CB7708'
    }
    # 发送 post 请求
    response = requests.post(url=url, json=param, headers=header, cookies=cookie)
    # print(response.json())
    lessons = response.json().get('data')
    print(len(lessons))
    get_cookie = {
        "cookie": 'CAS_AC_CURRENT_ROLE=%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86%E5%91%98-tag; OUTFOX_SEARCH_USER_ID_NCOO=1695596982.777571; fp=f154971e8762e73ed2a42337c8102c0f; kefu_chat_web_sessionid=OWU2ZTllNzYtZmQwMS00Y2I4LWI4NzUtMjhiZWIxYjhlOThk; GrafanaAuthProxyToken=eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJjYWxsY2VudGVyIn0.eyJpYXQiOjE2Njg2Nzk4NTQzOTcsImdyb3VwcyI6ImNhbGxjZW50ZXIiLCJ1c2VybmFtZSI6InlpbmNoYW8ifQ.I-g62CYX4hhrGMIKM5LuwHFQ2t91ooLMImSwV42N6WWTQokBgY7rf9XEPj4rXKX3Bma-44Vhqgr_qJyjxpSeXj3RsP8l1MlfoQ7ukQv2RFkjdER3k3RWTTYFW4MiWOfHGvkmqI9weFIj4tz0ZDi8jyG3gJAdU2H0oyIzZ69_nZWBSDSpY_nP9GZyYLMd2ZRd0p0uRqaIEuzoInccqBVa7NXAunookom-d3b8JlrA-wG8-5VlpkmB6DjmpDIwlGWofVxIaQMiU509J6yS6eQETpJhFPRn0_gPon5Q5tWbGvwykjR79l5fUBUgFieA4Bj7FjOav_MuO62nuxkoHLcOTw; _const_d_jsession_id_=4278e184afc3462ea55fb2fa03176566.a-be-api.baijia.com/auth/login?next=a.baijia.com; qingzhou_cas_login_cookie="um:gateway:qingzhouCasLogin:8A9A9D909B929C"; a_be_api_sessionid=3AB7ECE523ACB50EE14B3E8E13D0AB97'
    }
    ai_url = "https://a-be-api.baijia.com/duke/courseCheck/{0}/ai_check_info?seq=1"
    # ai_url_1 = "https://a-be-api.baijia.com/duke/courseCheck/3564032/ai_check_info?seq=1"
    excelList = []
    for lesson in lessons:
        url1 = ai_url.format(lesson.get('id'))
        ai_response = requests.get(url=url1, headers=cookie)
        contents = ai_response.json().get('data').get('content')
        for content in contents:
            sentItems = content.get('sentItems')
            sent = content.get('sent')
            for sentItem in sentItems:
                violation = sentItem.get('violation')
                if violation:
                    if violation.get('status') == 2:
                        excelObject = dict()
                        excelObject['illegalStatus'] = 1
                        excelObject['illegalWords'] = sentItem.get('sent')
                        excelObject['illegalSent'] = sent
                        excelList.append(excelObject)
                    elif violation.get('status') == 3:
                        excelObject = dict()
                        excelObject['illegalStatus'] = 0
                        excelObject['illegalWords'] = sentItem.get('sent')
                        excelObject['illegalSent'] = sent
                        excelList.append(excelObject)
    create_xl(excelList, "测试.xlsx")
    #print(len(excelList))


def create_xl(data, fileName):
    # 创建工作簿对象
    wb = op.Workbook()
    # 创建子表
    ws = wb['Sheet']
    ws.append(['AI违规词', '人工是否违规', '违规词所在句'])  # 添加表头
    for i in range(len(data)):
        d = data[i]["illegalWords"], data[i]["illegalStatus"], data[i]["illegalSent"]
        ws.append(d)  # 每次写入一行
    wb.save(fileName)


if __name__ == '__main__':
    url = "https://a-be-api.baijia.com/duke/course/manager"
    queryData(url)
