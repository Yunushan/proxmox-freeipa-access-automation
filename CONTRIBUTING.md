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

- `ansible-lint`
- `yamllint .`
- `ansible-playbook --syntax-check` for all playbooks

They generate a temporary example inventory under `.ansible/` so they do not depend on a contributor's real production inventory or encrypted vault.

## Running Playbooks Locally

For PowerShell users, the repository includes a small playbook wrapper:

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

Shell users can continue to call `ansible-playbook` directly.

When changing behavior that affects real infrastructure, contributors should prefer:

1. `validate.yml`
2. syntax and lint checks
3. a limited test run against one safe target or lab environment
4. broader rollout only after that

## Inventory and Secret Handling

Do not commit:

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/vault.yml`
- generated files under `collections/`
- compiled cache artifacts such as `__pycache__/` and `*.pyc`

Use the example files as templates:

- `inventories/production/hosts.yml.example`
- `inventories/production/group_vars/all/vault.yml.example`

Store secrets only in the vault file, not in plaintext inventory or group vars.
Keep public examples generic. Do not replace documentation placeholders with real company domains, internal hostnames, personal usernames, or private email addresses.

## Proxmox Compatibility

The repository currently targets Proxmox VE major versions:

- `7`
- `8`
- `9`

If you change Proxmox-facing behavior:

- review the `pveum` and `pvesh` flags being used
- update validation if the compatibility envelope changes
- update both `README.md` and `docs/ARCHITECTURE.md`

## Documentation Expectations

Update documentation when you change:

- installation flow
- supported platforms or versions
- playbook behavior
- validation or lint workflow
- repository helper scripts

At minimum, review:

- `README.md`
- `docs/ARCHITECTURE.md`
- this file

## Pre-commit Hooks

If you use `pre-commit`, install the hooks with:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

The hook uses the repository's cross-platform lint wrapper and runs the same checks intended for CI.

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
