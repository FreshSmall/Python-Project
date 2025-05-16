import json

import pandas as pd
import requests

templates = [
    {
        "subject": "【重要】高途集团自媒体账号授权邮件通知",
        "receiver": "收件人",
        "receiver_name": "账号管理者",
        "cc": "抄送人",
        "digits": [("管理者", "账号管理者"), ("账号平台", "账号平台"), ("账号ID", "账号ID"), ("账号名称", "账号名称"), ("是否授权", "是否授权")],
        "mail": """
<p><b>{receiver_name}</b>，你好</p>

<p>公司正在进行数字资产盘点，盘点到你名下资产如下：</p>
<p style="color: red;"><b>请回复下本邮件账号是否标记账号状态为停用</b></p>
<table border="1">
<thead>
<tr>
    <th>管理者</th>
    <th>账号平台</th>
    <th>账号ID</th>
    <th>账号名称</th>
    <th>是否授权</th>
</tr>
</thead>
<tbody>
{digits}
</tbody>
</table>

<p>【盘点时间】2023-07-20 8:00 到 2023-07-21 18:00</p>

<p>【盘点方式】</p>

<ol>
<li>点击登录 https://digit.baijia.com/</li>

<li>查看自己名下账号信息，进行授权操作。</li>

<img src="https://doc.baijia.com/uploader/f/QzJCiHF44IxV8XVG.png" alt="操作说明" width="800" />
</ol>
      
<p>【重点说明】</p>

<ul>
<li style="color: red;"><b>注意：该账号会成为后续财务打款依据，假设不在该系统中，不予进行财务打款操作。</b></li>
</ul>
<p>【疑问解答】</p>
<ul>
<li>如有任何疑问，联系周子晗或是张雯婷03，感谢各位伙伴的支持！祝好~</li>
</ul>

        """,
        "sheet_name": "Sheet1"
    }
]

mails = []

for template in templates:
    df = pd.read_excel("~/账号邮件0720.xlsx", sheet_name=template["sheet_name"])
    grouped = df.groupby(template["receiver"])
    # loop through each group
    for receiver, group in grouped:
        receiver_name = group[template["receiver_name"]].iloc[0]
        cc = group[template["cc"]].iloc[0] if template["cc"] else ""
        # loop through each row in the group
        digits = ""
        for index, row in group.iterrows():
            digits += "<tr>\n"
            for digit in template["digits"]:
                if digit[0] == '是否授权':
                    value = '否'
                else:
                    value = row[digit[1]] if digit[1] in row else "--"
                digits += f"<td>{value}</td>\n"
            digits += "</tr>\n"
        context = {
            "receiver_name": receiver_name,
            "digits": digits,
            "cc": cc,
            "receiver": receiver,
            "subject": template["subject"],
        }
        mail = template["mail"].format(**context)
        context['mail'] = mail
        mails.append(context)

# send
key = "SK9hrT4snezs91jihBJgqHPpW2kSzjoH"


def max_mails(mails):
    """
    获取邮件正文最长的邮件
    """
    max_len = 0
    max_mail = None
    for mail in mails:
        if len(mail["mail"]) > max_len:
            max_len = len(mail["mail"])
            max_mail = mail
    return max_mail


def demo_send(mail, receivers, ccs):
    body = {
        "channel": 1,
        "title": mail["subject"],
        "content": f"""
        <p>实际收件人: {mail["receiver"]}</p>
        <p>实际抄送人: {mail["cc"]}</p>
        {mail["mail"]}
        """,
        "receivers": receivers,
        "ccs": ccs,
    }
    print("发送邮件给", mail["receiver"], "抄送给", mail["cc"])
    requests.post(f"http://message-center.baijia.com/bailing/{key}.send", json=body)

sends =[
'liufangming',
'yangpingan',
'caoweijia',
'chenkaixuan',
'chenxu12',
'fanzongchao',
'fudi01',
'gaoxinxin',
'huangjie03',
'hutiebeibei',
'huyu01',
'jiaotianhui',
'lianying',
'liuchao08',
'liushenglai',
'liuwei46'
]

def real_send(mails):
    for mail in mails:
        # if mail["receiver"] in sends:
        #    continue
        body = {
            "channel": 1,
            "title": mail["subject"],
            "content": mail["mail"],
            "receivers": [mail["receiver"]],
            "ccs": [mail["cc"]] if mail["cc"] else [],
        }
        # print(json.dumps(body, indent=4, ensure_ascii=False))
        print("发送邮件给", mail["receiver"], "抄送给", mail["cc"])
        # print("发送邮件给", mail["receiver"])
        requests.post(f"http://message-center.baijia.com/bailing/{key}.send", json=body)


if __name__ == '__main__':
    real_send(mails)
    #for mail in mails:
        #demo_send(mail, ["yinchao"], ["yinchao"])
        #break
