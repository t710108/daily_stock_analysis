import unittest

class TestCISanityCheck(unittest.TestCase):
    """
    CI 环境健康检查（空测试）。
    目的：验证测试运行器（Test Runner）是否正常工作，不依赖任何业务代码。
    """
    
    def test_environment_is_ready(self):
        """这是一个永远会通过的测试"""
        # 这里的逻辑非常简单：1 等于 1，所以它永远不会报错
        self.assertEqual(1, 1, "CI 环境基础逻辑正常")

    def test_python_version(self):
        """打印当前 Python 版本，方便排查环境问题"""
        import sys
        print(f"当前运行环境的 Python 版本是: {sys.version}")
        self.assertTrue(True)
