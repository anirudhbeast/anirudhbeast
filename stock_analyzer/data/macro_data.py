from __future__ import annotations

import requests


class MacroDataClient:
    FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key

    def _fetch_fred_latest(self, series_id: str) -> float | None:
        if not self.api_key:
            return None
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 1,
        }
        response = requests.get(self.FRED_BASE, params=params, timeout=15)
        response.raise_for_status()
        observations = response.json().get("observations", [])
        if not observations:
            return None
        value = observations[0].get("value")
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def snapshot(self) -> dict:
        return {
            "inflation_cpi_yoy": self._fetch_fred_latest("CPIAUCSL"),
            "fed_funds_rate": self._fetch_fred_latest("FEDFUNDS"),
            "gdp": self._fetch_fred_latest("GDP"),
        }
