from database.candidate_repository import CandidateRepository
from core.evidence_model import EvidenceProfile

repo = CandidateRepository()

profile = EvidenceProfile(
    username="test_user",
    platform="Instagram",
    display_name="Test User",
    bio="Testing Candidate Repository",
    profile_url="https://instagram.com/test_user",
    followers=100,
    following=50,
    posts_count=10
)

repo.save(profile)

print("Profile saved!")

print("Total Profiles:", repo.count())

print("\nAll Profiles:")

for row in repo.get_all():
    print(row)