# Architecture

## Local
Client -> Flask REST API -> MySQL, orchestrated with Docker Compose.

## Kubernetes
External client -> LoadBalancer Service -> two Flask API replicas -> internal MySQL Service -> MySQL pod -> PersistentVolumeClaim.

Database connection details are injected from a Kubernetes Secret rather than stored in the application image or committed deployment manifest.

## Engineering choices
- REST CRUD endpoints demonstrate backend/API design.
- SQLAlchemy separates application models from raw database access.
- SQLite in-memory storage keeps unit tests isolated and fast.
- MySQL provides persistent relational storage in local/container and Kubernetes environments.
- Health probes allow Kubernetes to assess application availability.
- CPU/memory requests and limits model production scheduling constraints.
- CI executes tests and validates that the Docker image builds.
