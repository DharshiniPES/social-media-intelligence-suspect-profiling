from modules.real_dataset_loader import RealDatasetLoader

loader = RealDatasetLoader(
    "datasets/real/bot_detection_data.csv"
)

profiles = loader.load_profiles(limit=3)

for p in profiles:
    print("\nPROFILE")
    print("Username:", p["username"])
    print("Hashtags:", p["hashtags"])
    print("Links:", p["links"])