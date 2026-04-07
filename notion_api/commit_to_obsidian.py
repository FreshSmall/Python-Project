#!/usr/bin/env python3
"""
将 git commit 信息推送到 Obsidian 每日笔记的「今日产出」部分。
用法：
  1. 自动模式（在 git 仓库中运行，自动获取最新 commit）：
     python3 commit_to_obsidian.py --auto

  2. 手动模式：
     python3 commit_to_obsidian.py --repo "OES" --message "fix: xxx" --hash "abc1234"

  配置为 post-commit hook：
     在各仓库 .git/hooks/post-commit 中添加：
     #!/bin/bash
     python3 /Users/bjhl/PycharmProjects/pythonProject/notion_api/commit_to_obsidian.py --auto
"""

import argparse
import subprocess
import os
import sys
import re
import locale
from datetime import datetime

# Obsidian daily note 根目录
DAILY_NOTE_ROOT = "/Users/bjhl/GitRepository/knowledge/journal/daily"

# 每日模板路径
DAILY_TEMPLATE_PATH = "/Users/bjhl/GitRepository/knowledge/_template/daily_template.md"

# 要追加的 section 标题
TARGET_SECTION = "## 📤 今日产出"

# 中文星期映射
_WEEKDAY_CN = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def get_daily_note_path():
    # type: () -> str
    """获取今天的 daily note 文件路径"""
    now = datetime.now()
    return os.path.join(
        DAILY_NOTE_ROOT,
        now.strftime("%Y"),
        now.strftime("%m"),
        now.strftime("%Y-%m-%d") + ".md"
    )


def get_git_info():
    # type: () -> tuple
    """从当前 git 仓库获取最新 commit 信息，返回 (repo_name, message, hash)"""
    try:
        commit_hash = subprocess.check_output(
            ["git", "log", "-1", "--format=%H"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        commit_message = subprocess.check_output(
            ["git", "log", "-1", "--format=%s"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        # 通过 remote url 或目录名推断 repo name
        repo_name = _get_repo_name()

        return repo_name, commit_message, commit_hash
    except subprocess.CalledProcessError as e:
        print("错误：无法获取 git 信息，请确认在 git 仓库中运行。", file=sys.stderr)
        sys.exit(1)


def _get_repo_name():
    # type: () -> str
    """推断仓库名称：优先从 remote url 获取，否则用目录名"""
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        # 从 URL 提取仓库名：git@xxx:org/repo.git 或 https://xxx/org/repo.git
        name = remote_url.rstrip("/").rsplit("/", 1)[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return name
    except subprocess.CalledProcessError:
        # 没有 remote，用当前目录名
        try:
            toplevel = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            return os.path.basename(toplevel)
        except subprocess.CalledProcessError:
            return "unknown"


def create_daily_note_from_template(daily_note_path):
    # type: (str) -> bool
    """从模板创建 daily note，替换 Templater 占位符"""
    if not os.path.exists(DAILY_TEMPLATE_PATH):
        print(f"错误：模板文件不存在 {DAILY_TEMPLATE_PATH}", file=sys.stderr)
        return False

    with open(DAILY_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    weekday_cn = _WEEKDAY_CN[now.weekday()]
    date_with_weekday = f"{date_str} {weekday_cn}"

    # 替换 Templater 占位符
    content = template.replace('<% tp.date.now("YYYY-MM-DD") %>', date_str)
    content = content.replace('<% tp.date.now("YYYY-MM-DD dddd") %>', date_with_weekday)

    # 确保目录存在
    os.makedirs(os.path.dirname(daily_note_path), exist_ok=True)

    with open(daily_note_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"已创建 daily note：{daily_note_path}")
    return True


def append_commit_to_daily_note(repo_name, commit_message, commit_hash):
    # type: (str, str, str) -> bool
    """将 commit 信息追加到 daily note 的「今日产出」section"""
    daily_note_path = get_daily_note_path()

    if not os.path.exists(daily_note_path):
        if not create_daily_note_from_template(daily_note_path):
            return False

    with open(daily_note_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 去重：检查 commit hash 是否已存在
    short_hash = commit_hash[:7]
    if short_hash in content:
        print(f"跳过：commit {short_hash} 已存在于 daily note 中")
        return True

    # 找到目标 section
    lines = content.split("\n")
    target_idx = None
    next_section_idx = None

    for i, line in enumerate(lines):
        if line.strip().startswith(TARGET_SECTION.strip()):
            target_idx = i
            continue
        if target_idx is not None and line.strip().startswith("## "):
            next_section_idx = i
            break

    if target_idx is None:
        print(f"跳过：未找到「{TARGET_SECTION}」section", file=sys.stderr)
        return False

    # 构建新行
    new_line = f"- {repo_name}：{commit_message} <!-- hash:{short_hash} -->"

    # 找到插入位置：在 section 内容末尾、下一个 section 之前
    # 跳过 section 标题后的空行和已有内容，找到最后一个非空行
    insert_idx = next_section_idx if next_section_idx else len(lines)

    # 往回找，跳过空行，在内容末尾插入
    while insert_idx > target_idx + 1 and lines[insert_idx - 1].strip() == "":
        insert_idx -= 1

    # 如果 section 下只有 "- " 占位符，替换它
    if (insert_idx == target_idx + 2
            and lines[target_idx + 1].strip() == "-"):
        lines[target_idx + 1] = new_line
    else:
        lines.insert(insert_idx, new_line)

    # 写回文件
    with open(daily_note_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"已追加：{new_line}")
    return True


def main():
    parser = argparse.ArgumentParser(description="推送 git commit 到 Obsidian 每日笔记")
    parser.add_argument("--auto", action="store_true", help="自动从当前 git 仓库获取最新 commit")
    parser.add_argument("--repo", help="仓库名称")
    parser.add_argument("--message", "-m", help="commit message")
    parser.add_argument("--hash", help="commit hash")
    args = parser.parse_args()

    if args.auto:
        repo_name, message, commit_hash = get_git_info()
    elif args.repo and args.message and args.hash:
        repo_name = args.repo
        message = args.message
        commit_hash = args.hash
    else:
        parser.error("请使用 --auto 或同时提供 --repo, --message, --hash")
        return

    append_commit_to_daily_note(repo_name, message, commit_hash)


if __name__ == "__main__":
    main()
