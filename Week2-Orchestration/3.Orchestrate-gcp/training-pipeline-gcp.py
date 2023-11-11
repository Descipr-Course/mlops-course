import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.feature_extraction import DictVectorizer

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.model_selection import train_test_split

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LinearRegression
from prefect import task, flow

from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from google.cloud import storage
import gcsfs

client = storage.Client()

print("import executed")

TRACKING_SERVER_HOST = "34.93.131.49"
TRACKING_SERVER_PORT = "5000"
TRAIN_DATA_PATH = "gs://descipr_data/yellow_tripdata_2023-01.parquet"
VALID_DATA_PATH = "gs://descipr_data/yellow_tripdata_2023-01.parquet"
EXPERIMENT_NAME = "nyc-taxi-regression"
#model_name = "random-forest-regressor"

dv = DictVectorizer()

@task
def read_dataframe(filename):
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

@task
def vectorizer(df: pd.DataFrame):
    features = ['PU_DO', 'trip_distance']
    tdf = df[features]
    #dict_df = df[features].to_dict(orient='records')
    #tdf = dv.fit_transform(dict_df)
    return tdf

@task
def train_model_rf_search(x_train, x_val, y_train, y_val):
    
    mlflow.sklearn.autolog()

    def objective(params):
        with mlflow.start_run():
            mlflow.set_tag("model", "rf")
            mlflow.log_param("train_data",TRAIN_DATA_PATH)
            
            rf_model = RandomForestRegressor(**params)
            rf_model.fit(x_train, y_train)
            y_pred = rf_model.predict(x_val)
            rmse = mean_squared_error(y_val, y_pred, squared=False)
            r2score = r2_score(y_val, y_pred)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2_score", r2score)
                
            mlflow.sklearn.log_model(rf_model, artifact_path="models")

        return {'loss': rmse, 'status': STATUS_OK}


    search_space = {
        'n_estimators' : scope.int(hp.uniform('n_estimators',10,150)),
        'max_depth' : scope.int(hp.uniform('max_depth',1,40)),
        'min_samples_leaf' : scope.int(hp.uniform('min_samples_leaf',1,10)),
        'min_samples_split' : scope.int(hp.uniform('min_samples_split',2,10)),
        'random_state' : 42
    }
    
    rstate = np.random.default_rng(42)  # for reproducible results
    best_result =  fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=10,
        trials=Trials(),
        rstate=rstate
    )
    return

@flow(task_runner=SequentialTaskRunner())
def main_gcs():
    """
    Executes the training workflow
    """
    tracking_uri = f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}"

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    logger = get_run_logger()

    df_train = read_dataframe(TRAIN_DATA_PATH)
    df_val = read_dataframe(VALID_DATA_PATH)
    
    x_train = vectorizer(df_train)
    x_val = vectorizer(df_val)
    
    target = 'duration'
    y_train = df_train[target].values
    y_val = df_val[target].values

    train_model_rf_search(x_train, x_val, y_train, y_val)

    logger.info("Successfully executed our flow !!!")


if __name__ == "__main__":
    main_gcs()