import streamlit as st
from dotenv import load_dotenv
import os
import requests
from io import BytesIO
from modules.scrapers.creatorcrawl_instagram import CreatorCrawlInstagram
from dashboard.instagram_intelligence import InstagramIntelligence

from pipeline.normalizer import normalize_instagram
from pipeline.comparison_engine import ComparisonEngine

def display_profile_card(profile, title):

    st.subheader(title)

    # -----------------------------
    # Profile Picture
    # -----------------------------

    image_url = profile.get("profile_picture")

    if image_url:

        try:

            response = requests.get(
                image_url,
                timeout=15,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code == 200:

                st.image(
                    BytesIO(response.content),
                    width=180
                )

        except Exception:
            st.warning("Unable to load profile image.")

    # -----------------------------
    # Basic Information
    # -----------------------------

    st.write(f"**Username:** {profile.get('username','')}")

    st.write(f"**Display Name:** {profile.get('display_name','')}")

    verified = "✅ Verified" if profile.get("verified") else "❌ Not Verified"

    st.write(f"**Status:** {verified}")

    st.write(f"**Followers:** {profile.get('followers',0):,}")

    st.write(f"**Following:** {profile.get('following',0):,}")

    st.write(f"**Posts:** {profile.get('posts_count',0)}")

    st.write("**Bio**")

    st.info(profile.get("bio","No bio available"))
def show_profile_comparison():

    st.title("Profile Comparison")

    st.caption(
        "Compare two Instagram profiles using the forensic evidence pipeline."
    )

    col1, col2 = st.columns(2)

    with col1:
        username1 = st.text_input(
            "Instagram Profile A",
            placeholder="e.g. nasa"
        )

    with col2:
        username2 = st.text_input(
            "Instagram Profile B",
            placeholder="e.g. natgeo"
        )

    compare = st.button(
        "Compare Profiles",
        use_container_width=True
    )

    if not compare:
        return

    if not username1 or not username2:
        st.warning("Please enter both usernames.")
        return

    load_dotenv()

    api_key = os.getenv("CREATORCRAWL_API_KEY")

    scraper = CreatorCrawlInstagram(api_key)

    # -------------------------------------------------
    # Collect Profile A
    # -------------------------------------------------

    with st.spinner("Collecting Profile A..."):

        profile1 = scraper.scrape(username1)

        profile1 = InstagramIntelligence().analyze(profile1)

        evidence1 = normalize_instagram(profile1)

    # -------------------------------------------------
    # Collect Profile B
    # -------------------------------------------------

    with st.spinner("Collecting Profile B..."):

        profile2 = scraper.scrape(username2)

        profile2 = InstagramIntelligence().analyze(profile2)

        evidence2 = normalize_instagram(profile2)

    # -------------------------------------------------
    # Compare
    # -------------------------------------------------

    with st.spinner("Running forensic comparison..."):

        results = ComparisonEngine.compare(
            evidence1,
            evidence2
        )

    st.success("Comparison Complete")

    st.divider()

    st.subheader("Forensic Module Scores")

    left, right = st.columns(2)

    with left:

        st.metric(
            "Username Similarity",
            f"{results['username_score']:.3f}"
        )

        st.metric(
            "Bio Similarity",
            f"{results['bio_score']:.3f}"
        )

        st.metric(
            "Stylometry",
            f"{results['stylometry_score']:.3f}"
        )

        st.metric(
            "Emoji Similarity",
            f"{results['emoji_score']:.3f}"
        )

    with right:

        st.metric(
            "Behaviour",
            f"{results['behaviour_score']:.3f}"
        )

        st.metric(
            "Temporal",
            f"{results['temporal_score']:.3f}"
        )

        st.metric(
            "Hyperlink",
            f"{results['hyperlink_score']:.3f}"
        )

        st.metric(
            "Hashtag",
            f"{results['hashtag_score']:.3f}"
        )
    st.divider()

    st.subheader("Final Fusion Score")

    fusion = results["fusion_score"]

    st.metric(
        "Fusion Score",
        f"{fusion:.3f}"
    )
    if fusion >= 0.90:

        st.success("Identity Match")

    elif fusion >= 0.75:

        st.success("Strong Identity Similarity")

    elif fusion >= 0.60:

        st.info("Operationally Related")

    elif fusion >= 0.40:

        st.warning("Some Shared Characteristics")

    else:

        st.error("No Significant Relationship")

    st.divider()

    st.subheader("Explainability")

    for reason in results["explanation"]:

        st.write("•", reason)

    st.divider()

    left, right = st.columns(2)

    with left:

        display_profile_card(
            profile1,
            "Profile A"
        )

    with right:

        display_profile_card(
            profile2,
            "Profile B"
        )