# Session Memory — 2026-03-25 (updated)

## What we built today

### gigvenues-backend (`/home/blair/.openclaw/workspace/devbro/gigvenues-backend`)
- Cloned fresh from `git@github-blairhoddinott:blairhoddinott/gigvenues-backend.git`
- Lifted backend code out of gigvenues-frontend repo into this standalone repo
- Wired up PostgreSQL/PostGIS with SQLAlchemy (async, asyncpg driver)
- Set up Alembic migrations — initial schema covers all 12 tables
- All 12 API route files use real async SQLAlchemy (no mock store)
- Seed script: `uv run python -m app.seed.seed_db`
- **Key fix**: All enum columns use `native_enum=False` (VARCHAR storage) — asyncpg sends Python enum `.name` (uppercase) but native Postgres enums expect lowercase `.value`
- **Key fix**: Migration uses `sa.String(64)` for enum columns, not native Postgres ENUM types
- `docker-compose.yml` command runs `alembic upgrade head` before uvicorn
- Converted all tests to async SQLAlchemy + pytest-asyncio + httpx AsyncClient
- Tests use savepoint rollback against real Postgres (matching revmuzik pattern)
- `scripts/coverage.sh` auto-detects docker socket access, updates README badges
- **69/69 tests passing**, 75% coverage

### gigvenues-frontend (`/home/blair/.openclaw/workspace/devbro/gigvenues-frontend`)
- Backend directory removed (moved to gigvenues-backend)
- `docker-compose.yml` simplified to frontend only
- **Now wired to real backend** — all mock data imports replaced with API hooks
- New `src/api/` layer: `client.ts` (fetch wrapper), `types.ts` (snake_case API types), `adapters.ts` (snake→camelCase), `hooks.ts` (React hooks)
- Auth: `SessionContext` now calls `POST /auth/login`; token + role stored in localStorage; `X-Actor-Role` header sent on all API calls
- All 13 pages wired: GigFeed, GigDetail, VenueDirectory, VenueProfile, VenueScheduleDay, VenueDashboard, ArtistDirectory, ArtistProfile, ArtistDashboard, NearbyVenuesMap, Landing, AdminDashboard, AccessPage
- Demo credentials still work: `rex-demo@revmuzik.com / VenueDemo123!`, `book@lunavale.com / ArtistDemo123!`, `ops@revmuzik.com / AdminDemo123!`
- `frontend/.env` has `VITE_API_BASE_URL=http://localhost:8000/api/v1`

### gigvenues-backend — additional work (session 2)
- Expanded `Venue`, `ArtistProfile`, `Gig` models with rich display fields (images, lat/lng, capacity, stage details, social links, etc.)
- New migration: `2b3f8c1d4e7a_add_rich_display_fields.py`
- Full reseed with all 4 venues, 6 artists, 18 gigs from frontend mock data
- New endpoints: `GET /gigs/applications?venue_id=`, `GET /incidents`, `GET /appeals`
- Backend running at `http://localhost:8000`; DB on `localhost:5432`

## Stacking Tracker — work done 2026-03-23

### st-backend (`/home/blair/.openclaw/workspace/devbro/st-backend`)
- `POST /prices/daily-close` — internal-key-auth endpoint for daily OHLC upsert
- `POST /prices/intraday` — record intraday price ticks
- `GET /prices/intraday/{metal}` — today's ticks (ET day boundary)
- `DELETE /prices/intraday/cleanup` — delete rows older than 2 days
- `INTERNAL_API_KEY` config setting added
- 4 new `daily_price_*` tables + Alembic migration 0007
- **151 tests passing**, 84% coverage
- Backend has NO `/api/v1` prefix — routes are at `/prices/...` directly
- `BACKEND_URL` in fetcher should be `http://st-backend:8000` (no /api/v1)

