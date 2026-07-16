from itertools import product

prefixes = [
    "alex", "john", "rahul", "emma", "david",
    "mike", "anna", "sarah", "james", "lucas",
    "liam", "oliver", "noah", "ethan", "ava",
    "isabella", "mia", "charlie", "dev", "coder",
    "python", "security", "cyber", "cloud", "ai",
    "ml", "data", "open", "tech", "code"
]

suffixes = [
    "",
    "dev",
    "coder",
    "codes",
    "tech",
    "official",
    "123",
    "_dev",
    "_ai",
    "_ml",
    "_sec",
    "_official",
    "x",
    "pro",
    "labs"
]

usernames = set()

for p, s in product(prefixes, suffixes):
    usernames.add(f"{p}{s}")

# Add some real accounts
real_accounts = [
    "torvalds",
    "octocat",
    "google",
    "microsoft",
    "apple",
    "tensorflow",
    "pytorch",
    "huggingface",
    "openai",
    "aws",
    "docker",
    "kubernetes",
    "mozilla",
    "numpy",
    "pandas-dev",
    "nasa",
    "spacex",
    "isro",
    "mitre",
    "owasp"
]

usernames.update(real_accounts)

usernames = sorted(usernames)

with open(
    "datasets/seed/github_usernames.txt",
    "w",
    encoding="utf-8"
) as f:

    for u in usernames:
        f.write(u + "\n")

print(f"Generated {len(usernames)} usernames.")