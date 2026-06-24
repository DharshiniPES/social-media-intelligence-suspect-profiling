import streamlit as st
st.sidebar.title(
    "SOCMINT"
)

st.sidebar.caption(
    "Suspect Profiling System"
)

st.sidebar.divider()
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from database.db_manager import DatabaseManager
from modules.risk_tracker import risk_level
from modules.report_generator import (
    generate_report,
    save_report
)
from modules.contribution_engine import (
    get_contribution_data
)
# ==========================
# LOAD DATA
# ==========================

from modules.real_dataset_loader import RealDatasetLoader

loader = RealDatasetLoader(
    "datasets/real/bot_detection_data.csv"
)

profiles = loader.load_profiles(limit=100)

df = pd.DataFrame(profiles)

db = DatabaseManager()

comparisons = db.get_comparisons()

# ==========================
# SIDEBAR NAVIGATION
# ==========================

page = st.sidebar.selectbox(

    "Navigation",

    [
        "Case Summary",
        "Profile Analysis",
        "Identity Linkage Results",
        "Network Centrality Ranking",
        "Evidence Explorer",
        "Risk Assesment",
        "Community Detection",
        "Community Risk Ranking",
        "Investigation Narrative",
        "Export Investigation Package",
        "Account Risk Ranking",
        "Investigator Notes",
        "Investigation Reports",
        "Feature Contribution Analysis",
        "Correlation Heatmap",
        "System Evaluation",
        "Identity Linkage Network"
    ]
)


# ==========================
# PROFILES PAGE
# ==========================
if page == "Case Summary":

    st.title(
        "SOCMINT Case Summary"
    )

    total_profiles = len(
        profiles
    )

    total_comparisons = len(
        comparisons
    )


    linked_accounts = len(

        [
            row

            for row in comparisons

            if row[13] == 1
        ]
    )

    highest_score = max(

        row[11]

        for row in comparisons

    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Profiles Analysed",

            total_profiles
        )

        st.metric(

            "Total Comparisons",

            total_comparisons
        )

    with col2:

        st.metric(

            "Linked Accounts",

            linked_accounts
        )

        st.metric(

            "Highest Fusion Score",

            round(
                highest_score,
                3
            )
        )

    st.subheader(
        "Investigation Overview"
    )

    st.info(

        f"""
        Profiles Analysed: {total_profiles}

        Comparisons Performed: {total_comparisons}

        Linked Accounts Detected: {linked_accounts}

        Highest Fusion Score: {round(highest_score,3)}
        """
    )

    account_scores = {}

    for row in comparisons:

        profile1 = row[1]
        profile2 = row[2]

        fusion_score = row[10]

        account_scores[profile1] = (

            account_scores.get(
                profile1,
                0
            )

            +

            fusion_score
        )

        account_scores[profile2] = (

            account_scores.get(
                profile2,
                0
            )

            +

            fusion_score
        )

    most_suspicious = max(

        account_scores,

        key=account_scores.get
    )

    st.subheader(
        "Top Suspicious Account"
    )

    st.success(

        f"""
        Account ID: {most_suspicious}

        Risk Score:
        {round(account_scores[most_suspicious],3)}
        """
    )

elif page == "Profile Analysis":

    st.title(
        "Profile Analysis"
    )

    st.header(
        "Social Media Intelligence Dashboard"
    )
    total_profiles = len(profiles)

    total_comparisons = len(comparisons)

    linked_accounts = sum(
        1 for row in comparisons
        if row[13] == 1
    )
    fusion_scores = [
        row[11]
        for row in comparisons
    ]

    if len(fusion_scores) > 0:

        avg_fusion = round(
            sum(fusion_scores)
            / len(fusion_scores),
            3
        )

    else:

        avg_fusion = 0

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Profiles",
            total_profiles
        )

    with col2:
        st.metric(
            "Comparisons",
            total_comparisons
        )

    with col3:
        st.metric(
            "Linked",
            linked_accounts
        )
    with col4:
        st.metric(
            "Avg Fusion",
            avg_fusion
        )
    highest_fusion = max(
        row[11]
        for row in comparisons
    )

    with col5:
        st.metric(
            "Highest Fusion",
            round(highest_fusion, 3)
        )

    st.subheader(
        "Profile Dataset"
    )

    st.dataframe(
        df
    )

    st.subheader(
        "System Information"
    )

    st.write(
        "Total Profiles:",
        len(profiles)
    )


