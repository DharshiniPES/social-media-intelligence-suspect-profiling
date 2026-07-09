from datetime import datetime

def evidence_to_behavior_profile(evidence):
    """
    Convert EvidenceProfile into the format expected by
    behavioral_fingerprint.py
    """

    active_hours = []

    for ts in evidence.timestamps:
        try:
            active_hours.append(
                datetime.fromisoformat(ts).hour
            )
        except:
            pass

    return {
        "posts": " ".join(evidence.captions),
        "active_hours": active_hours or [0],
        "hashtags": evidence.hashtags
    }