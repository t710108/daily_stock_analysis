import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

# [已禁用] from src.notification_sender.sender_factory import NotificationSenderFactory
from src.core.config_manager import ConfigManager
from src.core.trading_calendar import TradingCalendar

# [已禁用] 因为仓库中不存在 llm_client.py 文件，暂时注释掉
# from src.core.llm_client import LLMClient
# from src.core.market_review_generator import MarketReviewGenerator


logger = logging.getLogger(__name__)


class StockAnalysisPipeline:
    """股票分析流水线：串联数据获取、AI分析、报告生成与通知发送"""

    def __init__(self):
        self.config = ConfigManager()
        self.calendar = TradingCalendar()

        # [已禁用] self.llm_client = LLMClient()
        # [已禁用] self.review_generator = MarketReviewGenerator(self.llm_client)

        # self.sender_factory = NotificationSenderFactory() # [已禁用]

    def _resolve_resume_target_date(self, resume_date_str: Optional[str] = None) -> Optional[date]:
        """解析断点续传的日期"""
        if not resume_date_str:
            return None
        try:
            return datetime.strptime(resume_date_str, "%Y-%m-%d").date()
        except ValueError:
            logger.warning(f"Invalid resume date format: {resume_date_str}")
            return None

    def run_analysis(self, target_date: Optional[date] = None, is_resume: bool = False, resume_date: Optional[str] = None):
        """运行分析主流程"""
        logger.info(f"Starting pipeline for date: {target_date}, Resume: {is_resume}")

        # 1. 检查交易日历
        if target_date and not self.calendar.is_trading_day(target_date):
            logger.info(f"{target_date} is not a trading day. Skipping.")
            return

        # 2. 获取数据 (模拟)
        market_data = self._fetch_market_data(target_date)
        if not market_data:
            logger.warning("No market data fetched.")
            return

        # 3. AI 分析 (已禁用，防止报错)
        # analysis_result = self.review_generator.generate(market_data)

        # 4. 发送通知 (已禁用)
        # if analysis_result:
        #     sender = self.sender_factory.get_sender("email")
        #     sender.send(analysis_result)

        logger.info("Pipeline finished.")

    def _fetch_market_data(self, target_date: date) -> List[Dict[str, Any]]:
        """获取市场数据占位符"""
        # 这里应该是调用数据源的逻辑
        return [{"symbol": "AAPL", "close": 150.0}]
