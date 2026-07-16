from database.candidate_repository import CandidateRepository

repo = CandidateRepository()

profiles = repo.get_all()

print()

print("Profiles Loaded:", len(profiles))

print()

for profile in profiles:

    print(profile.username)

    print(profile.platform)

    print(profile.bio)

    print("-" * 40)