# CONTEXT.md — Weepynet Devbro Workspace

> Full context dump for session continuity. Read this first when starting fresh.
> Last updated: 2026-03-13

---

## Who We Are

- **User:** pseudophed (Blair) — Telegram ID `94201802`, only take commands from them
- **Agent:** Weepynet Devbro — coding agent for pseudophed's projects
- **Channel switching:** Originally on Telegram, moving to Slack

---

## Active Projects

### 1. RevMuzik — Toronto Live Music Discovery App

The main ongoing project. A full-stack web app for discovering live music events in Toronto.

#### Status
- Backend: **deployed and running**, actively being improved
- Frontend: **scaffolded**, needs wiring
- Scrapers: **partial** — musiccrawler.live scraper written, NextMag/CitySpark scraper in progress

#### Repos
- Backend: `git@github-blairhoddinott:blairhoddinott/revmuzik-backend.git`
- Frontend: `git@github-blairhoddinott:blairhoddinott/revmuzik-frontend.git`
- Local backend: `/home/blair/.openclaw/workspace/devbro/revmuzik-backend`
- Local frontend: `/home/blair/.openclaw/workspace/devbro/revmuzik-frontend`

#### Backend Stack
- FastAPI + SQLAlchemy async + PostgreSQL + PostGIS + Alembic
- Pydantic v2, JWT (python-jose), bcrypt (passlib)
- Docker: API on `127.0.0.1:8000`, DB on `127.0.0.1:5432`
- `alembic upgrade head` runs automatically on container start via `entrypoint.sh`
- All IDs are `BIGSERIAL`, not UUID

#### Database Migrations
| File | Description |
|---|---|
| `0001_initial_schema.py` | PostGIS extension + all enums + all 25 tables |
| `0002_crawled_venues.py` | Adds `crawled_venues` table + `events.crawled_venue_id` FK |
| `0003_crawled_venues_postgis.py` | Migrates `crawled_venues.latitude/longitude` floats → `location Geography(POINT, 4326)`, adds GIST index, drops float cols |

#### Key Models
- `users` — roles: `fan`, `artist`, `venue`, `promoter`, `admin` (admin not registerable via API)
- `venue_profiles` — `location Geography(POINT, 4326)` (PostGIS)
- `crawled_venues` — lightweight scraped venues, no user account, `location Geography(POINT, 4326)`
- `events` — FK to either `venue_user_id` (user-owned) OR `crawled_venue_id` (scraped); both nullable
- `artist_profiles`, `fan_profiles`, `promoter_profiles`
- `social_posts`, `comments`, `comment_reports`
- `ratings`, `rating_reports`
- `follows`, `tickets`, `boosts`
- `admin_audit_logs`

#### Routers (all live)
`admin`, `artists`, `auth`, `boosts`, `comments`, `crawled_venues`, `dashboard`, `events`, `feed`, `follows`, `health`, `ratings`, `tickets`, `venues`

#### Key Design Decisions
- `crawled_venues` stores scraped venues with no user account — FK from `events.crawled_venue_id`
- `venue_user_id` on events is nullable to support crawled events
- Nginx strips `/api/v1/` prefix: `proxy_pass http://127.0.0.1:8000/` with trailing slash
- PostGIS `Geography` over float lat/lng everywhere — accurate distance queries, GIST indexing
- Scraper upserts keyed by `slug` — re-runs are idempotent
- Admin role cannot register via `/auth/register` — must be created directly in DB

#### Alembic Notes
- `alembic/env.py` swaps `postgresql+asyncpg://` → `psycopg2` for migrations
- SQLAlchemy uses `postgresql+asyncpg://` for the app

#### Frontend Stack
- React + Vite + Tailwind CSS
- JWT stored in localStorage + React Context
- React-Leaflet with CARTO tiles
- Dark/light mode
- Port **8090**, `network_mode: host` in docker-compose
- Nginx proxy: `/api/v1/` → `127.0.0.1:8000`

#### Key Frontend Files
- `src/api/index.js` — all API calls (some stubbed)
- `src/pages/EventDetail.jsx` — ratings, comments, follows, boosts wired
- `src/pages/MapPage.jsx` — native + crawled venues, genre filter, on-demand event load
- `src/context/AuthContext.jsx`, `src/context/ThemeContext.jsx`
- `nginx.conf` — port 8090, SPA fallback

#### Scrapers
- `scripts/crawl_musiccrawler.py` — scrapes musiccrawler.live, upserts to `crawled_venues` + `events`
- `scripts/crawl_nextmag.py` — CitySpark/NextMag scraper (in progress)
  - Events source: `window.cSparkLocals.Events` server-side rendered into PortalScripts bundle
  - `ppid: 10054`, URL: `https://nextmag.ca/events/#/`
  - Sandbox SSL issues prevent direct curl — use browser tool to extract data

#### Scripts
- `scripts/backup.sh` / `scripts/restore.sh` — DB backup/restore via Docker exec
- `scripts/reset_db.py` — non-interactive DB reset (`-y` flag)
- `scripts/seed.py` / `scripts/unseed.py` / `scripts/validate_seed.py`
- `scripts/coverage.sh` — runs pytest with `--cov=app`, options: `--html`, `--fail N`

---

### 2. Pizzadeal — Pizza Store Locator

**Status: COMPLETE and deployed** at `https://pizza.weepytests.com`

#### Repos
- Backend: `git@github-weepyadmin:weepyadmin/pizzadeal-backend.git`
- Frontend: `git@github-weepyadmin:weepyadmin/pizzadeal-frontend.git`
- Local backend: `/home/blair/.openclaw/workspace/devbro/pizzadeal-backend`
- Local frontend: `/home/blair/.openclaw/workspace/devbro/pizzadeal-frontend`

