import os

import mlflow
from flask import Flask, request, jsonify

from google.cloud import storage

client = storage.Client()

TRACKING_SERVER_HOST = "34.93.172.213"
TRACKING_SERVER_PORT = "5000"
MODEL_NAME = "nyc-regression-model"
RUN_ID = "1392e439ddbf457ab2b6a3db66af97a9"
MLFLOW_ENABLED = False #if set false it takes best model based on RUN ID from GCS bucket
TRACKING_URI = f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}"


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

def predict(features):
    """
    predict the count based on input features
    """
    model = load_model()
    preds = model.predict(features)
    return float(preds[0])

app = Flask('ride-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Flask App to get predictions
    """
    bike_data = request.get_json()

    pred = predict(bike_data)

    result = {
        'duration': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)