# ==========================
# LINKAGE RESULTS PAGE
# ==========================
elif page == "Identity Linkage Results":

    st.title(
        "Identity Linkage Results"
    )

    results = []

    for row in comparisons:

        profile1 = row[1]
        profile2 = row[2]

        fusion_score = row[11]
        explanation = row[12]
        linked = row[13]

        if linked == 1:

            status = "LINKED"

        else:

            status = "NOT LINKED"

        results.append(

            {
                "Profile 1": profile1,

                "Profile 2": profile2,

                "Fusion Score": round(
                    fusion_score,
                    3
                ),

                "Confidence %": round(
                    fusion_score * 100,
                    2
                ),

                "Explanation":
                explanation,

                "Risk": risk_level(
                    fusion_score
                ),

                "Status": status
            }
        )

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        by="Fusion Score",
        ascending=False
    )

    st.dataframe(
        results_df
    )
# =========================
# RISK TRACKER PAGE
# =========================
elif page == "Risk Assesment":

    st.title(
        "Risk Assessment"
    )

    risk_data = []

    for row in comparisons:

        profile1 = row[1]
        profile2 = row[2]

        fusion_score = row[11]

        risk_data.append(

            {
                "Profile Pair":
                f"{profile1} - {profile2}",

                "Fusion Score":
                round(
                    fusion_score,
                    3
                ),

                "Confidence %":
                round(
                    fusion_score * 100,
                    2
                ),

                "Risk":
                risk_level(
                    fusion_score
                )
            }
        )

    risk_df = pd.DataFrame(
        risk_data
    )

    risk_df = risk_df.sort_values(
        by="Fusion Score",
        ascending=False
    )

    st.dataframe(
        risk_df
    )
# ==========================
# EVALUATION PAGE
# ==========================
elif page == "Community Detection":

    st.title(
        "Community Detection"
    )

    from modules.network_analysis import (
        build_graph,
        add_link,
        detect_communities
    )

    G = build_graph(profiles)

    for row in comparisons:

        if row[13] == 1:

            add_link(
                G,
                row[1],
                row[2],
                row[10]
            )

    communities = detect_communities(G)

    for i, community in enumerate(
        communities,
        start=1
    ):

        st.subheader(
            f"Community {i}"
        )

        st.markdown(
            "**Members:**"
        )

        for member in community:

            st.write(
                f"• {member}"
            )
elif page == "Account Risk Ranking":

    st.title(
        "Account Risk Ranking"
    )

    account_scores = {}

    for row in comparisons:

        profile1 = row[1]
        profile2 = row[2]

        fusion_score = row[10]

        if profile1 not in account_scores:

            account_scores[profile1] = 0

        if profile2 not in account_scores:

            account_scores[profile2] = 0

        account_scores[profile1] += fusion_score

        account_scores[profile2] += fusion_score

    ranking = []

    for account, score in account_scores.items():

        ranking.append(

            {
                "Account": account,
                "Risk Score": round(
                    score,
                    3
                )
            }
        )

    ranking_df = pd.DataFrame(
        ranking
    )

    ranking_df = ranking_df.sort_values(

        by="Risk Score",

        ascending=False
    )
    ranking_df.reset_index(
        drop=True,
        inplace=True
    )

    ranking_df.index += 1

    st.dataframe(
        ranking_df
    )
elif page == "Investigator Notes":

    st.title(
        "Investigator Notes"
    )

    account_id = st.text_input(
        "Account ID"
    )

    note = st.text_area(
        "Investigation Note"
    )

    if st.button(
        "Save Note"
    ):

        db.save_note(
            account_id,
            note
        )

        st.success(
            "Note Saved"
        )

    notes = db.get_notes()

    st.subheader(
        "Saved Notes"
    )

    notes_data = []

    for row in notes:

        notes_data.append(

            {
                "Account ID": row[1],
                "Note": row[2]
            }
        )

    st.dataframe(
        pd.DataFrame(
            notes_data
        )
    )
