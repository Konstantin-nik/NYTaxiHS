import datetime
import prefect
import os

import utils.postgre_engine as pg_engine
import pandas as pd

from evidently.ui.workspace.cloud import CloudWorkspace
from evidently.metric_preset import RegressionPreset
from evidently import ColumnMapping
from evidently.report import Report
from dotenv import load_dotenv
from utils.log_reader import LogReader
from sqlalchemy import inspect, text


def log_df(df):
    print(df.head(5))
    print("DF size:", len(df))


@prefect.task
def get_data_from_logs(minutes=30):
    log_reader = LogReader()
    return log_reader.download_logs(last_n_minutes=30)


@prefect.task
def get_real_data(trip_ids):
    today_date = datetime.datetime.now()
    yesterday_date = today_date - datetime.timedelta(days=1)

    table_names = [
        f"trips_{today_date.strftime('%Y_%m_%d')}",
        f"trips_{yesterday_date.strftime('%Y_%m_%d')}"
    ]

    with pg_engine.get_engine().connect() as connection:
        inspector = inspect(connection)
        available_tables = inspector.get_table_names(schema="public")
        
        results_df = pd.DataFrame()

        for table_name in table_names:
            if table_name in available_tables:
                query = text(f"""
                    SELECT trip_id, tpep_pickup_datetime, tpep_dropoff_datetime
                    FROM public.{table_name}
                    WHERE trip_id = ANY(ARRAY[:trip_ids]::uuid[])
                """)
                result = pd.read_sql(query, connection, params=({'trip_ids':trip_ids},))
                
                results_df = pd.concat([results_df, result])

    print(f"Total matched records: {len(results_df)}")

    return results_df


@prefect.task
def merge_dataframes(df_predicted, df_result):
    df_predicted['trip_id'] = df_predicted['trip_id'].astype(str)
    df_result['trip_id'] = df_result['trip_id'].astype(str)

    df_merged = pd.merge(df_predicted, df_result, on="trip_id", how="inner")

    return df_merged


@prefect.task
def extract_features(df):
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    df["trip_time"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).apply(lambda x: x.total_seconds() / 60)

    return df


@prefect.task
def generate_report(df):
    load_dotenv()

    evidently_token = os.getenv("EVIDENTLY_TOKEN")
    evidently_project_id = os.getenv("EVIDENTLY_TAXI_METRICS_PROJECT_ID")
    
    ws = CloudWorkspace(
        token=evidently_token,
        url="https://app.evidently.cloud"
    )

    project = ws.get_project(evidently_project_id)

    report_cols = ['trip_time', 'prediction']

    column_mapping = ColumnMapping()

    column_mapping.target = 'trip_time'
    column_mapping.prediction = 'prediction'

    print(df.head(5))

    regression_performance_report = Report(metrics=[
        RegressionPreset(),
    ])

    regression_performance_report.run(
        reference_data=df[report_cols], 
        current_data=df[report_cols],
        column_mapping=column_mapping
    )

    ws.add_report(project.id, regression_performance_report)


def generate_flow_name_by_date():
    time_now = datetime.datetime.now()
    return time_now.strftime('%Y-%m-%d %H:%M:%S')


@prefect.flow(
    name="NY Taxi - Quality Report", 
    flow_run_name=generate_flow_name_by_date,
    log_prints=True
)
def generate_metrics_report():
    df_predicted = get_data_from_logs()[['prediction', 'trip_id']].copy()
    log_df(df_predicted)
    
    trip_ids = df_predicted['trip_id'].tolist()
    df_result = get_real_data(trip_ids)
    log_df(df_result)

    df_merged = merge_dataframes(df_predicted, df_result)
    log_df(df_merged)
    
    df_extracted = extract_features(df_merged)
    log_df(df_extracted)

    generate_report(df_extracted)


if __name__ == "__main__":
    generate_metrics_report.serve(name="NY Taxi - Scheduled Report", cron="*/15 * * * *")
    # generate_metrics_report()