### st-current-price-fetcher (`/home/blair/.openclaw/workspace/devbro/st-current-price-fetcher`)
- `fetcher/daily_close.py` — fetches OHLC from Stooq, POSTs to backend at 20:00 ET Mon-Fri
- `fetcher/intraday.py` — POSTs price ticks to backend after each Redis write
- APScheduler cron: daily close at 20:00 ET, cleanup at 06:00 ET
- `BACKEND_URL` + `INTERNAL_API_KEY` env vars (must be in both .env AND docker-compose.yml environment section)
- **55 tests passing**, 89% coverage

### st-frontend (`/home/blair/.openclaw/workspace/devbro/st-frontend`)
- Historical Prices page: full-width metal cards, trend indicators (SMA 20/50, RSI 14, vs SMA 50), short-term row (Williams %R, Avg Range, Closing Strength)
- `src/lib/indicators.ts`: full indicator library (SMA, RSI, Williams %R, closing strength, linear regression, etc.)
- `IntradayMiniCards` component in global right rail — sparkline + trend per metal, polls every 5 min
- Right rail: ProfileSummary → SpotPriceTicker → IntradayMiniCards (global on all pages)
- **400 tests passing**

## Stacking Tracker — work done 2026-03-25 (full day)

### st-frontend — Add to Stack form overhaul
- Product search deduped by name (no year duplicates in dropdown)
- Year dropdown shows all catalog years for a product + "Other year" option
- Weight auto-fills from selected year variant (editable)
- Custom year for known product: metal/mint/format pre-filled from catalog template
- Fully custom entry flow preserved via "Not in catalog?" link
- Progressive reveal: search → year → details → transaction fields

### st-frontend — Catalogue page
- New `/catalogue` route with BookOpen icon in sidebar
- Table of all products grouped by name+metal+mint, year shown as range (e.g. 1986–2024)
- Search by name/mint/country/year, filter by metal type
- Product names link to Wikipedia/source URL

### st-backend — mint_data CSVs + seed script
- seeds/mint_data/: 12 CSVs, 22 products from world mints (Perth, Austrian, RCM, US Mint, Royal Mint, etc.)
- scripts/seed_mint_products.py: reads CSVs, parses weights, resolves mint_id FK, upserts

## Stacking Tracker — work done 2026-03-25

### st-backend
- `GET /prices/latest-dates` — internal-key-auth endpoint, returns most recent date per metal
- Sampling bug fixed: last 7 rows always included unsampled so 1W view is never clipped
- Route ordering fix: `/latest-dates` placed before `/{metal}` wildcard

### st-current-price-fetcher
- `fetcher/backfill.py` — on startup, scans last 30 days, finds gaps vs stored dates, backfills from Stooq
- Backfill wired into `main.py` startup sequence (runs before scheduler)
- 68 tests passing

### st-frontend
- Historical Prices page: UTC date parse bug fixed (was showing Mar 23 instead of Mar 24)
- Chart right margin increased (last label was being clipped)
- X-axis tick interval: 1W and 1M now show every data point, longer periods still sample
- Coverage badge script fixed: reads from `coverage/coverage-summary.json` (volume-mounted from Docker), no longer crashes on test failures
- 400 tests passing, 64% coverage

## Stacking Tracker — work done 2026-03-26 (session 2)

### Multi-currency display (all three repos)

**st-current-price-fetcher**
- `fetcher/fx_rates.py`: `check_and_refresh_fx_rates()` — checks Redis every minute, fetches from frankfurter.app when `fx_rates` key is missing, stores with TTL=10800s (3h), always injects USD=1.0
- `main.py`: warms FX rates on startup, APScheduler job every 1 minute
- 75 tests passing

**st-backend**
- Migration 0014: `preferred_currency VARCHAR(3) DEFAULT 'USD'` on users table
- `PATCH /auth/me/preferences` — update preferred_currency (validated against USD/CAD/EUR/GBP/AUD/CHF)
- `GET /prices/fx-rates` — reads `fx_rates` Redis key, falls back to hardcoded defaults if absent
- `CurrentUser` schema now exposes `preferred_currency`
- 185 tests passing

