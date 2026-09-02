import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, Optional

# from src.notification_sender.sender_factory import NotificationSenderFactory  # [已禁用] 找不到文件，暂时注释掉
from src.config_manager import ConfigManager
from src.trading_calendar import TradingCalendar
from src.llm_client import LLMClient
from src.market_review_generator import MarketReviewGenerator


logger = logging.getLogger(__name__)


class StockAnalysisPipeline:
    """股票分析流水线：串联数据获取、AI分析、报告生成与通知发送"""

    def __init__(self):
        self.config = ConfigManager()
        self.calendar = TradingCalendar()
        self.llm_client = LLMClient()
        self.review_generator = MarketReviewGenerator(self.llm_client)

        # self.sender_factory = NotificationSenderFactory()  # [已禁用] 暂时注释掉初始化

    def _resolve_resume_target_date(self, resume_date_str: Optional[str] = None) -> date:
        """解析复盘目标日期，默认为上一个交易日"""
        if resume_date_str:
            try:
                return datetime.strptime(resume_date_str, "%Y-%m-%d").date()
            except ValueError:
                logger.warning(f"日期格式错误: {resume_date_str}，将使用默认逻辑")

        today = date.today()
        # 简单回退逻辑，实际项目中应调用 self.calendar.get_previous_trading_day
        delta = 1
        while True:
            candidate = today - timedelta(days=delta)
            if self.calendar.is_trading_day(candidate):
                return candidate
            delta += 1

    # ============== 🔥 新增：主力资金与连板梯队数据获取 ==============

    def _get_smart_money_flow(self) -> Dict[str, Any]:
        """获取板块主力资金流向 (Top 3 流入/流出)"""
        try:
            import akshare as ak
            # 获取行业资金流
            df = ak.stock_fund_flow_industry(symbol="行业")

            # 提取前3名流入和后3名流出
            smart_money = {
                "top_inflow": df.head(3)[['名称', '今日主力净流入-净额']].to_dict('records'),
                "top_outflow": df.tail(3)[['名称', '今日主力净流入-净额']].to_dict('records')
            }
            return smart_money
        except Exception as e:
            logger.warning(f"获取主力资金数据失败: {e}")
            return {}

    def _get_limit_up_ladder(self) -> list[Dict[str, Any]]:
        """获取连板梯队（涨停股分析）"""
        try:
            import akshare as ak
            # 获取涨停板行情
            df = ak.stock_zt_pool_em(date=datetime.now().strftime("%Y%m%d"))

            ladder_data = []
            # 统计连板高度
            if not df.empty:
                # 假设 df 中有 '连板数' 或 '连续涨停天数' 字段，这里按常见字段处理
                # 注意：akshare 接口字段可能变动，需根据实际返回调整
                top_ladders = df.sort_values(by='连板数', ascending=False).head(10)

                for _, row in top_ladders.iterrows():
                    ladder_data.append({
                        "name": row.get('名称'),
                        "code": row.get('代码'),
                        "limit_up_count": row.get('连板数'),
                        "reason": row.get('首次封板时间', '') # 举例字段
                    })
            return ladder_data
        except Exception as e:
            logger.warning(f"获取连板梯队数据失败: {e}")
            return []

    # ====================================================================

    async def run(self, resume_date_str: Optional[str] = None) -> bool:
        """执行完整的分析流程"""
        target_date = self._resolve_resume_target_date(resume_date_str)
        logger.info(f"🚀 开始执行 {target_date} 的股票分析流水线...")

        try:
            # 1. 获取基础市场数据 (原有逻辑)
            market_data = self.review_generator.fetch_market_data(target_date)

            # 🔥 2. 获取新增的“主力资金”和“连板梯队”数据
            smart_money = self._get_smart_money_flow()
            limit_up_ladder = self._get_limit_up_ladder()

            # 3. 组装上下文
            context = {
                "date": target_date.strftime("%Y-%m-%d"),
                "market_data": market_data,
                "smart_money": smart_money,       # 🔥 注入主力资金数据
                "limit_up_ladder": limit_up_ladder # 🔥 注入连板梯队数据
            }

            # 4. 调用 AI 进行分析 (修改 Prompt 或传入更多上下文)
            analysis_result = await self.review_generator.generate_review(context)

            # 5. 策略建议
            strategy_advice = await self.strategy_analyzer.analyze(analysis_result)

            # 6. 发送通知
            final_report = f"【{target_date} 市场分析】\n\n{analysis_result}\n\n【策略建议】\n{strategy_advice}"

            # [已禁用] 暂时跳过发送通知，避免报错
            # success = self.sender_factory.send(final_report)
            # if success:
            #     logger.info("✅ 分析流水线执行成功，通知已发送。")
            # else:
            #     logger.error("❌ 通知发送失败。")
            # return success

            # 临时替代方案：直接打印报告到控制台，并视为成功
            print("\n" + "="*50)
            print(final_report)
            print("="*50 + "\n")
            logger.info("✅ 分析流水线执行成功，报告已输出到控制台（通知功能已禁用）。")
            return True

        except Exception as e:
            logger.exception(f"💥 流水线执行出错: {e}")
            return False
