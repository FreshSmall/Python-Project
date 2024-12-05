import json

def load_json_data(file_path):
    """从JSON文件加载数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"找不到文件: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"JSON格式错误: {file_path}")
        return None


if __name__ == '__main__':
    data = load_json_data('/Users/bjhl/json-format.json')
    if data:
        for item in data:
            if item =='':
                pass
            if item.__contains__('37766'):
                print(item+",")
