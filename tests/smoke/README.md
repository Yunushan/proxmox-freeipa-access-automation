# Smoke Tests

The smoke-test workflow validates the repository's public examples and entrypoints without talking to real infrastructure.

## What It Checks

- the example inventory and split `group_vars/all` files load together
- the example vault placeholder is sufficient for syntax-only validation
- each shipped playbook passes `ansible-playbook --syntax-check`

## How To Run

```bash
python scripts/smoke-test.py
```

```powershell
python .\scripts\smoke-test.py
```

## Notes

- the smoke script builds a temporary inventory under `.ansible/`
- it uses `inventories/production/hosts.yml.example`
- it copies the public `group_vars/all` files and materializes `vault*.yml.example` files as matching `.yml` files
- it does not verify live connectivity, SSH trust, or target-side commands
