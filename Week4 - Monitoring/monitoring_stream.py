import os
import warnings
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
import gcsfs
import pandas_gbq
from datetime import datetime

from google.cloud import storage

REFERENCE_DATA_PATH = 'gs://descipr-reference/reference_data.csv'
CURRENT_DATA_PATH = 'gs://descipr-predictions/prediction.csv'
REPORT_PATH = "./dashboards/data_drift.html"

BQ_PROJECT_ID = "descipr-mlops-2023" 
BQ_TABLE_ID = 'monitoring.tb_monitoring'

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

    result = report.as_dict()
    
    prediction_drift = result['metrics'][0]['result']['drift_score']
    num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
    share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']
    
    data = {'timestamp':[datetime.now()],
        'prediction_drift':[prediction_drift],
        'num_drifted_columns':[num_drifted_columns],
        'share_missing_values':[share_missing_values]}

    df = pd.DataFrame(data)
    
    print("starting to load data to BQ")
    pandas_gbq.to_gbq(df, BQ_TABLE_ID, BQ_PROJECT_ID, if_exists="append")
    print("Data loaded to BQ")
    

if __name__ == "__main__":
    create_dashboard()