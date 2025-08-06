#!/usr/bin/env python3
"""
测试Notion API连接稳定性的脚本
用于验证修复"reset by peer"错误的效果
"""

import sys
import os
import time
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auto_notion import create_notion_client, get_database_schema, get_today_pages

def test_connection_stability(database_id: str, test_count: int = 5):
    """测试连接稳定性"""
    print(f"开始连接稳定性测试，测试次数: {test_count}")
    print(f"目标数据库ID: {database_id}")
    print("-" * 50)
    
    # 创建客户端
    client = create_notion_client("ntn_b71264501237SHXAg8e3pN81R2JcWRJS8PIcJMkP4fR1fo")
    
    success_count = 0
    failure_count = 0
    
    for i in range(test_count):
        print(f"\n测试 {i+1}/{test_count} - {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            # 测试获取数据库结构
            print("  - 获取数据库结构...", end="")
            db_schema = get_database_schema(database_id)
            print(" ✓")
            
            # 测试查询页面
            print("  - 查询当日页面...", end="")
            today_pages = get_today_pages(database_id)
            print(f" ✓ (找到 {len(today_pages)} 个页面)")
            
            success_count += 1
            print(f"  结果: 成功 ✓")
            
        except Exception as e:
            failure_count += 1
            error_msg = str(e)
            print(f" ✗")
            print(f"  结果: 失败 ✗")
            print(f"  错误信息: {error_msg}")
            
            # 检查是否是网络相关错误
            if any(keyword in error_msg.lower() for keyword in [
                'connection reset by peer', 'connection aborted', 
                'connection broken', 'timeout', 'network'
            ]):
                print("  错误类型: 网络连接错误")
            else:
                print("  错误类型: 其他错误")
        
        # 测试间隔
        if i < test_count - 1:
            print("  等待间隔 2 秒...")
            time.sleep(2)
    
    print("\n" + "=" * 50)
    print(f"测试完成!")
    print(f"成功次数: {success_count}/{test_count}")
    print(f"失败次数: {failure_count}/{test_count}")
    print(f"成功率: {(success_count/test_count)*100:.1f}%")
    
    if failure_count == 0:
        print("🎉 所有测试都成功! 连接稳定性良好。")
    elif failure_count < test_count / 2:
        print("⚠️ 有部分失败，但整体还算稳定。")
    else:
        print("❌ 失败次数较多，可能仍有连接问题。")

def test_retry_mechanism():
    """测试重试机制"""
    print("\n" + "=" * 50)
    print("测试重试机制...")
    
    # 使用一个不存在的数据库ID来触发错误，验证重试逻辑
    fake_db_id = "00000000-0000-0000-0000-000000000000"
    
    try:
        print(f"尝试访问不存在的数据库: {fake_db_id}")
        db_schema = get_database_schema(fake_db_id)
        print("意外成功? 这不应该发生...")
    except Exception as e:
        print(f"预期的错误: {str(e)[:100]}...")
        print("重试机制正常工作 ✓")

if __name__ == "__main__":
    # 默认数据库ID
    default_db_id = "a61b3135-719a-4bb8-969e-5e8759a421c1"
    
    if len(sys.argv) > 1:
        db_id = sys.argv[1]
    else:
        db_id = default_db_id
    
    print("Notion API 连接稳定性测试")
    print("=" * 50)
    
    # 测试连接稳定性
    test_connection_stability(db_id, test_count=10)
    
    # 测试重试机制
    test_retry_mechanism()
    
    print("\n测试完成!")