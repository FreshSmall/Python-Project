# Notion API "Connection Reset by Peer" 错误修复说明

## 问题描述

在调用 `auto_notion.py` 脚本时，经常会遇到 "connection reset by peer" 错误。这是一个常见的网络连接问题，通常由以下原因引起：

1. **网络不稳定** - 网络连接临时中断
2. **服务器负载** - Notion API 服务器暂时过载
3. **超时设置** - 默认的连接和读取超时时间过短
4. **缺乏重试机制** - 没有在网络错误时自动重试

## 解决方案

### 1. 网络连接优化

为 Notion 客户端配置了更稳定的网络设置：

```python
def create_notion_client(auth_token: str) -> Client:
    # 创建重试策略
    retry_strategy = Retry(
        total=3,  # 总重试次数
        backoff_factor=1,  # 重试间隔
        status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
    )
    
    # 设置连接和读取超时
    session.timeout = (10, 30)  # (连接超时, 读取超时)
```

### 2. 智能重试机制

实现了一个装饰器，为所有 API 调用添加自动重试功能：

```python
@retry_on_failure(max_retries=3, delay=1.0)
def api_function():
    # API 调用代码
```

**重试策略：**
- 自动识别网络相关错误（connection reset, timeout, etc.）
- 采用指数退避算法（exponential backoff）
- 最多重试3次
- 非网络错误直接抛出，不浪费时间

### 3. 修复的文件

1. **`auto_notion.py`** - 主要脚本文件
   - 添加了网络重试机制
   - 优化了客户端初始化
   - 为所有主要API调用添加了重试装饰器

2. **`notion_view.py`** - 视图脚本文件
   - 同样添加了网络优化和重试机制

3. **`test_connection.py`** - 新增的测试脚本
   - 用于验证连接稳定性
   - 测试重试机制是否正常工作

## 使用说明

### 正常使用

脚本的使用方式没有改变，只是现在更稳定了：

```bash
# 基本使用
python auto_notion.py

# 指定数据库
python auto_notion.py --database your-database-id

# 强制创建新页面
python auto_notion.py --force

# 启用调试模式
python auto_notion.py --debug
```

### 测试连接稳定性

运行测试脚本来验证修复效果：

```bash
# 使用默认数据库测试
python test_connection.py

# 指定数据库测试
python test_connection.py your-database-id
```

## 预期效果

修复后，您应该看到：

1. **减少错误发生** - "connection reset by peer" 错误应该明显减少
2. **自动恢复** - 即使遇到网络问题，脚本会自动重试
3. **更好的日志** - 能看到重试过程的详细信息
4. **更稳定的执行** - 整体执行成功率显著提高

## 监控和调试

### 开启调试模式

```bash
python auto_notion.py --debug
```

调试模式会显示：
- 详细的网络连接信息
- 重试过程的日志
- 错误的完整堆栈信息

### 查看重试日志

当发生网络错误时，您会看到类似的日志：

```
WARNING - 网络错误，1秒后重试 (尝试 1/3): Connection reset by peer
WARNING - 网络错误，2秒后重试 (尝试 2/3): Connection reset by peer
INFO - 重试成功，操作完成
```

## 故障排除

如果仍然遇到问题：

1. **检查网络连接** - 确保网络稳定
2. **验证 API 令牌** - 确保 Notion API 令牌有效
3. **查看服务状态** - 检查 Notion 服务是否正常
4. **增加重试次数** - 在代码中调整 `max_retries` 参数
5. **调整超时时间** - 修改 `session.timeout` 设置

## 技术细节

### 依赖项

新增的依赖项：
- `requests` - HTTP 客户端库
- `urllib3` - URL 处理库（通常随 requests 一起安装）

### 配置参数

可以调整的重要参数：

```python
# 重试次数
max_retries = 3

# 超时设置 (连接超时, 读取超时)
session.timeout = (10, 30)

# 退避因子（重试间隔倍数）
backoff_factor = 1
```

## 更新日志

- **2024-01-XX** - 初始修复版本
  - 添加网络重试机制
  - 优化连接设置
  - 创建测试脚本

---

**注意：** 这些修改向后兼容，不会影响现有的使用方式。如果您在使用过程中发现任何问题，请及时反馈。