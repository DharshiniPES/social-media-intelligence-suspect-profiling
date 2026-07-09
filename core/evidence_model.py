from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class EvidenceProfile:
    """
    Universal evidence model used by all social media platforms.
    Every collector should normalize into this structure.
    """

    # -------------------------
    # Identity Information
    # -------------------------
    username: str = ""
    display_name: str = ""
    bio: str = ""
    profile_url: str = ""
    profile_image: str = ""
    verified: bool = False
    platform: str = ""

    # -------------------------
    # Network Information
    # -------------------------
    followers: int = 0
    following: int = 0
    posts_count: int = 0

    # -------------------------
    # Content
    # -------------------------
    posts: List[Dict[str, Any]] = field(default_factory=list)

    # -------------------------
    # Extracted Features
    # -------------------------
    captions: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)
    hyperlinks: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)
    emojis: List[str] = field(default_factory=list)

    # -------------------------
    # Temporal Information
    # -------------------------
    timestamps: List[str] = field(default_factory=list)

    # -------------------------
    # Raw Response
    # -------------------------
    raw_data: Dict[str, Any] = field(default_factory=dict)