# Changelog

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows semantic versioning when tagged releases are introduced.

## [Unreleased]

### Added

- Split inventory variable files for features, FreeIPA, Linux clients, Proxmox LDAP, sync, and RBAC.
- Shared Linux inventory-preparation and hostname-resolution playbook includes.
- Linux guest source modes for static inventory, IP-only/manual definitions, and Proxmox VM discovery.
- Optional Linux local-user conflict detection so IPA-backed admin users can be checked against existing local `/etc/passwd` usernames in warn-only or fail-fast mode during enrollment.
- Proxmox discovery blacklist controls so infrastructure VMs can be excluded by VMID, IP, or name even on discovery-enabled nodes.
- A dedicated `linux-readiness-report.yml` playbook and `linux_readiness_report` role for read-only Linux runtime audits covering SSH readiness and Proxmox QEMU Guest Agent status.
- Proxmox LDAP realm automation no longer passes unsupported `--autocreate` or `--groups-autocreate` flags for LDAP realms, relying on sync defaults and realm sync behavior instead.
- A separate Windows management workflow with `windows_management_clients`, a dedicated `windows-management.yml` playbook, and a `windows_domain_membership` role for Active Directory domain membership.
- A separate helper-only Windows FreeIPA workflow with `windows_freeipa_helper_clients`, a dedicated `windows-freeipa-helpers.yml` playbook, and a `windows_freeipa_helpers` role for IPA CA trust import, optional CA auto-fetch with thumbprint pinning, hosts bootstrap, IPA service reachability checks, time-source validation, local group management, and OpenSSH helpers.
- A dedicated `windows-freeipa-validate.yml` playbook for validation-only checks against `windows_freeipa_helper_clients` without mutating CA trust, hosts entries, local groups, or OpenSSH state.
- Per-host `windows_freeipa_helpers_summary` reporting for the helper-only Windows FreeIPA workflow.
- An event-driven Proxmox hook and controller webhook workflow for immediate Linux guest onboarding after `post-start` and `post-migrate` VM events.
- Role-level `meta/main.yml` and `README.md` files for every local role.
- Repository governance files: `.editorconfig` and `.github/CODEOWNERS`.
- A dedicated `tests/` surface with smoke-test documentation and a reusable `scripts/smoke-test.py` entrypoint.
- Domain-scoped FreeIPA and Proxmox vault example files instead of one shared secret bundle.
- A separate Windows vault example and vault-helper support for optional WinRM and Windows domain-join secrets.
- Vault helper scripts and multi-vault playbook wrapper support for split FreeIPA and Proxmox secret handling.

### Changed

- Standalone playbooks now honor the same feature flags as the full-site rollout.
- Linux execution targets now use the generated `linux_ipa_clients_runtime` group.
- Windows support now runs as a separate AD-based workflow instead of being mixed into the Linux IPA enrollment path.
- Windows documentation now also distinguishes helper-only FreeIPA-aware Windows tasks from real AD-backed Windows domain membership.
- `scripts/run-playbook.ps1` now supports custom inventory paths, tags, skip-tags, become prompts, and repeated extra-vars inputs.
- Oversized FreeIPA and Proxmox role entrypoints are now split into smaller task include files for validation, state discovery, apply, sync, and guest-processing flows.
- Lint and smoke validation are now separated, and SSH host key checking is enabled by default again.
- The FreeIPA collection dependency is now pinned to an exact version, and smoke setup now materializes all example vault files automatically.
- Playbooks, preparation includes, and validation paths now use a documented and consistent operator tag model.
- Rollout serial and failure-budget controls are now centralized in inventory vars and applied across FreeIPA, Proxmox, Linux, and validation paths.
- Proxmox VM discovery can now optionally filter by VMID, which is used by the event-driven onboarding workflow.
