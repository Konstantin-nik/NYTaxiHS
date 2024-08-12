import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.model_executor import ModelExecutor

router = APIRouter()
logger = logging.getLogger(__name__)

MODEL_PATH = "models/xgb.json"
_model_executor = None


def get_model_executor() -> ModelExecutor:
    global _model_executor

    if _model_executor is None:
        _model_executor = ModelExecutor(model_path=MODEL_PATH)

    return _model_executor


class PredictionRequest(BaseModel):
    trip_id: str
    request_datetime: str
    trip_distance: float
    PULocationID: int 
    DOLocationID: int
    Airport: int


class PredictionResponse(BaseModel):
    prediction: float


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    model_executor: ModelExecutor = Depends(get_model_executor),
):  
    logger.info(f"Predicting trip with id: {request.trip_id}")
    prediction = model_executor.predict(request)
    
    return PredictionResponse(prediction=prediction)
    # return PredictionResponse(prediction=0.5)
