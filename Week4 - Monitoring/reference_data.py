import pandas as pd
from google.cloud import storage
import gcsfs

client = storage.Client()

TRAIN_DATA_PATH = "gs://descipr_data/yellow_tripdata_2023-01.parquet"


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

def vectorizer(df: pd.DataFrame):
    features = ['PU_DO', 'trip_distance', 'duration']
    tdf = df[features]
    return tdf


def main():

    df_train = read_dataframe(TRAIN_DATA_PATH)
    print("training data loaded")
    
    x_y_train = vectorizer(df_train)
    print("training data vectorized")
    
    x_y_train.to_csv('gs://descipr-reference/reference_data.csv')
    print("training data saved")

if __name__ == "__main__":
    main()