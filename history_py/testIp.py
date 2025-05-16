import pandas as pd
import json


def get_user_id_count(list):
    for item in list:
        data = json.loads(item)
        call_id = data.get('callId')
        print(call_id)


if __name__ == '__main__':
    df = pd.read_csv('/Users/bjhl/lishaoming.csv')
    grouped = df.query("_requestUri == '/call-record/get-mobile'").groupby('_IP')
    list = []
    count_1 = 0
    for group_label, group_indices in grouped.groups.items():
        dic ={}
        count = len(group_indices)
        dic['ip'] = group_label
        dic['time'] = df.loc[group_indices[0], "_@timestamp"]
        dic['外呼次数'] = len(group_indices)
        count_1 += count
        param = df.loc[group_indices,"_requestBody"].to_list()
        #print(get_user_id_count(param))
        #print("ip:", group_label)
        #print("time:", df.loc[group_indices[0], "_@timestamp"])
        list.append(dic)
        print(dic)
    #out_df = pd.DataFrame(list)
    #out_df.to_csv('/Users/bjhl/lishaoming_out2.csv', index=False)
