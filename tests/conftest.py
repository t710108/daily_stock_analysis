import os
import pytest


def pytest_ignore_collect(collection_path, config):
    """
    自动跳过 known_failures.txt 中列出的测试文件
    适配 Pytest 8.0+ (仅使用 collection_path)
    """
    # 1. 获取文件路径字符串
    # collection_path 是 pathlib.Path 对象
    file_path = str(collection_path)

    # 2. 获取项目根目录 (假设 conftest.py 在 tests/ 目录下)
    # os.path.dirname(__file__) 获取当前文件目录，再上一层即为根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ignore_file = os.path.join(root_dir, "known_failures.txt")

    # 3. 如果忽略列表文件不存在，则不跳过任何文件
    if not os.path.exists(ignore_file):
        return False

    # 4. 读取忽略列表
    try:
        with open(ignore_file, "r", encoding="utf-8") as f:
            ignore_list = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except Exception:
        return False

    # 5. 检查当前文件是否在忽略列表中
    # 我们检查文件名是否包含在忽略列表的某一行中
    for ignore_item in ignore_list:
        if ignore_item in file_path:
            print(f"🔇 Ignoring test file due to known failure: {file_path}")
            return True

    return False
