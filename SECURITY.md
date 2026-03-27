# Security Policy

## Scope

This repository automates security-sensitive infrastructure behavior, including:

- FreeIPA access model changes
- Proxmox LDAP realm configuration
- Proxmox RBAC bindings
- Linux guest enrollment into FreeIPA
- handling of bind credentials and vault-managed secrets

Because of that, issues in this project can have real access-control impact even when they look like ordinary automation bugs.

## Supported Code Line

This repository does not currently maintain multiple long-lived release branches.

Security fixes should be made against the latest maintained branch or latest repository state.
Older snapshots and forks should be treated as unsupported unless a maintainer explicitly states otherwise.

## Reporting a Vulnerability

Please do **not** open a public issue for a suspected vulnerability if it could expose:

- credentials
- vault content
- internal hostnames or inventory details
- access-control bypasses
- insecure default behavior that could be abused before a fix is available

Preferred reporting approach:

1. use a private vulnerability reporting channel if the repository host provides one
2. share the minimum information needed to reproduce the issue
3. redact secrets, inventory details, IPs, and hostnames unless they are absolutely required

If private reporting is not available, contact the maintainer through a private channel before publishing details.

## What to Include in a Report

A useful security report should include:

- affected file or playbook
- impacted environment area such as FreeIPA, Proxmox, or Linux clients
- what the unsafe behavior is
- how it can be reproduced
- what conditions are required
- expected impact
- whether credentials, tokens, vault values, or inventory data were exposed

## Secret Handling Expectations

When discussing or reproducing a security issue:

- never paste real vault content
- never paste real LDAP bind passwords
- never publish production inventory files
- use sanitized examples whenever possible

This repository is designed so secrets belong in:

- `inventories/production/group_vars/all/vault.yml`

They should not be moved into plaintext files for debugging or convenience.

## Safe Reproduction Guidance

If you are validating a suspected issue:

- prefer a lab or disposable environment
- limit tests to a narrow host set
- avoid running changes broadly until impact is understood
- document whether the issue affects Proxmox VE `6`, `7`, `8`, `9`, or provisional `10`

## Fix Expectations

Security-related fixes should usually include:

- the code change
- validation updates if relevant
- documentation updates in `README.md`, `docs/ARCHITECTURE.md`, or `CONTRIBUTING.md` when behavior changes
- notes about compatibility or rollout risk if the fix changes defaults

## Public Disclosure

Public disclosure should happen only after:

- the issue is understood
- affected users have a reasonable path to mitigation
- sensitive details have been removed from examples and discussion
