import sys
import os
import unittest

# 【严谨处理1】动态修正 Python 模块搜索路径
# 确保无论 CI 在哪个目录启动，都能正确找到 src 目录
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCIWorkflowContract(unittest.TestCase):
    """
    CI 工作流契约测试 (基础结构验证)
    注意：本测试仅验证核心类的导入与实例化，不包含具体业务逻辑调用。
    """

    def test_01_pipeline_import(self):
        """测试1：验证 StockPipeline 类能否被正确导入"""
        try:
            from src.pipeline import StockPipeline
        except ImportError as e:
            self.fail(f"模块导入失败，请检查 src/pipeline.py 是否存在及类名是否正确: {e}")
        except Exception as e:
            self.fail(f"导入过程中发生未知错误: {e}")
        
        # 验证导入后确实是一个类
        self.assertTrue(isinstance(StockPipeline, type), "StockPipeline 不是一个有效的类")

    def test_02_pipeline_instantiation(self):
        """测试2：验证 StockPipeline 类能否被成功实例化"""
        try:
            from src.pipeline import StockPipeline
        except ImportError:
            self.skipTest("类导入失败，跳过实例化测试")

        try:
            # 尝试无参实例化
            instance = StockPipeline()
            self.assertIsNotNone(instance, "实例化返回了 None")
        except TypeError as e:
            # 如果 __init__ 需要必填参数，捕获 TypeError 并给出明确提示
            self.fail(f"StockPipeline 实例化失败：__init__ 方法需要参数，但测试未提供。"
                      f"请检查 __init__ 签名或修改测试代码传入 Mock 参数。错误详情: {e}")
        except Exception as e:
            self.fail(f"实例化过程中发生未知错误: {e}")

if __name__ == '__main__':
    unittest.main()
