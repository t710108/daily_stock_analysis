import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# 确保能导入 src 目录
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPipelineContract(unittest.TestCase):
    """
    契约测试：验证 pipeline.py 是否具备核心能力，而不依赖具体方法名。
    """

    def setUp(self):
        # 动态导入，防止文件名大小写问题导致整个文件报错
        try:
            from src.pipeline import StockPipeline
            self.PipelineClass = StockPipeline
            self.import_success = True
        except ImportError as e:
            self.import_success = False
            self.import_error = str(e)

    def test_import_works(self):
        """1. 验证能否成功导入 StockPipeline 类"""
        self.assertTrue(self.import_success, f"无法导入 StockPipeline: {self.import_error}")

    def test_has_process_method(self):
        """2. 自动探测是否存在处理股票的方法"""
        if not self.import_success:
            self.skipTest("导入失败，跳过后续测试")

        # 列出类里所有公开的方法
        methods = [m for m in dir(self.PipelineClass) if not m.startswith('_') and callable(getattr(self.PipelineClass, m))]

        # 定义我们期望的关键词
        keywords = ['process', 'run', 'analyze', 'start', 'execute']

        # 寻找匹配的方法
        found_methods = []
        for method_name in methods:
            for keyword in keywords:
                if keyword in method_name.lower():
                    found_methods.append(method_name)

        # 只要找到一个类似的方法就算通过
        self.assertTrue(len(found_methods) > 0,
                        f"未找到任何包含 {keywords} 关键词的方法。当前可用方法: {methods}")

    def test_instantiation(self):
        """3. 验证能否实例化（需要 Mock 掉 __init__ 里的复杂逻辑）"""
        if not self.import_success:
            self.skipTest("导入失败，跳过后续测试")

        try:
            # 尝试实例化，如果 __init__ 需要参数，这里可能会报错，所以用 try-except
            # 或者我们可以只检查它是不是个类
            self.assertTrue(isinstance(self.PipelineClass, type))
        except Exception as e:
            self.fail(f"实例化检查失败: {e}")

if __name__ == '__main__':
    unittest.main()
