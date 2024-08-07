import logging

from src.pipeline.model_trainer import ModelTrainer
from config import PROCESSED_DATA_DIR, MODELS_DIR, TRAIN_DATA, VALIDATION_DATA, TEST_DATA, MODEL

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    trainer = ModelTrainer(PROCESSED_DATA_DIR, TRAIN_DATA, VALIDATION_DATA, TEST_DATA)
    trainer.run(n_trials=50, folder=MODELS_DIR, model_filename=MODEL)