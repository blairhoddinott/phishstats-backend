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

Seed studio albums, songs, and album track links:
```bash
.venv/bin/python scripts/seed_db.py
```

Verify seeded albums:
```bash
.venv/bin/python scripts/verify_seed.py
```

Reset albums and reseed:
```bash
.venv/bin/python scripts/reset_db.py
```

Backup database:
```bash
./scripts/backup_db.sh backup.sql
```

Restore database:
```bash
./scripts/restore_db.sh backup.sql
```

## Seed data
- `scripts/albums_seed.py` contains the current Phish studio album list and release years.
- `scripts/songs_seed.py` contains canonical studio album songs plus per-album ordered track mappings.
- `scripts/seed_db.py` inserts missing album rows, song rows, and ordered `album_songs` join rows.
- Current caveat: `Get More Down` remains in the album seed list, but no canonical tracklist was available from phish.net during compilation, so it is not mapped into `ALBUM_SONGS` yet.

## Documentation
- `docs/DATABASE.md`
- `docs/UNIT_TESTS.md`
- `docs/POSTGRES.md`
