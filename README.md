# XRP Trading Intelligence Platform

This repository provides a multi-service XRP-focused trading intelligence scaffold with signal computation, composite scoring, and executable FastAPI endpoints.

## Services
- **API**: FastAPI service exposing health and computed signal endpoints.
- **Signal Worker**: Periodic synthetic signal generator using deterministic features.
- **Redis/Postgres**: Core dependencies for state and pub/sub.

## Running locally
```bash
docker-compose up --build
```

Ensure all required environment variables are supplied (see `docker-compose.yml`).
