import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from engines.scanner_engine import ScannerEngine
from data.stocks import NSE_STOCKS
from utils.chart import create_chart
from services.analysis_service import analyze_stock
from engines.multitimeframe_engine import MultiTimeframeEngine
st.set_page_config(
    page_title="Institutional Trading AI",
    layout="wide"
)

st.title("📈 Institutional Trading AI")
st.write("Institutional Grade Stock Analysis")

symbol = st.text_input(
    "Enter NSE Symbol",
    value="MARICO.NS"
)
if st.button("Scan NSE Stocks"):
    scanner = ScannerEngine()

    results = scanner.scan(NSE_STOCKS)

    st.dataframe(results)
if st.button("Analyze Stock"):

    result = analyze_stock(symbol)
    df = result["df"]

    fig = create_chart(df)

    st.subheader("📈 Price Chart")

    st.plotly_chart(fig, use_container_width=True)

    signal = result["signal"]
    trade = result["risk"]
    prob = result["probability"]
    confluence = result["confluence"]
    rating = result["rating"]
    mtf = MultiTimeframeEngine()
    mtf_result = mtf.analyze(symbol)

    st.success(f"Analysis Completed for {symbol}")
    st.subheader("⭐ Institutional Rating")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rating", rating["Rating"])

    with col2:
        st.metric("Stars", rating["Stars"])

    with col3:
        st.metric("AI Score", rating["Score"])

    st.subheader("📊 Signal")

    st.metric("Signal", signal["Signal"])
    st.metric("Score", signal["Score"])

    st.subheader("Reasons")

    for reason in signal["Reasons"]:
        st.write("✅", reason)

    st.subheader("Trade Setup")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Entry", trade["Entry"])
        st.metric("Stop Loss", trade["StopLoss"])

    with col2:
        st.metric("Target 1", trade["Target1"])
        st.metric("Target 2", trade["Target2"])

    st.metric("Risk Reward", f'{trade["RR"]}:1')
    st.subheader("🎯 Institutional Confluence")

    st.metric(
        "Confluence Score",
        f'{confluence["ConfluenceScore"]}/100'
    )

    st.write("Reasons")

    for reason in confluence["Reasons"]:
        st.write("✅", reason)
        
    st.subheader("🕒 Multi-Timeframe Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("15 Minute", mtf_result["15m"])

    with col2:
        st.metric("1 Hour", mtf_result["1h"])

    with col3:
        st.metric("Daily", mtf_result["1d"])
    st.subheader("📈 Technical Indicators")

    latest = df.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("EMA20", round(latest["EMA20"], 2))
        st.metric("EMA50", round(latest["EMA50"], 2))

    with col2:
        st.metric("EMA200", round(latest["EMA200"], 2))
        st.metric("RSI", round(latest["RSI"], 2))

    with col3:
        st.metric("MACD", round(latest["MACD"], 2))
        
    st.subheader("🏦 Smart Money Concepts")

    latest = df.iloc[-1]

    st.write("Bullish BOS :", latest["Bullish_BOS"])
    st.write("Bearish BOS :", latest["Bearish_BOS"])
    st.write("Bullish CHOCH :", latest["Bullish_CHOCH"])
    st.write("Bearish CHOCH :", latest["Bearish_CHOCH"])
    st.write("Buy Side Liquidity :", latest["Buy_Side_Liquidity"])
    st.write("Sell Side Liquidity :", latest["Sell_Side_Liquidity"])
    st.write("Premium Zone :", latest["Premium_Zone"])
    st.write("Discount Zone :", latest["Discount_Zone"])
    
    st.subheader("🤖 AI Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Probability",
            f'{prob["Probability"]}%'
        )

        st.metric(
            "Confidence",
            prob["Confidence"]
        )

        st.metric(
            "Trend",
            prob["Trend"]
        )

    with col2:

        st.metric(
            "Momentum",
            prob["Momentum"]
        )

        st.metric(
            "Institutional Bias",
            prob["InstitutionalBias"]
        )

        st.metric(
            "Recommendation",
            prob["Recommendation"]
        )
