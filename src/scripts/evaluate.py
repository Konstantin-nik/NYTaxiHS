import logging
import os

from src.pipeline.model_evaluator import ModelEvaluator
from config import MODELS_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, MODEL, TEST_DATA, EVALUATION_REPORT

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    model_path = os.path.join(MODELS_DIR, MODEL)
    test_path = os.path.join(PROCESSED_DATA_DIR, TEST_DATA)
    evaluator = ModelEvaluator(model_path=model_path, test_file=test_path)
    evaluator.run(folder=REPORTS_DIR, filename=EVALUATION_REPORT)