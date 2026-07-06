import streamlit as st

# Setup page config FIRST - must be the absolute first Streamlit command
st.set_page_config(page_title="SOCMINT Suspect Profiling System", layout="wide")

st.sidebar.title("SOCMINT")
st.sidebar.caption("Suspect Profiling System")
st.sidebar.divider()

# --- HIGH-SPEED SPEED INTEGRATION CHECKPOINTS ---
# Using @st.cache_resource for data connections and heavy ML libraries
@st.cache_resource
def load_system_dependencies():
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import os
    from database.db_manager import DatabaseManager
    return pd, sns, plt, os, DatabaseManager()

# Using @st.cache_data to hold your static CSV profile allocations in memory
@st.cache_data
def load_socmint_profiles():
    from modules.real_dataset_loader import RealDatasetLoader
    loader = RealDatasetLoader("datasets/real/bot_detection_data.csv")
    raw_profiles = loader.load_profiles(limit=100)
    return raw_profiles, load_system_dependencies()[0].DataFrame(raw_profiles)

# Execute fast-load caching
pd, sns, plt, os, db = load_system_dependencies()
profiles, df = load_socmint_profiles()
comparisons = db.get_comparisons()

# --- STANDALONE IMPORTS ---
from modules.risk_tracker import risk_level
from modules.report_generator import generate_report, save_report
from modules.contribution_engine import get_contribution_data
from modules.pivot_analyzer import extract_advanced_pivots
from modules.scraper_collector import live_scrape_profile
from modules.multimodal_vision import extract_text_from_profile_image
from modules.vehicle_verifier import verify_and_route_vehicle

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
        "Identity Linkage Network",
        "Live Target Web Scraper",
        "Multimodal OCR Extractor",
        "Vehicle RC/DL Verification"
    ]
)

# ==========================
# 1. CASE SUMMARY
# ==========================
if page == "Case Summary":
    st.title("SOCMINT Case Summary")
    
    total_profiles = len(profiles)
    total_comparisons = len(comparisons)
    linked_accounts = len([row for row in comparisons if row[13] == 1])
    highest_score = max(row[11] for row in comparisons) if comparisons else 0.0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Profiles Analysed", total_profiles)
        st.metric("Total Comparisons", total_comparisons)
    with col2:
        st.metric("Linked Accounts", linked_accounts)
        st.metric("Highest Fusion Score", round(highest_score, 3))

    st.subheader("Investigation Overview")
    st.info(f"""
        Profiles Analysed: {total_profiles}
        Comparisons Performed: {total_comparisons}
        Linked Accounts Detected: {linked_accounts}
        Highest Fusion Score: {round(highest_score, 3)}
    """)

    account_scores = {}
    for row in comparisons:
        profile1, profile2, fusion_score = row[1], row[2], row[10]
        account_scores[profile1] = account_scores.get(profile1, 0) + fusion_score
        account_scores[profile2] = account_scores.get(profile2, 0) + fusion_score

    if account_scores:
        most_suspicious = max(account_scores, key=account_scores.get)
        st.subheader("Top Suspicious Account")
        st.success(f"""
            Account ID: {most_suspicious}
            Risk Score: {round(account_scores[most_suspicious], 3)}
        """)

# ==========================
# 2. PROFILE ANALYSIS
# ==========================
elif page == "Profile Analysis":
    st.title("Profile Analysis")
    st.header("Social Media Intelligence Dashboard")
    
    total_profiles = len(profiles)
    total_comparisons = len(comparisons)
    linked_accounts = sum(1 for row in comparisons if row[13] == 1)
    fusion_scores = [row[11] for row in comparisons]
    avg_fusion = round(sum(fusion_scores) / len(fusion_scores), 3) if fusion_scores else 0
    highest_fusion = max(row[11] for row in comparisons) if comparisons else 0.0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Profiles", total_profiles)
    with col2: st.metric("Comparisons", total_comparisons)
    with col3: st.metric("Linked", linked_accounts)
    with col4: st.metric("Avg Fusion", avg_fusion)
    with col5: st.metric("Highest Fusion", round(highest_fusion, 3))

    st.subheader("Profile Dataset")
    st.dataframe(df)
    st.subheader("System Information")
    st.write("Total Profiles:", len(profiles))

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

