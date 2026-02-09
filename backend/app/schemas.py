from pydantic import BaseModel, model_validator

from .model import FEATURE_KEYS


class FeatureInfo(BaseModel):
    key: str
    label: str
    group: str
    description: str
    min: float
    max: float
    mean: float


class Preset(BaseModel):
    label: str
    values: dict[str, float]


class FeaturesResponse(BaseModel):
    features: list[FeatureInfo]
    radar_categories: list[str]
    presets: list[Preset]


class PredictRequest(BaseModel):
    features: dict[str, float]

    @model_validator(mode="after")
    def validate_feature_keys(self):
        provided = set(self.features.keys())
        expected = set(FEATURE_KEYS)
        if provided != expected:
            missing = expected - provided
            extra = provided - expected
            parts = []
            if missing:
                parts.append(f"missing: {sorted(missing)}")
            if extra:
                parts.append(f"unexpected: {sorted(extra)}")
            raise ValueError(f"Feature keys mismatch: {'; '.join(parts)}")
        return self


class RadarData(BaseModel):
    mean: list[float]
    se: list[float]
    worst: list[float]


class PredictResponse(BaseModel):
    prediction: str
    probability_benign: float
    probability_malignant: float
    radar_data: RadarData
