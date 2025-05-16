import json

import pandas as pd
import requests

templates = [
    {
        "subject": "【重要】高途集团数字资产盘点通知",
        "receiver": "收件人",
        "receiver_name": "账号管理者",
        "cc": "抄送人",
        "digits": [("管理者", "账号管理者"), ("账号平台", "账号平台"), ("账号ID", "账号ID"), ("账号名称", "账号名称")],
        "mail": """
<p><b>{receiver_name}</b>，你好</p>

<p>公司正在进行数字资产盘点，盘点到你名下资产如下，请尽快补充：</p>


<table border="1" cellspacing="0" style="text-align:center;height:75px;font-size:14px;">
<thead>
<tr>
    <th>管理者</th>
    <th>账号平台</th>
    <th>账号ID</th>
    <th>账号名称</th>
</tr>
</thead>
<tbody>
{digits}
</tbody>
</table>

<p>【盘点时间】2023-06-26 08:00 到 2023-06-30 18:00</p>

<p>【盘点方式】</p>

<ol>
<li>点击登录 https://digit.baijia.com/</li>

<li>查看自己名下账号信息，进行更正以及校对，包括不限于账号平台，账号ID，账号名称，管理者，主体，企业认证，隶属学部，手机号等信息。</li>

<li>假设名下有其他平台账号需要及时录入进系统中，点击新建进行录入。

<p>数字资产系统操作说明：</p>
<img src="https://doc.baijia.com/uploader/f/h5opblKDHXyI2Oyb.png" alt="操作说明" width="800" />
</li>
</ol>
      
<p>【重点说明】</p>

<ul>
<li style="color: red;"><b>注意：该账号会成为后续财务打款依据，假设不在该系统中，不予进行财务打款操作。</b></li>

<li>请负责人务必尽快进行账号认领，每周会发送各个学部的盘点进度邮件，截至到6月30日，过时后仍未进行认领，公司市场部将在6月末起陆续开始进行回收，修改管理员信息。</li>
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
    df = pd.read_excel("~/店铺邮件0704.xlsx", sheet_name=template["sheet_name"])
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
    response = requests.post(f"http://message-center.baijia.com/bailing/{key}.send", json=body)
    print(response)


def real_send(mails):
    for mail in mails:
        body = {
            "channel": 1,
            "title": mail["subject"],
            "content": mail["mail"],
            "receivers": [mail["receiver"]],
            "ccs": [mail["cc"]] if mail["cc"] else [],
        }
        # print(json.dumps(body, indent=4, ensure_ascii=False))
        print("发送邮件给", mail["receiver"], "抄送给", mail["cc"])
        requests.post(f"http://message-center.baijia.com/bailing/{key}.send", json=body)


if __name__ == '__main__':
    real_send(mails)
