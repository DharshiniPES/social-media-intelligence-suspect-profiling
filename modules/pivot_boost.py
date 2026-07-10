def calculate_pivot_boost(evidence1, evidence2):
    """
    Returns a float (0.0 to 0.4) to boost fusion score 
    if hard identifiers match.
    """
    boost = 0.0
    
    # 1. Email Intersection (The 'Gold Standard' link)
    # If the same email exists in both, it's almost certainly the same person
    if set(evidence1.emails) & set(evidence2.emails):
        boost += 0.35
        
    # 2. Portfolio Match (Matching personal websites)
    # Exclude common hosting domains like github.com
    links1 = {l for l in evidence1.hyperlinks if 'github.com' not in l}
    links2 = {l for l in evidence2.hyperlinks if 'github.com' not in l}
    
    if links1.intersection(links2):
        boost += 0.25
        
    return min(0.4, boost) # Cap the total boost to keep it balanced