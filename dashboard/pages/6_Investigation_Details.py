import streamlit as st

st.set_page_config(
    page_title="Investigation Details",
    layout="wide"
)

st.title("Investigation Report")

st.divider()
st.subheader("Investigation Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Target",
        "nasa"
    )

with col2:
    st.metric(
        "Matched Candidate",
        "NASA (GitHub)"
    )

with col3:
    st.metric(
        "Confidence",
        "92%"
    )
st.divider()

st.success(
    """
### HIGH CONFIDENCE MATCH

The candidate demonstrates strong identity consistency across
multiple forensic signals.

Manual verification is recommended before final attribution.
"""
)
st.subheader("Evidence Breakdown")

st.write("Username Similarity")
st.progress(0.98)
st.caption("98%")

st.write("Bio Similarity")
st.progress(0.86)
st.caption("86%")

st.write("Stylometry")
st.progress(0.91)
st.caption("91%")

st.write("Behaviour")
st.progress(0.82)
st.caption("82%")

st.write("Temporal")
st.progress(0.73)
st.caption("73%")

st.write("Hyperlinks")
st.progress(0.25)
st.caption("25%")
st.divider()

st.subheader("Explainability")

st.info("""
✔ Username is highly similar.

✔ Bio contains similar keywords.

✔ Behavioural fingerprint is consistent.

⚠ Hyperlink evidence is weak.

Overall confidence remains HIGH due to strong multimodal evidence.
""")
st.divider()

st.subheader("Investigator Recommendation")

st.warning("""
Recommended Actions

• Review linked repositories

• Verify hyperlinks manually

• Inspect network graph

• Review timeline consistency

• Export investigation report
""")