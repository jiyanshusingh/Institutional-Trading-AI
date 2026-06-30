import streamlit as st


def show_confluence(confluence):
    st.subheader("🎯 Institutional Confluence")

    st.metric(
        "Confluence Score",
        f'{confluence["ConfluenceScore"]}/100'
    )

    st.write("Reasons")

    for reason in confluence["Reasons"]:
        st.write("✅", reason)