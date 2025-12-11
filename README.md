# XRP Trading Intelligence Platform

Deterministic multi-service XRP-focused trading intelligence stack providing feature construction, parallel signal modules, composite scoring, execution scaffolding, and research-ready backtesting utilities.

## Services
- **API** (`services/api`): FastAPI endpoints for health and composite signal retrieval.
- **Signal Worker** (`services/signal_worker`): Deterministic signal computation worker emitting scores.
- **Backtesting** (`services/backtesting`): FastAPI surface for walk-forward simulation.
- **Redis/Postgres**: Core dependencies for streaming and persistence.

## Environment
A unified environment template is available at `.env.example`. Copy it to `.env` and adjust values for your deployment.

```bash
cp .env.example .env
```

## Bootstrap database schemas
Create the core relational tables before running services:

```bash
python -m scripts.bootstrap_db
```

Ensure `DATABASE_URL` points at your Postgres/Timescale instance.

## Local runtime (Docker Compose)
Build and start all services locally:

```bash
docker-compose up --build
```

API will be exposed on port `8000` and backtesting service on `8010`.

## Railway
`railway.toml` declares individual service Dockerfiles and start commands for Railway deployments. Configure project-level environment variables using `.env` values within Railway.
