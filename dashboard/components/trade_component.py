import streamlit as st


def show_trade(trade):
    st.subheader("Trade Setup")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Entry", trade["Entry"])
        st.metric("Stop Loss", trade["StopLoss"])

    with col2:
        st.metric("Target 1", trade["Target1"])
        st.metric("Target 2", trade["Target2"])

    st.metric("Risk Reward", f'{trade["RR"]}:1')