# RevMuzik TODO

## Frontend

- [ ] **Promoter page** — wire `boostsApi.mine()` to show the promoter's own boost requests
- [ ] **MapPage** — add crawled venues as markers (they have lat/lon, just need to query `crawled_venues` via a new endpoint)
- [ ] **Admin section** — `/admin/*` pages not yet built (manage users, events, venues, ratings moderation)

## Backend

- [ ] **`GET /crawled-venues`** endpoint — so the map can show imported venues alongside native ones
- [ ] **Scheduled crawl** — cron job or systemd timer to re-run `crawl_musiccrawler.py` daily

## Deployment

- [ ] Set up domain + nginx SSL for RevMuzik frontend (similar to pizza.weepytests.com)
- [ ] Open `feature/dockerfile` PR for pizzadeal-backend on GitHub (no token, must be done manually)
