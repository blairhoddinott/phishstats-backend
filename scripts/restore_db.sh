#!/usr/bin/env bash
set -euo pipefail

INPUT_FILE="${1:-backup.sql}"
if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Backup file not found: $INPUT_FILE" >&2
  exit 1
fi
cat "$INPUT_FILE" | docker compose exec -T db psql -U phishstats -d phishstats
echo "Database restore completed from $INPUT_FILE"
