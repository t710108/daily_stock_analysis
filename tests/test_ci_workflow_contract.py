import os
import sys
import ast
import unittest

class TestStockAnalysisPipelineStaticContract(unittest.TestCase):
    """
    静态契约测试：
    不导入、不运行代码，仅通过语法树分析验证核心类结构是否完整。
    这种测试方法完全免疫 CI 环境缺失配置（如 API Key）的问题。
    """

    def setUp(self):
        # 定位到 src/pipeline.py 文件的绝对路径
        self.pipeline_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'src', 'pipeline.py'
        )

    def test_pipeline_file_exists(self):
        """验证 pipeline.py 文件是否存在"""
        self.assertTrue(
            os.path.exists(self.pipeline_path),
            f"找不到核心文件: {self.pipeline_path}"
        )

    def test_class_definition_exists(self):
        """验证 StockAnalysisPipeline 类是否已定义"""
        with open(self.pipeline_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())

        class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        self.assertIn(
            'StockAnalysisPipeline', class_names,
            "未在 pipeline.py 中找到 'StockAnalysisPipeline' 类定义"
        )

    def test_run_method_signature(self):
        """验证 run 方法是否存在"""
        with open(self.pipeline_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())

        found_run = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'StockAnalysisPipeline':
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == 'run':
                        found_run = True
                        break

        self.assertTrue(found_run, "StockAnalysisPipeline 类中缺少 'run' 方法")

if __name__ == '__main__':
    unittest.main()
