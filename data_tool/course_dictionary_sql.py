"""将三级课程数据（学科→年级→课程）生成字典表 SQL INSERT 语句，数据源为 xlsx 文件"""

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


@dataclass
class LevelData:
    id: int
    name: str
    level: int
    parent_id: int


SQL_TEMPLATE = (
    "INSERT INTO `course_center`.`course_center_dictionary` "
    "(`dictionary_div`, `dictionary_code`, `dictionary_name`, `dictionary_abbreviated_name`, "
    "`dictionary_remark`, `dictionary_levels`, `dictionary_level`, `parent_dictionary_code`, "
    "`sort_order`, `can_create`, `can_show`, `isdel`, `create_id`, `create_name`, `create_time`, "
    "`update_id`, `update_name`, `update_time`) VALUES "
    "('auditionContent', '{code}', '{name}', '', '', 3, {level}, '{parent}', "
    "0, 1, 1, 0, 0, '', '{now}', 0, '', '{now}');"
)


def read_xlsx(file_path: str | Path) -> list[tuple[str, str, str]]:
    """从 xlsx 读取数据，返回 (学科, 年级, 主题) 元组列表"""
    df = pd.read_excel(file_path, usecols=["学科", "所属年级", "体验课主题"])
    df = df.dropna(subset=["学科", "所属年级", "体验课主题"])
    return list(df.itertuples(index=False, name=None))


def build_hierarchy(data: list[tuple[str, str, str]]) -> list[LevelData]:
    """将三级数据构建层级结构，返回 LevelData 列表"""
    level1_ids: dict[str, int] = {}
    level2_ids: dict[str, int] = {}
    level3_ids: dict[str, int] = {}
    output: list[LevelData] = []
    current_id = 6500

    for subject, grade, topic in data:
        # Level 1: 学科
        if subject not in level1_ids:
            level1_ids[subject] = current_id
            output.append(LevelData(current_id, subject, 1, 0))
            current_id += 1
        l1_code = level1_ids[subject]

        # Level 2: 年级
        l2_key = f"{subject}-{grade}"
        if l2_key not in level2_ids:
            level2_ids[l2_key] = current_id
            output.append(LevelData(current_id, grade, 2, l1_code))
            current_id += 1
        l2_code = level2_ids[l2_key]

        # Level 3: 课程
        l3_key = f"{subject}-{grade}-{topic}"
        if l3_key not in level3_ids:
            level3_ids[l3_key] = current_id
            output.append(LevelData(current_id, topic, 3, l2_code))
            current_id += 1

    return output


def generate_sql(data: list[LevelData]) -> str:
    """生成 SQL INSERT 语句"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "\n".join(
        SQL_TEMPLATE.format(code=item.id, name=item.name, level=item.level, parent=item.parent_id, now=now)
        for item in data
    )


if __name__ == "__main__":
    xlsx_path = "/Users/bjhl/2026春季试听课标准主题.xlsx"
    rows = read_xlsx(xlsx_path)
    hierarchy = build_hierarchy(rows)
    sql_content = generate_sql(hierarchy)

    output_file = Path(__file__).parent / "course_dictionary.txt"
    output_file.write_text(sql_content, encoding="utf-8")
    print(f"已从 {xlsx_path} 读取 {len(rows)} 行，生成 {len(hierarchy)} 条 SQL → {output_file}")
