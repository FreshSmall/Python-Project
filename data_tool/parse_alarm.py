"""
从天眼告警接口拉取告警数据，提取 alarmInfo 和 description 字段中的报错信息，
将相同类型的报错进行聚合统计。

聚合维度：告警规则 + 异常类型 + 核心错误位置
"""

import math
import re
import time
from collections import defaultdict

import requests

# ==================== 接口配置 ====================
API_URL = "https://qingzhou.baijia.com/qingzhou/tianyan/alarmcenter/earlywarning/query"

# 默认请求体参数
DEFAULT_QUERY_PARAMS = {
    "appIds": [
        "baijia.gt.ecommerce.course.course-center-b"
    ],
    "alarmLevel": "standard;important;highPriority",
    "startTime": 1773244800000,
    "endTime": 1773849600000,
    "pageDto": {
        "pageNum": 1,
        "pageSize": 1000
    },
    "activeName": "earlyAlarmQuery",
    "appNid": "baijia.gt.ecommerce.course.course-center-b",
    "environment": "prod"
}
# =================================================


def fetch_alarm_data(query_params: dict = None) -> list:
    """
    从天眼告警接口分页拉取全量告警数据。
    """
    params = query_params or DEFAULT_QUERY_PARAMS.copy()
    all_data = []
    page_num = 1
    page_size = params.get("pageDto", {}).get("pageSize", 100)
    total_pages = None

    while True:
        params["pageDto"] = {"pageNum": page_num, "pageSize": page_size}

        resp = requests.post(
            API_URL,
            json=params,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        resp.raise_for_status()
        result = resp.json()

        if result.get("code") != 200:
            raise RuntimeError(f"接口返回错误: code={result.get('code')}, msg={result.get('msg')}")

        page_data = result.get("data", [])
        all_data.extend(page_data)

        # 首次请求时计算总页数
        if total_pages is None:
            total_count = result.get("pageDto", {}).get("count", 0)
            total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
            print(f"告警总数: {total_count}, 每页 {page_size} 条, 共 {total_pages} 页")

        print(f"  已拉取第 {page_num}/{total_pages} 页, 本页 {len(page_data)} 条")

        if page_num >= total_pages or len(page_data) == 0:
            break

        page_num += 1

    print(f"全部拉取完成, 共 {len(all_data)} 条\n")
    return all_data


def extract_exception_signature(text: str) -> str:
    """
    从告警文本中提取异常签名（异常类名 + 关键错误信息）。
    用于对相同类型的报错进行聚合。

    聚合维度：
    1. 异常类名（如果有）
    2. 核心错误信息（归一化数字、ID等变化部分）
    3. 对于日志格式：提取类名+核心信息，忽略时间、线程等变化元素
    4. 对于天眼预聚合格式：去除时间范围，使用alarmRule作为签名
    """
    if not text:
        return "未知异常"

    # ============ 优先处理：天眼系统的预聚合描述格式 ============
    # 格式如：08:<N>:00到08:<N>:00，发生<span style="color:red">2</span>次普通预警, <span style="color:red">其中一条</span>为：
    # 这是天眼二次聚合的结果，时间不同会导致签名不同，需要去除时间部分
    tianyan_agg_pattern = r'^\d{2}:<N>:00到\d{2}:<N>:00，发生.*?其中一条.*?为：\s*$'
    if re.match(tianyan_agg_pattern, text.strip()):
        # 返回空签名，让 alarmRule 成为唯一聚合键
        return ""

    # 匹配 Java 异常类名，如 java.lang.NullPointerException, com.xxx.BizException: message
    exception_pattern = r'([\w.]+(?:Exception|Error|Throwable))(?::\s*(.+?))?(?:\n|\r|$)'
    match = re.search(exception_pattern, text)
    if match:
        exception_class = match.group(1)
        short_class = exception_class.split('.')[-1]
        exception_msg = match.group(2).strip() if match.group(2) else ""
        if exception_msg:
            # 将数字 ID（10位以上）替换为占位符
            exception_msg = re.sub(r'\b\d{10,}\b', '<ID>', exception_msg)
            # 将统计数字归一化（如 "成功:1737, 数据不一致:3, 执行异常:18" -> "成功:<N>, ..."）
            exception_msg = re.sub(r'(?<=[:：])\d+', '<N>', exception_msg)
            # 将 teacher-basic：155990 类的具体数字替换
            exception_msg = re.sub(r'：\d+', '：<N>', exception_msg)
            # 归一化括号内的具体数量（如 total=1600, cost=600 -> total=<N>, cost=<N>）
            exception_msg = re.sub(r'=\d+', '=<N>', exception_msg)
            return f"{short_class}: {exception_msg}"
        return short_class

    # 匹配 xjob 任务失败的模式
    if 'xjob任务执行失败' in text:
        task_desc_match = re.search(r'任务描述：(.+?)(?:\n|$)', text)
        task_desc = task_desc_match.group(1) if task_desc_match else "未知任务"
        return f"xjob任务执行失败 - {task_desc}"

    # 匹配 http_api 相关异常（慢调用、异常监控等）
    # 格式：最近3分钟http_api:/feign/xxx，总调用 X 次，异常量：X，调用异常异常率为X.XX大于等于0.XX
    http_api_match = re.search(r'http_api:(/[^\s，]+)', text)
    if http_api_match:
        api_path = http_api_match.group(1)
        # 确定告警类型（慢调用或异常监控）
        if '慢调用' in text or 'Apdex' in text:
            alarm_type = 'http_api慢调用'
        elif '异常' in text or '异常率' in text:
            alarm_type = 'http_api异常'
        else:
            alarm_type = 'http_api'
        return f"{alarm_type} - {api_path}"

    # 兼容旧的 http_call 格式
    http_call_match = re.search(r'http_call:([^\s,，]+)', text)
    if http_call_match:
        return f"http_call异常 - {http_call_match.group(1)}"

    # 匹配 Send order message failed
    if 'Send order message failed' in text:
        topic_match = re.search(r'Topic is:(\S+)', text)
        topic = topic_match.group(1) if topic_match else "未知Topic"
        return f"Send order message failed - {topic}"

    # 匹配 doRebalance BUG
    if 'doRebalance' in text:
        return "RocketMQ doRebalance BUG"

    # ============ 新增：处理标准日志格式 ============
    # 匹配标准Java日志格式：日期 时间 级别 [线程] [类名:行号] UUID - [TID: ...] 消息
    # 例如：2026-02-25 13:57:40.207 ERROR [http-nio-28688-exec-30] [com.xxx.Class.method:2297] uuid - [TID: tid] message
    log_pattern = r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+\s+\w+\s+\[[^\]]+\]\s+\[([^\]:]+)(?::\d+)?\]\s*(.*)'
    log_match = re.match(log_pattern, text)

    if log_match:
        class_name = log_match.group(1).strip()
        message = log_match.group(2).strip()

        # 归一化类名（处理被截断的情况，如 ClazzArrangeLes...）
        if class_name.endswith('...'):
            class_name = class_name[:-3]

        # 归一化消息内容：移除UUID、TID、JSON等变化元素
        message = _normalize_message(message)

        if message:
            return f"[{class_name}] {message}"
        return f"[{class_name}]"

    # 兜底：取 description 的第一行关键信息
    first_line = text.split('\n')[0].strip()
    # 尝试去除时间戳和日志级别
    first_line = re.sub(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+\s+\w+\s+', '', first_line)
    # 去除方括号内容（线程名、TID等）
    first_line = re.sub(r'\[[^\]]*\]\s*', '', first_line)
    first_line = first_line.strip()

    # 归一化处理
    first_line = _normalize_message(first_line)

    if len(first_line) > 120:
        first_line = first_line[:120] + "..."
    return first_line if first_line else "未知异常"


def _normalize_message(message: str) -> str:
    """
    归一化消息内容，将变化的数字、ID等替换为占位符，
    确保相同类型的错误能够聚合在一起。

    处理内容：
    1. UUID（32位十六进制字符串）
    2. TID标记
    3. JSON对象（完全移除，因为会被截断导致内容不一致）
    4. 各类数字ID和浮点数
    """
    if not message:
        return ""

    # 1. 移除开头的 UUID（格式：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx 或 32位十六进制）
    # 例如：518504da5bedb150f674cb4030bdd1d1
    message = re.sub(r'^[a-f0-9]{32}(\s*-\s*)?', '', message)
    message = re.sub(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}(\s*-\s*)?', '', message)

    # 2. 移除 TID 标记 [TID: after-sales.xxx.xxx]
    message = re.sub(r'\[TID:\s*[^\]]+\]\s*', '', message)

    # 3. 移除 JSON 对象（关键！由于 API 会截断，导致结尾不一致，需要完全移除）
    # 移除 hour:[{ 开头的 JSON（到行尾或字符串尾）
    message = re.sub(r'\w+:\s*\[\{.*', '', message)
    # 移除 data:[{ 开头的 JSON
    message = re.sub(r'\w+:\s*\[\{.*', '', message)
    # 移除残留的 JSON 片段
    message = re.sub(r'\[\{.*', '', message)
    # 移除简化的 JSON 对象
    message = re.sub(r'\{[^}]{20,}\}', '{...}', message)

    # 4. 归一化 HTML 标签（如 <a href...>link</a>）
    message = re.sub(r'<a\s+[^>]*>[^<]*</a>', '<LINK>', message)

    # 5. 归一化浮点数（如 0.00, 10.50, 28.00 等）
    message = re.sub(r'\b\d+\.\d+\b', '<NUM>', message)

    # 6. 归一化长数字 ID（10位以上）
    message = re.sub(r'\b\d{10,}\b', '<ID>', message)

    # 7. 归一化中等长度数字（6-9位）
    message = re.sub(r'\b\d{6,9}\b', '<N>', message)

    # 8. 归一化 key=value 格式中的数字
    message = re.sub(r'(\w+=)\d+', r'\1<N>', message)

    # 9. 归一化冒号后的数字（如 "count:123" -> "count:<N>"）
    message = re.sub(r'(\w+)[:：]\d+', r'\1:<N>', message)

    # 10. 清理多余空格和分隔符
    message = re.sub(r'\s+-\s+', ' - ', message)
    message = re.sub(r'\s+', ' ', message)

    return message.strip()


def _normalize_alarm_rule(alarm_rule: str) -> str:
    """
    规范化 alarm_rule，去除空格、换行、标点等导致聚合失败的格式差异。
    """
    if not alarm_rule:
        return "未知规则"
    # 去除首尾空格、换行符
    alarm_rule = alarm_rule.strip()
    # 统一中英文括号
    alarm_rule = alarm_rule.replace('【', '[').replace('】', ']')
    # 去除 - 符号周围的空格
    alarm_rule = re.sub(r'\s*-\s*', '-', alarm_rule)
    # 去除所有剩余空格
    alarm_rule = alarm_rule.replace(' ', '')
    return alarm_rule


def _extract_alarm_content_from_info(alarm_info: str) -> str:
    """
    从 alarmInfo 中提取「告警信息」部分的实际错误内容。
    格式：...告警信息：\n{实际内容}
    """
    # 匹配 "告警信息：" 之后的内容
    match = re.search(r'告警信息：\s*(.+)', alarm_info, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def aggregate_alarms(alarm_list: list):
    """
    按异常签名聚合告警列表并输出报告。
    三级聚合：alarmRule → alarmKeyword → 异常签名
    """
    # 聚合结构: {alarm_rule: {keyword: {signature: [告警详情列表]}}}
    aggregated = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for item in alarm_list:
        alarm_rule = _normalize_alarm_rule(item.get('alarmRule', '未知规则'))
        alarm_keyword = item.get('alarmKeyword', '未分类')
        alarm_level = item.get('alarmLevelName', '未知')
        alarm_info = item.get('alarmInfo', '')
        description = item.get('description', '')
        status_name = item.get('statusName', '')
        sub_sys = item.get('subSysName', '')

        # 优先从 alarmInfo 提取告警内容，其次使用 description
        alarm_content = _extract_alarm_content_from_info(alarm_info)
        if not alarm_content:
            alarm_content = description

        signature = extract_exception_signature(alarm_content)
        # 如果签名为空（预聚合格式），使用默认签名
        if not signature:
            signature = "预聚合告警"

        time_match = re.search(r'告警时间：(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', alarm_info)
        alarm_time_str = time_match.group(1) if time_match else "未知时间"

        node_match = re.search(r'异常节点：(\S+)', alarm_info)
        node = node_match.group(1) if node_match else ""

        aggregated[alarm_rule][alarm_keyword][signature].append({
            'alarm_time': alarm_time_str,
            'alarm_level': alarm_level,
            'node': node,
            'sub_sys': sub_sys,
            'status': status_name,
        })

    # 扁平化用于排序：按告警规则聚合的总次数排序
    flat_groups = []
    for alarm_rule, keywords in aggregated.items():
        total_count = sum(len(sig_items) for sig_dicts in keywords.values() for sig_items in sig_dicts.values())
        flat_groups.append((alarm_rule, keywords, total_count))

    flat_groups.sort(key=lambda x: x[2], reverse=True)

    print("=" * 80)
    print("告警聚合分析报告（三级：规则 → 关键字 → 类型）")
    print("=" * 80)

    rule_counter = 1
    for alarm_rule, keywords, total_count in flat_groups:
        print(f"\n{'─' * 80}")
        print(f"【规则 {rule_counter}】[{alarm_rule}]")
        print(f"  总计: {total_count}次")

        # 按关键字内的次数排序
        sorted_keywords = sorted(keywords.items(), key=lambda x: sum(len(v) for v in x[1].values()), reverse=True)

        for keyword, signatures in sorted_keywords:
            keyword_total = sum(len(items) for items in signatures.values())
            print(f"\n  ├─ 关键字: [{keyword}] ({keyword_total}次)")

            # 按签名内的次数排序
            sorted_signatures = sorted(signatures.items(), key=lambda x: len(x[1]), reverse=True)

            for sig, items in sorted_signatures:
                sig_display = sig if sig != "预聚合告警" else ""
                indent = "     " if sig_display else "     "
                if sig_display:
                    print(f"{indent}└─ 类型: {sig_display}")
                print(f"{indent}   次数: {len(items)}")

                level_counts = defaultdict(int)
                for item in items:
                    level_counts[item['alarm_level']] += 1
                level_str = ", ".join(f"{level}: {count}次" for level, count in level_counts.items())
                print(f"{indent}   级别: {level_str}")

                times = sorted([item['alarm_time'] for item in items if item['alarm_time'] != "未知时间"])
                if times:
                    print(f"{indent}   时间: {times[0]} ~ {times[-1]}")

        rule_counter += 1

    # 总览
    print(f"\n{'=' * 80}")
    print("总览")
    print(f"{'=' * 80}")
    print(f"告警总数: {len(alarm_list)}")
    print(f"告警规则数: {len(aggregated)}")
    print(f"\n各规则出现次数:")
    for i, (alarm_rule, keywords, total_count) in enumerate(flat_groups, 1):
        print(f"  {i}. [{total_count}次] [{alarm_rule}]")


def test_aggregation():
    """
    测试聚合逻辑，验证相同类型的错误能够正确聚合。
    使用真实API返回的数据格式进行测试。
    """
    # 模拟真实API返回的错误日志：包含UUID、TID、JSON等变化元素
    test_cases = [
        {
            'alarmRule': '【聚合】-课时账户状态不能解冻',
            'alarmLevelName': '普通',
            'alarmInfo': '告警时间：2026-02-25 22:16:10',
            'description': '2026-02-25 22:15:07.124 ERROR [http-nio-28688-exec-29] [com.gaotu.course.center.domain.service.cost.impl.ClazzArrangeLessonCostService.getNextStatusForUnFreeze:2297] 518504da5bedb150f674cb4030bdd1d1 - [TID: after-sales.183792.17720288733020001] getNextStatusForUnFreeze cannotUnFreezeClazzHour, hour:[{"arrangedHour":0.00,"autoCostSwitch":false,"clazzNumber":523080508890963968}]',
            'statusName': '未响应',
            'subSysName': '应用日志告警系统'
        },
        {
            'alarmRule': '【聚合】-课时账户状态不能解冻',
            'alarmLevelName': '普通',
            'alarmInfo': '告警时间：2026-02-25 18:42:10',
            'description': '2026-02-25 18:42:06.230 ERROR [http-nio-28688-exec-2] [com.gaotu.course.center.domain.service.cost.impl.ClazzArrangeLessonCostService.getNextStatusForUnFreeze:2297] 795fb9e9e0c4cfb6e604b97e3db32213 - [TID: after-sales.194530.17720160936830001] getNextStatusForUnFreeze cannotUnFreezeClazzHour, hour:[{"arrangedHour":0.00,"autoCostSwitch":false,"clazzNumber":522355342053607424}]',
            'statusName': '未响应',
            'subSysName': '应用日志告警系统'
        },
        {
            'alarmRule': '【聚合】-课时账户状态不能解冻',
            'alarmLevelName': '普通',
            'alarmInfo': '告警时间：2026-02-25 18:41:10',
            'description': '2026-02-25 18:41:53.313 ERROR [http-nio-28688-exec-3] [com.gaotu.course.center.domain.service.cost.impl.ClazzArrangeLessonCostService.getNextStatusForUnFreeze:2297] ee506b9a7334d03baefcd27d984918a9 - [TID: after-sales.194530.17720160936830001] getNextStatusForUnFreeze cannotUnFreezeClazzHour, hour:[{"arrangedHour":0.00,"autoCostSwitch":false,"clazzNumber":522355342053607424}]',
            'statusName': '未响应',
            'subSysName': '应用日志告警系统'
        },
        {
            'alarmRule': '【聚合】-课时账户状态不能解冻',
            'alarmLevelName': '普通',
            'alarmInfo': '告警时间：2026-02-25 16:47:10',
            'description': '2026-02-25 16:47:24.676 ERROR [http-nio-28688-exec-23] [com.gaotu.course.center.domain.service.cost.impl.ClazzArrangeLessonCostService.getNextStatusForUnFreeze:2297] 4a53590ab609afa511f96c8586635b4c - [TID: after-sales.169361.17720092110150001] getNextStatusForUnFreeze cannotUnFreezeClazzHour, hour:[{"arrangedHour":0.00,"autoCostSwitch":false,"clazzNumber":523082932603082752}]',
            'statusName': '未响应',
            'subSysName': '应用日志告警系统'
        },
        {
            'alarmRule': '【聚合】-课时账户状态不能解冻',
            'alarmLevelName': '普通',
            'alarmInfo': '告警时间：2026-02-25 15:57:10',
            'description': '2026-02-25 15:57:48.381 ERROR [http-nio-28688-exec-19] [com.gaotu.course.center.domain.service.cost.impl.ClazzArrangeLessonCostService.getNextStatusForUnFreeze:2297] 61d79dd464d1555ec759418f3acec55f - [TID: after-sales.178139.17720061822590001] getNextStatusForUnFreeze cannotUnFreezeClazzHour, hour:[{"arrangedHour":0.00,"autoCostSwitch":false,"clazzNumber":491173053361870848}]',
            'statusName': '未响应',
            'subSysName': '应用日志告警系统'
        },
    ]

    print("=" * 80)
    print("聚合测试 - 使用真实数据格式")
    print("=" * 80)

    # 测试签名提取
    print("\n签名提取测试（应该都相同）：")
    for i, case in enumerate(test_cases, 1):
        signature = extract_exception_signature(case['description'])
        print(f"  测试{i}: {signature}")

    # 测试聚合
    print("\n聚合结果：")
    aggregate_alarms(test_cases)

    # 验证：应该聚合为1组，5次
    expected_groups = 1
    expected_count = 5

    # 计算实际聚合组数
    aggregated = defaultdict(list)
    for item in test_cases:
        alarm_rule = item.get('alarmRule', '未知规则')
        signature = extract_exception_signature(item['description'])
        agg_key = f"[{alarm_rule}] {signature}"
        aggregated[agg_key].append(item)

    actual_groups = len(aggregated)
    actual_count = len(list(aggregated.values())[0])

    print("\n" + "=" * 80)
    print("验证结果")
    print("=" * 80)
    print(f"预期聚合组数: {expected_groups}, 实际: {actual_groups}")
    print(f"预期每组条数: {expected_count}, 实际: {actual_count}")

    if actual_groups == expected_groups and actual_count == expected_count:
        print("✓ 测试通过！相同类型的错误已正确聚合")
        return True
    else:
        print("✗ 测试失败！聚合逻辑需要调整")
        # 打印实际的聚合键
        print("\n实际聚合键：")
        for key in aggregated.keys():
            print(f"  {key}")
        return False


if __name__ == "__main__":
    # 运行测试验证聚合逻辑
    alarm_data = fetch_alarm_data()
    aggregate_alarms(alarm_data)
        