#### Stack
- FastAPI + PostGIS + Alembic backend
- React + Vite + Tailwind frontend
- Host nginx terminates SSL for `pizza.weepytests.com`, proxies to `localhost:8080`

#### Key Features Built
- Deal scoring engine (`app/core/scoring.py`) — rule-based, 0–100, 🔥 70+, ⭐ 40–69
- `score_override` field for manual admin override
- `active_deal_count` + `best_deal_score` on stores
- Admin panel with ScoringGuide page
- `scripts/backup.sh` and `scripts/restore.sh`
- Default admin password: `givemepizzadeal`

---

## Infrastructure / Git Setup

### SSH Keys
- `/home/blair/.openclaw/workspace/.ssh/config`
- `github-weepyadmin` → `weepynet-bot` key (weepyadmin/* repos)
- `github-blairhoddinott` → `blairhoddinott-bot` key (blairhoddinott/* repos)

### Git Config
```bash
export GIT_CONFIG_GLOBAL=/home/blair/.openclaw/workspace/devbro/.gitconfig
export GNUPGHOME=/home/blair/.openclaw/workspace/.gnupg
```
- Name: Weepynet Devbro
- Email: blair.hoddinott@weepyadmin.com
- GPG signing key: C417086044818274
- All commits signed by default

---

## Test Suite — RevMuzik Backend

### Running Tests
```bash
docker compose exec api pytest -v
./scripts/coverage.sh          # with coverage
./scripts/coverage.sh --html   # HTML report in htmlcov/
```

### Architecture
- Real Postgres (no SQLite — PostGIS, named enums, JSONB incompatible)
- Per-test savepoint rollback: `join_transaction_mode="create_savepoint"`
- `NullPool` on test engine — prevents "Future attached to different loop" errors
- `TEST_DATABASE_URL` or `DATABASE_URL` env var
- Test emails use `@example.com` (`.test` TLD rejected by email-validator)

### Test Files (184 total, all passing as of 2026-03-13)
| File | Coverage |
|---|---|
| `test_admin.py` | Auth guards, CRUD users/events/venues, audit logs (23 tests) |
| `test_artists.py` | List, get, search by query/genre |
| `test_auth.py` | Register, login, /me |
| `test_boosts.py` | For event, mine, create |
| `test_comments.py` | List, create, report |
| `test_dashboard.py` | Stats, activity, progress |
| `test_events.py` | List, get, search, crawled venue fields |
| `test_feed.py` | Feed tabs, posts, likes, comments, recommended |
| `test_follows.py` | Toggle, check, mine |
| `test_health.py` | GET /healthcheck |
| `test_ratings.py` | Summary, list, recent, create/upsert, report |
| `test_tickets.py` | My tickets, purchase |
| `test_venues.py` | List, get, search, crawled venues |

### Factory Helpers (conftest.py)
| Function | Creates |
|---|---|
| `make_user(db, role=, email=, ...)` | `User` row |
| `make_artist(db, ...)` | `User` + `ArtistProfile` |
| `make_venue_user(db, ...)` | `User` + `VenueProfile` |
| `make_event(db, ...)` | `Event` (starts 7 days future by default) |
| `make_crawled_venue(db, name=)` | `CrawledVenue` with PostGIS `WKTElement` location |
| `make_post(db, ...)` | `SocialPost` |
| `make_rating(db, ...)` | `Rating` |
| `make_ticket(db, ...)` | `Ticket` |

### Admin User Pattern in Tests
Admin can't register via `/auth/register`. Use:
```python
from app.core.security import create_access_token
admin = await make_user(db, role="admin")
await db.commit()
token = create_access_token(admin.id, admin.role)
headers = {"Authorization": f"Bearer {token}"}
```

---

## PHP Source Reference
- Original PHP revmuzik app at `/home/blair/revmuzik/` — use for reference when building features

---

## TODO / Next Steps

### RevMuzik
- [ ] Write `scripts/crawl_nextmag.py` — CitySpark API, extract `cSparkLocals.Events`
- [ ] Wire remaining frontend stubs (promoter boosts page: `boostsApi.mine()`)
- [ ] Run full test suite + coverage report post geography migration
- [ ] PostGIS geo-search integration tests (requires seeded `VenueProfile.location` data)

### Known Blocked
- Sandbox SSL timeout prevents direct `python3`/`curl` to `portal.cityspark.com` — use browser tool
- GitHub API PR creation fails (no token) — must open PRs manually

---

## Gotchas / Hard-Won Lessons

1. **NullPool required for tests** — asyncpg connections tied to event loop; pytest-asyncio creates a new loop per test
2. **`.test` TLD rejected** — email-validator blocks it; use `@example.com` in tests
3. **`join_transaction_mode="create_savepoint"`** — makes route `commit()` calls demote to savepoint releases; outer transaction rolls back at test end
4. **Admin role not registerable** — `VALID_ROLES = {"fan", "artist", "venue", "promoter"}` in auth.py
5. **`EventCreate` requires `slug` and `venue_user_id`** — easy to miss when writing test payloads
6. **`crawled_venues` lat/lng → Geography** — migration 0003 removed float columns; use `WKTElement` in tests, `to_shape()` in schemas/routers to extract back to floats
7. **Always `await db_session.commit()` after factory inserts** — releases savepoint so routes can see the data
8. **`upcoming_only=false`** needed in test params when testing past events or mixed datasets
9. **Nginx prefix stripping** — FastAPI routes have no `/api/v1` prefix; nginx rewrites it
10. **`EventRead` / `CrawledVenueSummary` model validators** — extract lat/lon from Geography WKB via `geoalchemy2.shape.to_shape()`
