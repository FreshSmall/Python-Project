"""
比较 OES 和 CES 两个 CSV 文件中数据状态的不一致性

功能说明：
1. 通过 ces.oes_user_right_number 与 oes.number 进行关联
2. 过滤掉状态完全相同的数据
3. 保留状态字段任意不同的数据
4. 输出聚合后的结果到新的 CSV 文件
"""

import pandas as pd


def compare_status(oes_csv_path: str, ces_csv_path: str, output_csv_path: str = "status_diff.csv"):
    """
    比较两个CSV文件中的数据状态不一致

    参数:
        oes_csv_path: OES CSV文件路径
        ces_csv_path: CES CSV文件路径
        output_csv_path: 输出CSV文件路径
    """
    # 读取CSV文件
    # 注意：number 和 oes_user_right_number 是大整数，需要指定为字符串类型避免精度丢失
    print(f"读取 OES 文件: {oes_csv_path}")
    oes_df = pd.read_csv(oes_csv_path, dtype={'number': 'str'})
    print(f"OES 数据行数: {len(oes_df)}")

    print(f"读取 CES 文件: {ces_csv_path}")
    ces_df = pd.read_csv(ces_csv_path, dtype={'oes_user_right_number': 'str'})
    print(f"CES 数据行数: {len(ces_df)}")

    # 确保状态字段为整数类型（便于比较）
    oes_df['user_right_status'] = oes_df['user_right_status'].astype('Int64')
    oes_df['user_right_freeze_status'] = oes_df['user_right_freeze_status'].astype('Int64')
    ces_df['fulfill_status'] = ces_df['fulfill_status'].astype('Int64')
    ces_df['freeze_status'] = ces_df['freeze_status'].astype('Int64')

    # 检查必需字段是否存在
    oes_required = ['number', 'user_right_status', 'user_right_freeze_status', 'user_delivery_right_number']
    ces_required = ['oes_user_right_number', 'fulfill_status', 'freeze_status']

    missing_oes = [col for col in oes_required if col not in oes_df.columns]
    missing_ces = [col for col in ces_required if col not in ces_df.columns]

    if missing_oes:
        raise ValueError(f"OES CSV 缺少字段: {missing_oes}")
    if missing_ces:
        raise ValueError(f"CES CSV 缺少字段: {missing_ces}")

    # 选择需要的列
    oes_selected = oes_df[oes_required].copy()
    ces_selected = ces_df[ces_required].copy()

    # 重命名列以便合并
    oes_selected = oes_selected.rename(columns={
        'number': 'oes_number',
        'user_right_status': 'oes_user_right_status',
        'user_right_freeze_status': 'oes_user_right_freeze_status',
        'user_delivery_right_number': 'oes_user_right_delivery_number'
    })

    ces_selected = ces_selected.rename(columns={
        'oes_user_right_number': 'ces_oes_user_right_number',
        'fulfill_status': 'ces_fulfill_status',
        'freeze_status': 'ces_freeze_status',
        'delivery_number': 'ces_delivery_number'
    })
    

    # 通过 number 关联两个表
    print("执行数据关联...")
    merged_df = pd.merge(
        ces_selected,
        oes_selected,
        left_on='ces_oes_user_right_number',
        right_on='oes_number',
        how='inner'
    )

    print(f"关联后数据行数: {len(merged_df)}")

    # 判断状态是否一致
    # fulfill_status 对应 user_right_status
    # freeze_status 对应 user_right_freeze_status
    merged_df['status_match'] = (
        (merged_df['ces_fulfill_status'] == merged_df['oes_user_right_status']) &
        (merged_df['ces_freeze_status'] == merged_df['oes_user_right_freeze_status'])
    )

    # 过滤：保留状态不一致的数据
    diff_df = merged_df[~merged_df['status_match']].copy()

    print(f"状态不一致的数据行数: {len(diff_df)}")

    # 添加不一致类型标识
    diff_df['diff_type'] = diff_df.apply(
        lambda row: _get_diff_type(
            row['ces_fulfill_status'],
            row['oes_user_right_status'],
            row['ces_freeze_status'],
            row['oes_user_right_freeze_status']
        ),
        axis=1
    )

    # 重排输出列
    output_columns = [
        'oes_number',
        'oes_user_right_delivery_number',
        'diff_type',
        'ces_fulfill_status',
        'oes_user_right_status',
        'ces_freeze_status',
        'oes_user_right_freeze_status'
    ]

    # 重命名输出列为更友好的名称
    output_df = diff_df[output_columns].rename(columns={
        'oes_number': 'number',
        'right_delivery_number': 'oes_user_right_delivery_number',
        'ces_fulfill_status': 'ces_fulfill_status',
        'oes_user_right_status': 'oes_user_right_status',
        'ces_freeze_status': 'ces_freeze_status',
        'oes_user_right_freeze_status': 'oes_user_right_freeze_status'
    })

    # 输出结果
    output_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"\n结果已保存到: {output_csv_path}")

    # 打印统计信息
    print("\n=== 不一致类型统计 ===")
    print(output_df['diff_type'].value_counts().to_string())

    return output_df


def _get_diff_type(ces_fulfill, oes_fulfill, ces_freeze, oes_freeze):
    """
    获取不一致类型
    """
    fulfill_diff = ces_fulfill != oes_fulfill
    freeze_diff = ces_freeze != oes_freeze

    if fulfill_diff and freeze_diff:
        return "both_diff"
    elif fulfill_diff:
        return "fulfill_status_diff"
    elif freeze_diff:
        return "freeze_status_diff"
    return "unknown"


# 使用示例
if __name__ == "__main__":
    # ==================== 配置文件路径 ====================
    # 请修改为实际的文件路径
    OES_CSV_PATH = "/Users/bjhl/oes.csv"           # OES CSV文件路径
    CES_CSV_PATH = "/Users/bjhl/ces.csv"           # CES CSV文件路径
    OUTPUT_CSV_PATH = "/Users/bjhl/status_diff_4.csv"  # 输出文件路径
    # ===================================================

    try:
        result = compare_status(OES_CSV_PATH, CES_CSV_PATH, OUTPUT_CSV_PATH)
        print("\n执行成功!")
    except FileNotFoundError as e:
        print(f"\n错误: 找不到文件 - {e}")
        print("请检查文件路径是否正确")
    except ValueError as e:
        print(f"\n错误: {e}")
    except Exception as e:
        print(f"\n发生错误: {e}")