**st-frontend**
- `src/context/CurrencyContext.tsx`: `CurrencyProvider` + `useCurrency()` hook — fetches FX rates and user pref on mount, `convert(usd)`, `format(usd)`, `setCurrency()` persists to backend
- `src/components/common/CurrencyPicker.tsx`: dropdown in ProfileSummary sidebar
- `formatCurrency()` in formatters.ts now currency/rate aware, sign-safe
- All price display components wired to `useCurrency()`: SpotPriceTicker, StatCardGrid, MetalBreakdownCard (compact k/M formatter), MetalPnLCard, AvgCostPerOzCard, SoldStackCard, IntradayMiniCards, MarketRail, TransactionsPage, HistoricalPricesPage
- `CurrencyProvider` wraps entire App
- 400 tests passing

## Stacking Tracker — work done 2026-03-26 (session 3)

### Landing page + news feed
- `LandingPage` at `/` (public) with nav bar, hero, feature cards, news feed, footer
- Authenticated users redirected to `/dashboard` from `/`
- Dashboard moved from `/` to `/dashboard`; all internal nav updated
- `SpotTicker` (XAU/XAG/XPT/XPD) + currency dropdown centered in landing nav
- Settings modal (pencil button): name edit, dark/light theme, currency picker
- `SettingsModal`, `CurrencyPicker` components
- `GET /prices/fx-rates`, `PATCH /auth/me/preferences`, `PATCH /auth/me/profile` endpoints
- Migration 0014: `preferred_currency` on users table
- Currency preference persists across logout/login via `reloadUserPrefs()`

### News feed (Option A — Redis-backed)
- **Feeds**: FT Commodities, Investing.com Economy, Silver Institute
  - Kitco/mining.com both return 403 from server — replaced with FT + Investing.com
- `st-current-price-fetcher/fetcher/news.py`: fetches every 30 min, dedup by URL, sort by date, stores 30 items with 2h TTL
- `st-backend/app/routes/news.py`: `GET /news/feed` — reads Redis, no auth
- `st-frontend/src/components/landing/NewsFeed.tsx`: headlines with source badge, relative time, hover accent
- Test counts: fetcher 89, backend 185, frontend 400

## Stacking Tracker — work done 2026-03-26 (session 4 — end of day)

### Test counts (final)
- st-backend: **213 tests** (was 185 — added 28 new tests)
- st-current-price-fetcher: **89 tests** (unchanged)
- st-frontend: **400 tests** (unchanged)

### New backend tests
- `test_routes_fx_rates.py`: 7 tests for GET /prices/fx-rates
- `test_routes_news.py`: 8 tests for GET /news/feed
- `test_routes_preferences.py`: 13 tests for PATCH /auth/me/preferences + PATCH /auth/me/profile

### Bug fix — route ordering
- `GET /prices/fx-rates` was shadowed by `/{metal}` wildcard — moved before it

### Other fixes today
- Landing page: logo blend mode fix (mix-blend-multiply removes white border in light mode)
- AddToStackForm: Weight selector for multi-size products (e.g. American Gold Eagle 1/10oz, 1/4oz, etc.)
- Settings modal: Gravatar explanation note with link
- SettingsModal: "Size" → "Weight" label, weight fields hidden when catalogue variant selected
- Logo: new logo.png received, near-white background stripped transparent via PIL
- All docs updated (README + UNIT_TESTS.md) across all 3 repos

## Stacking Tracker — work done 2026-03-28

