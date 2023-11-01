


# Environmnent Isolation


1. Install pipenv

```
pip install pipenv
```


2. Activate pipenv: Ensure that you are in the directory where you want to create an isolated enviroment. Run the below command

```
pipenv shell
```

3. This will activate an envriment with the same name as directory where you ran this command

4. Now, from here on, to install any python package, run 

```
pipenv install <package_name>
```

# Settingup MLFlow Locally

1. We will need following package in this pipenv environment - so run the below command

```
pipenv install mlflow scikit-learn pandas seaborn hyperopt xgboost fastparquet boto3
```


2. Running mlflow locally

```
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

# MLFlow on server commands

1. Installations

```
sudo apt-get update
sudo apt-get install postgresql-client
```


2. list sql instances

```
gcloud sql instances list
```

3. check if you are able to access the database

```
psql -h <pstgre_private_ip> -U moubashsir mlflow_db
```

4. Starting mlflow server

```
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://moubashsir:<pass>@10.91.160.2:5432/mlflow_db --default-artifact-root gs://descipr_mlflow
```

