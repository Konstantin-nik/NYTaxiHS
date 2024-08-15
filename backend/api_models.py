from pydantic import BaseModel
import logging


class PredictionRequest(BaseModel):
    trip_id: str
    request_datetime: str
    trip_distance: float
    PULocationID: int 
    DOLocationID: int
    Airport: int

    class Config:
        extra = "ignore"

    def __str__(self):
        logger = logging.getLogger(__name__)

        try:
            line = (
                f"\tTrip id: {self.trip_id}\n"
                f"\tRequest datetime: {self.request_datetime}\n"
                f"\tTrip distance: {self.trip_distance}\n"
                f"\tPULocationID: {self.PULocationID}\n"
                f"\tDOLocationID: {self.DOLocationID}\n"
                f"\tAirport: {self.Airport}\n"
            )
            return line
        except Exception as e:
            logger.warning(f"Error formatting PredictionRequest: {e}")
            return "Error formatting PredictionRequest"


class PredictionResponse(BaseModel):
    prediction: float