# ==========================
# 11. SYSTEM EVALUATION
# ==========================
elif page == "System Evaluation":
    st.title("System Evaluation")
    thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
    threshold_data = []
    for t in thresholds:
        linked_count = sum(1 for row in comparisons if row[11] >= t)
        threshold_data.append({"Threshold": t, "Linked Accounts": linked_count})
    
    threshold_df = pd.DataFrame(threshold_data)
    st.subheader("Threshold Sensitivity Analysis")
    st.dataframe(threshold_df)
    st.subheader("Threshold vs Linked Accounts")
    st.line_chart(threshold_df.set_index("Threshold"))
    
    st.info("Threshold sensitivity analysis helps determine the optimal fusion score threshold.")
    best_threshold = 0.50
    st.success(f"Operational Threshold: {best_threshold} | Detected: {sum(1 for row in comparisons if row[11] >= best_threshold)}")
    
    fusion_scores = [row[11] for row in comparisons]
    st.subheader("Fusion Score Distribution")
    st.bar_chart(pd.DataFrame({"Fusion Score": fusion_scores})["Fusion Score"])

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

# ==========================
# 15. EVIDENCE EXPLORER
# ==========================
elif page == "Evidence Explorer":
    st.title("Evidence Explorer")
    profile_ids = [profile["id"] for profile in profiles]
    selected_id = st.selectbox("Select Account", profile_ids)
    selected_profile = next(p for p in profiles if p["id"] == selected_id)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Account Information")
        st.write("Account ID:", selected_profile["id"])
        st.write("Username:", selected_profile["username"])
        st.write("Followers:", selected_profile["followers"])
        st.write("Verified:", selected_profile["verified"])
        st.write("Bot Label:", selected_profile["bot_label"])
    with col2:
        st.subheader("Behaviour Profile")
        st.write("Active Hour:", selected_profile["active_hours"][0])
        st.write("Retweets:", selected_profile["retweets"])
        st.write("Hashtag Count:", len(selected_profile["hashtags"]))
        st.write("Link Count:", len(selected_profile["links"]))

    st.divider()
    
    st.subheader("🔍 Extracted Infrastructure Pivots")
    combined_text = str(selected_profile.get("posts", "")) + " " + str(selected_profile.get("bio", ""))
    extracted = extract_advanced_pivots(combined_text)
    
    pcol1, pcol2, pcol3 = st.columns(3)
    with pcol1:
        st.markdown("**Identified Emails:**")
        st.write(extracted["emails"] if extracted["emails"] else "None Extracted")
    with pcol2:
        st.markdown("**Identified Phones:**")
        st.write(extracted["phones"] if extracted["phones"] else "None Extracted")
    with pcol3:
        st.markdown("**Device Models / Locations:**")
        st.write(f"Devices: {extracted['devices']} | Regions: {extracted['locations']}")

    st.divider()
    st.subheader("Post Content")
    st.text_area("Tweet", selected_profile["posts"], height=150)
    st.subheader("Hashtags")
    st.write(selected_profile["hashtags"])
    st.subheader("Shared Links")
    st.write(selected_profile["links"])

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

# ==========================
# --- FORENSIC INTERFACES ---
# ==========================
elif page == "Live Target Web Scraper":
    st.title("🌐 Controlled Target Profile Scraper")
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
    st.title("👁️ Multimodal Image Analysis & OCR Engine")
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
    st.title("🚘 Logistical Asset Router (Vehicle RC/DL Verification)")
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
                st.markdown("### 🛠️ Gateway Diagnostic Logs:")
                for log in v_res["metadata"]["Gateway Error Trails"]:
                    st.error(log)