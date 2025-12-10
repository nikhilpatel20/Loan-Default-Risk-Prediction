import joblib
import pandas as pd
from pathlib import Path

# Model file ka naam EXACTLY waise hi rakho jaisa notebook me dump kiya hai:
# joblib.dump(pipeline, "lgbm_final.pkl")
MODEL_PATH = Path("lgbm_final.pkl")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file '{MODEL_PATH}' nahi mila. "
        f"Pehele notebook se joblib.dump(pipeline, 'lgbm_final.pkl') run karo."
    )

# Model ek sklearn Pipeline hai (ColumnTransformer + StandardScaler + RandomForest)
model = joblib.load(MODEL_PATH)

# PDF ke hisaab se feature list (input columns)
FEATURE_ORDER = [
    "Income",
    "Age",
    "Experience",
    "Married/Single",
    "House_Ownership",
    "Car_Ownership",
    "Profession",
    "STATE",
    "CURRENT_JOB_YRS",
    "CURRENT_HOUSE_YRS",
]


def _build_input_df(data: dict) -> pd.DataFrame:
    """
    Frontend se aane wale dict ko proper DataFrame me convert karega.
    Sab required columns hone chahiye.
    """
    missing = [col for col in FEATURE_ORDER if col not in data]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")

    row = {col: [data[col]] for col in FEATURE_ORDER}
    return pd.DataFrame(row)


THRESHOLD = 0.25  # 30% se upar ko High Risk maan lo

def predict_risk(data: dict) -> dict:
    df = _build_input_df(data)

    prob = float(model.predict_proba(df)[0][1])  # class 1 prob
    pred = 1 if prob >= THRESHOLD else 0

    status = "High Default Risk" if pred == 1 else "Low Default Risk"

    return {
        "prediction": pred,
        "default_probability": prob,
        "status": status,
    }


if __name__ == "__main__":
    # Quick manual test
    sample = {
        "Income": 0,
        "Age": 35,
        "Experience": 10,
        "Married/Single": "single",
        "House_Ownership": "rented",
        "Car_Ownership": "no",
        "Profession": "Software_Developer",
        "STATE": "Madhya_Pradesh",
        "CURRENT_JOB_YRS": 5,
        "CURRENT_HOUSE_YRS": 12,
    }
    print(predict_risk(sample))

