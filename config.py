import os
import yaml

from pathlib import Path


PROJECT_DIR = Path(".").absolute()
PARAMS_YAML_DIR = os.path.join(PROJECT_DIR, 'params.yaml')
with open(PARAMS_YAML_DIR, 'rb') as f:
    configs = yaml.safe_load(f.read())    

#######################################################
# Directories
#######################################################
RAW_DATA_DIR = configs.directories.data.raw
PROCESSED_DATA_DIR = configs.directories.data.processed
MODELS_DIR = configs.directories.model
REPORTS_DIR = configs.directories.report

#######################################################
# File names
#######################################################
TAXI_DATA = configs.filenames.data.taxi
ZONES_DATA = configs.filenames.data.zones
TRAIN_DATA = configs.filenames.data.train
VALIDATION_DATA = configs.filenames.data.validation
TEST_DATA = configs.filenames.data.test
MODEL = configs.filenames.model
EVALUATION_REPORT = configs.filenames.evaluation_report