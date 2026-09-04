import os
import sys
import unittest


# 自动添加项目根目录到路径，防止导入失败
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPipelineContract(unittest.TestCase):
    """
    极简契约测试：只验证核心类是否存在且可实例化。
    这是 CI 通过的底线，不依赖具体业务方法名。
    """

    def test_class_exists_and_instantiable(self):
        """测试 StockPipeline 类是否可以被导入并实例化"""
        try:
            # 1. 尝试从 src.pipeline 导入类
            from src.pipeline import StockPipeline
            
            # 2. 尝试实例化（假设不需要复杂参数，或者参数有默认值）
            # 如果初始化需要参数，这里可能会报错，请根据实际情况调整
            instance = StockPipeline()
            
            # 3. 断言实例化成功
            self.assertIsNotNone(instance, "StockPipeline 实例化失败")
            
        except ImportError as e:
            self.fail(f"无法导入 StockPipeline 类，请检查 src/pipeline.py 是否存在: {e}")
        except Exception as e:
            self.fail(f"StockPipeline 实例化出错，请检查 __init__ 方法: {e}")

if __name__ == '__main__':
    unittest.main()