elif page == "Investigation Reports":

    st.title(
        "Investigation Reports"
    )

    account_id = st.text_input(
        "Account ID"
    )

    risk_score = st.number_input(
        "Risk Score",
        value=0.0
    )

    explanation = st.text_area(
        "Explanation"
    )

    notes = st.text_area(
        "Investigator Notes"
    )

    if st.button(
        "Generate Report"
    ):

        report = generate_report(

            account_id,

            risk_score,

            explanation,

            notes
        )

        filename = save_report(

            account_id,

            report
        )

        st.success(
            f"Report saved to {filename}"
        )

        st.text(report)
elif page == "Community Risk Ranking":

    st.title(
        "Community Risk Ranking"
    )

    from modules.network_analysis import (
        build_graph,
        add_link,
        detect_communities
    )

    G = build_graph(
        profiles
    )

    for row in comparisons:

        if row[13] == 1:

            add_link(

                G,

                row[1],

                row[2],

                row[10]
            )

    communities = detect_communities(
        G
    )

    community_data = []

    for i, community in enumerate(

        communities,

        start=1

    ):

        risk_scores = []

        for row in comparisons:

            profile1 = row[1]
            profile2 = row[2]

            if (

                profile1 in community

                and

                profile2 in community

            ):

                risk_scores.append(
                    row[10]
                )

        if len(risk_scores) > 0:

            avg_risk = round(

                sum(risk_scores)

                /

                len(risk_scores),

                3
            )

        else:

            avg_risk = 0

        community_data.append(

            {
                "Community": i,

                "Members":
                len(
                    community
                ),

                "Average Risk":
                avg_risk
            }
        )

    community_df = pd.DataFrame(
        community_data
    )

    community_df = community_df.sort_values(

        by="Average Risk",

        ascending=False
    )
    community_df.reset_index(
        drop=True,
        inplace=True
    )

    community_df.index += 1
    st.dataframe(
        community_df
    )
elif page == "Feature Contribution Analysis":

    st.title(
        "Feature Contribution Analysis"
    )

    contribution_data = []

    for row in comparisons:

        contribution_data.append(

            {
                "Username":
                round(
                    row[3],
                    3
                ),

                "Stylometry":
                round(
                    row[5],
                    3
                ),
                "Behavior":
                round(row[10], 3),

                "Temporal":
                round(
                    row[7],
                    3
                ),

                "Fusion":
                round(
                    row[11],
                    3
                )
            }
        )

    contribution_df = pd.DataFrame(
        contribution_data
    )
    contribution_df = contribution_df.sort_values(
        by="Fusion",
        ascending=False
    )

    contribution_df.reset_index(
        drop=True,
        inplace=True
    )

    contribution_df.index += 1

    st.dataframe(
        contribution_df
    )
    st.subheader(
        "Fusion Score Distribution"
    )

    st.bar_chart(
        contribution_df["Fusion"]
    )
elif page == "System Evaluation":

    st.title(
        "System Evaluation"
    )

    thresholds = [
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60
    ]

    threshold_data = []

    for threshold in thresholds:

        linked_count = sum(

            1

            for row in comparisons

            if row[11] >= threshold

        )

        threshold_data.append(

            {
                "Threshold":
                threshold,

                "Linked Accounts":
                linked_count
            }

        )

    threshold_df = pd.DataFrame(
        threshold_data
    )

    st.subheader(
        "Threshold Sensitivity Analysis"
    )

    st.dataframe(
        threshold_df
    )

    st.subheader(
        "Threshold vs Linked Accounts"
    )

    st.line_chart(
        threshold_df.set_index(
            "Threshold"
        )
    )

    st.info(

        """
        Threshold sensitivity analysis helps determine
        the optimal fusion score threshold for identity
        linkage detection.

        Higher thresholds reduce false positives but may
        miss legitimate linked accounts.

        Lower thresholds increase detection sensitivity
        but may introduce false positives.
        """
    )

    best_threshold = 0.50

    st.success(

        f"""
        Current Operational Threshold: {best_threshold}

        Linked Accounts Detected:
        {
            sum(
                1
                for row in comparisons
                if row[11] >= best_threshold
            )
        }
        """
    )
    fusion_scores = [
        row[11]
        for row in comparisons
    ]

    fusion_df = pd.DataFrame(
        {"Fusion Score": fusion_scores}
    )

    st.subheader(
        "Fusion Score Distribution"
    )

    st.bar_chart(
        fusion_df["Fusion Score"]
    )