### st-frontend
- **Catalogue filter bug fix**: React key collision on `ProductGroupRow` — key was `name||metal_type||mint` but grouping key included weight. Multi-variant products (e.g. American Gold Eagle 4 weights) caused keys to collide → table appeared frozen while count updated. Fixed by including weight in the row key.
- **Mint filter dropdown**: Dynamic dropdown on catalogue page, populates from loaded products, chains with metal pills + search. Highlights accent colour when active.
- **year_start/year_end in ProductCombobox**: Dropdown items and selected label now show `1986–present` instead of single year. Year search also queries year_start/year_end.
- **AddToStackForm year picker**: Now expands full `year_start–year_end` range (e.g. 1986–present → 1986 through current year) instead of just the single DB row year.
- **AddToStackForm name suggestion list**: Was showing `Gold · 1 year` (DB row count). Now shows `Gold · 1979–present` from year_start/year_end.

### st-backend
- **Migration 0015**: `year_start` (nullable int) + `year_end` (nullable int) on products table
- **Product model + schema**: Both fields added, exposed in `ProductResponse`
- **seed_mint_products.py**: `_parse_years()` parses `years_issued` column (handles em-dash, en-dash, ascii dash, "present", single years, ranges). Sets `year_start`/`year_end`; `year` column set to `year_end` or `year_start` for ongoing products (no more hardcoded 2024)
- **Tests**: 9 new `_parse_years` unit tests + 3 product field assertions → 223 tests passing

## Stacking Tracker — production deployment (2026-03-28)

### Architecture
- Host machine runs: PostgreSQL (port 5432), Redis (172.17.0.1 + 127.0.0.1)
- st-backend: Docker container, binds to `172.17.0.1:8020` (not public)
- st-frontend: Docker container, public port 3000, nginx proxies `/api/` → `host.docker.internal:8020`
- st-current-price-fetcher: Docker container, connects to Redis + backend via `host.docker.internal`
- `extra_hosts: host-gateway` in all three docker-compose files for Linux host resolution

### st-backend
- `APP_PORT=8020` in `.env` (configurable via `APP_PORT` env var)
- Port bound to `172.17.0.1` only — not public internet
- `DATABASE_URL` uses `host.docker.internal` to reach host Postgres
- `pg_hba.conf` needs `host stacking_tracker stacker 172.16.0.0/12 scram-sha-256`
- Pydantic Settings has `extra = "ignore"` so `POSTGRES_*` vars don't error

### st-frontend
- `VITE_API_BASE_URL=/api` (relative, baked in at build time)
- `BACKEND_PORT=8020` (injected into nginx.conf via envsubst at container start)
- nginx.conf in `templates/` dir for envsubst; proxies `/api/` → `host.docker.internal:${BACKEND_PORT}`
- `buildUrl()` in api.ts handles relative base URLs (was crashing with `new URL('/api', ...)`)
- Both `request()` and `adminRequest()` use `buildUrl()`

### st-current-price-fetcher
- `REDIS_URL=redis://host.docker.internal:6379`
- `BACKEND_URL=http://host.docker.internal:8020` (no `/api/v1` prefix — backend routes are at `/prices/...` directly)
- Backfill uses batch range queries (1 HTTP call per metal) to avoid yfinance rate limiting
- yfinance fallback: GC=F (gold), SI=F (silver), PL=F (platinum), PA=F (palladium)

### Redis security
- Bound to `127.0.0.1 172.17.0.1` only — not exposed publicly

## Rev V2 — work done 2026-03-29 (full day session)

### rev-v2-backend — complete API build-out

Starting from a basic scaffold, we closed every frontend API gap and built a production-ready backend structure.

**Config cleanup:**
- Replaced monolithic `REV_V2_DATABASE_URL` with `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DATABASE`, `DB_PORT`
- Removed dead `REV_V2_FRONTEND_URL` and `REV_V2_DEMO_SECRET`
- `docker-compose.yml` now reads `.env` with `${VAR:-default}` fallback

**Schema rename (gigs → events):**
- `Gig` → `Event`, `GigApplication` → `EventApplication`, `GigStatus` → `EventStatus`
- `gig_id` FK columns → `event_id` across all tables
- Two old migrations squashed into single `0001_initial_schema.py`
- Added `hero_image_path` and `age_limit` to events table

