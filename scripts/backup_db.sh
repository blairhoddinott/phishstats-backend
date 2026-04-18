#!/usr/bin/env bash
set -euo pipefail

OUTPUT_FILE="${1:-backup.sql}"
docker compose exec -T db pg_dump -U phishstats -d phishstats > "$OUTPUT_FILE"
echo "Database backup written to $OUTPUT_FILE"
