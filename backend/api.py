from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from backend.model_executor import ModelExecutor

router = APIRouter()

MODEL_PATH = "models/xgb.json"
_model_executor = None


def get_model_executor() -> ModelExecutor:
    global _model_executor

    if _model_executor is None:
        _model_executor = ModelExecutor(model_path=MODEL_PATH)

    return _model_executor


class PredictionRequest(BaseModel):
    trip_id: int
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
    prediction = model_executor.predict(request)
    
    return PredictionResponse(prediction=prediction)
    # return PredictionResponse(prediction=0.5)
