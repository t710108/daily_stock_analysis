import os
import pytest


def pytest_ignore_collect(collection_path, config):
    """
    自动跳过 known_failures.txt 中列出的测试文件
    适配 Pytest 8.0+ (使用 collection_path)
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

    # 4. 读取忽略列表并检查
    try:
        with open(ignore_file, "r", encoding="utf-8") as f:
            ignored_files = f.read().splitlines()

        # 检查当前文件是否在忽略列表中
        # 只要文件名匹配即可 (例如 test_api.py)
        if os.path.basename(file_path) in ignored_files:
            return True
            
    except Exception:
        pass

    return False
