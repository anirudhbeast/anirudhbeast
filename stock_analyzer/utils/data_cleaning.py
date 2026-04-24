from __future__ import annotations

import pandas as pd


def clean_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned[~cleaned.index.duplicated(keep="last")]
    cleaned = cleaned.sort_index()
    cleaned = cleaned.ffill().dropna()
    return cleaned
