import requests

cookies = {'test_tmk_crm_sessionid_version_6': 'Y2ViOTNkNjUtNTNiNC00NGE0LThhZWItMDMzMzZhZjYyMTMz'}

# 通话记录列表
host1 = 'https://test-api-tmk-crm.baijia.com/call-record/list'
# 获取通话记录手机号
host2 = 'https://test-api-tmk-crm.baijia.com/call-record/get-mobile'

# 短信记录列表
host3 = 'https://test-api-tmk-crm.baijia.com/sms-record/list'
# 获取短信记录手机号
host4 = 'https://test-api-tmk-crm.baijia.com/sms-record/get-mobile'

# 人工外呼列表
host5 = 'https://test-api-tmk-crm.baijia.com/task/to-be-executed'
# 人工外呼手机号
host6 = 'https://test-api-tmk-crm.baijia.com/task/get-mobile'
# 预测式外呼手机号
host7 = 'https://test-api-tmk-crm.baijia.com/predict-task/get-mobile'


# 黑名单列表
host8 = 'https://test-api-tmk-crm.baijia.com/blacklist/list'
# 获取黑名单手机号
host9 = 'https://test-api-tmk-crm.baijia.com/blacklist/decrypt'

# 线索列表
host10 = 'https://test-api-tmk-crm.baijia.com/clue-pool/list'
# 任务包任务列表
host11 = 'https://test-api-tmk-crm.baijia.com/task/list'
# 任务执行列表
host12 = 'https://test-api-tmk-crm.baijia.com/task-execute/list'

host_dic = {}
host_dic['host1'] = host1
host_dic['host2'] = host2
host_dic['host3'] = host3
host_dic['host4'] = host4
host_dic['host5'] = host5
host_dic['host6'] = host6
host_dic['host7'] = host7
host_dic['host8'] = host8
host_dic['host9'] = host9
host_dic['host10'] = host10
host_dic['host11'] = host11
host_dic['host12'] = host12



data1 = {"page":{"pageSize":10,"pageNum":1},"pageSize":10,"currentPage":1,"totalPage":51,"total":502,"sceneId":"5d97"}
data2 = {"callId":10483,"sceneId":"5d97"}
data3 = {"page":{"pageSize":10,"pageNum":1},"sceneId":"5d97"}
data4 = {"smsId":449669,"sceneId":"5d97"}
data5 = {"taskPackageId":1479,"taskStatus":[1],"page":{"pageNum":1,"pageSize":20},"sceneId":"5d97"}
data6 = {"taskId":654090,"sceneId":"5d97"}
data7 = {"queryType":1,"taskId":654478,"sceneId":"5d97"}
data8 = {"page":{"pageSize":10,"pageNum":1},"sceneId":"5d97"}
data9 = {"id":140426,"sceneId":"5d97"}
data10 = {"poolId":561,"page":{"pageNum":1,"pageSize":10},"sceneId":"5d97"}
data11 = {"taskPackageId":1221,"page":{"pageNum":1,"pageSize":10},"sceneId":"5d97"}
data12 = {"taskPackageId":1479,"page":{"pageNum":1,"pageSize":10},"sceneId":"5d97"}

data_dic = {}
data_dic['data1'] = data1
data_dic['data2'] = data2
data_dic['data3'] = data3
data_dic['data4'] = data4
data_dic['data5'] = data5
data_dic['data6'] = data6
data_dic['data7'] = data7
data_dic['data8'] = data8
data_dic['data9'] = data9
data_dic['data10'] = data10
data_dic['data11'] = data11
data_dic['data12'] = data12


for i in range(12):
    index = i+1
    print(f'host{index}')
    host_index = f'host{index}'
    data_index = f'data{index}'
    r = requests.post(url=host_dic[host_index], json=data_dic[data_index], cookies=cookies)
    print(host_dic[host_index])
    print(r.json())