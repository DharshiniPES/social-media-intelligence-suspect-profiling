import json
from modules.feature_contribution import feature_contributions
from modules.behavioral_fingerprint import fingerprint_similarity
from modules.explanation_engine import generate_explanation
from database.db_manager import DatabaseManager
from evaluation import *
from modules.hashtag_analysis import hashtag_score
from modules.hyperlink_analysis import hyperlink_score
from modules.username_similarity import username_score
from modules.bio_similarity import bio_score
from modules.stylometry import stylometry_score
from modules.emoji_analysis import emoji_score
from modules.temporal_analysis import temporal_score
from modules.bot_risk_analysis import bot_risk_score
from modules.network_analysis import (
    build_graph,
    add_link,
    draw_graph,
    detect_communities
)
from fusion.fusion_engine import fusion_score
from modules.pivot_analyzer import extract_advanced_pivots, calculate_pivot_similarity
from modules.scraper_collector import live_scrape_profile
from modules.multimodal_vision import extract_text_from_profile_image
from modules.vehicle_verifier import verify_and_route_vehicle
from modules.active_watchdog import ActiveWatchdog
from modules.real_dataset_loader import RealDatasetLoader

# Initialize Metrics
tp, fp, fn, tn = 0, 0, 0, 0

# Load profiles
loader = RealDatasetLoader("datasets/real/bot_detection_data.csv")
profiles = loader.load_profiles(limit=100)

db = DatabaseManager()
db.create_tables()
G = build_graph(profiles)

# =====================================================================
# ⚡ OPTIMIZATION STEP: RUN SINGLE-PASS HEAVY OPERATIONS OUTSIDE LOOPS
# =====================================================================
print("[SYSTEM] Executing heavy forensic utility handshakes globally...")

# Run OCR exactly once instead of 200 times
ocr_result = extract_text_from_profile_image("data/placeholder_banner.png")

# Run Vehicle API verification exactly once instead of 200 times
vehicle_result = verify_and_route_vehicle("KA05NB1234")

# Pre-calculate infrastructure text pivots in a fast single linear loop
print("[SYSTEM] Pre-compiling advanced infrastructure pivots...")
profile_pivots = {}
for p in profiles:
    t = p.get("posts", p.get("text", ""))
    b = p.get("bio", p.get("description", ""))
    profile_pivots[p["id"]] = extract_advanced_pivots(t + " " + b)

print("[SYSTEM] Entering high-speed pairwise processing matrix...")
# =====================================================================

for i in range(len(profiles)):
    for j in range(i + 1, len(profiles)):
        if j > i + 2: 
            break 

        profile1 = profiles[i]
        profile2 = profiles[j]

        # Use our pre-calculated text pivots instantly (0 milliseconds)
        pivots1 = profile_pivots[profile1["id"]]
        pivots2 = profile_pivots[profile2["id"]]
        pivot_similarity = calculate_pivot_similarity(pivots1, pivots2)

        # Basic text extractions
        user_score = username_score(profile1["username"], profile2["username"])
        bio_similarity = 0  # Kept matching your default assignment
        
        style_score = stylometry_score(profile1["posts"], profile2["posts"])
        behavior_score = fingerprint_similarity(profile1, profile2)
        emoji_similarity = emoji_score(profile1["posts"], profile2["posts"])
        temporal_similarity = temporal_score(profile1["active_hours"], profile2["active_hours"])
        link_similarity = hyperlink_score(profile1["links"], profile2["links"])
        hashtag_similarity = hashtag_score(profile1["hashtags"], profile2["hashtags"])

        # Live scrape simulation (Only if needed, but skipped or mocked to prevent loop crashes)
        # To make it truly live without hanging, you can run this selectively or keep it commented out.

        # Calculate fusion matrix metrics
        final_score = fusion_score(
            user_score, bio_similarity, style_score, behavior_score,
            emoji_similarity, temporal_similarity, link_similarity, hashtag_similarity
        )
        
        explanations = generate_explanation(user_score, style_score, behavior_score, temporal_similarity)
        contributions = feature_contributions(user_score, style_score, behavior_score, temporal_similarity)
        explanation_text = ", ".join(explanations)
        
        risk_score = bot_risk_score(
            profile1.get("followers", 0),
            profile1.get("retweets", 0),
            profile1.get("verified", False)
        )

        # Print outputs
        print(f"\n========================================\n{profile1['id']} vs {profile2['id']}\n========================================")
        print("Bot Risk Score:", round(risk_score, 3))
        print("Username Score:", round(user_score, 3))
        print("Bio Score:", round(bio_similarity, 3))
        print("Stylometry Score:", round(style_score, 3))
        print("Behavior Score:", round(behavior_score, 3))
        print("Emoji Score:", round(emoji_similarity, 3))
        print("Temporal Score:", round(temporal_similarity, 3))
        print("Hyperlink Score:", round(link_similarity, 3))
        print("Hashtag Score:", round(hashtag_similarity, 3))
        print("Infrastructure Pivot Similarity:", round(pivot_similarity, 3))
        print("Fusion Score:", round(final_score, 3))
        
        print("Explanation:")
        for reason in explanations:
            print("-", reason)
            
        print("\nFeature Contributions:")
        for feature, score in contributions.items():
            print(f"{feature}: {round(score,3)}")

        print("Confidence:", round(final_score * 100, 2), "%")
        print("\n===================\nFINAL EVALUATION\n===================")

        p = precision(tp, fp)
        r = recall(tp, fn)
        f1 = f1_score(p, r)

        print("True Positives :", tp)
        print("False Positives:", fp)
        print("False Negatives:", fn)
        print("True Negatives :", tn)
        print("Precision:", round(p, 3))
        print("Recall:", round(r, 3))
        print("F1 Score:", round(f1, 3))

        predicted = (final_score >= 0.65)
        
        db.insert_comparison(
            profile1["id"], profile2["id"], user_score, bio_similarity,
            style_score, emoji_similarity, temporal_similarity, link_similarity,
            hashtag_similarity, behavior_score, final_score, explanation_text, int(predicted)
        )

        print("FINAL SCORE =", final_score)
        print("PREDICTED =", predicted)
        
        if predicted:
            add_link(G, profile1["id"], profile2["id"], final_score)
            print("LINKED")
        else:
            print("NOT LINKED")

# Finalize visualizations and triggers
draw_graph(G)
communities = detect_communities(G)

print("\n=== COMMUNITIES ===")
for i, community in enumerate(communities, start=1):
    print(f"Community {i}:", list(community))

print("\nNetwork graph generated.")

print("\n[WATCHDOG ENGINE] Execution sequence complete. Triggering timeline state snapshot...")
watchdog = ActiveWatchdog(db_path="database/socmint.db")
watchdog.orchestrate_state_snapshot()
print("[SYSTEM] All tracking operations successfully closed.")