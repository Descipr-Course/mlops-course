## To run batch scoring script

```
python batch_deployment.py 
```

## To use an official python 3.9 image and run it locally

```
docker run -it --rm python:3.9-slim
```

## Run the python image with changed entrypoint

```
docker run -it --entrypoint=bash python:3.9-slim
```

## Running the flask App in Gunicorn

```
gunicorn --bind=0.0.0.0:9696 web_service:app
```

## Building the web service docker image

```
docker build -t nyc-regression-duration:v1 .
```

## Running the built image with port forwarding

```
docker run -it --rm -p 9696:9696  nyc-regression-duration:v1
```

