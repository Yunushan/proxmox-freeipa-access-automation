#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ansible-galaxy collection install -r requirements.yml -p "$ROOT_DIR/collections"
python scripts/patch_freeipa_collection.py

echo "Collections installed and patched successfully."
