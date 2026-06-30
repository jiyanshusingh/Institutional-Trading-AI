import streamlit as st


def show_rating(rating):
    st.subheader("⭐ Institutional Rating")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rating", rating["Rating"])

    with col2:
        st.metric("Stars", rating["Stars"])

    with col3:
        st.metric("AI Score", rating["Score"])