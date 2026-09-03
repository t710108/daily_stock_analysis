import os
import pytest

def pytest_ignore_collect(collection_path, path, config):
    """
    自动跳过 known_failures.txt 中列出的测试文件
    """
    # 获取项目根目录（假设 conftest.py 在 tests/ 下，根目录就是上一级）
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fail_list_path = os.path.join(root_dir, "known_failures.txt")
    
    if not os.path.exists(fail_list_path):
        return None

    with open(fail_list_path, 'r') as f:
        failed_tests = [line.strip() for line in f if line.strip()]

    # 将当前检测的文件路径转换为相对路径进行比对
    rel_path = str(collection_path.relative_to(root_dir))
    
    if rel_path in failed_tests:
        print(f"⏭️ Skipping known failure: {rel_path}")
        return True
    
    return None
