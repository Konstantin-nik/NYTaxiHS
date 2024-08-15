import logging

import pandas as pd
import xgboost as xgb

from typing import List, Dict


class ModelExecutor:
    def __init__(self, model_path: str):
        self.logger = logging.getLogger(__name__)
        self.model = xgb.Booster()
        self.model.load_model(model_path)

    def chech_features(self, data):
        if data.trip_distance < 0: 
            self.logger.warning(f"Trip distance is negative!!! trip_distance: {data.trip_distance}")
            data.trip_distance = -data.trip_distance
        return True

    def extract_features(self, data):
        data.request_datetime = data.request_datetime.replace('/', ':')
        try:
            request_datetime = pd.to_datetime(data.request_datetime)
        except:
            self.logger.warning("Datetime format", data.request_datetime)
            request_datetime = pd.to_datetime(data.request_datetime, format='%Y-%m-%dT%H:%M:%S%z')

        features = {
            "trip_distance": data.trip_distance,
            "pickup_hour": request_datetime.hour,
            "pickup_minute": request_datetime.minute,
            "pickup_dayofweek": request_datetime.dayofweek,
            "pickup_dayofmonth": request_datetime.day,
            "is_from_airport": data.Airport,
            "PULocationID": data.PULocationID,
            "DOLocationID": data.DOLocationID,
        }

        df = pd.DataFrame([features])
        df = df.astype(float)
        self.logger.info("Feature extraction for inference completed")
        
        return df

    def predict(self, data: Dict[str, List[float]]) -> List[float]:
        df = self.extract_features(data)
        dmatrix = xgb.DMatrix(df)
        predictions = self.model.predict(dmatrix, validate_features=False)
        return predictions[0]
