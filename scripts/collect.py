from pipeline.data_collector import DataCollector
import logging

from config import RAW_DATA_DIR, TAXI_DATA, ZONES_DATA

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    collector = DataCollector()
    collector.run(folder=RAW_DATA_DIR, file_name=TAXI_DATA, zones_file_name=ZONES_DATA)