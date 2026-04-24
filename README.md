# Institutional Stock Market Analyzer

A production-style multi-factor stock analysis platform combining:
- Real-time + historical market data
- Technical indicators
- Fundamental scoring
- NLP sentiment analysis
- Machine-learning probability forecasts
- Backtesting and risk management
- Streamlit dashboard and alerting

> **Important**: This project is for research/education and is **not financial advice**.

## 1) Project Structure

```text
stock_analyzer/
├── app/
│   └── streamlit_app.py          # UI dashboard (charts, signals, alerts)
├── alerts/
│   └── notifier.py               # Email + Telegram alerts
├── backtest/
│   └── backtester.py             # Strategy performance metrics
├── config/
│   └── settings.py               # Environment-based secrets/config
├── core/
│   ├── analyzer_service.py       # End-to-end orchestration
│   ├── fundamental_analysis.py   # Fundamental scoring + intrinsic value
│   ├── risk_management.py        # Position sizing + RR
│   ├── signal_engine.py          # Multi-factor signal confirmation
│   └── technical_analysis.py     # Indicator and pattern logic
├── data/
│   ├── fundamental_data.py       # Financial statements + ratios
│   ├── macro_data.py             # FRED macro indicators
│   ├── market_data.py            # OHLCV + quote fetch
│   └── sentiment_data.py         # News feed + VADER scoring
├── models/
│   └── ml_engine.py              # RandomForest movement classifier
└── utils/
    └── data_cleaning.py          # Cleaning and normalization

tests/
└── test_risk_management.py

main.py                            # Streamlit entrypoint helper
requirements.txt
```

## 2) Features Delivered

### Data integration
- **Market**: Yahoo Finance (historical + near real-time quote)
- **Fundamentals**: ratios + financial statements via Yahoo Finance
- **Sentiment**: Google News RSS + NLP sentiment scoring via VADER
- **Macro**: FRED API support (inflation, Fed funds, GDP)
- Includes missing data handling and forward-fill cleanup.

### Analysis engine
- **Technical**: SMA/EMA, RSI, MACD, Bollinger Bands, volume trend, support/resistance, bullish engulfing pattern.
- **Fundamental**: P/E, P/B, ROE, Debt/Equity, growth factors + simple intrinsic valuation.
- **Sentiment**: Bullish/Bearish/Neutral from title sentiment.
- **AI/ML**: RandomForest movement probability and confidence.

### Signal generation
- Emits `BUY` / `SELL` / `HOLD` only when multi-factor votes align and confidence exceeds 80%.
- Returns entry, stop-loss, target, risk-reward ratio.

### Backtesting
- Reports win rate, max drawdown, CAGR, Sharpe ratio.

### Dashboard
- Streamlit UI with:
  - candlestick + indicator overlays,
  - signal and confidence cards,
  - backtest panel,
  - sentiment article feed,
  - risk-based position sizing,
  - alert triggers.

### Alerts
- Telegram notifications
- Email notifications (SMTP)

## 3) Setup Instructions

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run app:

```bash
streamlit run stock_analyzer/app/streamlit_app.py
```

## 4) Required Libraries

All dependencies are listed in `requirements.txt`. Key packages:
- `streamlit`, `plotly`
- `pandas`, `numpy`
- `yfinance`, `ta`
- `scikit-learn`, `xgboost` (ready for extension)
- `vaderSentiment`, `feedparser`
- `requests`, `python-dotenv`

## 5) API Integration Guide

Create a `.env` file in repo root:

```env
# Optional market/fundamental extension keys
ALPHA_VANTAGE_API_KEY=

# Macro data
FRED_API_KEY=

# News API (optional if you want to extend beyond RSS)
NEWS_API_KEY=

# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Email SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=app-password
ALERT_EMAIL_TO=receiver@email.com
```

### Adding more data providers
- Add a provider client under `stock_analyzer/data/`.
- Normalize columns to `open/high/low/close/volume`.
- Plug into `AnalyzerService`.

## 6) Performance and Scalability Notes
- Cache API responses at service layer (recommended Redis/TTL cache for production).
- Batch symbol downloads and async requests for multi-asset watchlists.
- Add websocket ingestion for true tick-level real-time streams.

## 7) Risk Management Included
- Position sizing based on account value and max risk/trade (default 1%).
- Structured stop-loss/target and risk-reward calculations.
- Easy extension to enforce portfolio-level diversification constraints.

## 8) Future Institutional Upgrades
- Replace RSS sentiment with event-level transformer model.
- Add walk-forward validation and regime detection.
- Add ensemble (LSTM + XGBoost + RF).
- Integrate broker APIs for execution and paper trading.
