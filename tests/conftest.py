import os
import pytest


def pytest_ignore_collect(collection_path, config):
    """
    自动跳过 known_failures.txt 中列出的测试文件
    严格适配 Pytest 8.0+ (仅接受 collection_path)
    """
    # 1. 将 pathlib.Path 对象转换为字符串
    file_path = str(collection_path)

    # 2. 获取项目根目录 (假设 conftest 在 tests 目录下，根目录在其上一级)
    # 如果你的目录结构不同，请调整这里的 os.path.dirname 层级
    root_dir = os.path.dirname(os.path.dirname(file_path))

    # 3. 构建失败列表文件的绝对路径
    fail_list_path = os.path.join(root_dir, "known_failures.txt")

    # 4. 如果列表文件存在，执行跳过逻辑
    if os.path.exists(fail_list_path):
        with open(fail_list_path, "r", encoding="utf-8") as f:
            # 读取每一行，去除空白，忽略空行和注释
            ignore_files = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#")
            ]

        # 检查当前文件是否在忽略列表中
        # 使用文件名匹配（更稳健）或全路径匹配
        current_file_name = os.path.basename(file_path)

        for ignore_item in ignore_files:
            # 如果列表里写的是文件名（如 test_xxx.py）或者包含在路径中
            if ignore_item in file_path or ignore_item == current_file_name:
                return True  # 返回 True 表示忽略（跳过）该文件

    return False  # 默认不跳过
