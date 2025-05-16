import os
from llm_common import kotlin_to_java


def read_kotlin_file(directory):
    kotlin_files = []

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为 .kt
            if file.endswith('.kt'):
                # 获取文件的完整路径
                full_path = os.path.join(root, file)
                kotlin_files.append((file, full_path))

    return kotlin_files


def write_java_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    kotlin_files = read_kotlin_file("/Users/bjhl/IdeaProjects/baijiahulian/tmk-crm/service/src/main/kotlin")
    # 打印文件名和路径
    for file_name, file_path in kotlin_files:
        print(file_name, file_path)
        with open(file_path, 'r') as file:
            out_file = kotlin_to_java(file.read())
            write_java_file(file_path.replace('.kt', '.java'), out_file)
