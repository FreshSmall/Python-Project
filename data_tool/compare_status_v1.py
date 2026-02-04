import pandas as pd


def get_oes_not_in_ces(
    oes_csv_path: str,
    ces_csv_path: str,
    output_csv_path: str = "oes_not_in_ces.csv"
) -> pd.DataFrame:
    """
    获取 OES 表中 number 不在 CES 表中的数据（左排除/Left Anti-Join）

    参数:
        oes_csv_path: OES CSV文件路径
        ces_csv_path: CES CSV文件路径
        output_csv_path: 输出CSV文件路径

    返回:
        包含 OES 表中独有的数据的 DataFrame
    """
    print(f"读取 OES 文件: {oes_csv_path}")
    oes_df = pd.read_csv(oes_csv_path, dtype={'number': 'str'})
    print(f"OES 数据行数: {len(oes_df)}")

    print(f"读取 CES 文件: {ces_csv_path}")
    ces_df = pd.read_csv(ces_csv_path, dtype={'oes_user_right_number': 'str'})
    print(f"CES 数据行数: {len(ces_df)}")

    # 使用 left join + indicator 实现左排除
    print("执行数据关联（查找 OES 独有数据）...")
    merged = pd.merge(
        oes_df,
        ces_df[['oes_user_right_number']],  # 只需要关联列
        left_on='number',
        right_on='oes_user_right_number',
        how='left',
        indicator=True
    )

    # 过滤出只在 OES 表中存在的数据
    oes_only = merged[merged['_merge'] == 'left_only'].drop(
        columns=['_merge', 'oes_user_right_number']
    )

    print(f"OES 表中不在 CES 中的数据行数: {len(oes_only)}")

    # 输出结果
    oes_only.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"结果已保存到: {output_csv_path}")

    return oes_only


def get_ces_not_in_oes(
    oes_csv_path: str,
    ces_csv_path: str,
    output_csv_path: str = "ces_not_in_oes.csv"
) -> pd.DataFrame:
    """
    获取 CES 表中 oes_user_right_number 不在 OES 表中的数据（右排除/Right Anti-Join）

    参数:
        oes_csv_path: OES CSV文件路径
        ces_csv_path: CES CSV文件路径
        output_csv_path: 输出CSV文件路径

    返回:
        包含 CES 表中独有的数据的 DataFrame
    """
    print(f"读取 OES 文件: {oes_csv_path}")
    oes_df = pd.read_csv(oes_csv_path, dtype={'number': 'str'})
    print(f"OES 数据行数: {len(oes_df)}")

    print(f"读取 CES 文件: {ces_csv_path}")
    ces_df = pd.read_csv(ces_csv_path, dtype={'oes_user_right_number': 'str'})
    print(f"CES 数据行数: {len(ces_df)}")

    # 使用 right join + indicator 实现右排除
    print("执行数据关联（查找 CES 独有数据）...")
    merged = pd.merge(
        oes_df[['number']],  # 只需要关联列
        ces_df,
        left_on='number',
        right_on='oes_user_right_number',
        how='right',
        indicator=True
    )

    # 过滤出只在 CES 表中存在的数据
    ces_only = merged[merged['_merge'] == 'right_only'].drop(
        columns=['_merge', 'number']
    )

    print(f"CES 表中不在 OES 中的数据行数: {len(ces_only)}")

    # 输出结果
    ces_only.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"结果已保存到: {output_csv_path}")

    return ces_only


if __name__ == '__main__':
    # ==================== 配置文件路径 ====================
    OES_CSV_PATH = "/Users/bjhl/oes-1.csv"
    CES_CSV_PATH = "/Users/bjhl/ces-1.csv"
    # ===================================================

    # 选择要执行的操作（取消注释即可）
    OPERATION = "oes_not_in_ces"  # 可选: "oes_not_in_ces" 或 "ces_not_in_oes"

    try:
        if OPERATION == "oes_not_in_ces":
            # 获取 OES 表中不在 CES 中的数据
            result = get_oes_not_in_ces(OES_CSV_PATH, CES_CSV_PATH, "/Users/bjhl/oes_not_in_ces-1.csv")
        elif OPERATION == "ces_not_in_oes":
            # 获取 CES 表中不在 OES 中的数据
            result = get_ces_not_in_oes(OES_CSV_PATH, CES_CSV_PATH, "/Users/bjhl/ces_not_in_oes-1.csv")
        else:
            print(f"未知的操作类型: {OPERATION}")
            exit(1)

        print("\n执行成功!")
    except FileNotFoundError as e:
        print(f"\n错误: 找不到文件 - {e}")
        print("请检查文件路径是否正确")
    except Exception as e:
        print(f"\n发生错误: {e}")