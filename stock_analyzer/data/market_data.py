from __future__ import annotations

from datetime import datetime
import pandas as pd
import yfinance as yf


class MarketDataClient:
    """Fetches historical and near-real-time market data."""

    def get_ohlcv(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval, auto_adjust=False)
        if df.empty:
            raise ValueError(f"No OHLCV data returned for {symbol}.")
        df = df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )
        df.index = pd.to_datetime(df.index)
        return df[["open", "high", "low", "close", "volume"]].dropna()

    def get_realtime_quote(self, symbol: str) -> dict:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        return {
            "symbol": symbol,
            "last_price": float(info.get("last_price") or 0),
            "bid": float(info.get("bid") or 0),
            "ask": float(info.get("ask") or 0),
            "timestamp": datetime.utcnow().isoformat(),
        }
