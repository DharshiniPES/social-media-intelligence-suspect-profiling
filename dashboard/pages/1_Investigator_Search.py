import streamlit as st
import pandas as pd

from pipeline.search_pipeline import SearchPipeline
from pipeline.ranking_pipeline import RankingPipeline
from pipeline.normalizer import normalize_instagram
from modules.scrapers.instagram_collector import InstagramCollector

st.set_page_config(
    page_title="Investigator Search",
    layout="wide"
)

st.title("Investigator Search")

st.caption(
    "Adaptive Explainable Cross-Platform Identity Attribution"
)

st.divider()

username = st.text_input(
    "Target Username",
    placeholder="Enter username..."
)

col1, col2, col3 = st.columns(3)

with col1:
    instagram = st.checkbox("Instagram", value=True)

with col2:
    github = st.checkbox("GitHub", value=True)

with col3:
    website = st.checkbox("Website", value=True)

if st.button("🚀 Start Investigation", use_container_width=True):

    if username.strip() == "":
        st.error("Enter a username.")
        st.stop()

    platforms = []

    if instagram:
        platforms.append("Instagram")

    if github:
        platforms.append("GitHub")

    if website:
        platforms.append("Website")

    with st.spinner("Collecting OSINT..."):

        target_raw = InstagramCollector().scrape(username)

        target = normalize_instagram(target_raw)

        candidates = SearchPipeline.search(
            username,
            platforms
        )

        results = RankingPipeline.rank(
            target,
            candidates
        )

    st.session_state["results"] = results
    st.session_state["target"] = username

    st.success("Investigation Complete!")