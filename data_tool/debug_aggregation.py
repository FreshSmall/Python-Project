"""
诊断脚本：检查相同告警的 alarmRule 是否一致
"""

import json
import re
from collections import defaultdict

def check_aggregation_keys(json_file_path):
    """
    检查所有【聚合】-课时账户状态不能解冻告警的聚合键
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 筛选目标告警
    target_alarms = []
    for item in data.get('data', []):
        alarm_rule = item.get('alarmRule', '')
        if '课时账户状态不能解冻' in alarm_rule:
            target_alarms.append(item)

    if not target_alarms:
        print("未找到【聚合】-课时账户状态不能解冻告警")
        return

    print(f"找到 {len(target_alarms)} 条相关告警\n")

    # 分析 alarmRule 的唯一值
    alarm_rules = {}
    for item in target_alarms:
        rule = item.get('alarmRule', '')
        if rule not in alarm_rules:
            alarm_rules[rule] = []
        alarm_rules[rule].append(item)

    print("=" * 80)
    print("alarmRule 字段分析")
    print("=" * 80)
    print(f"发现 {len(alarm_rules)} 种不同的 alarmRule 值:\n")

    for i, (rule, items) in enumerate(alarm_rules.items(), 1):
        print(f"{i}. 值: {repr(rule)}")
        print(f"   长度: {len(rule)} 字符")
        print(f"   数量: {len(items)} 条")
        # 显示第一条的告警时间
        alarm_info = items[0].get('alarmInfo', '')
        time_match = re.search(r'告警时间：(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', alarm_info)
        if time_match:
            print(f"   示例时间: {time_match.group(1)}")
        print()

    # 检查 alarmRule 是否完全一致
    if len(alarm_rules) == 1:
        print("✓ alarmRule 完全一致，问题可能在别处")
        check_signature_consistency(target_alarms)
    else:
        print("✗ 发现 alarmRule 存在差异！这会导致聚合失败")
        print("\n建议修复方案:")
        print("1. 在聚合前对 alarmRule 进行规范化处理（去除空格、换行等）")
        print("2. 或者使用模糊匹配来识别相同类型的告警规则")


def check_signature_consistency(alarms):
    """
    检查签名提取是否一致
    """
    print("\n" + "=" * 80)
    print("签名一致性检查")
    print("=" * 80)

    signatures = {}
    for item in alarms:
        desc = item.get('description', '')
        # 简单签名提取（去除变化元素）
        desc_clean = re.sub(r'\b[a-f0-9]{32}\b', '<UUID>', desc)  # UUID
        desc_clean = re.sub(r'\[TID:[^\]]+\]', '[TID:<TID>]', desc_clean)  # TID
        desc_clean = re.sub(r'clazzNumber":\d+', 'clazzNumber":<N>', desc_clean)  # ID
        desc_clean = re.sub(r'\d{2}:\d{2}:\d{2}\.\d+', '<TIME>', desc_clean)  # 时间

        sig_key = desc_clean[:100]  # 取前100字符作为签名
        if sig_key not in signatures:
            signatures[sig_key] = []
        signatures[sig_key].append(item)

    print(f"发现 {len(signatures)} 种不同的签名")
    if len(signatures) > 1:
        print("\n签名不完全一致，可能是由于:")
        print("1. description 内容确实有差异")
        print("2. JSON 被截断的位置不同导致内容不一致")


if __name__ == "__main__":
    import sys
    json_file = sys.argv[1] if len(sys.argv) > 1 else "data_tool/response.json"
    check_aggregation_keys(json_file)
