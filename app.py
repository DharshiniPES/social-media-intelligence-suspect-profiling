import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from dashboard.live_intelligence import show_live_intelligence
from dashboard.profile_comparison import show_profile_comparison
from pipeline.search_pipeline import SearchPipeline
from pipeline.ranking_pipeline import RankingPipeline
from pipeline.normalizer import normalize_instagram
from modules.scrapers.instagram_collector import InstagramCollector
from database.candidate_repository import CandidateRepository
from modules.candidate_retrieval.retrieval_engine import CandidateRetrievalEngine
from modules.candidate_pool.pool_builder import CandidatePoolBuilder
from modules.deduplication.deduplicator import CandidateDeduplicator
page = "None"

# =====================================================
# PAGE CONFIG
# =====================================================
def safe_progress(value):
    value = float(value)

    if value < 0:
        value = 0

    if value > 1:
        value = 1

    return value
st.set_page_config(
    page_title="SOCMINT Investigation Platform",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PROFESSIONAL CSS
# =====================================================

st.markdown("""
<style>

/* -----------------------------
   GLOBAL
------------------------------*/

.main .block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    max-width:1600px;
}

/* -----------------------------
   SIDEBAR
------------------------------*/

section[data-testid="stSidebar"]{
    background:#0B1220;
}

/* -----------------------------
   METRICS
------------------------------*/

div[data-testid="metric-container"]{
    background:#111827;
    border:1px solid #263041;
    border-radius:14px;
    padding:18px;
    box-shadow:0 4px 12px rgba(0,0,0,.20);
}

/* -----------------------------
   DATAFRAMES
------------------------------*/

div[data-testid="stDataFrame"]{
    border-radius:12px;
    border:1px solid #1F2937;
}

/* -----------------------------
   BUTTONS
------------------------------*/

.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-weight:600;
}

/* -----------------------------
   INPUT BOXES
------------------------------*/

.stTextInput input{
    border-radius:10px;
}

/* -----------------------------
   EXPANDERS
------------------------------*/

.streamlit-expanderHeader{
    font-size:16px;
    font-weight:bold;
}

/* -----------------------------
   TABS
------------------------------*/

button[data-baseweb="tab"]{
    font-size:16px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# CACHE
# =====================================================

@st.cache_resource
def load_database():
    from database.db_manager import DatabaseManager
    return DatabaseManager()

@st.cache_data
def load_profiles():
    from modules.real_dataset_loader import RealDatasetLoader
    loader = RealDatasetLoader(
        "datasets/real/bot_detection_data.csv"
    )
    profiles = loader.load_profiles(limit=100)
    return profiles

db = load_database()
profiles = load_profiles()
comparisons = db.get_comparisons()
df = pd.DataFrame(profiles)

# =====================================================
# MODULE IMPORTS
# =====================================================

from modules.risk_tracker import risk_level
from modules.report_generator import generate_report, save_report
from modules.contribution_engine import get_contribution_data
from modules.pivot_analyzer import extract_advanced_pivots
from modules.scraper_collector import live_scrape_profile
from modules.multimodal_vision import extract_text_from_profile_image
from modules.vehicle_verifier import verify_and_route_vehicle

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def dashboard_metrics():
    total_profiles = len(profiles)
    total_comparisons = len(comparisons)
    linked_accounts = sum(
        1 for row in comparisons if row[13] == 1
    )
    fusion_scores = [row[11] for row in comparisons]
    average_fusion = (
        sum(fusion_scores)/len(fusion_scores)
        if fusion_scores else 0
    )
    highest_fusion = (
        max(fusion_scores)
        if fusion_scores else 0
    )
    return {
        "profiles":total_profiles,
        "comparisons":total_comparisons,
        "linked":linked_accounts,
        "avg_fusion":average_fusion,
        "highest_fusion":highest_fusion
    }

metrics = dashboard_metrics()

# =====================================================
# ENTERPRISE SIDEBAR
# =====================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        SOCMINT
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.caption("Investigator Intelligence Platform")
st.sidebar.divider()

# -------------------------
# BIFURCATED NAVIGATION ENGINE
# -------------------------
app_mode = st.sidebar.radio(
    "Select System Engine",
    [
        "Platform Overview",
        "Historical Dataset Analytics",
        "Live OSINT Ingestion & Profiling"
    ]
)

st.sidebar.divider()

if app_mode == "Historical Dataset Analytics":
    section = st.sidebar.radio(
        "Dataset Workspace",
        [
            "Executive Dashboard",
            "Investigation",
            "Analytics",
            "Reports"
        ]
    )

    if section == "Executive Dashboard":
        page = st.sidebar.radio(
            "Pages",
            [
                "Case Summary",
                "Profile Analysis",
                "Identity Linkage Results"
            ]
        )
    elif section == "Investigation":
        page = st.sidebar.radio(
            "Pages",
            [
                "Evidence Explorer",
                "Investigation Narrative",
                "Investigator Notes",
                "Community Detection",
                "Community Risk Ranking",
                "Identity Linkage Network",
                "Network Centrality Ranking",
                "Risk Assesment",
                "Account Risk Ranking"
            ]
        )
    elif section == "Analytics":
        page = st.sidebar.radio(
            "Pages",
            [
                "Feature Contribution Analysis",
                "Correlation Heatmap",
                "System Evaluation"
            ]
        )
    else:
        page = st.sidebar.radio(
            "Pages",
            [
                "Investigation Reports",
                "Export Investigation Package"
            ]
        )

if app_mode == "Platform Overview":
    st.title("🛡️ SOCMINT Intelligence Platform")
    st.markdown("### Multi-Modal Identity Attribution & Forensic Fusion Suite")
    
    st.info("Select an engine from the sidebar to begin your investigation.")
    
    st.divider()
    
    # 1. Executive Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Profiles", metrics["profiles"])
    col2.metric("Total Comparisons", metrics["comparisons"])
    col3.metric("Linked Identities", metrics["linked"])
    col4.metric("Highest Fusion", round(metrics["highest_fusion"], 3))
    
    st.divider()

    # 2. Clear, understandable engine distinction
    st.subheader("Choose Your Intelligence Engine")
    st.write("Our platform is divided into two specialized workflows based on your investigation needs:")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 📊 Historical Dataset Analytics")
        st.write("""
        **Best for: Big-picture research.**
        
        Use this engine to analyze large, pre-existing collections of data. It is designed to find hidden connections, patterns, and community structures across thousands of profiles at once. 
        *   **Key focus:** Trend analysis, network-wide risk ranking, and data correlation.
        """)

    with col_b:
        st.markdown("### 🔍 Live OSINT Ingestion")
        st.write("""
        **Best for: Real-time, tactical investigation.**
        
        Use this engine when you need to focus on a specific target. It pulls fresh data directly from the web, allowing you to verify evidence like vehicle IDs, extract text from images, and confirm identities across multiple live platforms.
        *   **Key focus:** Targeted acquisition, forensic extraction, and real-time attribution.
        """)
        
    st.divider()

    # 3. Simple Workflow Steps
    st.subheader("How the Platform Works")
    step1, step2, step3 = st.columns(3)
    
    with step1:
        st.markdown("#### 1. Data Ingestion")
        st.write("Start by collecting data—either by uploading a dataset or targeting a specific user profile.")
    with step2:
        st.markdown("#### 2. Forensic Fusion")
        st.write("Our algorithms bridge the gap between different data points to find matches and inconsistencies.")
    with step3:
        st.markdown("#### 3. Intelligence Attribution")
        st.write("Review the final fusion report to confidently attribute identities and document findings.")
 
elif app_mode == "Live OSINT Ingestion & Profiling":
    page = st.sidebar.radio(
        "Live OSINT Workspace",
        [
            
            "One-to-Many Investigator Search",
            "Live Target Web Scraper",
            "Multimodal OCR Extractor",
            "Vehicle RC/DL Verification",
            "Live Intelligence",
            "Profile Comparison",
            "Cross-Platform Comparison"  # <--- NEW TAB ADDED HERE
        ]
    )

st.sidebar.divider()

st.sidebar.caption("SOCMINT v2.0")

# =====================================================
# INVESTIGATION COMMAND CENTER
# =====================================================

if page == "Investigation Command Center":

    import re

    st.title("Investigation Command Center")
    st.caption("Unified Intelligence Search Workspace")

    # -----------------------------
    # DEFAULT VALUES
    # -----------------------------

    query = ""
    search = False
    detected = "Username"

    # -----------------------------
    # SEARCH BAR
    # -----------------------------

    search_col, button_col = st.columns([6, 1])

    with search_col:
        query = st.text_input(
            "Universal Search",
            placeholder="Username • Email • Phone • Vehicle • URL • Domain"
        )

    with button_col:
        st.write("")
        st.write("")
        search = st.button(
            "Search",
            use_container_width=True
        )

    # -----------------------------
    # DETECT SEARCH TYPE
    # -----------------------------

    if search and query:

        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", query):
            detected = "Email"

        elif re.fullmatch(r"\+?\d{10,13}", query):
            detected = "Phone"

        elif re.fullmatch(
            r"[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}",
            query.upper()
        ):
            detected = "Vehicle"

        elif query.startswith("http://") or query.startswith("https://"):
            detected = "URL"

        elif "." in query:
            detected = "Domain"

        else:
            detected = "Username"

    st.divider()

    routing_colors = {
        "Username": "👤",
        "Email": "📧",
        "Phone": "📱",
        "Vehicle": "🚗",
        "URL": "🌐",
        "Domain": "🌍"
    }

    st.success(
        f"{routing_colors.get(detected,'🔍')} Routed to **{detected}** Intelligence"
    )

    # -----------------------------
    # TABS
    # -----------------------------

    tab_search, tab_ocr, tab_scraper, tab_vehicle, tab_pivot, tab_summary = st.tabs([
        "Search",
        "OCR",
        "Live Scraper",
        "Vehicle",
        "Pivot Intelligence",
        "AI Summary"
    ])
    
    # =====================================================
    # SEARCH TAB
    # =====================================================

    with tab_search:

        st.subheader("Profile Search Results")

        if not search:
            st.info("Enter a search query above and click **Search**.")

        elif detected in ["Vehicle", "URL"]:
            st.info(
                f"The query has been routed to the **{detected}** tab."
            )

        else:
            matches = []

            for profile in profiles:
                searchable_text = " ".join([
                    str(profile.get("username", "")),
                    str(profile.get("bio", "")),
                    str(profile.get("posts", "")),
                    " ".join(profile.get("hashtags", [])),
                    " ".join(profile.get("links", []))
                ]).lower()

                if query.lower() in searchable_text:
                    matches.append(profile)

            if not matches:
                st.warning("No matching profiles found.")
            else:
                st.success(f"{len(matches)} matching profile(s) found.")

                for profile in matches:
                    with st.container(border=True):
                        header_left, header_right = st.columns([4, 1])

                        with header_left:
                            st.subheader(profile["username"])
                            st.write(
                                f"**Followers:** {profile['followers']}"
                            )
                            st.write(
                                f"**Verified:** {profile['verified']}"
                            )

                        with header_right:
                            risk = (
                                "High"
                                if profile["bot_label"]
                                else "Low"
                            )
                            st.metric(
                                "Risk",
                                risk
                            )

                        st.write("### Bio")
                        st.write(
                            profile.get(
                                "bio",
                                "No bio available."
                            )
                        )

                        st.write("### Recent Post")
                        st.write(
                            profile.get(
                                "posts",
                                "No posts available."
                            )[:250]
                        )

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "Hashtags",
                                len(profile["hashtags"])
                            )

                        with col2:
                            st.metric(
                                "Links",
                                len(profile["links"])
                            )

                        with col3:
                            st.metric(
                                "Retweets",
                                profile["retweets"]
                            )

                        st.divider()
                        
    # =====================================================
    # VEHICLE TAB
    # =====================================================

    with tab_vehicle:
        st.subheader("Vehicle Intelligence")

        if detected != "Vehicle":
            st.info(
                "Enter a valid vehicle number in the search bar (e.g. KA01AB1234)."
            )

        else:
            with st.spinner("Verifying vehicle registration..."):
                result = verify_and_route_vehicle(query)

            if result.get("verified", False):
                st.success("Vehicle verified successfully.")
                st.json(result["metadata"])
            else:
                st.error(result.get("message", "Verification failed."))
                
    # =====================================================
    # LIVE SCRAPER TAB
    # =====================================================

    with tab_scraper:
        st.subheader("Live Web Intelligence")

        if detected != "URL":
            st.info(
                "Search using a URL to automatically scrape public intelligence."
            )

        else:
            with st.spinner("Scraping target..."):
                scraped = live_scrape_profile(query)

            if scraped:
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Status",
                        "Success"
                    )
                    st.write("### Page")
                    st.write(scraped.get("scraped_name", "Unknown"))

                with col2:
                    st.write("### Description")
                    st.write(scraped.get("scraped_bio", "No description"))

                st.divider()
                st.json(scraped)

            else:
                st.error("Unable to scrape target.")

        with tab_ocr:
            st.subheader("Multimodal OCR Intelligence")

            uploaded_image = st.file_uploader(
                "Upload Screenshot / Profile Image",
                type=["png", "jpg", "jpeg"],
                key="ocr_upload"
            )

            if uploaded_image is not None:
                st.image(
                    uploaded_image,
                    width=350
                )

                if st.button(
                    "Extract Intelligence",
                    key="run_ocr"
                ):
                    with st.spinner("Running OCR Engine..."):
                        ocr = extract_text_from_profile_image(uploaded_image)

                    st.success("OCR Completed")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Detected Emails")
                        if ocr["embedded_emails"]:
                            for email in ocr["embedded_emails"]:
                                st.code(email)
                        else:
                            st.caption("No emails detected.")

                    with col2:
                        st.subheader("Detected Phones")
                        if ocr["embedded_phones"]:
                            for phone in ocr["embedded_phones"]:
                                st.code(phone)
                        else:
                            st.caption("No phone numbers detected.")

                    st.subheader("OCR Text")
                    st.text_area(
                        "",
                        ocr["raw_ocr_dump"],
                        height=220
                    )
                    
        with tab_pivot:
            st.subheader("Infrastructure Pivot Intelligence")

            pivot_text = st.text_area(
                "Paste text from any profile",
                height=180
            )

            if st.button(
                "Extract Pivots",
                key="pivot"
            ):
                pivots = extract_advanced_pivots(
                    pivot_text
                )

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.write("### Emails")
                    st.write(pivots["emails"])

                    st.write("### Phones")
                    st.write(pivots["phones"])

                with c2:
                    st.write("### URLs")
                    st.write(pivots["urls"])

                    st.write("### Devices")
                    st.write(pivots["devices"])

                with c3:
                    st.write("### Locations")
                    st.write(pivots["locations"])
                    
        with tab_summary:
            st.subheader("AI Investigation Summary")

            if search and query:
                st.info(
        f"""
        Search Query
        {query}

        Detected Type
        {detected}

        The command center searched every available intelligence source.

        Available Modules
        • Username Matching
        • Pivot Intelligence
        • OCR Intelligence
        • Vehicle Intelligence
        • Live Web Scraper

        Recommended Next Step
        Review evidence before investigator confirmation.
        """
                )
            else:
                st.caption(
                    "Run a search to generate an AI summary."
                )
                
elif page == "Live Intelligence":
    show_live_intelligence()
    
elif page == "Profile Comparison":
    show_profile_comparison()
    
elif page == "Case Summary":

    st.markdown(
    """
# SOCMINT Investigation Platform

Executive Intelligence Dashboard

---
"""
)
    st.caption("Real-time overview of identity linkage investigations")

    # ------------------------------------
    # KPI CARDS
    # ------------------------------------

    fusion_scores = [row[11] for row in comparisons]

    linked_accounts = sum(
        1 for row in comparisons
        if row[13] == 1
    )

    avg_fusion = (
        sum(fusion_scores)/len(fusion_scores)
        if fusion_scores else 0
    )

    highest_fusion = (
        max(fusion_scores)
        if fusion_scores else 0
    )

    col1,col2,col3,col4,col5 = st.columns(
        5,
        gap="large"
    )

    col1.metric(
        "Profiles",
        metrics["profiles"]
    )

    col2.metric(
        "Comparisons",
        metrics["comparisons"]
    )

    col3.metric(
        "Linked Accounts",
        linked_accounts
    )

    col4.metric(
        "Average Fusion",
        round(avg_fusion,3)
    )

    col5.metric(
        "Highest Fusion",
        round(highest_fusion,3)
    )

    st.divider()
    status1,status2,status3,status4 = st.columns(4)

    status1.success("Fusion Engine")
    status2.success("Evidence Pipeline")
    status3.success("SQLite Database")
    status4.success("OSINT Modules")

    st.divider()
    # ------------------------------------
    # ROW 1
    # ------------------------------------

    left,right = st.columns([2,1])

    with left:
        st.subheader("Fusion Score Distribution")

        if fusion_scores:
            fig = px.histogram(
                x=fusion_scores,
                nbins=20,
                labels={
                    "x":"Fusion Score"
                }
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=40,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:
        st.subheader("System Health")
        st.success("Database Connected")
        st.success("Fusion Engine Running")
        st.success("Evidence Modules Loaded")
        st.success("SQLite Online")

        st.info(
            f"Profiles Loaded : {metrics['profiles']}"
        )

        st.info(
            f"Pairwise Comparisons : {metrics['comparisons']}"
        )

    st.divider()

    # ------------------------------------
    # ROW 2
    # ------------------------------------

    left,right = st.columns(2)

    with left:
        st.subheader("Risk Distribution")

        risk_counts = {
            "High":0,
            "Medium":0,
            "Low":0
        }

        for row in comparisons:
            score = row[11]

            if score >= 0.75:
                risk_counts["High"] += 1
            elif score >= 0.50:
                risk_counts["Medium"] += 1
            else:
                risk_counts["Low"] += 1

        fig = px.bar(
            x=list(risk_counts.keys()),
            y=list(risk_counts.values()),
            labels={
                "x":"Risk Level",
                "y":"Count"
            }
        )

        fig.update_layout(height=330)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:
        st.subheader("Followers Distribution")

        follower_values = [
            p["followers"]
            for p in profiles
        ]

        fig = px.histogram(
            x=follower_values,
            nbins=20,
            labels={
                "x":"Followers"
            }
        )

        fig.update_layout(height=330)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ------------------------------------
    # ROW 3
    # ------------------------------------

    left,right = st.columns([1,1])

    with left:
        st.subheader("Highest Risk Accounts")

        account_scores = {}

        for row in comparisons:
            account_scores[row[1]] = account_scores.get(
                row[1],0
            ) + row[11]

            account_scores[row[2]] = account_scores.get(
                row[2],0
            ) + row[11]

        ranking = sorted(
            account_scores.items(),
            key=lambda x:x[1],
            reverse=True
        )[:10]

        ranking_df = pd.DataFrame(
            ranking,
            columns=[
                "Account",
                "Risk Score"
            ]
        )

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

    with right:
        st.subheader("Recent Investigation Feed")

        latest = sorted(
            comparisons,
            key=lambda x:x[0],
            reverse=True
        )[:10]

        for row in latest:
            st.markdown(
                f"""
**{row[1]} ↔ {row[2]}**

Fusion Score : **{round(row[11],3)}**
"""
            )
            st.divider()




# =====================================================
# INVESTIGATION WORKSPACE
# =====================================================

elif page == "Profile Analysis":

    import re

    st.title("Investigation Workspace")
    st.caption("Universal Intelligence Search")

    # =====================================================
    # UNIVERSAL SEARCH
    # =====================================================

    search_col, button_col = st.columns([6, 1])

    with search_col:
        query = st.text_input(
            "Universal Search",
            placeholder="Username • Email • Phone • URL • Domain • Vehicle • Hashtag"
        )

    with button_col:
        st.write("")
        st.write("")
        search_btn = st.button(
            "Search",
            use_container_width=True
        )

    st.divider()

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Profiles",
        len(profiles)
    )

    metric2.metric(
        "Comparisons",
        len(comparisons)
    )

    metric3.metric(
        "Linked Accounts",
        sum(1 for row in comparisons if row[13] == 1)
    )

    metric4.metric(
        "Fusion Records",
        len(comparisons)
    )

    st.divider()

    detected_type = "Unknown"
    if query:
        query = query.strip()

        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", query):
            detected_type = "Email"
        elif re.fullmatch(r"\+?\d{10,13}", query):
            detected_type = "Phone"
        elif re.fullmatch(r"[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}", query.upper()):
            detected_type = "Vehicle"
        elif query.startswith("http://") or query.startswith("https://"):
            detected_type = "URL"
        elif query.startswith("#"):
            detected_type = "Hashtag"
        elif "." in query:
            detected_type = "Domain"
        else:
            detected_type = "Username"

    col1, col2 = st.columns([1,5])

    with col1:
        st.metric("Detected", detected_type)

    with col2:
        st.info(
            "The search engine automatically determines the evidence type and searches available intelligence."
        )

    if search_btn and query:
        results = []
        search_term = query.lower()

        for profile in profiles:
            combined_text = " ".join([
                str(profile.get("username", "")),
                str(profile.get("bio", "")),
                str(profile.get("posts", "")),
                " ".join(profile.get("hashtags", [])),
                " ".join(profile.get("links", []))
            ]).lower()

            pivots = extract_advanced_pivots(combined_text)
            match_found = False

            if search_term in combined_text:
                match_found = True
            elif search_term in " ".join(pivots["emails"]).lower():
                match_found = True
            elif search_term in " ".join(pivots["phones"]).lower():
                match_found = True
            elif search_term in " ".join(pivots["urls"]).lower():
                match_found = True
            elif search_term in " ".join(pivots["devices"]).lower():
                match_found = True
            elif search_term in " ".join(pivots["locations"]).lower():
                match_found = True

            if match_found:
                profile["pivot_data"] = pivots
                results.append(profile)

        st.divider()
        st.subheader("Investigation Results")
        st.caption(f"{len(results)} intelligence record(s) matched your search.")

        if len(results) == 0:
            st.warning("No matching intelligence found.")
        else:
            st.success("Search completed successfully.")

        for profile in results:
            pivots = profile["pivot_data"]
            risk = "High" if profile["bot_label"] else "Low"

            with st.container(border=True):
                
                # =====================================================
                # HEADER
                # =====================================================

                top_left, top_middle, top_right = st.columns([4, 2, 2])

                with top_left:
                    st.subheader(profile["username"])
                    st.caption(f"Account ID : {profile['id']}")

                    verified = "Yes" if profile["verified"] else "No"

                    st.write(f"**Followers:** {profile['followers']}")
                    st.write(f"**Verified:** {verified}")

                with top_middle:
                    fusion_scores = []
                    for row in comparisons:
                        if profile["id"] in (row[1], row[2]):
                            fusion_scores.append(row[11])

                    highest_fusion = max(fusion_scores) if fusion_scores else 0

                    st.metric(
                        "Highest Fusion",
                        round(highest_fusion, 3)
                    )

                with top_right:
                    st.metric(
                        "Risk Level",
                        risk
                    )

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.write("### Emails")
                    if pivots["emails"]:
                        st.write(pivots["emails"])
                    else:
                        st.write("-")

                with c2:
                    st.write("### Phones")
                    if pivots["phones"]:
                        st.write(pivots["phones"])
                    else:
                        st.write("-")

                with c3:
                    st.write("### Links")
                    if profile["links"]:
                        st.write(profile["links"])
                    else:
                        st.write("-")
                with c4:
                    st.write("### Locations")
                    if pivots["locations"]:
                        for location in pivots["locations"]:
                            st.write(location)
                    else:
                        st.write("-")
                        
                st.divider()

                left, right = st.columns([3, 2])

                with left:
                    st.write("### AI Investigation Summary")
                    st.info(
                        f"""
                Username : {profile['username']}

                Followers : {profile['followers']}

                Verified : {verified}

                Risk Level : {risk}

                Highest Fusion : {round(highest_fusion,3)}

                Detected Emails : {len(pivots['emails'])}

                Detected Phones : {len(pivots['phones'])}

                Detected URLs : {len(pivots['urls'])}

                Detected Locations : {len(pivots['locations'])}
                """
                    )

                with right:
                    st.write("### Intelligence Statistics")
                    st.metric(
                        "Hashtags",
                        len(profile["hashtags"])
                    )
                    st.metric(
                        "Links",
                        len(profile["links"])
                    )
                    st.metric(
                        "Emails",
                        len(pivots["emails"])
                    )
                    st.metric(
                        "Phones",
                        len(pivots["phones"])
                    )

                # =====================================================
                # QUICK ACTIONS
                # =====================================================

                st.divider()
                st.write("### Quick Actions")

                action1, action2, action3 = st.columns(3)

                with action1:
                    if st.button(
                        "Open Investigation",
                        key=f"open_{profile['id']}",
                        use_container_width=True
                    ):
                        st.session_state["selected_profile"] = profile["id"]
                        st.success("Investigation workspace opened.")

                with action2:
                    if st.button(
                        "View Evidence",
                        key=f"evidence_{profile['id']}",
                        use_container_width=True
                    ):
                        st.info(
                            "Evidence Explorer integration will be connected in the next update."
                        )

                with action3:
                    if st.button(
                        "Generate Report",
                        key=f"report_{profile['id']}",
                        use_container_width=True
                    ):
                        report = generate_report(
                            profile["id"],
                            highest_fusion,
                            "Generated from Universal Search",
                            "Auto-generated"
                        )

                        filename = save_report(
                            profile["id"],
                            report
                        )

                        st.success(f"Saved to {filename}")
                        
                st.divider()

                st.write("### Fusion Confidence")
                st.progress(
                    min(highest_fusion, 1.0)
                )

                st.caption(
                    f"Fusion Confidence : {round(highest_fusion*100,2)}%"
                )
                
                st.divider()

                st.write("### Linked Identity Matches")

                linked = []
                for row in comparisons:
                    if row[1] == profile["id"]:
                        linked.append(
                            (row[2], row[11])
                        )
                    elif row[2] == profile["id"]:
                        linked.append(
                            (row[1], row[11])
                        )

                if linked:
                    linked = sorted(
                        linked,
                        key=lambda x: x[1],
                        reverse=True
                    )

                    linked_df = pd.DataFrame(
                        linked,
                        columns=[
                            "Related Account",
                            "Fusion Score"
                        ]
                    )

                    st.dataframe(
                        linked_df,
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("No linked identities detected.")
                    
                st.divider()

                st.write("### Investigator Notes")

                notes = db.get_notes()
                profile_notes = [
                    n for n in notes
                    if n[1] == profile["id"]
                ]

                if profile_notes:
                    for note in profile_notes[-3:]:
                        st.info(note[2])
                else:
                    st.caption("No investigator notes available.")
                    
                st.divider()

                with st.expander("Raw Profile Data"):
                    st.json(profile)

# ==========================
# 3. IDENTITY LINKAGE RESULTS
# ==========================
elif page == "Identity Linkage Results":
    st.title("Identity Linkage Results")
    results = []
    for row in comparisons:
        status = "LINKED" if row[13] == 1 else "NOT LINKED"
        results.append({
            "Profile 1": row[1],
            "Profile 2": row[2],
            "Fusion Score": round(row[11], 3),
            "Confidence %": round(row[11] * 100, 2),
            "Explanation": row[12],
            "Risk": risk_level(row[11]),
            "Status": status
        })
    if results:
        results_df = pd.DataFrame(results).sort_values(by="Fusion Score", ascending=False)
        st.dataframe(results_df)

# ==========================
# 4. RISK ASSESSMENT
# ==========================
elif page == "Risk Assesment":
    st.title("Risk Assessment")
    risk_data = []
    for row in comparisons:
        risk_data.append({
            "Profile Pair": f"{row[1]} - {row[2]}",
            "Fusion Score": round(row[11], 3),
            "Confidence %": round(row[11] * 100, 2),
            "Risk": risk_level(row[11])
        })
    if risk_data:
        risk_df = pd.DataFrame(risk_data).sort_values(by="Fusion Score", ascending=False)
        st.dataframe(risk_df)

# ==========================
# 5. COMMUNITY DETECTION
# ==========================
elif page == "Community Detection":
    st.title("Community Detection")
    from modules.network_analysis import build_graph, add_link, detect_communities
    G = build_graph(profiles)
    for row in comparisons:
        if row[13] == 1:
            add_link(G, row[1], row[2], row[10])
    communities = detect_communities(G)
    for i, community in enumerate(communities, start=1):
        st.subheader(f"Community {i}")
        st.markdown("**Members:**")
        for member in community:
            st.write(f"• {member}")

# ==========================
# 6. ACCOUNT RISK RANKING
# ==========================
elif page == "Account Risk Ranking":
    st.title("Account Risk Ranking")
    account_scores = {}
    for row in comparisons:
        account_scores[row[1]] = account_scores.get(row[1], 0) + row[10]
        account_scores[row[2]] = account_scores.get(row[2], 0) + row[10]
    
    ranking = [{"Account": acc, "Risk Score": round(sc, 3)} for acc, sc in account_scores.items()]
    if ranking:
        ranking_df = pd.DataFrame(ranking).sort_values(by="Risk Score", ascending=False)
        ranking_df.reset_index(drop=True, inplace=True)
        ranking_df.index += 1
        st.dataframe(ranking_df)

# ==========================
# 7. INVESTIGATOR NOTES
# ==========================
elif page == "Investigator Notes":
    st.title("Investigator Notes")
    account_id = st.text_input("Account ID")
    note = st.text_area("Investigation Note")
    if st.button("Save Note"):
        db.save_note(account_id, note)
        st.success("Note Saved")
    
    notes = db.get_notes()
    st.subheader("Saved Notes")
    notes_data = [{"Account ID": row[1], "Note": row[2]} for row in notes]
    st.dataframe(pd.DataFrame(notes_data))

# ==========================
# 8. INVESTIGATION REPORTS
# ==========================
elif page == "Investigation Reports":
    st.title("Investigation Reports")
    account_id = st.text_input("Account ID")
    risk_score = st.number_input("Risk Score", value=0.0)
    explanation = st.text_area("Explanation")
    notes = st.text_area("Investigator Notes")
    if st.button("Generate Report"):
        report = generate_report(account_id, risk_score, explanation, notes)
        filename = save_report(account_id, report)
        st.success(f"Report saved to {filename}")
        st.text(report)

# ==========================
# 9. COMMUNITY RISK RANKING
# ==========================
elif page == "Community Risk Ranking":
    st.title("Community Risk Ranking")
    from modules.network_analysis import build_graph, add_link, detect_communities
    G = build_graph(profiles)
    for row in comparisons:
        if row[13] == 1:
            add_link(G, row[1], row[2], row[10])
    communities = detect_communities(G)
    
    community_data = []
    for i, community in enumerate(communities, start=1):
        risk_scores = [row[10] for row in comparisons if row[1] in community and row[2] in community]
        avg_risk = round(sum(risk_scores) / len(risk_scores), 3) if risk_scores else 0
        community_data.append({"Community": i, "Members": len(community), "Average Risk": avg_risk})
    
    if community_data:
        community_df = pd.DataFrame(community_data).sort_values(by="Average Risk", ascending=False)
        community_df.reset_index(drop=True, inplace=True)
        community_df.index += 1
        st.dataframe(community_df)

# ==========================
# 10. FEATURE CONTRIBUTION ANALYSIS
# ==========================
elif page == "Feature Contribution Analysis":
    st.title("Feature Contribution Analysis")
    contribution_data = []
    for row in comparisons:
        contribution_data.append({
            "Username": round(row[3], 3),
            "Stylometry": round(row[5], 3),
            "Behavior": round(row[10], 3),
            "Temporal": round(row[7], 3),
            "Fusion": round(row[11], 3)
        })
    if contribution_data:
        contribution_df = pd.DataFrame(contribution_data).sort_values(by="Fusion", ascending=False)
        contribution_df.reset_index(drop=True, inplace=True)
        contribution_df.index += 1
        st.dataframe(contribution_df)
        st.subheader("Fusion Score Distribution")
        st.bar_chart(contribution_df["Fusion"])

# =====================================================
# EXECUTIVE ANALYTICS
# =====================================================

elif page == "System Evaluation":

    st.title("Executive Analytics")
    st.caption("System-wide Intelligence Analytics")

    fusion_scores = [row[11] for row in comparisons]

    followers = [
        p["followers"]
        for p in profiles
    ]

    risk_levels = []

    for row in comparisons:
        if row[11] >= 0.75:
            risk_levels.append("High")
        elif row[11] >= 0.50:
            risk_levels.append("Medium")
        else:
            risk_levels.append("Low")

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Fusion Score Distribution")
        fig = px.histogram(
            x=fusion_scores,
            nbins=20,
            title="Fusion Score Histogram"
        )
        fig.update_layout(
            height=420
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with row1_col2:
        st.subheader("Followers Distribution")
        fig = px.histogram(
            x=followers,
            nbins=20,
            title="Followers Histogram"
        )
        fig.update_layout(
            height=420
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        risk_df = pd.DataFrame({
            "Risk": risk_levels
        })
        fig = px.pie(
            risk_df,
            names="Risk",
            title="Risk Distribution"
        )
        fig.update_layout(
            height=420
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with row2_col2:
        verified = sum(
            1 for p in profiles
            if p["verified"]
        )
        unverified = len(profiles) - verified
        fig = px.bar(
            x=["Verified", "Unverified"],
            y=[verified, unverified],
            title="Verified Accounts"
        )
        fig.update_layout(
            height=420
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()
    # =====================================================
    # HASHTAGS & LINKS
    # =====================================================

    row3_col1, row3_col2 = st.columns(2)

    hashtags = {}
    links = {}

    for profile in profiles:
        for tag in profile["hashtags"]:
            hashtags[tag] = hashtags.get(tag, 0) + 1
        for link in profile["links"]:
            links[link] = links.get(link, 0) + 1

    with row3_col1:
        if hashtags:
            hashtag_df = pd.DataFrame(
                sorted(
                    hashtags.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10],
                columns=["Hashtag", "Count"]
            )
            fig = px.bar(
                hashtag_df,
                x="Hashtag",
                y="Count",
                title="Top Hashtags"
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with row3_col2:
        if links:
            link_df = pd.DataFrame(
                sorted(
                    links.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10],
                columns=["Link", "Count"]
            )
            fig = px.bar(
                link_df,
                x="Link",
                y="Count",
                title="Top Shared Links"
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()
    # =====================================================
    # LEADERBOARDS
    # =====================================================

    left, right = st.columns(2)

    with left:
        st.subheader("Top 10 Accounts by Followers")
        follower_df = pd.DataFrame(
            sorted(
                [
                    (
                        p["username"],
                        p["followers"]
                    )
                    for p in profiles
                ],
                key=lambda x: x[1],
                reverse=True
            )[:10],
            columns=[
                "Username",
                "Followers"
            ]
        )
        st.dataframe(
            follower_df,
            use_container_width=True,
            hide_index=True
        )

    with right:
        st.subheader("Highest Fusion Pairs")
        fusion_df = pd.DataFrame(
            sorted(
                [
                    (
                        row[1],
                        row[2],
                        round(row[11],3)
                    )
                    for row in comparisons
                ],
                key=lambda x: x[2],
                reverse=True
            )[:10],
            columns=[
                "Profile 1",
                "Profile 2",
                "Fusion"
            ]
        )
        st.dataframe(
            fusion_df,
            use_container_width=True,
            hide_index=True
        )

# ==========================
# 12. CORRELATION HEATMAP
# ==========================
elif page == "Correlation Heatmap":
    st.title("Feature Correlation Heatmap")
    heatmap_data = []
    for row in comparisons:
        heatmap_data.append({
            "Username": row[3], "Bio": row[4], "Stylometry": row[5], "Emoji": row[6],
            "Temporal": row[7], "Hyperlink": row[8], "Hashtag": row[9], "Behavior": row[10], "Fusion": row[11]
        })
    if heatmap_data:
        heatmap_df = pd.DataFrame(heatmap_data)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_df.corr(), annot=True, cmap="Blues", ax=ax)
        st.pyplot(fig)

# ==========================
# 13. IDENTITY LINKAGE NETWORK
# ==========================
elif page == "Identity Linkage Network":
    st.title("Identity Linkage Network")
    from modules.network_analysis import build_graph, add_link, generate_interactive_graph
    G = build_graph(profiles)
    for row in comparisons:
        if row[13] == 1:
            add_link(G, row[1], row[2], row[11])
    generate_interactive_graph(G)
    
    if os.path.exists("network_graph.html"):
        with open("network_graph.html", "r", encoding="utf-8") as f:
            html = f.read()
        st.components.v1.html(html, height=800, scrolling=True)

# ==========================
# 14. NETWORK CENTRALITY RANKING
# ==========================
elif page == "Network Centrality Ranking":
    st.title("Network Centrality Ranking")
    from modules.network_analysis import build_graph, add_link, calculate_centrality
    G = build_graph(profiles)
    for row in comparisons:
        if row[13] == 1:
            add_link(G, row[1], row[2], row[11])
    ranking = calculate_centrality(G)
    ranking_data = [{"Account": acc, "Centrality": round(sc, 4)} for acc, sc in ranking]
    ranking_df = pd.DataFrame(ranking_data)
    ranking_df.index += 1
    st.dataframe(ranking_df)

# =====================================================
# EVIDENCE EXPLORER
# =====================================================

elif page == "Evidence Explorer":

    st.title("Evidence Explorer")
    st.caption("Unified Evidence & Intelligence Workspace")

    profile_ids = [profile["id"] for profile in profiles]

    selected_id = st.selectbox(
        "Select Account",
        profile_ids
    )

    profile = next(
        p for p in profiles
        if p["id"] == selected_id
    )

    pivots = extract_advanced_pivots(
        profile.get("posts", "") +
        " " +
        profile.get("bio", "")
    )

    fusion_scores = []

    for row in comparisons:
        if profile["id"] in (row[1], row[2]):
            fusion_scores.append(row[11])

    highest_fusion = (
        max(fusion_scores)
        if fusion_scores
        else 0
    )

    risk = "High" if profile["bot_label"] else "Low"

    left, right = st.columns([3, 1])

    with left:
        st.subheader(profile["username"])
        st.caption(f"Account ID : {profile['id']}")

    with right:
        st.metric(
            "Fusion",
            round(highest_fusion, 3)
        )

    st.progress(highest_fusion)

    st.divider()
    # =====================================================
    # PROFILE OVERVIEW
    # =====================================================
    badge1,badge2,badge3 = st.columns(3)

    with badge1:
        st.info(
            f"Fusion : {round(highest_fusion,3)}"
        )

    with badge2:
        st.warning(
            f"Risk : {risk}"
        )

    with badge3:
        st.success(
            f"Followers : {profile['followers']}"
        )

    st.divider()
    st.subheader("Profile Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Followers",
            profile["followers"]
        )

    with col2:
        st.metric(
            "Verified",
            "Yes" if profile["verified"] else "No"
        )

    with col3:
        st.metric(
            "Risk",
            risk
        )

    with col4:
        st.metric(
            "Bot Label",
            profile["bot_label"]
        )

    st.divider()

    # =====================================================
    # ACCOUNT DETAILS
    # =====================================================

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Account Information")
        st.write(f"**Username:** {profile['username']}")
        st.write(f"**Account ID:** {profile['id']}")
        st.write(f"**Followers:** {profile['followers']}")
        st.write(f"**Verified:** {profile['verified']}")
        st.write(f"**Retweets:** {profile['retweets']}")
        st.write(f"**Active Hour:** {profile['active_hours'][0]}")

    with right:
        st.subheader("Investigation Summary")
        st.info(
            f"""
Highest Fusion : {round(highest_fusion,3)}

Risk Level : {risk}

Bot Label : {profile['bot_label']}

Hashtags : {len(profile['hashtags'])}

Links : {len(profile['links'])}
"""
        )

    st.divider()
    # =====================================================
    # EVIDENCE INTELLIGENCE GRID
    # =====================================================

    st.subheader("Extracted Intelligence")

    email_col, phone_col, domain_col = st.columns(3)

    with email_col:
        st.markdown("#### Emails")
        if pivots["emails"]:
            for email in pivots["emails"]:
                st.code(email)
        else:
            st.caption("No emails detected")
            
            analytics1,analytics2,analytics3,analytics4 = st.columns(4)

            analytics1.metric(
                "Profiles",
                len(profiles)
            )

            analytics2.metric(
                "Comparisons",
                len(comparisons)
            )

            analytics3.metric(
                "Communities",
                len(set([r[13] for r in comparisons]))
            )

            analytics4.metric(
                "Average Fusion",
                round(
                    sum([r[11] for r in comparisons])/len(comparisons),
                    3
                )
            )

    with phone_col:
        st.markdown("#### Phone Numbers")
        if pivots["phones"]:
            for phone in pivots["phones"]:
                st.code(phone)
        else:
            st.caption("No phone numbers detected")

    with domain_col:
        st.markdown("#### Domains")
        domains = []
        for url in pivots["urls"]:
            try:
                domain = url.split("/")[2]
                if domain not in domains:
                    domains.append(domain)
            except Exception:
                pass

        if domains:
            for domain in domains:
                st.code(domain)
        else:
            st.caption("No domains detected")

    st.write("")

    url_col, device_col, location_col = st.columns(3)

    with url_col:
        st.markdown("#### URLs")
        if pivots["urls"]:
            for url in pivots["urls"]:
                st.code(url)
        else:
            st.caption("No URLs detected")

    with device_col:
        st.markdown("#### Devices")
        if pivots["devices"]:
            for device in pivots["devices"]:
                st.code(device)
        else:
            st.caption("No devices detected")

    with location_col:
        st.markdown("#### Locations")
        if pivots["locations"]:
            for location in pivots["locations"]:
                st.code(location)
        else:
            st.caption("No locations detected")

    st.divider()
    
    # =====================================================
    # LINKED IDENTITIES
    # =====================================================

    st.subheader("Linked Identity Analysis")

    linked_accounts = []

    for row in comparisons:
        if row[1] == profile["id"]:
            linked_accounts.append({
                "Related Account": row[2],
                "Fusion Score": round(row[11],3),
                "Status": "Linked" if row[13] else "Candidate"
            })
        elif row[2] == profile["id"]:
            linked_accounts.append({
                "Related Account": row[1],
                "Fusion Score": round(row[11],3),
                "Status": "Linked" if row[13] else "Candidate"
            })

    if linked_accounts:
        linked_df = pd.DataFrame(linked_accounts)
        linked_df = linked_df.sort_values(
            "Fusion Score",
            ascending=False
        )
        st.dataframe(
            linked_df,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No related identities discovered.")

    st.divider()
    
    # =====================================================
    # INVESTIGATION COMMAND CENTER
    # =====================================================

    st.subheader("Investigation Command Center")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Timeline",
        "Narrative",
        "Investigator Notes",
        "Raw Evidence"
    ])

    # =====================================================
    # TIMELINE
    # =====================================================

    with tab1:
        st.write("### Investigation Timeline")
        timeline = []

        for row in comparisons:
            if profile["id"] in (row[1], row[2]):
                timeline.append({
                    "Compared With": row[2] if row[1] == profile["id"] else row[1],
                    "Fusion Score": round(row[11], 3),
                    "Decision": "Linked" if row[13] else "Candidate"
                })

        if timeline:
            timeline_df = pd.DataFrame(timeline)
            st.dataframe(
                timeline_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No investigation timeline available.")

    # =====================================================
    # AI NARRATIVE
    # =====================================================

    with tab2:
        st.write("### AI Investigation Narrative")

        narrative = f"""
Account **{profile['username']}** was analysed using the SOCMINT evidence fusion engine.

Highest Fusion Score : {round(highest_fusion,3)}

Risk Level : {risk}

Followers : {profile['followers']}

Verified : {profile['verified']}

Evidence extracted:

• Emails : {len(pivots['emails'])}

• Phones : {len(pivots['phones'])}

• URLs : {len(pivots['urls'])}

• Devices : {len(pivots['devices'])}

• Locations : {len(pivots['locations'])}

Overall assessment indicates this account should be reviewed by an investigator before a final attribution decision.
"""

        st.text_area(
            "",
            narrative,
            height=300
        )

    # =====================================================
    # INVESTIGATOR NOTES
    # =====================================================

    with tab3:
        st.write("### Investigator Notes")

        note = st.text_area(
            "Add Note",
            key=f"note_{profile['id']}"
        )

        if st.button(
            "Save Note",
            key=f"save_note_{profile['id']}"
        ):
            db.save_note(
                profile["id"],
                note
            )
            st.success("Note saved.")

        st.write("#### Previous Notes")

        notes = db.get_notes()
        found = False

        for n in notes:
            if n[1] == profile["id"]:
                found = True
                st.info(n[2])

        if not found:
            st.caption("No notes available.")

    # =====================================================
    # RAW PROFILE
    # =====================================================

    with tab4:
        st.write("### Raw Profile JSON")
        st.json(profile)

# ==========================
# 16. INVESTIGATION NARRATIVE
# ==========================
elif page == "Investigation Narrative":
    st.title("Investigation Narrative")
    if len(comparisons) == 0:
        st.warning("No comparison data available.")
    else:
        best_match = max(comparisons, key=lambda row: row[11])
        narrative = f"""INVESTIGATION SUMMARY\n\nAccount Pair: {best_match[1]} ↔ {best_match[2]}
        \n• Username: {round(best_match[3],3)} | Bio: {round(best_match[4],3)}
        \n• Stylometry: {round(best_match[5],3)} | Emoji: {round(best_match[6],3)}
        \n• Temporal: {round(best_match[7],3)} | Hyperlink: {round(best_match[8],3)}
        \n• Hashtag: {round(best_match[9],3)} | Behavior: {round(best_match[10],3)}
        \n\nFusion Score: {round(best_match[11],3)}\n\nAssessment indicates identity linkage alignment."""
        st.text_area("Generated Narrative", narrative, height=500)

# ==========================
# 17. EXPORT INVESTIGATION PACKAGE
# ==========================
elif page == "Export Investigation Package":
    st.title("Export Investigation Package")
    if st.button("Generate Case Package"):
        os.makedirs("reports", exist_ok=True)
        total_profiles, total_comparisons = len(profiles), len(comparisons)
        linked_accounts = sum(1 for row in comparisons if row[13] == 1)
        highest_fusion = max(row[11] for row in comparisons) if comparisons else 0.0

        with open("reports/case_summary.txt", "w", encoding="utf-8") as f:
            f.write(f"SOCMINT PROFILE EXPORT\nProfiles: {total_profiles}\nLinked: {linked_accounts}\nMax Fusion: {highest_fusion}")
        
        linked_df = pd.DataFrame([{"Profile1": r[1], "Profile2": r[2], "Score": r[11]} for r in comparisons if r[13] == 1])
        linked_df.to_csv("reports/linked_accounts.csv", index=False)
        st.success("Case package generated successfully inside reports/ folder.")

# =====================================================
# LIVE FORENSIC TOOLS MODULES
# =====================================================
elif page == "Live Target Web Scraper":
    st.title("Controlled Target Profile Scraper")
    st.markdown("Simulate direct client HTTP headers to query public handles when access points are rate-limited.")
    target_url = st.text_input("Enter Suspect Profile URL (e.g., https://twitter.com/suspect_handle)", "https://example.com/target")
    
    if st.button("Initialize Scrape"):
        with st.spinner("Rotating User-Agents and requesting target DOM structural tree..."):
            scraped = live_scrape_profile(target_url)
            if scraped:
                st.subheader("Extracted Content Meta-Blocks")
                st.write("**Name Element:**", scraped["scraped_name"])
                st.write("**Bio Element:**", scraped["scraped_bio"])
                st.success("Live fetch sequence executed successfully.")
            else:
                st.error("Target node dropped connection or required active captive login bypass.")

elif page == "Multimodal OCR Extractor":
    st.title("Multimodal Image Analysis & OCR Engine")
    st.markdown("Scan graphic files (screenshots, banner text, avatar data) to parse obfuscated text indicators.")
    uploaded_file = st.file_uploader("Upload Profile Image Banner/Screenshot", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Target Forensic Asset Queue", width=400)
        if st.button("Run Text Character Recognition"):
            with st.spinner("Analyzing high-contrast character matrices..."):
                ocr_res = extract_text_from_profile_image(uploaded_file)
                st.subheader("OCR Raw Dump Output")
                st.code(ocr_res["raw_ocr_dump"] if ocr_res["raw_ocr_dump"] else "[Demo Sandbox] No characters extracted.")
                st.write("**Embedded Phones Parse:**", ocr_res["embedded_phones"])
                st.write("**Embedded Emails Parse:**", ocr_res["embedded_emails"])

elif page == "Vehicle RC/DL Verification":
    st.title("Logistical Asset Router (Vehicle RC/DL Verification)")
    st.markdown("Verify regional transport vehicle syntactic layout configurations gathered from text evidence trails.")
    veh_input = st.text_input("Enter Vehicle Registration Number (Indian Format, e.g., KA05NB1234)", "KA05NB1234")
    
    if st.button("Verify Registry Syntax"):
        v_res = verify_and_route_vehicle(veh_input)
        if v_res["verified"]:
            st.success(f"Syntax Match: {v_res['status']}")
            st.json(v_res["metadata"])
        else:
            st.error(f"Syntax Failure: {v_res['status']} - {v_res['message']}")
            
            if "metadata" in v_res and "Gateway Error Trails" in v_res["metadata"]:
                st.markdown("### Gateway Diagnostic Logs:")
                for log in v_res["metadata"]["Gateway Error Trails"]:
                    st.error(log)


# New Tab
elif page == "One-to-Many Investigator Search":
    st.title("One-to-Many Investigator Search")

    st.markdown(
        "Search and correlate identities across multiple OSINT platforms."
    )

    st.divider()

    # --- NEW UI: Clear up the Insta doubt! ---
    col_input, col_source = st.columns([2, 1])
    
    with col_input:
        username = st.text_input(
            "Target Username",
            placeholder="Enter username..."
        )
        
    with col_source:
        source_platform = st.selectbox(
            "Baseline Profile", 
            ["Instagram", "GitHub", "Website"],
            help="This is the target profile we are trying to find matches for."
        )

    st.write("### Hunt on these platforms:")
    col1, col2, col3 = st.columns(3)

    with col1:
        use_instagram = st.checkbox("Instagram", value=(source_platform != "Instagram"))

    with col2:
        use_github = st.checkbox("GitHub", value=(source_platform != "GitHub"))

    with col3:
        use_website = st.checkbox("Website", value=(source_platform != "Website"))

    start = st.button(
        "Start Investigation",
        use_container_width=True
    )
    
    if start:

        platforms = []

        if use_instagram:
            platforms.append("Instagram")

        if use_github:
            platforms.append("GitHub")

        if use_website:
            platforms.append("Website")

        with st.spinner(f"Collecting Baseline OSINT from {source_platform}..."):

            # ----------------------------------------
            # Collect target profile dynamically!
            # ----------------------------------------
            from modules.scrapers.github_scraper import GitHubScraper
            from modules.scrapers.website_scraper import WebsiteScraper
            from pipeline.normalizer import normalize_github, normalize_website
            
            if source_platform == "Instagram":
                target_raw = InstagramCollector().scrape(username)
                target = normalize_instagram(target_raw)
            elif source_platform == "GitHub":
                target_raw = GitHubScraper().scrape(username)
                target = normalize_github(target_raw)
            elif source_platform == "Website":
                target_raw = WebsiteScraper().scrape(username)
                target = normalize_website(target_raw)

            # ----------------------------------------
            # Live collection & Ranking
            # ----------------------------------------
            with st.spinner("Hunting for candidates..."):
                SearchPipeline.search(
                    username,
                    platforms
                )

                repo = CandidateRepository()

                live_profiles = SearchPipeline.search(
                    username,
                    platforms
                )

                repository_profiles = repo.get_all()

                candidate_pool = CandidatePoolBuilder.build(
                    live_profiles,
                    []
                )

                candidate_pool = CandidateDeduplicator.deduplicate(
                    candidate_pool
                )

                retrieved = CandidateRetrievalEngine.retrieve(
                    target,
                    candidate_pool,
                    top_k=100
                )

                results = RankingPipeline.rank(
                    target,
                    retrieved
                )

        repo = CandidateRepository()

        # Aligning summary metrics exactly with badge thresholds
        high = sum(1 for r in results if r["fusion_score"] >= 0.90)
        medium = sum(1 for r in results if 0.70 <= r["fusion_score"] < 0.90)
        low = sum(1 for r in results if 0.40 <= r["fusion_score"] < 0.70)
        reject = sum(1 for r in results if r["fusion_score"] < 0.40)

        st.markdown("## Investigation Summary")

        # Changed to 3 columns for a cleaner UI
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Candidates Found", len(results))

        with c2:
            st.metric("High Confidence", high)

        with c3:
            st.metric("Rejected / Low", low + reject)


        st.divider()
        import pandas as pd

        rows = []

        for r in results:

            rows.append({

                "Username": r["candidate"].username,

                "Platform": r["candidate"].platform,

                "Fusion (%)": round(
                    r["fusion_score"] * 100,
                    2
                )

            })

        df = pd.DataFrame(rows)

        st.markdown("## 🎯 Top Matches")

        for i, candidate in enumerate(results[:10]):

            score = float(candidate["fusion_score"])

            if score >= 0.90:
                badge = "🟢 HIGH"

            elif score >= 0.70:
                badge = "🟡 MEDIUM"

            elif score >= 0.40:
                badge = "🟠 LOW"

            else:
                badge = "🔴 REJECT"

            with st.container(border=True):

                c1, c2 = st.columns([3,1])

                with c1:

                    st.subheader(
                        f"#{i+1}  {candidate['candidate'].username}"
                    )

                    st.caption(
                        candidate["candidate"].platform
                    )

                with c2:

                    st.metric(
                        badge,
                        f"{score*100:.1f}%"
                    )

                st.progress(score)
                with st.expander("Information-Theoretic Linkage Bound", expanded=False):
                    st.markdown("Based on the intersection of cross-platform features, we calculate the formal probability of identity linkage:")
                    
                    # Display the formal math equation using Streamlit's LaTeX engine
                    st.latex(r"P(Link | Evidence) = 1 - e^{-\lambda \left(\frac{N}{K}\right)}")
                    
                    # Calculate the dynamic bound based on their actual score
                    features_matched = int(score * 10) 
                    total_features = 10
                    decay_constant = 0.5
                    
                    import math
                    probability = 1.0 - math.exp(-decay_constant * (features_matched / total_features))
                    
                    st.info(f"**Calculated Probability Limit:** {probability * 100:.2f}%")
                    st.caption("Where N = active features matched, K = total feature dimensions, and λ = decay constant (0.5).")
                
                col1, col2 = st.columns(2)

                with col1:

                    st.write("Username")
                    st.progress(safe_progress(candidate["username_score"]))

                    st.write("Bio")
                    st.progress(safe_progress(candidate["bio_score"]))

                    st.write("Stylometry")
                    st.progress(safe_progress(candidate["stylometry_score"]))
                  
                    st.write("Emoji Fingerprint")
                    st.progress(safe_progress(candidate["emoji_score"]))

                with col2:

                    st.write("Behaviour")
                    st.progress(safe_progress(candidate["behaviour_score"]))

                    st.write("Temporal")
                    st.progress(safe_progress(candidate["temporal_score"]))

                    st.write("Hyperlinks")
                    st.progress(safe_progress(candidate["hyperlink_score"]))
                st.write(candidate["explanation"])


# =====================================================
# CROSS-PLATFORM COMPARISON (GLITCH-PROOF VERSION)
# =====================================================
elif page == "Cross-Platform Comparison":
    st.title("Cross-Platform Identity Resolution")
    st.markdown("Run live multi-domain scraping to mathematically compare footprints across different platforms.")

    # 1. State Initialization
    if 'results' not in st.session_state: st.session_state.results = None
    if 'p1' not in st.session_state: st.session_state.p1 = None
    if 'p2' not in st.session_state: st.session_state.p2 = None
    if 'fusion_score' not in st.session_state: st.session_state.fusion_score = None
    if 'report_text' not in st.session_state: st.session_state.report_text = None

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Target Alpha")
        source1 = st.selectbox("Platform", ["GitHub", "Website"], key="s1")
        target1 = st.text_input("Handle / URL", key="t1")
    with col2:
        st.subheader("Target Beta")
        source2 = st.selectbox("Platform", ["GitHub", "Website"], key="s2")
        target2 = st.text_input("Handle / URL", key="t2")

    st.divider()

    # 2. Scrape and Fusion Logic
    if st.button("Initialize Cross-Platform Fusion", type="primary", use_container_width=True):
        if target1 and target2:
            with st.spinner("Scraping and running adaptive fusion..."):
                from core.evidence_model import EvidenceProfile
                from pipeline.intelligence_pipeline import IntelligencePipeline
                from pipeline.comparison_engine import ComparisonEngine
                from modules.scrapers.github_scraper import GitHubScraper
                from modules.scrapers.website_scraper import WebsiteScraper
                from modules.pivot_boost import calculate_pivot_boost

                pipeline = IntelligencePipeline()
                
                # Scrape logic
                if source1 == "GitHub":
                    raw1 = GitHubScraper().scrape(target1)
                    norm1 = pipeline.normalize_github(raw1)
                    p1 = EvidenceProfile(username=norm1["identity"]["username"], bio=norm1["identity"]["bio"], captions=[norm1["content"]], hyperlinks=raw1.get("html_url", []), platform="GitHub")
                else:
                    raw1 = WebsiteScraper().scrape(target1)
                    p1 = EvidenceProfile(username=target1, bio=raw1.get("description", ""), captions=[raw1.get("visible_text", "")], hyperlinks=raw1.get("urls", []), platform="Website")

                if source2 == "GitHub":
                    raw2 = GitHubScraper().scrape(target2)
                    norm2 = pipeline.normalize_github(raw2)
                    p2 = EvidenceProfile(username=norm2["identity"]["username"], bio=norm2["identity"]["bio"], captions=[norm2["content"]], hyperlinks=raw2.get("html_url", []), platform="GitHub")
                else:
                    raw2 = WebsiteScraper().scrape(target2)
                    p2 = EvidenceProfile(username=target2, bio=raw2.get("description", ""), captions=[raw2.get("visible_text", "")], hyperlinks=raw2.get("urls", []), platform="Website")

                results = ComparisonEngine.compare(p1, p2)
                pivot_bonus = calculate_pivot_boost(p1, p2)
                
                # Score adjustment
                scores = {"username": results['username_score'], "bio": results['bio_score'], "stylometry": results['stylometry_score'], "behaviour": results['behaviour_score'], "temporal": results['temporal_score'], "hyperlink": results['hyperlink_score'], "hashtag": results['hashtag_score']}
                active_scores = [s for s in scores.values() if s > 0.05]
                if active_scores:
                    results['fusion_score'] = min(1.0, (sum(active_scores) / len(active_scores)) + pivot_bonus)
                
                # SAVE TO STATE
                st.session_state.results = results
                st.session_state.p1 = p1
                st.session_state.p2 = p2
                st.session_state.fusion_score = results.get('fusion_score', 0.0)
                st.session_state.report_text = None

    # 3. Display Results from State
    if st.session_state.results:
        res = st.session_state.results
        fusion = st.session_state.fusion_score
        
        st.success("Fusion Engine Analysis Complete")
        st.metric("Adjusted Identity Confidence", f"{fusion * 100:.1f}%")
        st.progress(float(min(fusion, 1.0)))
        
        st.write("### Feature Breakdown")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Username", f"{res.get('username_score', 0):.3f}")
        m2.metric("Stylometry", f"{res.get('stylometry_score', 0):.3f}")
        m3.metric("Behavior", f"{res.get('behaviour_score', 0):.3f}")
        m4.metric("Temporal", f"{res.get('temporal_score', 0):.3f}")
        
        m5, m6, m7, m8 = st.columns(4)
        m5.metric("Bio", f"{res.get('bio_score', 0):.3f}")
        m6.metric("Emoji", f"{res.get('emoji_score', 0):.3f}")
        m7.metric("Hyperlinks", f"{res.get('hyperlink_score', 0):.3f}")
        m8.metric("Hashtags", f"{res.get('hashtag_score', 0):.3f}")
        
        # 4. GLITCH-FREE BUTTON
        if st.button("Generate Security Disclosure Report", type="secondary"):
            from modules.vulnerability_reporter import generate_vulnerability_disclosure
            st.session_state.report_text = generate_vulnerability_disclosure(
                st.session_state.p1, st.session_state.p2, st.session_state.fusion_score
            )
        
        if st.session_state.report_text:
            st.markdown(st.session_state.report_text)
            st.download_button("Download Disclosure", st.session_state.report_text, file_name="disclosure.md")
    else:
        st.warning("Please provide handles or URLs for both targets.")