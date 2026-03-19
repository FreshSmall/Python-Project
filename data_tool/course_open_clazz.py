import csv
import requests

API_URL = "https://api-medusa.baijia.com/department/commonSearch.json"
HEADERS = {
    "appId": "ticket-access-token",
    "time": "1638344398",
    "sign": "42020b5c0fff5bf7c96273a5240eaf97",
    "Content-Type": "application/json",
}
INPUT_FILE = "/Users/bjhl/线下课程开班数.csv"
OUTPUT_FILE = "/Users/bjhl/线下课程开班数_部门名称.csv"
BATCH_SIZE = 50


def query_department_names(dept_ids: list[str]) -> dict[str, str]:
    """批量查询部门ID对应的中文名称，返回 {id: name} 映射"""
    mapping = {}
    for i in range(0, len(dept_ids), BATCH_SIZE):
        batch = dept_ids[i : i + BATCH_SIZE]
        resp = requests.post(API_URL, headers=HEADERS, json={"numbers": batch})
        resp.raise_for_status()
        data = resp.json().get("data", [])
        for dept in data:
            mapping[dept["number"]] = dept["name"]
    return mapping


def main():
    # 1. 读取CSV，收集所有唯一部门ID
    rows = []
    all_dept_ids = set()
    with open(INPUT_FILE, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            path_ids = row["department_path"].split("/")
            all_dept_ids.update(path_ids)
            rows.append((path_ids, row['sum(b.cnt)']))

    # 2. 批量查询部门名称
    dept_map = query_department_names(list(all_dept_ids))

    # 3. 生成新CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["一级部门", "二级部门", "三级部门", "开班数"])
        for path_ids, count in rows:
            names = [dept_map.get(did, did) for did in path_ids]
            # 补齐到3级
            while len(names) < 3:
                names.append("")
            writer.writerow([names[0], names[1], names[2], count])

    print(f"完成！共处理 {len(rows)} 条记录，输出文件: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
