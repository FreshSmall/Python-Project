from notion_client import Client
from datetime import datetime, timedelta
import pytz
from typing import List, Optional, Dict, Any
import json
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("notion-api")
# 初始化客户端
notion = Client(auth="ntn_b71264501237SHXAg8e3pN81R2JcWRJS8PIcJMkP4fR1fo")
def get_database_schema(database_id: str) -> dict:
    """获取数据库结构，查看可用的属性"""
    try:
        return notion.databases.retrieve(database_id=database_id)
    except Exception as e:
        logger.error(f"获取数据库结构失败: {str(e)}")
        raise

def get_template_page(template_id: str) -> Dict[str, Any]:
    """获取模板页面的内容"""
    try:
        # 获取页面信息
        template_page = notion.pages.retrieve(page_id=template_id)
        
        # 获取页面内容块
        blocks = notion.blocks.children.list(block_id=template_id)
        
        return {
            "page_info": template_page,
            "blocks": blocks.get("results", [])
        }
    except Exception as e:
        print(f"获取模板失败: {str(e)}")
        return {"page_info": {}, "blocks": []}

def print_template_info(template_data: Dict[str, Any]) -> None:
    """打印模板信息以便于调试"""
    page_info = template_data.get("page_info", {})
    blocks = template_data.get("blocks", [])
    
    print("===== 模板信息 =====")
    print(f"标题: {page_info.get('properties', {}).get('标题', {})}")
    print(f"图标: {page_info.get('icon')}")
    print(f"封面: {page_info.get('cover')}")
    
    print("\n===== 模板内容块 =====")
    for i, block in enumerate(blocks):
        block_type = block.get("type", "unknown")
        block_id = block.get("id")
        print(f"{i+1}. 类型: {block_type}, ID: {block_id}")
    
    print("=====================")

def get_today_pages(database_id: str) -> List[dict]:
    """获取当日创建的所有页面"""
    tz = pytz.timezone('Asia/Shanghai')
    today_start = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    response = notion.databases.query(
        database_id=database_id,
        filter={
            "and": [
                {
                    "timestamp": "created_time",
                    "created_time": {
                        "on_or_after": today_start.isoformat()
                    }
                },
                {
                    "timestamp": "created_time",
                    "created_time": {
                        "before": today_end.isoformat()
                    }
                }
            ]
        }
    )
    return response.get("results", [])

