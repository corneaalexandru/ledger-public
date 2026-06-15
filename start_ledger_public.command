#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

HOST="${LEDGER_HOST:-127.0.0.1}"
PORT="${LEDGER_PORT:-8765}"
PYTHON_BIN="${LEDGER_PYTHON:-python3}"

if [ -d ".git" ] && command -v git >/dev/null 2>&1; then
  echo "Checking for Ledger Public updates..."
  git pull --ff-only || echo "Update skipped. Continuing with the installed version."
fi

if ! "$PYTHON_BIN" - <<'PY' >/dev/null 2>&1
import googleapiclient.discovery
import google.oauth2.service_account
PY
then
  echo "Installing Google Sheets requirements..."
  "$PYTHON_BIN" -m pip install -r requirements-google.txt
fi

REQUESTED_PORT="$PORT"
PORT="$("$PYTHON_BIN" - "$HOST" "$REQUESTED_PORT" <<'PY'
import socket
import sys

host = sys.argv[1] or "127.0.0.1"
start = int(sys.argv[2])
bind_host = "127.0.0.1" if host in {"", "0.0.0.0", "::"} else host
family = socket.AF_INET6 if ":" in bind_host else socket.AF_INET
for port in range(start, start + 100):
    with socket.socket(family, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((bind_host, port))
        except OSError:
            continue
        print(port)
        break
else:
    raise SystemExit(f"No free port found from {start} to {start + 99}.")
PY
)"

if [ "$PORT" != "$REQUESTED_PORT" ]; then
  echo "Port ${REQUESTED_PORT} is already in use. Using ${PORT} instead."
fi

echo "Starting Ledger Public at http://${HOST}:${PORT}"
exec "$PYTHON_BIN" server.py --setup --store google --host "$HOST" --port "$PORT" --open
