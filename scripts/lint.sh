#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

for cmd in ansible-lint yamllint ansible-playbook; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "$cmd was not found in PATH." >&2
    exit 1
  fi
done

LINT_INVENTORY_ROOT="$ROOT_DIR/.ansible/lint-inventory"
LINT_GROUP_VARS_DIR="$LINT_INVENTORY_ROOT/group_vars/all"
LINT_INVENTORY_FILE="$LINT_INVENTORY_ROOT/hosts.yml"

mkdir -p "$LINT_GROUP_VARS_DIR"
cp inventories/production/hosts.yml.example "$LINT_INVENTORY_FILE"
cp inventories/production/group_vars/all/main.yml "$LINT_GROUP_VARS_DIR/main.yml"
cp inventories/production/group_vars/all/vault.yml.example "$LINT_GROUP_VARS_DIR/vault.yml"
export ANSIBLE_INVENTORY="$LINT_INVENTORY_FILE"

cleanup() {
  rm -rf "$LINT_INVENTORY_ROOT"
}
trap cleanup EXIT

echo "Running: ansible-lint"
ansible-lint

echo "Running: yamllint ."
yamllint .

for playbook in \
  playbooks/freeipa.yml \
  playbooks/proxmox.yml \
  playbooks/linux-clients.yml \
  playbooks/site.yml \
  playbooks/validate.yml
do
  echo "Running: ansible-playbook --syntax-check -i $LINT_INVENTORY_FILE $playbook"
  ansible-playbook --syntax-check -i "$LINT_INVENTORY_FILE" "$playbook"
done
