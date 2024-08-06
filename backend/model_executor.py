import xgboost as xgb
from typing import List, Dict


class ModelExecutor:
    def __init__(self, model_path: str):
        self.model = xgb.Booster()
        self.model.load_model(model_path)

    def predict(self, data: Dict[str, List[float]]) -> List[float]:
        dmatrix = xgb.DMatrix(data)
        predictions = self.model.predict(dmatrix, validate_features=False)
        return predictions.tolist()
