

# Setting up Conda Environment 

1. Setup conda environment with a python version of your choice

```
conda create -n env_prefect python=3.9.12
```

2. Once the environment is created, activate it 

```
conda activate env_prefect
```

# Install dependencies

```
pip install -r requirements.txt
```

# Lauch Prefect server locally

1. Run the below command to start a prefect server locally. Ensure that you run the command in a new terminal where you have activated the conda environment in which you installed prefect library

```
prefect server start
```

2. Set prefect API address so that prefect commands can point to prefect address. Ensure that you run the command in a new terminal where you have activated the conda environment in which you installed prefect library

```
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```





prefect deployment

prefect project init - this is going to create 4 files - ensure that you run it from the root of the repo so that the 4 files created are the top level of the repository folder structure

prefect work-pool create --type process nyc_taxi_trainig

prefect deploy Week2-Orchestration/2.Basic-training-orchestrate/training-pipeline.py:main -n nyctaxi1 -p nyc_taxi_trainig 


prefect worker start -p nyc_taxi_trainig

prefect deploy --help - to check the syntax of the command



prefect worker start -p zoompool 

prefect deployment run 

prefect profile ls

prefect profile login

prefect profile use 

prefect version

prefect worker start -p zoompool -t process



