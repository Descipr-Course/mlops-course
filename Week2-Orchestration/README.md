

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


# Working with deployment

1. To start a prefect deployment project run the below command. Ensure that you run this command at the top of your git repository folder so that the prefect.yaml and deployment.yaml files are created at the root of the git repository

```
prefect project init
```

2. To get any help on any of the prefect command you can run it with suffix "--help". For an example if you want to understand the syntax for prefect deploy command, run below

```
prefect deploy --help
```

3. To create a workpool, run the below command

```
prefect work-pool create --type process nyc_taxi_trainig
```

4. Once you have written all the codes, commit your code to the git repo

5. Create a prefect deployment using below command

```
prefect deploy Week2-Orchestration/2.Basic-training-orchestrate/training-pipeline.py:main -n nyctaxi1 -p nyc_taxi_trainig 
```

6. Start the workpool on which deployment is made

```
prefect worker start -p nyc_taxi_trainig
```

7. Run the deployment

```
prefect deployment run main/nyctaxi1
```

# Working with multiple deployments

1. Edit the deployment.yaml file in below format

```
deployments:
- name: nyc_taxi_local
  entrypoint: Week2-Orchestration/2.Basic-training-orchestrate/training-pipeline.py:main
  work_pool:
    name: nyc_taxi_trainig
- name: nyc_taxi_gcs
  entrypoint: Week2-Orchestration/3.Orchestrate-gcp/training-pipeline-gcp.py:main_gcs
  work_pool:
    name: nyc_taxi_trainig
```

2. Once the deployment.yaml file is ready, deploy all the deployment mentioned in yaml file together

```
prefect deploy --all
```
3. You can again start the worker (in this case workpool) and then run the specific deployment using the above command mentioned

# Scheduling

1. Run the below command to get the syntax of scheduling

```
prefect deployment set-schedule --help
```

2. Setting up the run the code every 120 seconds

```
prefect deployment set-schedule main/nyctaxi1 interval 120
```