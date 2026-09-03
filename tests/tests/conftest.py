import os
import pytest


def pytest_ignore_collect(collection_path, config):
    """
    自动跳过 known_failures.txt 中列出的测试文件
    严格适配 Pytest 8.0+ (仅使用 collection_path)
    """
    # 1. 获取文件路径字符串
    # collection_path 是 pathlib.Path 对象
    file_path = str(collection_path)

    # 2. 获取项目根目录下的 known_failures.txt 路径
    # 这里的逻辑假设 conftest.py 在 tests/tests/ 下，
    # 所以需要向上跳两级 (..) 才能回到项目根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ignore_file = os.path.join(root_dir, "known_failures.txt")

    # 3. 如果忽略列表文件存在，则读取并比对
    if os.path.exists(ignore_file):
        with open(ignore_file, "r") as f:
            ignored_files = [line.strip() for line in f if line.strip()]

        # 检查当前文件是否在忽略列表中
        # 使用文件名或相对路径匹配均可，这里做简单的包含检查
        for ignored in ignored_files:
            if ignored in file_path:
                return True

    return False
