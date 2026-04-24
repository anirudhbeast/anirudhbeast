from __future__ import annotations

import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentClient:
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def fetch_news(self, symbol: str, limit: int = 25) -> list[dict]:
        query = symbol.replace(".", "%20")
        url = f"https://news.google.com/rss/search?q={query}+stock+when:7d&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        entries = []
        for e in feed.entries[:limit]:
            entries.append({"title": e.get("title", ""), "link": e.get("link", ""), "published": e.get("published", "")})
        return entries

    def score(self, symbol: str) -> dict:
        news = self.fetch_news(symbol)
        if not news:
            return {"label": "Neutral", "score": 0.0, "articles": []}

        compound_scores = [self.analyzer.polarity_scores(item["title"])["compound"] for item in news]
        avg_score = sum(compound_scores) / len(compound_scores)

        if avg_score > 0.15:
            label = "Bullish"
        elif avg_score < -0.15:
            label = "Bearish"
        else:
            label = "Neutral"

        return {"label": label, "score": avg_score, "articles": news}
