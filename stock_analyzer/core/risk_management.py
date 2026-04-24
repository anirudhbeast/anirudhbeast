from __future__ import annotations


def position_size(account_value: float, risk_per_trade: float, entry: float, stop: float) -> int:
    risk_amount = account_value * risk_per_trade
    per_share_risk = abs(entry - stop)
    if per_share_risk <= 0:
        return 0
    return max(int(risk_amount / per_share_risk), 0)


def risk_reward(entry: float, stop: float, target: float) -> float:
    risk = abs(entry - stop)
    reward = abs(target - entry)
    if risk == 0:
        return 0.0
    return reward / risk
