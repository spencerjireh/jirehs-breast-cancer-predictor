from fastapi import APIRouter

from . import model
from .schemas import FeaturesResponse, PredictRequest, PredictResponse

router = APIRouter(prefix="/api")


@router.get("/features", response_model=FeaturesResponse)
def get_features():
    return FeaturesResponse(
        features=model.get_feature_metadata(),
        radar_categories=model.RADAR_CATEGORIES,
        presets=model.get_presets(),
    )


@router.post("/predict", response_model=PredictResponse)
def post_predict(body: PredictRequest):
    result = model.predict(body.features)
    return PredictResponse(**result)
