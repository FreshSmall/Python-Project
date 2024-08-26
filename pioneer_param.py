import pandas as pd
from datetime import datetime


def switch(row, str_path):
    if str_path == "/clue-pool/list":
        startTime = row['createTimeStart']
        endTime = row['createTimeEnd']
        time_str = f'{startTime}---{endTime}'
        return time_str
    elif str_path == "/task-execute/list":
        startTime = row['taskAssignTimeStart']
        endTime = row['taskAssignTimeEnd']
        time_str = f'{startTime}---{endTime}'
        return time_str
    elif str_path == "/task/list":
        startTime = row['clueCreateTimeStart']
        endTime = row['clueCreateTimeEnd']
        time_str = f'{startTime}---{endTime}'
        return time_str
    elif str_path == "/user-task/list":
        startTime = row['executeTimeStart']
        endTime = row['executeTimeEnd']
        time_str = f'{startTime}---{endTime}'
        return time_str


# 定义一个辅助函数来计算时间范围的差值
def time_difference_in_seconds(time_range: str) -> int:
    start_str, end_str = time_range.split('---')
    if start_str == 'nan':
        return 1000000000000
    start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
    return (end_time - start_time).total_seconds()


if __name__ == '__main__':
    dic = {}
    param_dic = {}
    df = pd.read_csv('/Users/bjhl/tmk_param')
    grouped = df.groupby('path')
    for group_label, group_indices in grouped.groups.items():
        group_data = df.loc[group_indices]
        param_list = []
        param_count = 0
        param_dic = {}
        for idx, row in group_data.iterrows():
            time_str = switch(row, group_label)
            param_dic[time_str] = param_dic.get(time_str, 0) + 1
            if time_str not in param_list:
                param_list.append(time_str)
        dic[group_label] = param_dic
        group_label = group_label.replace('/list', '')
        df1 = pd.DataFrame(param_dic.items(), columns=['time_range', 'count'])
        df1.to_excel(f'/Users/bjhl/{group_label}.xlsx', index=False)
        print(f"{group_label} done")
    # for key, value in dic.items():
    #     print(key)
    #     total = 0
    #     sorted_time_ranges = sorted(value, key=lambda x: -time_difference_in_seconds(x))
    #     for time_range in sorted_time_ranges:
    #         print(f"time_range={time_range},count={value[time_range]}")
    #         total += value[time_range]
    #     print(f"total={total}")
