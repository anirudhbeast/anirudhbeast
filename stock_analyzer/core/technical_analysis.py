from __future__ import annotations

import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, SMAIndicator
from ta.volatility import BollingerBands


class TechnicalAnalyzer:
    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        data["sma_20"] = SMAIndicator(close=data["close"], window=20).sma_indicator()
        data["sma_50"] = SMAIndicator(close=data["close"], window=50).sma_indicator()
        data["ema_12"] = EMAIndicator(close=data["close"], window=12).ema_indicator()
        data["ema_26"] = EMAIndicator(close=data["close"], window=26).ema_indicator()

        macd = MACD(close=data["close"], window_slow=26, window_fast=12, window_sign=9)
        data["macd"] = macd.macd()
        data["macd_signal"] = macd.macd_signal()

        data["rsi"] = RSIIndicator(close=data["close"], window=14).rsi()

        bb = BollingerBands(close=data["close"], window=20, window_dev=2)
        data["bb_high"] = bb.bollinger_hband()
        data["bb_low"] = bb.bollinger_lband()

        data["vol_sma_20"] = data["volume"].rolling(20).mean()
        data["support"] = data["low"].rolling(20).min()
        data["resistance"] = data["high"].rolling(20).max()

        data["bullish_engulfing"] = (
            (data["close"] > data["open"]) &
            (data["close"].shift(1) < data["open"].shift(1)) &
            (data["close"] > data["open"].shift(1)) &
            (data["open"] < data["close"].shift(1))
        )
        return data.dropna()

    def score(self, df: pd.DataFrame) -> dict:
        latest = df.iloc[-1]
        bullish_conditions = [
            latest["sma_20"] > latest["sma_50"],
            latest["macd"] > latest["macd_signal"],
            45 < latest["rsi"] < 70,
            latest["volume"] > latest["vol_sma_20"],
            latest["close"] > latest["support"],
        ]
        bearish_conditions = [
            latest["sma_20"] < latest["sma_50"],
            latest["macd"] < latest["macd_signal"],
            latest["rsi"] > 70,
            latest["close"] < latest["support"],
        ]

        bull_score = sum(bool(x) for x in bullish_conditions) / len(bullish_conditions)
        bear_score = sum(bool(x) for x in bearish_conditions) / len(bearish_conditions)
        label = "Bullish" if bull_score > bear_score else "Bearish"
        return {"label": label, "score": max(bull_score, bear_score), "latest": latest.to_dict()}
