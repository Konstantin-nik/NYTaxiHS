import logging
from model.model_evaluator import ModelEvaluator

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    evaluator = ModelEvaluator(model_path="models/xgb.json", test_file="data/test.csv")
    evaluator.run()