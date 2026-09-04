import os
import sys
import ast
import unittest

class TestStockAnalysisPipelineStaticContract(unittest.TestCase):
    """
    静态契约测试：
    通过解析 Python 语法树 (AST) 来验证核心类的结构完整性。
    优点：不导入模块，不执行代码，完全免疫 CI 环境缺失配置/依赖的问题。
    """

    def setUp(self):
        # 定位到 src/pipeline.py 文件的绝对路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pipeline_path = os.path.join(base_dir, 'src', 'pipeline.py')

    def test_file_exists(self):
        """验证核心文件是否存在"""
        self.assertTrue(
            os.path.exists(self.pipeline_path),
            f"核心文件未找到: {self.pipeline_path}"
        )

    def test_class_and_method_structure(self):
        """验证类名和方法定义是否符合契约"""
        with open(self.pipeline_path, 'r', encoding='utf-8') as f:
            source = f.read()

        # 解析语法树
        tree = ast.parse(source)

        # 1. 查找 StockAnalysisPipeline 类
        pipeline_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'StockAnalysisPipeline':
                pipeline_class = node
                break

        self.assertIsNotNone(pipeline_class, "未找到 'StockAnalysisPipeline' 类定义")

        # 2. 验证关键方法是否存在
        method_names = [n.name for n in pipeline_class.body if isinstance(n, ast.FunctionDef)]

        # 检查 __init__
        self.assertIn('__init__', method_names, "缺少 __init__ 初始化方法")

        # 检查 run 方法 (这是流水线的入口)
        self.assertIn('run', method_names, "缺少核心的 'run' 方法")

if __name__ == '__main__':
    unittest.main()
