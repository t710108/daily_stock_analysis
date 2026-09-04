import os
import ast
import unittest

class TestStockAnalysisPipelineStaticContract(unittest.TestCase):
    """
    静态契约测试（最终版）：
    1. 不导入业务模块（避免缺配置报错）。
    2. 不读取 requirements.txt（避免编码报错）。
    3. 仅通过 AST 语法树分析验证核心类结构。
    """

    def setUp(self):
        # 动态获取项目根目录和 pipeline.py 的路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pipeline_path = os.path.join(base_dir, 'src', 'pipeline.py')

    def test_pipeline_file_exists(self):
        """验证核心文件是否存在"""
        self.assertTrue(
            os.path.exists(self.pipeline_path),
            f"核心文件未找到: {self.pipeline_path}"
        )

    def test_stock_analysis_pipeline_class_exists(self):
        """验证 StockAnalysisPipeline 类是否定义"""
        with open(self.pipeline_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=self.pipeline_path)

        class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        self.assertIn(
            'StockAnalysisPipeline', 
            class_names, 
            "未在 src/pipeline.py 中找到 StockAnalysisPipeline 类定义"
        )

    def test_run_method_exists(self):
        """验证 run 方法是否存在于类中"""
        with open(self.pipeline_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=self.pipeline_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'StockAnalysisPipeline':
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                self.assertIn('run', method_names, "StockAnalysisPipeline 类中缺少 run 方法")
                return
        
        self.fail("StockAnalysisPipeline 类未找到，无法检查方法")

if __name__ == '__main__':
    unittest.main()
