import streamlit as st


def show_ai(prob):
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