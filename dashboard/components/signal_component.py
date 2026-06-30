import streamlit as st


def show_signal(signal):

    st.subheader("📊 Signal")

    st.metric("Signal", signal["Signal"])
    st.metric("Score", signal["Score"])

    st.subheader("Reasons")

    for reason in signal["Reasons"]:
        st.write("✅", reason)