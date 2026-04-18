# phishstats-backend

A FastAPI backend scaffold for the phishstats web application.

## Stack
- FastAPI with async handlers
- SQLAlchemy async + asyncpg
- PostgreSQL with PostGIS
- Alembic migrations
- Docker and Docker Compose

## Project layout
- `app/` application code
- `alembic/` migrations
- `scripts/` helper scripts for seed/reset/backup/restore
- `docs/` supporting project documentation
- `tests/` test suite

## Running with Docker

```bash
docker compose up --build
```

The backend container runs `alembic upgrade head` automatically before starting FastAPI.

API base URL:
- `http://localhost:8000/api/v1`

## Useful commands

Run tests locally:
```bash
pytest
```

Seed placeholder:
```bash
python scripts/seed_db.py
```

Backup database:
```bash
./scripts/backup_db.sh backup.sql
```

Restore database:
```bash
./scripts/restore_db.sh backup.sql
```

## Documentation
- `docs/DATABASE.md`
- `docs/UNIT_TESTS.md`
- `docs/POSTGRES.md`
