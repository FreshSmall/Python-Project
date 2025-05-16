from notion_client import Client
from typing import Dict, List, Optional
from pprint import pprint

notion = Client(auth="ntn_b71264501237SHXAg8e3pN81R2JcWRJS8PIcJMkP4fR1fo")

def get_page_details(page_id: str) -> Dict:
    """获取页面完整详情（属性+内容）"""
    try:
        # 获取页面属性
        page = notion.pages.retrieve(page_id)
        
        # 递归获取所有内容块
        blocks = []
        cursor = None
        while True:
            response = notion.blocks.children.list(
                block_id=page_id,
                page_size=100,
                start_cursor=cursor
            )
            blocks.extend(response.get("results", []))
            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
        
        return {
            "page_info": page,
            "content_blocks": process_blocks(blocks)
        }
    except Exception as e:
        print(f"获取页面失败: {str(e)}")
        return None

def process_blocks(blocks: List[Dict]) -> List[Dict]:
    """解析块内容结构"""
    processed = []
    for block in blocks:
        block_type = block["type"]
        content = {
            "id": block["id"],
            "type": block_type,
            "text": extract_text(block),
            "children": []
        }
        
        # 递归处理子块
        if block.get("has_children"):
            child_blocks = []
            cursor = None
            while True:
                response = notion.blocks.children.list(
                    block_id=block["id"],
                    page_size=100,
                    start_cursor=cursor
                )
                child_blocks.extend(response.get("results", []))
                if not response.get("has_more"):
                    break
                cursor = response.get("next_cursor")
            content["children"] = process_blocks(child_blocks)
        
        # 处理特殊块类型
        if block_type == "image":
            content["url"] = block["image"]["file"]["url"]
        elif block_type == "bookmark":
            content["link"] = block["bookmark"]["url"]
        
        processed.append(content)
    return processed

def extract_text(block: Dict) -> str:
    """提取块中的文本内容"""
    rich_text = block.get(block["type"], {}).get("rich_text", [])
    return " ".join([rt["plain_text"] for rt in rich_text])

# 使用示例
if __name__ == "__main__":
    page_id = "1f21a8c4ffcb801d81e2d190c492b45e"  # 替换实际页面ID
    details = get_page_details(page_id)
    
    if details:
        print("页面属性：")
        pprint(details["page_info"]["properties"])
        
        print("\n内容结构：")
        for idx, block in enumerate(details["content_blocks"][:3], 1):
            print(f"{idx}. [{block['type']}] {block['text'][:50]}...")
