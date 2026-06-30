import streamlit as st
from utils.chart import create_chart


def show_chart(df):
    st.subheader("📈 Price Chart")

    fig = create_chart(df)

    st.plotly_chart(
        fig,
        width="stretch"
    )