**New models + migrations:**
- `0002` — `crawled_venues`
- `0003` — `feed_posts`, `feed_post_likes`, `feed_comments`
- `0004` — `follows`
- `0005` — `tickets`
- `0006` — `conversation_threads`, `conversation_messages` + venue workspace fields
- `0007` — `boosts`

**AccountType enum:** `fan`, `artist`, `venue`, `promoter`, `admin`

**Routes added/updated:**
- `GET /venues/search` (q ILIKE, city, limit)
- `GET /venues/{id}` now accepts UUID or user_id
- `VenueSummary` exposes `user_id`, `image_path`, `address`, `location` aliases
- `GET/POST /venues/{id}` auto-populates `location_point` PostGIS from lat/lng
- `GET /artists` with limit; `GET /artists/{id}` accepts UUID or user_id
- `ArtistSummary` exposes `user_id`, `image_path`, `genre` (comma string), `artist_type`, `follower_count` aliases
- `GET /crawled-venues` with `has_location`, city, limit
- Full feed system: `GET/POST /feed/posts`, `POST /feed/posts/{id}/like`, `GET/POST /feed/posts/{id}/comments`, `GET /feed/recommended`
- `POST /follows/toggle`, `GET /follows/check`, `GET /follows/mine`
- `GET /tickets/mine`, `POST /tickets`
- `GET /ratings/subject/{type}/{id}/summary`, `GET /ratings/subject/{type}/{id}`, `GET /ratings/recent`, `POST /ratings`, `POST /ratings/{id}/report`
- Full dashboard: `GET /dashboard/stats`, `/activity`, `/progress`, `/venue-workspace`, `/artist-workspace`, `/admin-workspace`
- `GET /boosts/event/{id}`, `GET /boosts/mine`, `POST /boosts`
- Register/login now accept frontend shape: `{ email, password, display_name, role }`
- `SessionResponse` exposes top-level `role`, `display_name`, `user_id`
- `SessionUser` exposes `role` and `display_name` aliases
- Duplicate email on register → 409

**Docs:**
- README.md — full rewrite
- UNIT_TESTS.md — full rewrite (19 test files)
- POSTGRES.md — new: full manual DB setup guide with all GRANTs, PostGIS, Docker-on-host config

**Tests:** 19 test files covering every endpoint

## Rev V2 — work done 2026-03-29 (initial)

### Repos cloned
- `rev-v2-backend` → `/home/blair/.openclaw/workspace/devbro/rev-v2-backend`
- `rev-v2-frontend` → `/home/blair/.openclaw/workspace/devbro/rev-v2-frontend`
- Both use `github-paindog` SSH host alias (blairhoddinott-bot key)

### rev-v2-backend
- **Stack:** FastAPI + SQLAlchemy async (asyncpg) + PostgreSQL/PostGIS + Alembic + Pydantic v2 + uv
- **Prefix:** all routes under `/api/v1`
- **Config:** no `REV_V2_` prefix anymore — bare `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DATABASE`, `DB_PORT` env vars; assembled into psycopg URL in `Settings.effective_database_url`; docker-compose reads `.env` with `${VAR:-default}` fallback
- **Auth:** demo-grade placeholder — no bcrypt, no real JWT; token format `demo:<role>:<user_id>`; roles enforced via `X-Actor-Role` header
- **Schema rename:** `gigs` → `events`, `gig_applications` → `event_applications`; all `gig_id` FK columns → `event_id`; `GigStatus` → `EventStatus`; two Alembic migrations squashed into single `0001_initial_schema.py`
- **New fields on events table:** `hero_image_path`, `age_limit`
- **Routes:** `/events` replaces `/gigs` — full lifecycle (create/list/search/get/patch/apply/select-artist/confirm/decline/cancel/complete) + new `GET /events/search?venue_id&artist_id&upcoming_only&q&limit`
- **Seed:** `seed_db.py` has 18 events, 6 artists, 4 venues, full applications/confirmations/map_events/notifications/incidents/appeals
- **Tests:** 12 test files, all updated to use `make_event` / `/events` / `event_id`

