# PostgreSQL and PostGIS Setup

## Docker path
The included `docker-compose.yaml` starts a `postgis/postgis` container with:
- database: `phishstats`
- user: `phishstats`
- password: `phishstats`

## Manual setup example

```sql
CREATE DATABASE phishstats;
CREATE USER phishstats WITH PASSWORD 'phishstats';
GRANT ALL PRIVILEGES ON DATABASE phishstats TO phishstats;
\c phishstats
CREATE EXTENSION IF NOT EXISTS postgis;
```

## Connection strings
Async SQLAlchemy:
```text
postgresql+asyncpg://phishstats:phishstats@localhost:5432/phishstats
```

Alembic / sync driver:
```text
postgresql://phishstats:phishstats@localhost:5432/phishstats
```

## Notes
- PostGIS must be enabled before spatial columns are used.
- The container entrypoint runs `alembic upgrade head` before uvicorn starts.
