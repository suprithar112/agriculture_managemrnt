import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "crop_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "crop_model.pkl")

# Load dataset
df = pd.read_csv(DATASET_PATH)

print(df.head())

# Convert season to numeric
season_map = {
    "Kharif": 0,
    "Rabi": 1,
    "Zaid": 2,
    "Summer": 3,
    "Winter": 4,
    "Monsoon": 5
}

df["season"] = df["season"].map(season_map)

# Features
X = df[
    [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall",
        "season"
    ]
]

# Target
y = df["crop"]

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Create model directory
os.makedirs(MODEL_DIR, exist_ok=True)

# Save model
joblib.dump(
    model,
    MODEL_PATH
)

print("✅ Model trained successfully!")
print("✅ Saved to model/crop_model.pkl")
