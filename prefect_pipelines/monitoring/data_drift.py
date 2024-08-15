import datetime
import prefect
import os

import pandas as pd

from config import PROCESSED_DATA_DIR, TRAIN_DATA, VALIDATION_DATA
from evidently.ui.workspace.cloud import CloudWorkspace
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.report import Report
from dotenv import load_dotenv
from utils.log_reader import LogReader


def log_df(df):
    print(df.head(5))
    print("DF size:", len(df))


@prefect.task
def get_data_from_logs(minutes=30):
    log_reader = LogReader()
    return log_reader.download_logs(last_n_minutes=minutes)


@prefect.task
def get_historical_data():
    df_train = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, TRAIN_DATA))
    df_val = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, VALIDATION_DATA))
    return pd.concat([df_train, df_val])


@prefect.task
def generate_report(df_current, df_historical):
    load_dotenv()

    evidently_token = os.getenv("EVIDENTLY_TOKEN")
    evidently_project_id = os.getenv("EVIDENTLY_TAXI_DATA_PROJECT_ID")
    
    ws = CloudWorkspace(
        token=evidently_token,
        url="https://app.evidently.cloud")

    project = ws.get_project(evidently_project_id)

    report_cols = [
        col for col in df_current.columns if col not in ['trip_id', 'prediction', 'trip']
    ]


    data_report = Report(
        metrics=[
            DataDriftPreset(stattest='psi', stattest_threshold='0.3'),
            DataQualityPreset(),
        ],
    )

    data_report.run(
        reference_data=df_historical[report_cols], 
        current_data=df_current[report_cols],
    )

    ws.add_report(project.id, data_report)


def generate_flow_name_by_date():
    time_now = datetime.datetime.now()
    return time_now.strftime('%Y-%m-%d %H:%M:%S')


@prefect.flow(
    name="NY Taxi - Data Report", 
    flow_run_name=generate_flow_name_by_date,
    log_prints=True
)
def generate_metrics_report():
    df_current = get_data_from_logs(minutes=23*60)
    log_df(df_current)
    
    df_historical = get_historical_data()
    log_df(df_historical)
    
    if not df_current.empty and not df_historical.empty:
        generate_report(df_current, df_historical)


if __name__ == "__main__":
    generate_metrics_report.serve(
        name="NY Taxi - Scheduled Report", 
        cron="* */12 * * *",
    )
    # generate_metrics_report()
