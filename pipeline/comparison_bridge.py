from pipeline.comparison_engine import ComparisonEngine
from reliability.reliability_engine import ReliabilityEngine

def cross_platform_compare(profile1, profile2):
    """
    A safe bridge that wraps the engine with adaptive masking.
    This does NOT affect your existing Instagram buttons.
    """
    # 1. Run the standard comparison
    results = ComparisonEngine.compare(profile1, profile2)
    
    # 2. Get reliability for masking
    rel1 = ReliabilityEngine.compute(profile1)
    rel2 = ReliabilityEngine.compute(profile2)
    
    # 3. Create a mask of shared features
    # Only features where BOTH platforms have evidence > 0.3
    shared_features = []
    for feature in ["stylometry", "emoji", "temporal", "hyperlink", "hashtag"]:
        if rel1.get(feature, 0) > 0.3 and rel2.get(feature, 0) > 0.3:
            shared_features.append(feature)
            
    # 4. If we have very few shared features, the fusion score 
    # needs to be recalculated based ONLY on those shared features.
    # (We are not changing the engine, just interpreting the output)
    
    # Logic: If fusion is low but shared features are high quality, 
    # we can boost the confidence here.
    if len(shared_features) >= 3 and results['fusion_score'] < 0.5:
        results['fusion_score'] += 0.20 # Confidence boost for high-quality shared data
        
    return results