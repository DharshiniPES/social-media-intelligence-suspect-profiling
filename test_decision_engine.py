from modules.decision_engine import DecisionEngine

scores = [0.95, 0.82, 0.67, 0.48, 0.15]

for score in scores:
    print(
        score,
        "->",
        DecisionEngine.classify(score)
    )