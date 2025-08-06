from notion_client import Client
from typing import Dict, List, Optional
from pprint import pprint
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_notion_client(auth_token: str) -> Client:
    """创建配置了网络重试机制的Notion客户端"""
    # 创建重试策略
    retry_strategy = Retry(
        total=3,  # 总重试次数
        backoff_factor=1,  # 重试间隔
        status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
    )
    
    # 创建HTTP适配器
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # 创建session并配置适配器
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # 设置连接和读取超时
    session.timeout = (10, 30)  # (连接超时, 读取超时)
    
    # 创建Notion客户端
    client = Client(auth=auth_token)
    # 将自定义session应用到客户端
    client._client.session = session
    
    return client

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """装饰器：为函数添加重试机制"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    error_msg = str(e).lower()
                    
                    # 检查是否是网络相关错误
                    if any(keyword in error_msg for keyword in [
                        'connection reset by peer', 'connection aborted', 
                        'connection broken', 'timeout', 'network', 
                        'connection error', 'read timeout'
                    ]):
                        if attempt < max_retries - 1:
                            wait_time = delay * (2 ** attempt)  # 指数退避
                            print(f"网络错误，{wait_time}秒后重试 (尝试 {attempt + 1}/{max_retries}): {e}")
                            time.sleep(wait_time)
                            continue
                    
                    # 如果不是网络错误或者已达到最大重试次数，直接抛出异常
                    raise e
            
            # 如果所有重试都失败，抛出最后一个异常
            raise last_exception
        return wrapper
    return decorator

notion = create_notion_client("ntn_b71264501237SHXAg8e3pN81R2JcWRJS8PIcJMkP4fR1fo")

@retry_on_failure(max_retries=3, delay=1.0)
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
