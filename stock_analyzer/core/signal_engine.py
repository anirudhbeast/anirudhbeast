from __future__ import annotations

from stock_analyzer.core.risk_management import risk_reward


class SignalEngine:
    def generate(
        self,
        current_price: float,
        technical: dict,
        fundamental: dict,
        sentiment: dict,
        ml: dict,
    ) -> dict:
        labels = [technical["label"], fundamental["label"], sentiment["label"], ml["label"]]

        bullish_votes = sum(1 for label in labels if label == "Bullish")
        bearish_votes = sum(1 for label in labels if label == "Bearish")

        confidence = (
            technical["score"] * 0.35
            + fundamental["score"] * 0.25
            + (sentiment["score"] + 1) / 2 * 0.15
            + ml["score"] * 0.25
        )

        action = "HOLD"
        if bullish_votes >= 3 and confidence > 0.80:
            action = "BUY"
        elif bearish_votes >= 3 and confidence > 0.80:
            action = "SELL"

        stop_loss = current_price * (0.97 if action == "BUY" else 1.03)
        target = current_price * (1.06 if action == "BUY" else 0.94)

        return {
            "action": action,
            "confidence": round(float(confidence), 4),
            "entry": round(current_price, 2),
            "stop_loss": round(stop_loss, 2),
            "target": round(target, 2),
            "risk_reward": round(risk_reward(current_price, stop_loss, target), 2),
            "votes": {"bullish": bullish_votes, "bearish": bearish_votes},
        }
