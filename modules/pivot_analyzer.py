import re
from urllib.parse import urlparse

def extract_advanced_pivots(text):
    """
    Scans unstructured text (tweets, bios, or posts) to extract high-value
    forensic markers: emails, phone numbers, website links, phone models, and locations.
    """
    # 1. Regex patterns for core infrastructure
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Matches various phone patterns (e.g., +91 98765 43210, 123-456-7890)
    phone_pattern = r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    url_pattern = r'https?://[^\s]+'
    
    # 2. Regex signatures for common mobile devices/phone models
    # This catches strings like "Sent from my iPhone 15", "Pixel 8 Pro", "Samsung S24"
    device_pattern = r'(iphone\s?\d*|ipad|android|samsung\s?s\d+|pixel\s?\d+|oneplus|xiaomi)'
    
    # 3. Basic keyword extractor for explicit locations (e.g., "Based in Bangalore", "Lives in Mumbai")
    location_keywords = r'(?:lives\s+in|based\s+in|location:?|from\s+)\s*([a-zA-Z\s]+)'

    # Find matches (case-insensitive for text fields)
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    urls = re.findall(url_pattern, text)
    devices = re.findall(device_pattern, text.lower())
    locations = re.findall(location_keywords, text.lower())

    return {
        "emails": emails,
        "phones": phones,
        "urls": urls,
        "devices": [d.strip() for d in devices],
        "locations": [l.strip() for l in locations]
    }

def calculate_pivot_similarity(pivots1, pivots2):
    """
    Compares the extracted pivots between two profiles.
    Returns a similarity score between 0.0 (no match) and 1.0 (perfect infrastructure overlap).
    """
    score = 0.0
    matches_found = 0
    
    # Check 1: Exact Email match
    if pivots1["emails"] and pivots2["emails"]:
        matches_found += 1
        if set(pivots1["emails"]).intersection(set(pivots2["emails"])):
            score += 0.30  # High weight: sharing an identical email address
            
    # Check 2: Exact Phone number match
    if pivots1["phones"] and pivots2["phones"]:
        matches_found += 1
        if set(pivots1["phones"]).intersection(set(pivots2["phones"])):
            score += 0.30  # High weight: sharing an identical phone number

    # Check 3: Domain overlap (Checks if they link to the exact same website net location)
    if pivots1["urls"] and pivots2["urls"]:
        matches_found += 1
        domains1 = {urlparse(u).netloc for u in pivots1["urls"]}
        domains2 = {urlparse(u).netloc for u in pivots2["urls"]}
        if domains1.intersection(domains2):
            score += 0.15

    # Check 4: Device/Phone Model alignment
    if pivots1["devices"] and pivots2["devices"]:
        matches_found += 1
        if set(pivots1["devices"]).intersection(set(pivots2["devices"])):
            score += 0.15  # Supporting evidence: matching device model type

    # Check 5: Extracted text Location alignment
    if pivots1["locations"] and pivots2["locations"]:
        matches_found += 1
        if set(pivots1["locations"]).intersection(set(pivots2["locations"])):
            score += 0.10  # Supporting evidence: matching regional keywords

    # If no overlapping attributes were present to evaluate, default to 0
    if matches_found == 0:
        return 0.0
        
    # Cap score cleanly between 0.0 and 1.0
    return round(min(score, 1.0), 3)