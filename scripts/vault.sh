#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v ansible-vault >/dev/null 2>&1; then
  echo "ansible-vault was not found in PATH." >&2
  exit 1
fi

ACTION=""
ENVIRONMENT="production"
FREEIPA_VAULT_ID="freeipa@prompt"
PROXMOX_VAULT_ID="proxmox@prompt"
DOMAINS=()

usage() {
  cat <<'EOF'
Usage: ./scripts/vault.sh --action <encrypt|decrypt|view> [--domain <freeipa|proxmox|all>] [--environment <name>] [--freeipa-vault-id <spec>] [--proxmox-vault-id <spec>]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --action)
      ACTION="$2"
      shift 2
      ;;
    --domain)
      DOMAINS+=("$2")
      shift 2
      ;;
    --environment)
      ENVIRONMENT="$2"
      shift 2
      ;;
    --freeipa-vault-id)
      FREEIPA_VAULT_ID="$2"
      shift 2
      ;;
    --proxmox-vault-id)
      PROXMOX_VAULT_ID="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$ACTION" ]]; then
  echo "--action is required." >&2
  usage >&2
  exit 1
fi

case "$ACTION" in
  encrypt|decrypt|view) ;;
  *)
    echo "Unsupported action: $ACTION" >&2
    exit 1
    ;;
esac

if [[ ${#DOMAINS[@]} -eq 0 ]]; then
  DOMAINS=("all")
fi

map_domain() {
  local domain="$1"
  case "$domain" in
    freeipa)
      VAULT_PATH="inventories/$ENVIRONMENT/group_vars/all/vault-freeipa.yml"
      VAULT_EXAMPLE_PATH="inventories/$ENVIRONMENT/group_vars/all/vault-freeipa.yml.example"
      VAULT_ID_SPEC="$FREEIPA_VAULT_ID"
      ;;
    proxmox)
      VAULT_PATH="inventories/$ENVIRONMENT/group_vars/all/vault-proxmox.yml"
      VAULT_EXAMPLE_PATH="inventories/$ENVIRONMENT/group_vars/all/vault-proxmox.yml.example"
      VAULT_ID_SPEC="$PROXMOX_VAULT_ID"
      ;;
    *)
      echo "Unsupported domain: $domain" >&2
      exit 1
      ;;
  esac
}

is_encrypted() {
  local path="$1"
  [[ -f "$path" ]] && head -n 1 "$path" | grep -q '^\$ANSIBLE_VAULT'
}

run_domain() {
  local domain="$1"
  map_domain "$domain"

  if [[ "$ACTION" == "encrypt" && ! -f "$VAULT_PATH" ]]; then
    if [[ ! -f "$VAULT_EXAMPLE_PATH" ]]; then
      echo "Vault example file does not exist: $VAULT_EXAMPLE_PATH" >&2
      exit 1
    fi

    cp "$VAULT_EXAMPLE_PATH" "$VAULT_PATH"
  fi

  if [[ ! -f "$VAULT_PATH" ]]; then
    echo "Vault file does not exist: $VAULT_PATH" >&2
    exit 1
  fi

  if [[ "$ACTION" == "encrypt" ]] && is_encrypted "$VAULT_PATH"; then
    echo "Skipping already encrypted $domain vault: $VAULT_PATH"
    return
  fi

  if [[ "$ACTION" == "decrypt" ]] && ! is_encrypted "$VAULT_PATH"; then
    echo "Skipping plaintext $domain vault: $VAULT_PATH"
    return
  fi

  if [[ "$ACTION" == "view" ]] && ! is_encrypted "$VAULT_PATH"; then
    echo "Contents of plaintext $domain vault: $VAULT_PATH"
    cat "$VAULT_PATH"
    return
  fi

  echo "Running: ansible-vault $ACTION --vault-id $VAULT_ID_SPEC $VAULT_PATH"
  ansible-vault "$ACTION" --vault-id "$VAULT_ID_SPEC" "$VAULT_PATH"
}

if printf '%s\n' "${DOMAINS[@]}" | grep -qx 'all'; then
  run_domain freeipa
  run_domain proxmox
else
  for domain in "${DOMAINS[@]}"; do
    run_domain "$domain"
  done
fi