def create_custom_page(database_id: str, title_property_name: str) -> Optional[dict]:
    """创建具有特定结构的页面"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 创建新页面的基本属性
        properties = {
            title_property_name: {
                "title": [
                    {
                        "type": "mention",
                        "mention": {
                            "type": "date",
                            "date": {
                                "start": today,
                                "end": None,
                                "time_zone": None
                            }
                        }
                    },
                    {
                        "type": "text",
                        "text": {
                            "content": " ",
                            "link": None
                        }
                    }
                ]
            },
            "完成": {
                "checkbox": False
            },
            "完成度": {
                "number": 0
            },
            "类别": {
                "multi_select": [
                    {
                        "name": "每日计划"
                    }
                ]
            }
        }
        # 页面图标
        icon = {
            "type": "emoji",
            "emoji": "📌"
        } 
        print(f"正在创建页面，属性：{json.dumps(properties, ensure_ascii=False, indent=2)}")
        # 创建页面
        new_page = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            icon=icon
        )
        
        print(f"页面创建成功，ID: {new_page['id']}")
        
        # 构建自定义内容结构
        content_blocks = [
            # 工作部分
            {
                "heading_2": {
                    "rich_text": [{
                        "text": {"content": "工作"}
                    }]
                }
            },
            {
                "divider": {}
            },
            {
                "toggle": {
                    "rich_text": [{
                        "text": {"content": "插入需求"},
                        "annotations": {
                            "bold": True,
                            "color": "red"
                        }
                    }],
                    "children": [
                        {
                            "callout": {
                                "rich_text": [
                                    {
                                        "text": {"content": "待定"}
                                    }
                                ],
                                "icon": {
                                    "emoji": "🔥"
                                },
                                "color": "red_background",
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    },
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "toggle": {
                    "rich_text": [{
                        "text": {"content": "优先级P1"},
                        "annotations": {
                            "bold": True,
                            "color": "red"
                        }
                    }],
                    "children": [
                        {
                            "callout": {
                                "rich_text": [
                                    {
                                        "text": {"content": "待定"}
                                    }
                                ],
                                "icon": {
                                    "emoji": "1️⃣"
                                },
                                "color": "red_background",
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    },
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "toggle": {
                    "rich_text": [{
                        "text": {"content": "优先级P2"},
                        "annotations": {
                            "bold": True,
                            "color": "orange"
                        }
                    }],
                    "children": [
                        {
                            "numbered_list_item": {
                                "rich_text": [{
                                    "text": {"content": "待定"}
                                }],
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "numbered_list_item": {
                                "rich_text": [{
                                    "text": {"content": "待定"}
                                }],
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "toggle": {
                    "rich_text": [{
                        "text": {"content": "优先级P3"},
                        "annotations": {
                            "bold": True,
                            "color": "purple"
                        }
                    }],
                    "children": [
                        {
                            "numbered_list_item": {
                                "rich_text": [{
                                    "text": {"content": "待定"}
                                }],
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "numbered_list_item": {
                                "rich_text": [{
                                    "text": {"content": "待定"}
                                }],
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "numbered_list_item": {
                                "rich_text": [{
                                    "text": {"content": "待定"}
                                }],
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            
            # 学习部分
            {
                "heading_2": {
                    "rich_text": [{
                        "text": {"content": "学习"}
                    }]
                }
            },
            {
                "toggle": {
                    "rich_text": [{
                        "text": {"content": "插入内容"},
                        "annotations": {
                            "bold": True,
                            "color": "red"
                        }
                    }],
                    "children": [
                        {
                            "callout": {
                                "rich_text": [
                                    {
                                        "text": {"content": "待定"}
                                    }
                                ],
                                "icon": {
                                    "emoji": "💡"
                                },
                                "color": "red_background",
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    },
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "toggle": {
                    "rich_text": [{
                        "text": {"content": "既定内容"},
                        "annotations": {
                            "bold": True,
                            "color": "blue"
                        }
                    }],
                    "children": [
                        {
                            "callout": {
                                "rich_text": [
                                    {
                                        "text": {"content": "任务"}
                                    }
                                ],
                                "icon": {
                                    "emoji": "🗣"
                                },
                                "color": "blue_background",
                                "children": [
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    },
                                    {
                                        "to_do": {
                                            "rich_text": [{
                                                "text": {"content": "todo"}
                                            }],
                                            "checked": False
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            
            # 问题反思部分
            {
                "heading_2": {
                    "rich_text": [{
                        "text": {"content": "问题反思"}
                    }]
                }
            },
            {
                "table": {
                    "table_width": 3,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        {
                            "table_row": {
                                "cells": [
                                    [
                                        {
                                            "text": {
                                                "content": "问题"
                                            },
                                            "annotations": {
                                                "bold": True,
                                                "color": "red"
                                            }
                                        }
                                    ],
                                    [
                                        {
                                            "text": {
                                                "content": "反思"
                                            },
                                            "annotations": {
                                                "bold": True,
                                                "color": "blue"
                                            }
                                        }
                                    ],
                                    [
                                        {
                                            "text": {
                                                "content": "解决办法"
                                            },
                                            "annotations": {
                                                "bold": True,
                                                "color": "green"
                                            }
                                        }
                                    ]
                                ]
                            }
                        },
                        {
                            "table_row": {
                                "cells": [
                                    [
                                        {
                                            "text": {
                                                "content": ""
                                            }
                                        }
                                    ],
                                    [
                                        {
                                            "text": {
                                                "content": ""
                                            }
                                        }
                                    ],
                                    [
                                        {
                                            "text": {
                                                "content": ""
                                            }
                                        }
                                    ]
                                ]
                            }
                        }
                    ]
                }
            }
        ]
        
        # 添加内容块
        notion.blocks.children.append(
            block_id=new_page["id"],
            children=content_blocks
        )
        
        print(f"内容添加完成")
        return new_page
    except Exception as e:
        print(f"操作失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main(database_id: str, template_id: str = None, force_create: bool = False, debug: bool = False):
    # 设置日志级别
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("启用调试模式")

    # 首先获取数据库结构，检查标题属性的名称
    try:
        logger.info(f"正在连接数据库: {database_id}")
        db_schema = get_database_schema(database_id)
        properties = db_schema.get("properties", {})
        # 查找标题类型的属性
        title_property_name = None
        for name, prop in properties.items():
            if prop.get("type") == "title":
                title_property_name = name
                break
        
        if not title_property_name:
            logger.error("错误：无法找到标题类型的属性")
            logger.debug("数据库属性列表：")
            for name, prop in properties.items():
                logger.debug(f"- {name} ({prop.get('type')})")
            return
        
        logger.info(f"找到标题属性：{title_property_name}")
    
        # 查询当日页面
        today_pages = get_today_pages(database_id)
        
        if today_pages and not force_create:
            logger.info(f"找到{len(today_pages)}个当日页面")
            for page in today_pages:
                logger.info(f"- {page['id']} | {page['url']}")
        else:
            if force_create:
                logger.info("强制创建新页面...")
            else:
                logger.info("当日无页面，开始创建...")
            
            # 根据参数决定使用哪种方法创建页面
            try:
                logger.info("使用自定义格式创建页面...")
                if created_page := create_custom_page(database_id, title_property_name):
                    logger.info(f"创建成功: {created_page['url']}")
            except Exception as e:
                logger.error(f"创建页面失败: {str(e)}")
                import traceback
                logger.debug(traceback.format_exc())
    except Exception as e:
        logger.error(f"出现错误: {str(e)}")
        if debug:
            import traceback
            logger.debug(traceback.format_exc())

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="创建Notion每日页面")
    parser.add_argument("--database", "-d", default="a61b3135-719a-4bb8-969e-5e8759a421c1", help="数据库ID")
    parser.add_argument("--template", "-t", default="47dd593c8e474515928f8824a398a5b9", help="模板页面ID")
    parser.add_argument("--force", "-f", action="store_true", help="强制创建新页面，即使当日已有页面")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--token", help="Notion API 令牌，如果不提供则使用默认令牌")
    
    args = parser.parse_args()
    
    # 如果提供了令牌，重新初始化客户端
    if args.token:
        notion = Client(auth=args.token)
        logger.info("使用提供的令牌初始化Notion客户端") 
    main(args.database, args.template, args.force, args.debug)
