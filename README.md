# Practical ML System Design Cohort
This is a 6-week long instructor-led, community-driven Live cohort-based course on MLOps. This course is carefully designed to help you understand the intricacies of building a Practical ML System taking into consideration various functional and non-functional requirements in the enterprise setup.

## Best Practices


### Building container with docker compose

```
docker-compose build
```
### Starting the containers

```
docker-compose up
```

### Stopping the container

```
docker-compose down
```

### Listing existing containers
```
docker container ls
```

### Submitting a task to a container

```
docker exec -t prefect-server python 3.Orchestrate-gcp/training-pipeline-gcp.py
```