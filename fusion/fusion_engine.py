def fusion_score(
    username_score,
    bio_score,
    stylometry_score,
    behavior_score,
    emoji_score,
    temporal_score,
    hyperlink_score,
    hashtag_score
):
    features = {
        "username": (username_score, 0.25),      
        "bio": (bio_score, 0.10),
        "stylometry": (stylometry_score, 0.30),  
        "behavior": (behavior_score, 0.10),
        "emoji": (emoji_score, 0.05),
        "temporal": (temporal_score, 0.05),
        "hyperlink": (hyperlink_score, 0.05),
        "hashtag": (hashtag_score, 0.10)
    }
    total_score = 0.0
    active_weight_sum = 0.0
    
    for name, (score, weight) in features.items():
        # If a feature is completely empty/missing, skip it 
        # so it doesn't penalize the final score.
        if name == "bio" and bio_score == 0:
            continue
        if name == "hyperlink" and hyperlink_score == 0:
            continue
        if name == "emoji" and emoji_score == 0:
            continue
            
        total_score += score * weight
        active_weight_sum += weight
        
    # Re-normalize weights dynamically
    if active_weight_sum > 0:
        final_bounded_score = total_score / active_weight_sum
    else:
        final_bounded_score = 0.0
        
    return round(final_bounded_score, 3)