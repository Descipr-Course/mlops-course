
import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.ensemble import RandomForestRegressor

import mlflow

from google.cloud import storage
import gcsfs

client = storage.Client()

TRACKING_SERVER_HOST = "34.93.172.213"
TRACKING_SERVER_PORT = "5000"
PRED_DATA_PATH = "gs://descipr_data/yellow_tripdata_2023-02.parquet"
EXPERIMENT_NAME = "nyc-taxi-regression"
MODEL_NAME = "nyc-regression-model"
RUN_ID = "1392e439ddbf457ab2b6a3db66af97a9"
MLFLOW_ENABLED = True #if set false it takes best model based on RUN ID from GCS bucket


TRACKING_URI = f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}"

def read_dataframe(filename):
    """
    Loads data set
    """
    
    if filename.endswith('.csv'):
        df = pd.read_csv(filename)

        
        df.lpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.lpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    elif filename.endswith('.parquet'):
        df = pd.read_parquet(filename, engine = 'pyarrow')

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df = df.sample(frac=0.01)
    df.reset_index(inplace=True)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    
    return df


def vectorizer(df: pd.DataFrame):
    features = ['PU_DO', 'trip_distance']
    tdf = df[features]
    return tdf


def load_model():
    """
    Loads the ML model either from ML flow registry or from GCS bucket
    """
    tracking_uri = TRACKING_URI
    mlflow.set_tracking_uri(tracking_uri)
    model_uri = f"models:/{MODEL_NAME}/latest"
    
    gcs_bucket = f"gs://descipr_mlflow/1/{RUN_ID}/artifacts/model"

    if MLFLOW_ENABLED:
        print("Model loaded from registry")
        return mlflow.pyfunc.load_model(model_uri)
    else:
        print("Model loaded from GCS bucket")
        return mlflow.pyfunc.load_model(gcs_bucket)
    


#def predict(features):
#    """
##    predict the count based on input features
#    """
#    model = load_model()
#    preds = model.predict(features)
#    return float(preds[0])

def main():
    """
    All stuff together
    """
    
    df_pred = read_dataframe(PRED_DATA_PATH)
    
    print("data loaded")
    
    x_pred = vectorizer(df_pred)
    
    rf_model = load_model()
    y_pred = rf_model.predict(x_pred)
    
    df_pred['predicted_duration'] = y_pred
    
    print("Prediction completed")
    
    df_pred.to_csv('gs://descipr-predictions/prediction.csv')
    
    print("Prediction saved to GCS bucket")

if __name__ == "__main__":
    main()