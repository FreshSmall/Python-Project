import json
import requests


query_abnormalty_cno_list = [
10001229,
10001230,
10001231,
10001232,
10001233,
10001234,
10001236,
10001237,
10001238,
10001239,
10001243,
10001244,
10001249,
10001252,
10001253,
10001254,
10001256,
10001257,
10001259,
10001264,
10001265,
10001273,
10001274,
10001275,
10001276,
10001278,
10001283,
10001287,
10001288,
10001289,
10001290,
10001291,
10001292,
10001293,
10001296,
10001298,
10001300,
10001301,
10001312,
10001313,
10001319,
10001321,
10001324,
10001327,
10001328,
10001333,
10001334,
10001337,
10001338,
10001340,
10001341,
10001342,
10001344,
10001346,
10001348,
10001349,
10001350,
10001352,
10001353,
10001355,
10001358,
10001359,
10001364,
10001368,
10001371,
10001372,
10001373,
10001376,
10001378,
10001380,
10001381,
10001382,
10001383,
10001384,
10001387,
10001388,
10001389,
10001390,
10001392,
10001394,
10001395,
10001396,
10001397,
10001398,
10001399,
10001400,
10001401,
10001402,
10001403,
10001404,
10001405,
10001406,
10001407,
10001408,
10001409,
10001410,
10001412,
10001413,
10001414,
10001415,
10001418,
10001419,
10001420,
10001421,
10001422,
10001423,
10001424,
10001425,
10001426,
10001428,
10001429,
10001430,
10001431,
10001433,
10001434,
10001435,
10001436,
10001437,
10001438,
10001444,
10001447,
10001449,
10001452,
10001453,
10001454,
10001455,
10001457,
10001458,
10001459,
10001460,
10001463,
10001465,
10001466,
10001469,
10001472,
10001473,
10001474,
10001475,
10001476,
10001477,
10001478,
10001479,
10001481,
10001482,
10001483,
10001487,
10001488,
10001491
]

def load_json_data(file_path):
    """从JSON文件加载数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"找不到文件: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"JSON格式错误: {file_path}")
        return None
def query_abnormalty_cno(path):
    data = load_json_data(path)
    if data:
        for item in data:
            if item =='':
                pass
            if item.__contains__('37766'):
                print(item+",")


def agent_logout(cno, business_id):
    url = 'https://k8s-call-center-web.baijia.com/agent/logout'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json'
    }
    data = {
        'businessId': business_id,
        'cno': cno
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 检查响应状态
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None
    


if __name__ == '__main__':
    #query_abnormalty_cno('/Users/bjhl/json-format.json')
    for item in query_abnormalty_cno_list:
        logout_result = agent_logout(str(item), 'fc3e')
        print(logout_result)
    print("执行完毕")