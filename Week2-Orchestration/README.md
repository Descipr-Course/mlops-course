

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



