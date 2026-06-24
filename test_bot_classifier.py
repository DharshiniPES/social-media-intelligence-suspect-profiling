from modules.bot_classifier import (
    train_bot_classifier
)

model, accuracy = (
    train_bot_classifier(
        "datasets/real/bot_detection_data.csv"
    )
)

print(
    "Bot Classifier Accuracy:",
    round(
        accuracy * 100,
        2
    ),
    "%"
)