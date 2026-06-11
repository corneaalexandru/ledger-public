#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

HOST="${LEDGER_HOST:-127.0.0.1}"
PORT="${LEDGER_PORT:-8765}"
PYTHON_BIN="${LEDGER_PYTHON:-python3}"

echo "Starting Ledger Public at http://${HOST}:${PORT}"
exec "$PYTHON_BIN" server.py --host "$HOST" --port "$PORT" --open
