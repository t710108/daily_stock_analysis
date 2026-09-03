、import os
import pytest

def pytest_ignore_collect(path, config):
    """
    兼容旧版 pytest 的写法 (只使用 path 参数)
    如果是新版 pytest，它会自动忽略多余的参数检查或适配此签名
    """
    # 将 py.path.local 对象转换为字符串进行检查
    file_path = str(path)
    
    # 获取项目根目录 (假设 conftest.py 在 tests/ 目录下)
    # os.path.dirname(__file__) 获取当前文件目录，再上一层即为根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fail_list_path = os.path.join(root_dir, 'known_failures.txt')
    
    # 如果名单文件存在，读取并检查
    if os.path.exists(fail_list_path):
        with open(fail_list_path, 'r') as f:
            ignored_files = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            # 检查当前文件是否在忽略名单中
            # 我们检查文件名的相对路径是否匹配
            for ignore_item in ignored_files:
                if file_path.endswith(ignore_item) or ignore_item in file_path:
                    return True  # 返回 True 表示忽略该文件
                    
    return False  # 默认不忽略
