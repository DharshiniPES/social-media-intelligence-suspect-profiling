import pandas as pd

df = pd.read_csv(
    "datasets/real/bot_detection_data.csv"
)

print(df.shape)

print(df.columns.tolist())

print("\nFirst Row:")

print(df.iloc[0])