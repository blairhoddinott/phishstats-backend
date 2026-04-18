# Unit Tests

## Test stack
- `pytest`
- `pytest-asyncio`
- `httpx`

## Running tests

Create a virtualenv, install dependencies, then run:

```bash
pytest
```

## Current coverage
The scaffold currently covers:
- API root smoke test
- health endpoint smoke test
- static album seed data shape and completeness checks
- static song seed uniqueness and album track mapping checks
- direct song-to-album seed coverage via per-album ordered track mappings
- repeated-track edge case coverage (`Rift` includes `Lengthwise` twice)
- migration-aware documentation of the direct `songs.album_id` + `songs.track_number` model

Expand coverage as real business routes, migration tests, and database-backed seed tests are added.
