import streamlit as st


def show_indicators(indicators):

    st.subheader("Technical Indicators")

    col1, col2, col3 = st.columns(3)

    keys = list(indicators.keys())

    for i, key in enumerate(keys):

        if i % 3 == 0:
            with col1:
                st.metric(key, indicators[key])

        elif i % 3 == 1:
            with col2:
                st.metric(key, indicators[key])

        else:
            with col3:
                st.metric(key, indicators[key])