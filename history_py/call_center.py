import pandas as pd
import json


def main():
    df = pd.read_csv('/Users/bjhl/Downloads/fe3c.csv')
    call_event_list = []
    for row, it in df.iterrows():
        dic = {}
        message = it["message"]
        payload_str = message.split('payload=')[1]
        payload = payload_str[:len(payload_str) - 1]
        print(payload)
        dic_json = json.loads(payload)
        type_value = dic_json.get('type')
        if type_value == 1:
            dic['type'] = type_value
            dic['result'] = dic_json.get('data').get('result')
            dic['result_code'] = dic_json.get('data').get('result_code')
            dic['callId'] = dic_json.get('data').get('callid')
            call_event_list.append(dic)

    out_df = pd.DataFrame(call_event_list)
    out_df.to_excel('/Users/bjhl/Downloads/fe3c_out.xlsx', index=False)


def main1():
    txt_url = '/Users/bjhl/计算机单词.txt'
    with open(txt_url, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    word_list = []
    for item in lines:
        try:
            dic = {}
            word_array = item.split(',', 1)
            en_word_str = word_array[0].split('.')
            en_word = en_word_str[1]
            ch_word = word_array[1]
            dic['en'] = en_word
            dic['ch'] = ch_word
            word_list.append(dic)
        except Exception as e:
            print(e)
            print(item)
    out_df = pd.DataFrame(word_list)
    out_df.to_excel('/Users/bjhl/Downloads/word_out.xlsx', index=False)


if __name__ == '__main__':
    main1()
