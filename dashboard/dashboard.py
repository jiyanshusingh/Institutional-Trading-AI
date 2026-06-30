import streamlit as st
from dashboard.components.chart_component import show_chart
from engines.scanner_engine import ScannerEngine
from data.stocks import NSE_STOCKS
from utils.chart import create_chart
from services.analysis_service import analyze_stock
from engines.multitimeframe_engine import MultiTimeframeEngine
from dashboard.components.signal_component import show_signal
from dashboard.components.trade_component import show_trade
from dashboard.components.indicator_component import show_indicators
from dashboard.components.smc_component import show_smc
from dashboard.components.rating_component import show_rating
from dashboard.components.confluence_component import show_confluence
from dashboard.components.multitimeframe_component import show_multitimeframe
from dashboard.components.ai_component import show_ai

def main():
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

        from services.dashboard_service import DashboardService
        service = DashboardService()
        result = service.analyze(symbol)
        st.success(f"Analysis Completed for {symbol}")

        show_chart(result["df"])

        show_rating(result["rating"])

        show_signal(result["signal"])

        show_trade(result["risk"])

        show_confluence(result["confluence"])

        show_multitimeframe(result["mtf"])

        show_indicators(result["indicators"])

        show_smc(result["df"].iloc[-1])

        show_ai(result["probability"])
        
        
