import os
import warnings
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
import gcsfs

from google.cloud import storage

REFERENCE_DATA_PATH = 'gs://descipr-reference/reference_data.csv'
CURRENT_DATA_PATH = 'gs://descipr-predictions/prediction.csv'
REPORT_PATH = "./dashboards/data_drift.html"

client = storage.Client()

app = FastAPI()


def load_ref_data(filename):
    """Load data"""
    df = pd.read_csv(filename, sep=',')

    req_column = ['PU_DO', 'trip_distance', 'duration']

    return df[req_column]


def load_predicted_data(filename):
    """Load data"""
    df = pd.read_csv(filename, sep=',')

    req_column = ['PU_DO', 'trip_distance', 'predicted_duration']

    ret_df = df[req_column]
    ret_df.columns = ['PU_DO', 'trip_distance', 'duration']

    return ret_df


def create_dashboard():
    """create dashboard"""

    ref_data_sample = load_ref_data(REFERENCE_DATA_PATH)
    prod_data_sample = load_predicted_data(CURRENT_DATA_PATH)
    num_features = ['trip_distance']
    cat_features = ['PU_DO']

    column_mapping = ColumnMapping(prediction='duration', numerical_features=num_features, categorical_features=cat_features, target=None)

    report = Report(metrics=[ColumnDriftMetric(column_name='duration'), DatasetDriftMetric(), DatasetMissingValuesMetric()])

    report.run(reference_data=ref_data_sample, current_data=prod_data_sample, column_mapping=column_mapping)

    report.save_html(REPORT_PATH)


@app.get("/get_dashboard")
async def data_drift():
    """api to get dashboard"""
    create_dashboard()
    with open(REPORT_PATH, "r", encoding="utf-8") as file:
        dashboard = file.read()

    return HTMLResponse(content=dashboard, status_code=200)

