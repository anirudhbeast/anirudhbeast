from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from stock_analyzer.alerts.notifier import AlertNotifier
from stock_analyzer.config.settings import settings
from stock_analyzer.core.analyzer_service import AnalyzerService
from stock_analyzer.core.risk_management import position_size


st.set_page_config(page_title="Institutional Stock Analyzer", layout="wide")
st.title("📈 Institutional-Grade Stock Market Analyzer")

service = AnalyzerService()
notifier = AlertNotifier()

with st.sidebar:
    st.header("Configuration")
    symbol = st.text_input("Ticker", value="AAPL").upper().strip()
    period = st.selectbox("Lookback", ["6mo", "1y", "2y", "5y"], index=1)
    interval = st.selectbox("Interval", ["1d", "1h"], index=0)
    account_value = st.number_input("Portfolio Value ($)", value=100000.0, step=1000.0)
    risk_pct = st.slider("Max Risk Per Trade", 0.005, 0.03, 0.01, 0.005)

if st.button("Run Analysis", type="primary"):
    result = service.analyze(symbol=symbol, period=period, interval=interval)
    df: pd.DataFrame = result["ohlcv"]

    col1, col2, col3, col4 = st.columns(4)
    signal = result["signal"]

    col1.metric("Signal", signal["action"])
    col2.metric("Confidence", f"{signal['confidence'] * 100:.1f}%")
    col3.metric("Entry", f"${signal['entry']:.2f}")
    col4.metric("Risk/Reward", f"{signal['risk_reward']:.2f}")

    shares = position_size(account_value, risk_pct, signal["entry"], signal["stop_loss"])
    st.info(f"Suggested position size: **{shares} shares** at {risk_pct:.2%} risk budget.")

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="OHLC",
            ),
            go.Scatter(x=df.index, y=df["sma_20"], mode="lines", name="SMA 20"),
            go.Scatter(x=df.index, y=df["sma_50"], mode="lines", name="SMA 50"),
        ]
    )
    fig.update_layout(height=550, xaxis_rangeslider_visible=False, title=f"{symbol} Chart + Indicators")
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Module Scores")
        st.json(
            {
                "technical": result["technical"],
                "fundamental": result["fundamental"],
                "sentiment": {
                    "label": result["sentiment"]["label"],
                    "score": round(result["sentiment"]["score"], 4),
                },
                "ml": result["ml"],
            }
        )

        st.subheader("Backtest")
        st.json(result["backtest"])

    with right:
        st.subheader("Trade Plan")
        st.write(
            {
                "action": signal["action"],
                "entry": signal["entry"],
                "stop_loss": signal["stop_loss"],
                "target": signal["target"],
            }
        )
        st.subheader("Fundamental Snapshot")
        st.write(result["fundamental_snapshot"])
        st.write({"intrinsic_value_estimate": result["intrinsic_value"]})

        st.subheader("Latest News (Sentiment Feed)")
        for article in result["sentiment"]["articles"][:10]:
            st.markdown(f"- [{article['title']}]({article['link']})")

    alert_text = (
        f"{symbol} | {signal['action']} | confidence={signal['confidence']:.2f} | "
        f"entry={signal['entry']} stop={signal['stop_loss']} target={signal['target']}"
    )
    if st.checkbox("Send Telegram alert"):
        notifier.send_telegram(settings.telegram_bot_token, settings.telegram_chat_id, alert_text)
        st.success("Telegram alert attempted.")

    if st.checkbox("Send email alert"):
        notifier.send_email(
            settings.smtp_host,
            settings.smtp_port,
            settings.smtp_username,
            settings.smtp_password,
            settings.alert_email_to,
            f"Signal alert: {symbol}",
            alert_text,
        )
        st.success("Email alert attempted.")
