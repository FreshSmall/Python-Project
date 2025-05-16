import re
import requests

def extract_cno(json_string):
    """
    从JSON字符串中提取cno值
    :param json_string: 输入的JSON字符串
    :return: 提取到的cno值，如果没找到返回None
    """
    pattern = r'"cno"\s*:\s*"(\d+)"'
    match = re.search(pattern, json_string)
    
    if match:
        return match.group(1)
    return None

def logout_agent(business_id, cno):
    """
    调用登出接口
    :param business_id: 业务ID
    :param cno: 坐席号
    :return: 响应结果
    """
    url = 'https://test-k8s-call-center-web.baijia.com/agent/logout'
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

# 测试代码
if __name__ == '__main__':
    # 测试提取cno
    test_json = '''{"bsi":"fc3e","bt":2,"tid":0,"ect":"Dec 4, 2024, 8:42:25 PM","cno":"10001491","si":"201430","bindTel":"10001491","extType":0,"predictTaskId":"37766","callType":0}'''
    cno = extract_cno(test_json)
    if cno:
        print(f"提取到的cno值: {cno}")
    
    # 测试登出接口
    result = logout_agent('5eca', '5003')
    if result:
        print(f"登出结果: {result}") 