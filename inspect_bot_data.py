import pandas as pd

df = pd.read_csv(
    "datasets/real/bot_detection_data.csv"
)

print(df["Bot Label"].value_counts())

print("\nVerified Values:")

print(df["Verified"].value_counts())