import os
import pytest

def pytest_ignore_collect(collection_path, path, config):
    """
    自动跳过 known_failures.txt 中列出的测试文件
    兼容新旧版本的 pytest (同时处理 collection_path 和 path)
    """
    # 1. 确定要检查的文件路径对象
    # 优先使用新版 API 的 collection_path，如果为 None 则使用旧版 path
    check_path = collection_path if collection_path else path
    
    # 2. 获取项目根目录 (假设 conftest.py 在 tests/ 目录下)
    # os.path.dirname(__file__) 获取当前文件目录，再上一层即为根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 3. 读取失败列表文件
    fail_list_file = os.path.join(root_dir, "known_failures.txt")
    
    if not os.path.exists(fail_list_file):
        return False  # 如果文件不存在，不跳过任何测试

    try:
        with open(fail_list_file, "r") as f:
            # 读取每一行并去除首尾空白，过滤空行
            ignored_files = [line.strip() for line in f.readlines() if line.strip()]
            
            # 将路径转换为字符串进行比较
            current_file_str = str(check_path)
            
            # 4. 检查当前文件是否在忽略列表中
            for ignored in ignored_files:
                # 支持相对路径匹配 (例如: tests/test_xxx.py)
                if ignored in current_file_str or current_file_str.endswith(ignored):
                    return True  # 返回 True 表示忽略该文件
                    
    except Exception:
        pass  # 如果读取出错，为了保证 CI 不挂，默认不跳过

    return False
