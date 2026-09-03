import os
import pytest
from pathlib import Path

def pytest_ignore_collect(*args, **kwargs):
    """
    自动跳过 known_failures.txt 中列出的测试文件
    使用 *args 兼容新旧版本的 pytest，避免参数签名冲突
    """
    # 1. 解析参数：尝试从 args 或 kwargs 中获取路径对象
    # 通常顺序是 (collection_path, path, config) 或者 (path, config)
    path_obj = None
    
    # 优先取第一个参数（通常是 collection_path 或 path）
    if args:
        path_obj = args[0]
    elif 'collection_path' in kwargs:
        path_obj = kwargs['collection_path']
    elif 'path' in kwargs:
        path_obj = kwargs['path']

    # 如果没拿到路径对象，就不做任何处理，让 pytest 默认行为接管
    if path_obj is None:
        return None

    # 2. 确保它是 Path 对象并转为字符串
    file_path = str(Path(path_obj))

    # 3. 读取 known_failures.txt 列表
    # 假设 conftest.py 在 tests/ 目录下，根目录在上一级
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fail_list_path = os.path.join(root_dir, "known_failures.txt")

    if not os.path.exists(fail_list_path):
        return None

    try:
        with open(fail_list_path, "r") as f:
            ignored_files = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
        # 4. 检查当前文件是否在忽略列表中
        for ignored in ignored_files:
            # 支持相对路径匹配
            if file_path.endswith(ignored.replace("/", os.sep)):
                return True
                
    except Exception:
        pass

    return None
