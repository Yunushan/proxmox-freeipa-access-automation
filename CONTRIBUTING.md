# Contributing

Thanks for contributing to this repository.

This project is an Ansible automation workspace for:

- FreeIPA access modeling
- Proxmox LDAP realm and RBAC automation
- Linux guest enrollment into FreeIPA

The repository assumes that FreeIPA remains the source of truth.
Contributions should preserve that model unless the change is explicitly intended to redesign it.

## Development Principles

- keep secrets out of Git
- preserve idempotent behavior where possible
- prefer small, reviewable changes
- update docs when behavior or supported versions change
- avoid adding alternate workflows that duplicate existing helpers unless there is a clear reason

## Environment Setup

Install the required Ansible collection first:

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

If you want the same checks used in CI, make sure these tools are installed and available in `PATH`:

- `ansible-playbook`
- `ansible-inventory`
- `ansible-lint`
- `yamllint`

Optional but recommended:

- `pre-commit`

## Local Validation Workflow

For the full local lint pass:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

Those wrappers run:

- `python scripts/lint.py`
- `python scripts/smoke-test.py`

The smoke layer generates a temporary example inventory under `.ansible/` so it does not depend on a contributor's real production inventory or encrypted vault.

For the smoke checks directly:

```bash
python scripts/smoke-test.py
```

## Running Playbooks Locally

For PowerShell users, the repository includes a small playbook wrapper:

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook proxmox -Inventory inventories\production\hosts.yml -Tags proxmox,proxmox_rbac -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Shell users can continue to call `ansible-playbook` directly.

Repository defaults keep SSH host key checking enabled. For isolated lab work only, opt out per shell session with `ANSIBLE_HOST_KEY_CHECKING=False` instead of changing `ansible.cfg`.

The wrapper now supports these first-class options:

- `-Inventory`
- `-Tags`
- `-SkipTags`
- `-VaultId`
- `-AskBecomePass`
- repeated `-ExtraVars` values

For split vault operations, use:

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
.\scripts\vault.ps1 -Action view -Domain freeipa -FreeipaVaultId freeipa@prompt
```

```bash
./scripts/vault.sh --action encrypt --domain all
./scripts/vault.sh --action view --domain proxmox --proxmox-vault-id proxmox@prompt
```

Use `-AskVaultPass` only when both vault files share the same password. Use `-VaultId` when FreeIPA and Proxmox secrets are encrypted separately.

The stable operator tags are:

- `freeipa`, `freeipa_access`
- `proxmox`, `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `linux`, `linux_enroll`
- `inventory`, `discovery`, `hostnames`
- `validate`

When changing behavior that affects real infrastructure, contributors should prefer:

1. `validate.yml`
2. syntax and lint checks
3. a limited test run against one safe target or lab environment
4. broader rollout only after that

## Inventory and Secret Handling

Do not commit:

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- generated files under `collections/`
- compiled cache artifacts such as `__pycache__/` and `*.pyc`

Use the example files as templates:

- `inventories/production/hosts.yml.example`
- `inventories/production/group_vars/all/vault-freeipa.yml.example`
- `inventories/production/group_vars/all/vault-proxmox.yml.example`

Store secrets only in the vault file, not in plaintext inventory or group vars.
Keep public examples generic. Do not replace documentation placeholders with real company domains, internal hostnames, personal usernames, or private email addresses.

## Proxmox Compatibility

The repository currently targets Proxmox VE major versions:

- `6`
- `7`
- `8`
- `9`
- `10` (provisional future-release gate)

If you change Proxmox-facing behavior:

- review the `pveum` and `pvesh` flags being used
- update validation if the compatibility envelope changes
- update both `README.md` and `docs/ARCHITECTURE.md`
- keep future-major entries clearly labeled as provisional until they are verified against a released Proxmox version
- do not claim legacy `1.x` to `5.x` support in public documentation unless the full workflow has been validated against those releases

## Documentation Expectations

Update documentation when you change:

- installation flow
- supported platforms or versions
- playbook behavior
- variable file layout
- rollout-control defaults
- validation or lint workflow
- repository helper scripts

At minimum, review:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/VARIABLES.md`
- this file

## Role Packaging

Every local role should keep a minimum documentation and metadata surface:

- `defaults/main.yml` for public defaults
- `tasks/main.yml` for the role entrypoint
- `meta/main.yml` for metadata
- `README.md` for role purpose, variables, and execution notes

## Pre-commit Hooks

If you use `pre-commit`, install the hooks with:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

The hook intentionally runs the fast lint layer only. Use `scripts/lint.sh`, `scripts/lint.ps1`, or `python scripts/smoke-test.py` for the full smoke pass.

## Pull Requests

A good pull request should include:

- a clear statement of what changed
- why the change is needed
- any compatibility or migration notes
- any documentation updates required by the change

If the change affects infrastructure behavior, include what was used to validate it:

- syntax check only
- lint only
- lab test
- targeted host test
- production verification
