from __future__ import annotations

import pandas as pd
import yfinance as yf


class FundamentalDataClient:
    def get_fundamental_snapshot(self, symbol: str) -> dict:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "de_ratio": info.get("debtToEquity"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "market_cap": info.get("marketCap"),
            "free_cashflow": info.get("freeCashflow"),
            "shares_outstanding": info.get("sharesOutstanding"),
        }

    def get_financial_statements(self, symbol: str) -> dict[str, pd.DataFrame]:
        ticker = yf.Ticker(symbol)
        return {
            "income_statement": ticker.financials.fillna(0),
            "balance_sheet": ticker.balance_sheet.fillna(0),
            "cash_flow": ticker.cashflow.fillna(0),
        }