elif page == "Correlation Heatmap":

    st.title(
        "Feature Correlation Heatmap"
    )

    heatmap_data = []

    for row in comparisons:

        heatmap_data.append(

            {

                "Username":
                row[3],

                "Bio":
                row[4],

                "Stylometry":
                row[5],

                "Emoji":
                row[6],

                "Temporal":
                row[7],

                "Hyperlink":
                row[8],

                "Hashtag":
                row[9],

                "Behavior":
                row[10],

                "Fusion":
                row[11]

            }

        )

    heatmap_df = pd.DataFrame(
        heatmap_data
    )

    correlation_matrix = (
        heatmap_df.corr()
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    sns.heatmap(

        correlation_matrix,

        annot=True,

        cmap="Blues",

        ax=ax

    )

    st.pyplot(
        fig
    )
# ==========================
# NETWORK GRAPH PAGE
# ==========================

elif page == "Identity Linkage Network":

    st.title(
        "Identity Linkage Network"
    )

    from modules.network_analysis import (

        build_graph,

        add_link,

        generate_interactive_graph

    )

    G = build_graph(
        profiles
    )

    for row in comparisons:

        if row[13] == 1:

            add_link(

                G,

                row[1],

                row[2],

                row[11]

            )

    generate_interactive_graph(
        G
    )

    with open(

        "network_graph.html",

        "r",

        encoding="utf-8"

    ) as f:

        html = f.read()

    st.components.v1.html(

        html,

        height=800,

        scrolling=True

    )
elif page == "Network Centrality Ranking":

    st.title(
        "Network Centrality Ranking"
    )

    from modules.network_analysis import (
        build_graph,
        add_link,
        calculate_centrality
    )

    G = build_graph(
        profiles
    )

    for row in comparisons:

        if row[13] == 1:

            add_link(

                G,

                row[1],

                row[2],

                row[11]

            )

    ranking = calculate_centrality(
        G
    )

    ranking_data = []

    for account, score in ranking:

        ranking_data.append(

            {
                "Account":
                account,

                "Centrality":
                round(
                    score,
                    4
                )
            }

        )

    ranking_df = pd.DataFrame(
        ranking_data
    )

    ranking_df.index += 1

    st.dataframe(
        ranking_df
    )
elif page == "Evidence Explorer":

    st.title(
        "Evidence Explorer"
    )

    profile_ids = [

        profile["id"]

        for profile in profiles

    ]

    selected_id = st.selectbox(

        "Select Account",

        profile_ids

    )

    selected_profile = next(

        profile

        for profile in profiles

        if profile["id"] == selected_id

    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Account Information"
        )

        st.write(
            "Account ID:",
            selected_profile["id"]
        )

        st.write(
            "Username:",
            selected_profile["username"]
        )

        st.write(
            "Followers:",
            selected_profile["followers"]
        )

        st.write(
            "Verified:",
            selected_profile["verified"]
        )

        st.write(
            "Bot Label:",
            selected_profile["bot_label"]
        )

    with col2:

        st.subheader(
            "Behaviour Profile"
        )

        st.write(
            "Active Hour:",
            selected_profile["active_hours"][0]
        )

        st.write(
            "Retweets:",
            selected_profile["retweets"]
        )

        st.write(
            "Hashtag Count:",
            len(
                selected_profile["hashtags"]
            )
        )

        st.write(
            "Link Count:",
            len(
                selected_profile["links"]
            )
        )

    st.divider()

    st.subheader(
        "Post Content"
    )

    st.text_area(

        "Tweet",

        selected_profile["posts"],

        height=150

    )

    st.subheader(
        "Hashtags"
    )

    st.write(

        selected_profile["hashtags"]

    )

    st.subheader(
        "Shared Links"
    )

    st.write(

        selected_profile["links"]

    )
elif page == "Investigation Narrative":

    st.title(
        "Investigation Narrative"
    )

    if len(comparisons) == 0:

        st.warning(
            "No comparison data available."
        )

    else:

        best_match = max(
            comparisons,
            key=lambda row: row[11]
        )

        profile1 = best_match[1]
        profile2 = best_match[2]

        username = best_match[3]
        bio = best_match[4]
        stylometry = best_match[5]
        emoji = best_match[6]
        temporal = best_match[7]
        hyperlink = best_match[8]
        hashtag = best_match[9]
        behavior = best_match[10]

        fusion = best_match[11]

        narrative = f"""
INVESTIGATION SUMMARY

Account Pair:
{profile1} ↔ {profile2}

Similarity Evidence

• Username Similarity: {round(username,3)}
• Bio Similarity: {round(bio,3)}
• Stylometry Similarity: {round(stylometry,3)}
• Emoji Similarity: {round(emoji,3)}
• Temporal Similarity: {round(temporal,3)}
• Hyperlink Similarity: {round(hyperlink,3)}
• Hashtag Similarity: {round(hashtag,3)}
• Behavioral Similarity: {round(behavior,3)}

Fusion Score:
{round(fusion,3)}

Assessment:

This account pair exhibits multiple
behavioral and content-based similarities.

The fusion score indicates a potential
identity linkage candidate requiring
further investigation by analysts.
"""

        st.text_area(
            "Generated Narrative",
            narrative,
            height=500
        )
elif page == "Export Investigation Package":

    st.title(
        "Export Investigation Package"
    )

    if st.button(
        "Generate Case Package"
    ):

        os.makedirs(
            "reports",
            exist_ok=True
        )

        # =====================
        # CASE SUMMARY
        # =====================

        total_profiles = len(
            profiles
        )

        total_comparisons = len(
            comparisons
        )

        linked_accounts = sum(

            1

            for row in comparisons

            if row[13] == 1

        )

        highest_fusion = max(

            row[11]

            for row in comparisons

        )

        with open(

            "reports/case_summary.txt",

            "w",

            encoding="utf-8"

        ) as f:

            f.write(

                f"""
SOCMINT CASE SUMMARY

Profiles Analysed:
{total_profiles}

Comparisons:
{total_comparisons}

Linked Accounts:
{linked_accounts}

Highest Fusion Score:
{round(highest_fusion,3)}
"""
            )

        # =====================
        # LINKED ACCOUNTS CSV
        # =====================

        linked_data = []

        for row in comparisons:

            if row[13] == 1:

                linked_data.append(

                    {
                        "Profile1":
                        row[1],

                        "Profile2":
                        row[2],

                        "Fusion Score":
                        row[11]
                    }
                )

        linked_df = pd.DataFrame(
            linked_data
        )

        linked_df.to_csv(

            "reports/linked_accounts.csv",

            index=False

        )

        # =====================
        # RISK RANKING CSV
        # =====================

        account_scores = {}

        for row in comparisons:

            profile1 = row[1]
            profile2 = row[2]

            fusion_score = row[11]

            account_scores[profile1] = (

                account_scores.get(
                    profile1,
                    0
                )

                +

                fusion_score

            )

            account_scores[profile2] = (

                account_scores.get(
                    profile2,
                    0
                )

                +

                fusion_score

            )

        ranking = []

        for account, score in account_scores.items():

            ranking.append(

                {
                    "Account":
                    account,

                    "Risk Score":
                    round(
                        score,
                        3
                    )
                }

            )

        ranking_df = pd.DataFrame(
            ranking
        )

        ranking_df = ranking_df.sort_values(

            by="Risk Score",

            ascending=False

        )

        ranking_df.to_csv(

            "reports/risk_rankings.csv",

            index=False

        )

        st.success(

            """
Case package generated successfully.

Files Created:

• case_summary.txt

• linked_accounts.csv

• risk_rankings.csv
"""
        )