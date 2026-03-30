# Changelog

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows semantic versioning when tagged releases are introduced.

## [Unreleased]

### Added

- Split inventory variable files for features, FreeIPA, Linux clients, Proxmox LDAP, sync, and RBAC.
- Shared Linux inventory-preparation and hostname-resolution playbook includes.
- Linux guest source modes for static inventory, IP-only/manual definitions, and Proxmox VM discovery.
- Role-level `meta/main.yml` and `README.md` files for every local role.
- Repository governance files: `.editorconfig` and `.github/CODEOWNERS`.
- A dedicated `tests/` surface with smoke-test documentation and a reusable `scripts/smoke-test.py` entrypoint.
- Domain-scoped FreeIPA and Proxmox vault example files instead of one shared secret bundle.
- Vault helper scripts and multi-vault playbook wrapper support for split FreeIPA and Proxmox secret handling.

### Changed

- Standalone playbooks now honor the same feature flags as the full-site rollout.
- Linux execution targets now use the generated `linux_ipa_clients_runtime` group.
- `scripts/run-playbook.ps1` now supports custom inventory paths, tags, skip-tags, become prompts, and repeated extra-vars inputs.
- Oversized FreeIPA and Proxmox role entrypoints are now split into smaller task include files for validation, state discovery, apply, sync, and guest-processing flows.
- Lint and smoke validation are now separated, and SSH host key checking is enabled by default again.
- The FreeIPA collection dependency is now pinned to an exact version, and smoke setup now materializes all example vault files automatically.
- Playbooks, preparation includes, and validation paths now use a documented and consistent operator tag model.
- Rollout serial and failure-budget controls are now centralized in inventory vars and applied across FreeIPA, Proxmox, Linux, and validation paths.
