from core.evidence_model import EvidenceProfile
from pipeline.comparison_engine import ComparisonEngine

profile1 = EvidenceProfile(
    username="johnsmith",
    bio="AI Researcher 🤖",
    captions=[
        "Learning #AI",
        "Building cool projects 🚀"
    ],
    hashtags=["AI", "Python"],
    hyperlinks=["https://github.com/john"],
    timestamps=[
        "2026-07-09T10:00:00",
        "2026-07-09T15:30:00"
    ]
)

profile2 = EvidenceProfile(
    username="john_smith",
    bio="AI Researcher 🤖",
    captions=[
        "Learning #AI",
        "Building amazing projects 🚀"
    ],
    hashtags=["AI", "Python"],
    hyperlinks=["https://github.com/john"],
    timestamps=[
        "2026-07-09T10:30:00",
        "2026-07-09T15:00:00"
    ]
)

result = ComparisonEngine.compare(profile1, profile2)

print(result)