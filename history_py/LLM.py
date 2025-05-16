import pandas as dp
import requests
from openai import OpenAI

api_key = 'sk-9f79766b955742159e55b2e241cecaa1'
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'

client = OpenAI(
    api_key="gAAAAABmFmLplODi2NxnZYnkqEG177I6cfZguGJ_kYncc6y95ViTka9uMryxXla1KJWSRtp2Lv7-p5Gk-rCxMvALTUneEykefaUIkhPeD_uDam3ENi2OMoKn3ui5FWMIeHcbUXfbQ_Yl",
    base_url="https://aiops-api.baijia.com/openai/v1"
)


def get_llm_answer(input):
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_key}'}
    body = {
        'model': 'qwen-turbo',
        "input": {
            "messages": [
                {
                    "role": "system",
                    "content": "请参考下面格式，输入题目信息以及对应的候选知识标签集，我会根据你的题目信息给您确定题目在候选知识标签集合中最匹配的知识点标签。### 题目题干信息：{body}### 题目选项信息：{selection}### 题目解析信息：{answerInfo}### 题目答案信息：{answer}### 候选知识标签集：{topK}"
                },
                {
                    "role": "user",
                    "content": f"{input}"
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()['output']['choices'][0]['message']['content']


def get_openapi_answer(input):
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system",
             "content": "现在你扮演一名中国高中数学老师，你对高中数学的题目及其对应考察的知识点非常熟悉。请参考下面格式，输入题目信息以及对应的候选知识标签集，我会根据你的题目信息给您确定题目在候选知识标签集合中最匹配的知识点标签,匹配的标签需要从候选的知识标签集中获取。匹配知识标签时需要提前分析选择该标签的原因，返回的数据格式中只包含最符合候选知识的标签，多个标签只用逗号分隔。### 题目题干信息：{body}### 题目选项信息：{selection}### 题目解析信息：{answerInfo}### 题目答案信息：{answer}### 候选知识标签集：{topK}"},
            {"role": "user", "content": f"{input}"}
        ]
    )
    return completion.choices[0].message.content


def get_mark_accuracy(param):
    url = 'https://jiaoyan-gateway.baijia.com/jiaoyan-tiku/question/manage/getMarkAccuracy'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=param)
    print(param)
    return response.json()


def get_top_count(topN, count):
    list = topN.split(',')
    if len(list) > count:
        return ','.join(list[:count])
    else:
        return topN



if __name__ == '__main__':
    df = dp.read_excel('/Users/bjhl/test_label.xlsx')
    list = []
    param_dic = {}
    row = 1
    for item in df.iterrows():
        id = item[1]['题目id']
        topN = item[1]['小模型推荐的topN']
        top5 = get_top_count(topN, 5)
        question = item[1]['逻辑题型']
        tigan = item[1]['题干']
        jiexi = item[1]['解析']
        answer = item[1]['答案']
        biaoqian = item[1]['题目绑定的核心标签名称']
        content = f'题目题干信息：{tigan} \r\n 题目解析信息:{jiexi} \r\n 题目答案信息:{answer} \r\n 候选知识标签集:{topN}'
        result = get_openapi_answer(content)
        print(f'第{row}行,题型:{question},正确标签集:{biaoqian}》》》》》》计算的标签集:{result}')
        dic = {}
        dic['questionId'] = id
        dic['labelNames'] = result.split(',')
        list.append(dic)
        row += 1
        if row > 5:
            break
    param_dic['labelMarkReqs'] = list
    param_dic['onlyCoreLabel'] = True
    param_dic['useNameMark'] = True
    score = get_mark_accuracy(param_dic)
    print(score)
