import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    accuracy_score
)


def train_bot_classifier(filepath):

    df = pd.read_csv(filepath)

    df["Tweet Length"] = (
        df["Tweet"]
        .astype(str)
        .apply(len)
    )

    df["Username Length"] = (
        df["Username"]
        .astype(str)
        .apply(len)
    )

    df["Hashtag Count"] = (
        df["Hashtags"]
        .fillna("")
        .astype(str)
        .apply(
            lambda x: len(x.split())
        )
    )

    X = df[
        [
            "Follower Count",
            "Retweet Count",
            "Mention Count",
            "Verified",
            "Tweet Length",
            "Username Length",
            "Hashtag Count"
        ]
    ]

    X["Verified"] = (
        X["Verified"]
        .astype(int)
    )

    y = df["Bot Label"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    return model, accuracy