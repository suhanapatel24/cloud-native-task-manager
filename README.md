# Cloud-Native Task Manager

A backend + DevOps portfolio project: a RESTful task-management API with persistent SQL storage, containerized local development, automated tests, and a path to Kubernetes deployment.

## Why this project
This is not a copied tutorial application. It uses a small real application domain to demonstrate API design, persistence, validation, containerization, health checks, and delivery practices.

## API
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/tasks | List tasks |
| POST | /api/tasks | Create a task |
| GET | /api/tasks/:id | Get one task |
| PATCH | /api/tasks/:id | Update a task |
| DELETE | /api/tasks/:id | Delete a task |
| GET | /healthz | Health check |

## Run with Docker Compose
```bash
docker compose up --build
```
API: http://localhost:8080

Example:
```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Ship cloud portfolio","priority":"high"}'
```

## Stack
Python, Flask, SQLAlchemy, MySQL, Docker, Docker Compose, Pytest. Kubernetes and CI/CD are added in the next layer.

## Portfolio integrity
Cloud deployment outcomes and performance metrics are documented only after they are actually verified.
