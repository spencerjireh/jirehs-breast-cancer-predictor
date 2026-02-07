import pickle
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

FEATURE_LABELS: list[tuple[str, str, str]] = [
    ("Radius (mean)", "radius_mean", "mean"),
    ("Texture (mean)", "texture_mean", "mean"),
    ("Perimeter (mean)", "perimeter_mean", "mean"),
    ("Area (mean)", "area_mean", "mean"),
    ("Smoothness (mean)", "smoothness_mean", "mean"),
    ("Compactness (mean)", "compactness_mean", "mean"),
    ("Concavity (mean)", "concavity_mean", "mean"),
    ("Concave points (mean)", "concave points_mean", "mean"),
    ("Symmetry (mean)", "symmetry_mean", "mean"),
    ("Fractal dimension (mean)", "fractal_dimension_mean", "mean"),
    ("Radius (se)", "radius_se", "se"),
    ("Texture (se)", "texture_se", "se"),
    ("Perimeter (se)", "perimeter_se", "se"),
    ("Area (se)", "area_se", "se"),
    ("Smoothness (se)", "smoothness_se", "se"),
    ("Compactness (se)", "compactness_se", "se"),
    ("Concavity (se)", "concavity_se", "se"),
    ("Concave points (se)", "concave points_se", "se"),
    ("Symmetry (se)", "symmetry_se", "se"),
    ("Fractal dimension (se)", "fractal_dimension_se", "se"),
    ("Radius (worst)", "radius_worst", "worst"),
    ("Texture (worst)", "texture_worst", "worst"),
    ("Perimeter (worst)", "perimeter_worst", "worst"),
    ("Area (worst)", "area_worst", "worst"),
    ("Smoothness (worst)", "smoothness_worst", "worst"),
    ("Compactness (worst)", "compactness_worst", "worst"),
    ("Concavity (worst)", "concavity_worst", "worst"),
    ("Concave points (worst)", "concave points_worst", "worst"),
    ("Symmetry (worst)", "symmetry_worst", "worst"),
    ("Fractal dimension (worst)", "fractal_dimension_worst", "worst"),
]

FEATURE_KEYS: list[str] = [key for _, key, _ in FEATURE_LABELS]

RADAR_CATEGORIES: list[str] = [
    "Radius",
    "Texture",
    "Perimeter",
    "Area",
    "Smoothness",
    "Compactness",
    "Concavity",
    "Concave Points",
    "Symmetry",
    "Fractal Dimension",
]

_model = None
_scaler = None
_feature_stats: dict[str, dict[str, float]] = {}


def load_artifacts() -> None:
    global _model, _scaler, _feature_stats

    with open(BASE_DIR / "model" / "model.pkl", "rb") as f:
        _model = pickle.load(f)

    with open(BASE_DIR / "model" / "scaler.pkl", "rb") as f:
        _scaler = pickle.load(f)

    data = pd.read_csv(BASE_DIR / "data" / "data.csv")
    data = data.drop(["Unnamed: 32", "id"], axis=1)

    for _, key, _ in FEATURE_LABELS:
        col = data[key]
        _feature_stats[key] = {
            "min": float(col.min()),
            "max": float(col.max()),
            "mean": float(col.mean()),
        }


def get_feature_metadata() -> list[dict]:
    return [
        {
            "key": key,
            "label": label,
            "group": group,
            "min": _feature_stats[key]["min"],
            "max": _feature_stats[key]["max"],
            "mean": _feature_stats[key]["mean"],
        }
        for label, key, group in FEATURE_LABELS
    ]


def predict(features: dict[str, float]) -> dict:
    input_array = np.array([features[key] for key in FEATURE_KEYS]).reshape(1, -1)

    input_array_scaled = _scaler.transform(input_array)
    prediction = _model.predict(input_array_scaled)
    probabilities = _model.predict_proba(input_array_scaled)[0]

    # Min-max scale for radar chart
    scaled: dict[str, float] = {}
    for key in FEATURE_KEYS:
        min_val = _feature_stats[key]["min"]
        max_val = _feature_stats[key]["max"]
        denom = max_val - min_val
        scaled[key] = (features[key] - min_val) / denom if denom != 0 else 0.0

    # Group into 10-element arrays for mean, se, worst
    mean_keys = [k for _, k, g in FEATURE_LABELS if g == "mean"]
    se_keys = [k for _, k, g in FEATURE_LABELS if g == "se"]
    worst_keys = [k for _, k, g in FEATURE_LABELS if g == "worst"]

    radar_data = {
        "mean": [scaled[k] for k in mean_keys],
        "se": [scaled[k] for k in se_keys],
        "worst": [scaled[k] for k in worst_keys],
    }

    return {
        "prediction": "Benign" if prediction[0] == 0 else "Malignant",
        "probability_benign": float(probabilities[0]),
        "probability_malignant": float(probabilities[1]),
        "radar_data": radar_data,
    }
