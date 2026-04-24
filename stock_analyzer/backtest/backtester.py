from __future__ import annotations

import numpy as np
import pandas as pd


class Backtester:
    def run(self, df: pd.DataFrame) -> dict:
        bt = df.copy()
        bt["returns"] = bt["close"].pct_change().fillna(0)
        bt["signal"] = np.where((bt["sma_20"] > bt["sma_50"]) & (bt["rsi"] > 45) & (bt["macd"] > bt["macd_signal"]), 1, 0)
        bt["strategy_returns"] = bt["signal"].shift(1).fillna(0) * bt["returns"]
        bt["equity"] = (1 + bt["strategy_returns"]).cumprod()

        trades = bt[bt["signal"].diff() != 0]
        wins = (trades["strategy_returns"] > 0).sum()
        total = len(trades) if len(trades) else 1

        equity = bt["equity"]
        peak = equity.cummax()
        drawdown = (equity / peak - 1).min()

        periods_per_year = 252
        cagr = equity.iloc[-1] ** (periods_per_year / max(len(bt), 1)) - 1
        sharpe = 0.0
        if bt["strategy_returns"].std() > 0:
            sharpe = (bt["strategy_returns"].mean() / bt["strategy_returns"].std()) * np.sqrt(periods_per_year)

        return {
            "win_rate": round(float(wins / total), 4),
            "max_drawdown": round(float(drawdown), 4),
            "cagr": round(float(cagr), 4),
            "sharpe": round(float(sharpe), 4),
        }
