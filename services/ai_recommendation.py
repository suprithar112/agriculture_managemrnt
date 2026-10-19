import joblib
import os
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "model",
    "crop_model.pkl"
)

model = None

season_map = {
    "kharif": 0,
    "rabi": 1,
    "zaid": 2,
    "summer": 3,
    "winter": 4,
    "monsoon": 5
}

def recommend_crop(
    season,
    temperature,
    humidity,
    ph,
    rainfall,
    N=50,
    P=40,
    K=40
):
    global model

    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Crop model not found. Run: python services/train_model.py"
            )
        model = joblib.load(MODEL_PATH)

    season_value = season_map.get(
        season.lower(),
        0
    )

    data = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
        "season": season_value
    }])

    prediction = model.predict(data)

    return prediction[0]
