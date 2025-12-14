import joblib
import pandas as pd
from pathlib import Path

# Load model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "lgbm_final.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

# Expected schema (TRAINING DATA CONTRACT)
EXPECTED_COLUMNS = [
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

NUMERIC_COLS = [
    "Income",
    "Age",
    "Experience",
    "CURRENT_JOB_YRS",
    "CURRENT_HOUSE_YRS",
]

CATEGORICAL_COLS = [
    "Married/Single",
    "House_Ownership",
    "Car_Ownership",
    "Profession",
    "STATE",
]

# Input normalization (THIS WAS MISSING IN YOUR CODE)

def normalize_input(data: dict) -> dict:
    normalized = {}

    # 1️⃣ Check missing columns
    missing = [col for col in EXPECTED_COLUMNS if col not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    # 2️⃣ Numeric casting
    for col in NUMERIC_COLS:
        try:
            normalized[col] = int(data[col])
        except Exception:
            raise ValueError(f"Invalid numeric value for '{col}': {data[col]}")

    # 3️⃣ Categorical normalization (MATCH TRAINING DATA EXACTLY)
    normalized["Married/Single"] = str(data["Married/Single"]).strip().lower()
    normalized["House_Ownership"] = str(data["House_Ownership"]).strip().lower()
    normalized["Car_Ownership"] = str(data["Car_Ownership"]).strip().lower()

    normalized["Profession"] = (
        str(data["Profession"])
        .strip()
        .replace("_", " ")
    )

    normalized["STATE"] = (
        str(data["STATE"])
        .strip()
        .replace("_", " ")
    )

    return normalized

# Prediction function

def predict_risk(data: dict) -> dict:
    # 1️⃣ Normalize & validate input
    clean_data = normalize_input(data)

    # 2️⃣ Convert to DataFrame (correct column order)
    df = pd.DataFrame([clean_data], columns=EXPECTED_COLUMNS)

    # 3️⃣ Model prediction
    pred = int(model.predict(df)[0])

    proba = model.predict_proba(df)[0][1]
    if pd.isna(proba):
        raise ValueError("Model returned NaN probability (input invalid)")

    proba = float(proba)

    return {
        "prediction": pred,
        "default_probability": round(proba, 4),
        "status": "High Default Risk" if pred == 1 else "Low Default Risk",
    }
