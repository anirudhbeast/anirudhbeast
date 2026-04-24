from __future__ import annotations


class FundamentalAnalyzer:
    def score(self, snapshot: dict) -> dict:
        points = 0
        checks = 0

        checks += 1
        if snapshot.get("pe") and snapshot["pe"] < 30:
            points += 1

        checks += 1
        if snapshot.get("pb") and snapshot["pb"] < 5:
            points += 1

        checks += 1
        roe = snapshot.get("roe")
        if roe and roe > 0.12:
            points += 1

        checks += 1
        de_ratio = snapshot.get("de_ratio")
        if de_ratio is not None and de_ratio < 120:
            points += 1

        checks += 1
        rg = snapshot.get("revenue_growth")
        if rg and rg > 0.05:
            points += 1

        checks += 1
        eg = snapshot.get("earnings_growth")
        if eg and eg > 0.05:
            points += 1

        score = points / checks if checks else 0
        label = "Bullish" if score >= 0.6 else "Bearish"
        return {"label": label, "score": score}

    def intrinsic_value_simple(self, snapshot: dict, discount_rate: float = 0.1, growth_rate: float = 0.04) -> float | None:
        fcf = snapshot.get("free_cashflow")
        shares = snapshot.get("shares_outstanding")
        if not fcf or not shares:
            return None
        projected = fcf * (1 + growth_rate)
        terminal_value = projected / max(discount_rate - growth_rate, 0.01)
        return terminal_value / shares
