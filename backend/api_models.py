from pydantic import BaseModel


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
        return f"\tTrip id: {self.trip_id}\n" + \
            f"\request_datetime: {self.request_datetime}\n" + \
            f"\trip_distance: {self.trip_distance}\n" + \
            f"\PULocationID: {self.PULocationID}\n" + \
            f"\DOLocationID: {self.DOLocationID}\n" + \
            f"\Airport: {self.Airport}\n"


class PredictionResponse(BaseModel):
    prediction: float
