import streamlit as st


def show_smc(latest):
    st.subheader("🏦 Smart Money Concepts")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Bullish BOS :", latest["Bullish_BOS"])
        st.write("Bearish BOS :", latest["Bearish_BOS"])
        st.write("Bullish CHOCH :", latest["Bullish_CHOCH"])
        st.write("Bearish CHOCH :", latest["Bearish_CHOCH"])

    with col2:
        st.write("Buy Side Liquidity :", latest["Buy_Side_Liquidity"])
        st.write("Sell Side Liquidity :", latest["Sell_Side_Liquidity"])
        st.write("Premium Zone :", latest["Premium_Zone"])
        st.write("Discount Zone :", latest["Discount_Zone"])