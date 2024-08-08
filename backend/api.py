from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from model_executor import ModelExecutor

router = APIRouter()

MODEL_PATH = "models/model.json"
_model_executor = None


def get_model_executor() -> ModelExecutor:
    global _model_executor

    if _model_executor is None:
        _model_executor = ModelExecutor(model_path=MODEL_PATH)

    return _model_executor


class PredictionRequest(BaseModel):
    request_datetime: str
    trip_distance: float
    PULocationID: int 
    DOLocationID: int
    Airport: int


class PredictionResponse(BaseModel):
    predictions: List[float]


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    requests: PredictionRequest,
    model_executor: ModelExecutor = Depends(get_model_executor),
):
    data = {
        "request_datetime": [req.request_datetime for req in requests],
        "trip_distance": [req.trip_distance for req in requests],
        "PULocationID": [req.PULocationID for req in requests],
        "DOLocationID": [req.DOLocationID for req in requests],
        "Airport": [req.Airport for req in requests],
    }
    
    predictions = model_executor.predict(data)
    
    return PredictionResponse(predictions=predictions)
