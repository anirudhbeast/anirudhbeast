from __future__ import annotations

from stock_analyzer.backtest.backtester import Backtester
from stock_analyzer.core.fundamental_analysis import FundamentalAnalyzer
from stock_analyzer.core.signal_engine import SignalEngine
from stock_analyzer.core.technical_analysis import TechnicalAnalyzer
from stock_analyzer.data.fundamental_data import FundamentalDataClient
from stock_analyzer.data.market_data import MarketDataClient
from stock_analyzer.data.sentiment_data import SentimentClient
from stock_analyzer.models.ml_engine import MLEngine
from stock_analyzer.utils.data_cleaning import clean_ohlcv


class AnalyzerService:
    def __init__(self) -> None:
        self.market = MarketDataClient()
        self.fundamentals = FundamentalDataClient()
        self.sentiment = SentimentClient()
        self.ta = TechnicalAnalyzer()
        self.fa = FundamentalAnalyzer()
        self.ml = MLEngine()
        self.signal_engine = SignalEngine()
        self.backtester = Backtester()

    def analyze(self, symbol: str, period: str = "1y", interval: str = "1d") -> dict:
        ohlcv = self.market.get_ohlcv(symbol, period=period, interval=interval)
        ohlcv = clean_ohlcv(ohlcv)
        enriched = self.ta.enrich(ohlcv)

        technical = self.ta.score(enriched)
        fundamental_snapshot = self.fundamentals.get_fundamental_snapshot(symbol)
        fundamental = self.fa.score(fundamental_snapshot)
        fair_value = self.fa.intrinsic_value_simple(fundamental_snapshot)
        sentiment = self.sentiment.score(symbol)
        ml_result = self.ml.train_random_forest(enriched)

        current_price = float(enriched.iloc[-1]["close"])
        signal = self.signal_engine.generate(
            current_price=current_price,
            technical=technical,
            fundamental=fundamental,
            sentiment=sentiment,
            ml=ml_result,
        )
        backtest = self.backtester.run(enriched)

        return {
            "symbol": symbol,
            "ohlcv": enriched,
            "technical": technical,
            "fundamental": fundamental,
            "fundamental_snapshot": fundamental_snapshot,
            "intrinsic_value": fair_value,
            "sentiment": sentiment,
            "ml": {k: v for k, v in ml_result.items() if k != "model"},
            "signal": signal,
            "backtest": backtest,
        }
