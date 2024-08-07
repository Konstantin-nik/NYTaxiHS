from src.pipeline.data_processor import DataProcessor
import logging

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, TAXI_DATA, ZONES_DATA, TRAIN_DATA, VALIDATION_DATA, TEST_DATA

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    processor = DataProcessor(
        data_filename=TAXI_DATA,
        zones_filename=ZONES_DATA,
        input_folder=RAW_DATA_DIR,
    )
    processor.run(PROCESSED_DATA_DIR, TRAIN_DATA, VALIDATION_DATA, TEST_DATA)