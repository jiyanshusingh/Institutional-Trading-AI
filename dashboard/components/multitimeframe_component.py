import streamlit as st


def show_multitimeframe(mtf_result):
    st.subheader("🕒 Multi-Timeframe Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("15 Minute", mtf_result.get("15m", "Unavailable"))

    with col2:
        st.metric("1 Hour", mtf_result.get("1h", "Unavailable"))

    with col3:
        st.metric("Daily", mtf_result.get("1d", "Unavailable"))