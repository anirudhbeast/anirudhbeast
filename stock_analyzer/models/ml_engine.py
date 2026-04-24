from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


FEATURES = [
    "sma_20",
    "sma_50",
    "ema_12",
    "ema_26",
    "macd",
    "macd_signal",
    "rsi",
    "bb_high",
    "bb_low",
    "volume",
]


class MLEngine:
    def train_random_forest(self, df: pd.DataFrame) -> dict:
        dataset = df.copy()
        dataset["target"] = (dataset["close"].shift(-1) > dataset["close"]).astype(int)
        dataset = dataset.dropna()

        X = dataset[FEATURES]
        y = dataset["target"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        model = RandomForestClassifier(n_estimators=300, max_depth=7, random_state=42)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds) if len(y_test) else 0.0
        last_prob_up = float(model.predict_proba(X.iloc[[-1]])[0][1])

        return {
            "model": model,
            "accuracy": acc,
            "prob_up": last_prob_up,
            "label": "Bullish" if last_prob_up >= 0.5 else "Bearish",
            "score": max(last_prob_up, 1 - last_prob_up),
        }
