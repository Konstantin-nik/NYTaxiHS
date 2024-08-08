import os

from prefect import flow, task
from src.pipeline.data_collector import DataCollector
from src.pipeline.data_processor import DataProcessor
from src.pipeline.model_trainer import ModelTrainer
from src.pipeline.model_evaluator import ModelEvaluator
from config import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, 
    TAXI_DATA, ZONES_DATA, TRAIN_DATA, VALIDATION_DATA, TEST_DATA, MODEL, 
    EVALUATION_REPORT
)


@task
def collect():
    collector = DataCollector()
    collector.run(folder=RAW_DATA_DIR, file_name=TAXI_DATA, zones_file_name=ZONES_DATA)

@task
def process():
    processor = DataProcessor(
        data_filename=TAXI_DATA,
        zones_filename=ZONES_DATA,
        input_folder=RAW_DATA_DIR,
    )
    processor.run(PROCESSED_DATA_DIR, TRAIN_DATA, VALIDATION_DATA, TEST_DATA)

@task
def train():
    trainer = ModelTrainer(PROCESSED_DATA_DIR, TRAIN_DATA, VALIDATION_DATA, TEST_DATA)
    trainer.run(n_trials=50, folder=MODELS_DIR, model_filename=MODEL)

@task
def evaluate():
    model_path = os.path.join(MODELS_DIR, MODEL)
    test_path = os.path.join(PROCESSED_DATA_DIR, TEST_DATA)
    evaluator = ModelEvaluator(model_path=model_path, test_file=test_path)
    evaluator.run(folder=REPORTS_DIR, filename=EVALUATION_REPORT)

@flow(log_prints=True)
def pipeline():
    collect()
    process()
    train()
    evaluate()
    

if __name__ == "__main__":
    pipeline.serve(name="training-pipeline-deployment")