### rev-v2-frontend
- **Stack:** React 18 + Vite, React Router v6, Tailwind, Leaflet, Axios
- **Public homepage:** `/map` — Leaflet map of Toronto venues, clusters, genre filter, user geolocation
- **API layer:** `src/api/index.js` — all calls use `withFallback(realFn, mockFn)` pattern; falls back to demo data if backend is down or user is in demo session
- **Demo accounts:** `fan/artist/venue/admin @revdemo.com` / `Demo123!`
- **Key gap:** frontend calls `/events`, `/events/search`, `/crawled-venues`, `/feed/*`, `/follows/*`, `/tickets/*`, `/ratings/*`, `/dashboard/*`, `/boosts/*` — most of these don't exist in backend yet
- **Workspace UIs:** VenueWorkspace + ArtistWorkspace are fully built but all writes are local-state only (not wired to backend)
- **Fan role** not yet in backend `AccountType` enum

## Future projects / backlog

### Google OAuth (st-backend + st-frontend)
- Use `authlib` + `httpx` in FastAPI — no Better Auth needed (TS only, not Python)
- New endpoints: `GET /auth/google`, `GET /auth/google/callback`
- DB: add nullable `google_id` to users, make `password_hash` nullable
- Alembic migration 0008
- Frontend: "Sign in with Google" button → backend redirect → callback route reads `?token=` from URL → localStorage
- Needs: Google Cloud project with OAuth 2.0 credentials (Client ID + Secret)
- Plan is fully worked out, ready to build when the time comes

## Important rules Blair set
- **Default coding path:** for heavier development work, use a **Claude Code** ACP session with the `sonnet` model alias (Claude Sonnet 4.6)
- **Always ask before spawning agents** — no exceptions
- **Simple edits / one-liners:** do them directly without spawning an agent when appropriate
- **Always `git pull` before starting any work**
- **Always `git pull` before pushing**
- **Blair's name is capitalized: Blair, not blair**

## SSH / Git setup
- SSH key for blairhoddinott GitHub: `/home/blair/.openclaw/workspace/.ssh/blairhoddinott-bot`
- SSH host alias: `github-blairhoddinott`
- SSH host alias: `github-paindog` (paindog org, same blairhoddinott-bot key)
- Git config: `GIT_CONFIG_GLOBAL=/home/blair/.openclaw/workspace/devbro/.gitconfig`
- GPG: `GNUPGHOME=/home/blair/.openclaw/workspace/.gnupg`
- **NEVER use `GIT_SSH_COMMAND`** — `core.sshCommand` in `.gitconfig` handles it
- **NEVER use raw `git@github.com:...` URLs** — always use `git push origin` / `git pull origin`
- Only two env vars needed for ALL git ops: `GIT_CONFIG_GLOBAL` + `GNUPGHOME`
- SSH config is at `/home/blair/.openclaw/workspace/.ssh/config` (NOT `~/.ssh/config`)
- `.gitconfig` `core.sshCommand` explicitly points to this config + blairhoddinott-bot key
- Remotes use `github-blairhoddinott` host alias — raw `github.com` URLs bypass this and fail

## Docker
- Docker is installed on this server
- `blair` user is in the `docker` group but the process needs a full re-login to pick it up
- Workaround: `sudo -g docker docker ...` until blair reboots/re-logs in
- coverage.sh auto-detects and uses `sudo -g docker` if needed

## Stack context
- gigvenues / RevMuzik: FastAPI + PostGIS backend, Vite/React frontend
- GitHub: blairhoddinott account
- revmuzik-backend is also in workspace at `/home/blair/.openclaw/workspace/devbro/revmuzik-backend`
