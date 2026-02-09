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

FEATURE_DESCRIPTIONS: dict[str, str] = {
    "radius": "Mean distance from center to perimeter points",
    "texture": "Standard deviation of gray-scale values",
    "perimeter": "Total boundary length of the nucleus",
    "area": "Total area of the cell nucleus",
    "smoothness": "Local variation in radius lengths",
    "compactness": "Perimeter\u00b2 / Area \u2212 1.0",
    "concavity": "Severity of concave portions of the contour",
    "concave points": "Number of concave portions of the contour",
    "symmetry": "Symmetry of the nucleus shape",
    "fractal_dimension": "Boundary complexity (coastline approximation)",
}


def _get_description(key: str) -> str:
    """Extract base measurement name from feature key to look up description."""
    for suffix in ("_mean", "_se", "_worst"):
        if key.endswith(suffix):
            base = key[: -len(suffix)]
            return FEATURE_DESCRIPTIONS.get(base, "")
    return ""


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
_presets: list[dict] = []


def load_artifacts() -> None:
    global _model, _scaler, _feature_stats, _presets

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

    # Compute presets from diagnosis groups
    benign = data[data["diagnosis"] == "B"]
    malignant = data[data["diagnosis"] == "M"]
    keys = [key for _, key, _ in FEATURE_LABELS]

    benign_vals = {k: float(benign[k].median()) for k in keys}
    malignant_vals = {k: float(malignant[k].median()) for k in keys}
    borderline_vals = {k: 0.6 * benign_vals[k] + 0.4 * malignant_vals[k] for k in keys}

    _presets = [
        {"label": "Typical Benign", "values": benign_vals},
        {"label": "Borderline", "values": borderline_vals},
        {"label": "Typical Malignant", "values": malignant_vals},
    ]


def get_presets() -> list[dict]:
    return _presets


def get_feature_metadata() -> list[dict]:
    return [
        {
            "key": key,
            "label": label,
            "group": group,
            "description": _get_description(key),
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
