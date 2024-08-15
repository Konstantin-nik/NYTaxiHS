import logging
import json

import pandas as pd
import numpy as np

from fastapi import APIRouter, Depends
from backend.model_executor import ModelExecutor
from backend.api_models import PredictionRequest, PredictionResponse

router = APIRouter()

MODEL_PATH = "models/xgb.json"
_model_executor = None
logger = logging.getLogger(__name__)


def log_trip_prediction(trip_id, features, prediction):
    features_dict = dict()
    for key, value in features.items():
        if isinstance(value, np.ndarray):
            features_dict[key] = value[0]
        elif isinstance(value, pd.Series):
            features_dict[key] = value.iloc[0]
        else:
            features_dict[key] = value

    log_dict = {
        "trip_id": trip_id,
        "features": features_dict,
        "prediction": float(prediction)
    }

    log_str = json.dumps(log_dict)

    logger.info(f"Prediction result: {log_str}")


def get_model_executor() -> ModelExecutor:
    global _model_executor

    if _model_executor is None:
        _model_executor = ModelExecutor(model_path=MODEL_PATH)

    return _model_executor


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    model_executor: ModelExecutor = Depends(get_model_executor),
):  
    logger.info(f"Predicting trip with id: {request.trip_id}")
    logger.info("Request:", str(request))
    features = model_executor.extract_features(request)
    prediction = model_executor.predict(request)
    
    log_trip_prediction(
        trip_id=request.trip_id,
        features=features,
        prediction=prediction,
    )
    return PredictionResponse(prediction=prediction)
