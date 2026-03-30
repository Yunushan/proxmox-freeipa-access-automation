#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "python or python3 was not found in PATH." >&2
  exit 1
fi

echo "Running: $PYTHON_BIN scripts/lint.py"
"$PYTHON_BIN" scripts/lint.py

echo "Running: $PYTHON_BIN scripts/smoke-test.py"
"$PYTHON_BIN" scripts/smoke-test.py
