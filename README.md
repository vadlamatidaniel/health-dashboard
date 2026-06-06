# DevOps Health Dashboard

A containerized service health monitoring API built with Python Flask and Redis.

## Features
- Monitor health of external services with latency tracking
- Persistent metrics storage using Redis
- Production-grade Docker setup with non-root user
- Custom Docker network and named volumes

## Endpoints
- `GET /health` — API status and uptime
- `GET /services` — Health status of monitored services
- `GET /metrics` — Total requests and services checked

## Running locally
docker compose up --build

## Stack
- Python Flask
- Redis
- Docker + Docker Compose