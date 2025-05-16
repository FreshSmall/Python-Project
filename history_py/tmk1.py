import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('/Users/bjhl/pioneer_clue.csv', delimiter=',')
    list_dic = []
    for index, row in df.iterrows():
        dic = {}
        str_body = row['mail_body']
        if str_body.__contains__('线索上传成功'):
            str_array = str_body.split('，')
            dic['场景名称'] = str_array[0]
            count = 0
            if str_array[1] == '线索上传成功':
                count = str_array[2].split('：')[1]
            else:
                count_str = str_array[1].split('：')[1]
                count = count_str.split(' ,')[0]
            dic['success_count'] = count
            list_dic.append(dic)
    total_count = 0
    business_dic_list = {}
    business_list = []
    for item in list_dic:
        business_str = item['场景名称']
        if business_dic_list.get(business_str) is None:
            business_dic_list[business_str] = int(item['success_count'])
        else:
            business_dic_list[business_str] += int(item['success_count'])

    for item in business_dic_list.items():
        business_list.append(item)
    out = pd.DataFrame(business_list)
    out.to_excel('/Users/bjhl/clue_upload_result.xlsx', index=False)

