<div align="center">

# Proxmox + FreeIPA Access Automation

**FreeIPA-first Ansible automation for Proxmox VE access, LDAP realm sync, RBAC, and Linux guest enrollment.**

<p>
  <img src="https://img.shields.io/badge/Ansible-Core%202.14%2B-EE0000?style=for-the-badge&logo=ansible&logoColor=white" alt="Ansible Core 2.14+" />
  <img src="https://img.shields.io/badge/Proxmox-VE%206.x%20%7C%207.x%20%7C%208.x%20%7C%209.x%20%7C%2010.x-E57000?style=for-the-badge" alt="Proxmox VE 6.x 7.x 8.x 9.x 10.x" />
  <img src="https://img.shields.io/badge/FreeIPA-Source%20of%20Truth-1778F2?style=for-the-badge" alt="FreeIPA Source of Truth" />
  <img src="https://img.shields.io/badge/Linux-IPA%20Enrollment-0B7D69?style=for-the-badge&logo=linux&logoColor=white" alt="Linux IPA Enrollment" />
  <img src="https://img.shields.io/badge/Secrets-Ansible%20Vault-4C9A2A?style=for-the-badge" alt="Ansible Vault" />
  <img src="https://img.shields.io/badge/PowerShell-Friendly-5391FE?style=for-the-badge&logo=powershell&logoColor=white" alt="PowerShell Friendly" />
</p>

<p>
  <a href="#quick-start">Quick Start</a> •
  <a href="#rollout-order">Rollout Order</a> •
  <a href="#inventory-model">Inventory Model</a> •
  <a href="#verification">Verification</a> •
  <a href="#development">Development</a> •
  <a href="CONTRIBUTING.md">Contributing</a> •
  <a href="SECURITY.md">Security</a>
</p>

</div>

This repository treats **FreeIPA as the source of truth** for identity and access. Proxmox consumes that directory through an LDAP realm, Linux guests join FreeIPA through the upstream `ipaclient` role, and access stays centralized through synced groups and HBAC instead of local account sprawl.

> [!IMPORTANT]
> This project does **not** use FreeRADIUS as the identity source, does **not** create local users inside every VM, and does **not** try to manage every possible Proxmox permission edge case.

## Why This Exists

Use this project when you already have:

- a healthy FreeIPA deployment
- a Proxmox VE cluster
- Linux guests that should authenticate centrally
- a dedicated FreeIPA service account for Proxmox LDAP bind
- a clear user-group model for admins and operators

This is a good fit when you want onboarding and offboarding to be mostly:

1. create or update users and groups in FreeIPA
2. sync those identities into Proxmox
3. apply Proxmox roles and ACLs from synced groups
4. allow Linux guest access through FreeIPA login plus HBAC

## What You Get

- FreeIPA user group, hostgroup, and HBAC rule management
- Proxmox LDAP realm configuration against FreeIPA
- recurring Proxmox realm sync from one designated cluster node
- Proxmox RBAC bindings for synced directory groups
- Linux guest enrollment into FreeIPA with the upstream `freeipa.ansible_freeipa.ipaclient` role

## Scope

| Included | Not Included |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| Proxmox RBAC from synced groups | FreeIPA user lifecycle creation |
| Linux IPA client enrollment | Full Proxmox multi-tenant policy coverage |

## Architecture

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

For the longer design explanation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Requirements

### Controller

- Ansible Core 2.14+
- SSH reachability to your Proxmox primary node, IPA server, and Linux clients
- sudo or root where required

### Targets

- Proxmox VE 6.x, 7.x, 8.x, 9.x, or provisionally 10.x on the host in `proxmox_primary`
- FreeIPA reachable from Proxmox and Linux clients
- sane DNS and time synchronization
- for `proxmox_primary`, either connect as `root` or use an SSH user that can run `sudo` for `pveversion`, `pvesh`, and `pveum`

## Compatibility

The Proxmox automation in this repository is written around the `pveum` and `pvesh` realm and RBAC interfaces used by Proxmox VE 6.x, 7.x, 8.x, 9.x, and anticipated 10.x releases.

- Supported major versions by default: `6`, `7`, `8`, `9`, `10`
- Validation checks the detected Proxmox version with `pveversion`
- The supported version list can be overridden with `proxmox_supported_major_versions` if you need to narrow or extend it in your environment
- `10.x` is included as a provisional future-release compatibility gate so a new major version does not fail validation by default on day one; it should still be treated as unvalidated until the released Proxmox VE 10 interface is checked against this automation
- Older legacy majors such as `1` through `5` are not claimed as tested support by this public repository; if you add them locally, treat that as an explicit compatibility override and validate the full workflow in a lab first

Example local override for a legacy lab environment:

```yaml
proxmox_supported_major_versions:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
  - 9
  - 10
```

## Quick Start

Examples below use shell commands. PowerShell equivalents are included where that is likely to matter.

### 1. Copy the example inventory and vault template

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault.yml.example inventories/production/group_vars/all/vault.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault.yml.example inventories\production\group_vars\all\vault.yml
```

### 2. Edit the environment-specific files

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/main.yml`
- `inventories/production/group_vars/all/vault.yml`

If you want to SSH to Proxmox with a regular sudo-capable user instead of `root`, set that under `proxmox_primary` in `hosts.yml` and keep the sudo password in `vault.yml`:

```yaml
proxmox_primary:
  vars:
    ansible_user: automation-user
    ansible_become_method: sudo
    ansible_become_password: "{{ vault_proxmox_become_password }}"
  hosts:
    pve01.example.com:
      ansible_host: 192.0.2.11
```

In that setup, `vault_proxmox_become_password` is the password you would normally type for `sudo` on the Proxmox host.

### 3. Encrypt the vault file

```bash
ansible-vault encrypt inventories/production/group_vars/all/vault.yml
```

### 4. Install the required collection

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Or directly:

```powershell
ansible-galaxy collection install -r requirements.yml
```

### 5. Run validation first

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

### 6. Optional: preview planned changes

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Treat check mode as a partial preview, not a full simulation. This repository uses direct CLI commands for part of the Proxmox configuration and the upstream FreeIPA client role for Linux enrollment, so `--check` is useful but not authoritative.
>
> For FreeIPA HBAC rules, check mode validates the rule-definition step but skips the follow-up enable or disable action. That avoids false failures where FreeIPA reports the rule as missing because it was not actually created during the dry run.

### 7. Apply the full configuration

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

## Rollout Order

For the first deployment, apply the stack in this order:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

That sequence makes troubleshooting much easier than running everything at once.

For a limited PowerShell rollout, for example one Linux guest:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

## Inventory Model

This repository uses three main inventory groups:

- `ipa_servers`: one or more FreeIPA servers
- `proxmox_primary`: one Proxmox node chosen to own realm configuration and the recurring sync timer
- `linux_ipa_clients`: Linux guests to enroll into FreeIPA

You can add your own inventory groups and reference them from FreeIPA hostgroup definitions.

> [!IMPORTANT]
> Hosts in `linux_ipa_clients` should use the guest's final FQDN, not a short alias, VM ID, or temporary template name. The hostgroup logic expands inventory hostnames directly into FreeIPA hostgroup membership, so those names need to match what FreeIPA and DNS expect.

> [!TIP]
> Do not enroll a reusable golden template into FreeIPA. Clone the VM first, assign the final hostname, and enroll the resulting guest instead.

## Configuration Surface

Most values live in:

- `inventories/production/group_vars/all/main.yml`
- `inventories/production/group_vars/all/vault.yml`

Key variable families:

| Area | Variables |
| --- | --- |
| FreeIPA access model | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit` |
| Ansible connection secrets | `vault_proxmox_become_password` when `proxmox_primary` uses a sudo-capable non-root SSH user |

## Example Group Strategy

A simple pattern that scales well:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- Proxmox ACL binding for synced group `proxmox-admins-ipa`

Remember that Proxmox LDAP sync creates synced groups with the suffix:

```text
<group-name>-<realm>
```

If your FreeIPA group is `proxmox-admins` and the Proxmox realm is `ipa`, the synced PVE group becomes:

```text
proxmox-admins-ipa
```

## Security

- store all secrets in `vault.yml`, not in `main.yml`
- prefer a dedicated read-only LDAP bind account for Proxmox
- prefer TLS with certificate verification enabled
- do not reuse the IPA admin account as the Proxmox LDAP bind account
- review `proxmox_ldap_filter` and `proxmox_ldap_group_filter` before production rollout to avoid importing too much

## Idempotency and Caveats

This project is written to be reusable and mostly idempotent, but it should still be tested in a lab before production rollout.

Known caveats:

- Proxmox CLI output can vary slightly across releases
- FreeIPA directory layouts are flexible, so LDAP filters may need tuning for your tree
- existing hand-managed PVE ACLs and roles should be compared before applying automation over them
- the Proxmox plays run with privilege escalation, so a non-root SSH user must have working `sudo` and you must supply a become password with `-K` unless that user has passwordless sudo
- if you store `ansible_become_password` in `vault.yml`, you can skip `-K` because Ansible will read the sudo password from the encrypted variable instead

## Verification

After a successful rollout, verify the resulting state instead of assuming every access path is correct.

### In FreeIPA

- confirm the expected user groups exist
- confirm the expected hostgroups exist
- confirm the expected HBAC rules exist and are enabled

### In Proxmox

- confirm the LDAP realm exists
- confirm the initial sync imported the expected users or groups
- confirm the intended synced group has the expected ACL binding

### On a Linux Guest

- confirm an allowed IPA user can log in
- confirm a disallowed user is blocked by HBAC
- confirm a home directory is created on first login if `linux_ipaclient_mkhomedir` is enabled

## Repository Layout

<details>
<summary>Show repository layout</summary>

```text
.
├── LICENSE
├── README.md
├── ansible.cfg
├── requirements.yml
├── docs/
│   └── ARCHITECTURE.md
├── inventories/
│   └── production/
│       ├── hosts.yml.example
│       └── group_vars/
│           └── all/
│               ├── main.yml
│               └── vault.yml.example
├── playbooks/
│   ├── freeipa.yml
│   ├── linux-clients.yml
│   ├── proxmox.yml
│   ├── site.yml
│   └── validate.yml
├── roles/
│   ├── freeipa_access_model/
│   ├── linux_freeipa_enroll/
│   ├── proxmox_ldap_realm/
│   ├── proxmox_rbac/
│   └── proxmox_realm_sync_timer/
└── scripts/
    ├── bootstrap.ps1
    ├── lint.py
    ├── lint.ps1
    ├── lint.sh
    ├── run-playbook.ps1
    └── bootstrap.sh
```

</details>

## Development

Repository helper files included here:

- `.gitattributes` keeps common text files on LF line endings
- `.gitignore` keeps generated inventory, vault data, local collections, and editor files out of Git
- `.ansible-lint` excludes vendored collections and suppresses only the YAML line-length rule
- `.yamllint` keeps YAML formatting checks consistent across playbooks, inventories, and workflow files
- `.github/workflows/ci.yml` runs `ansible-lint`, `yamllint`, and playbook syntax checks on pushes and pull requests
- `.pre-commit-config.yaml` runs the local lint wrapper before commits when `pre-commit` is installed
- `scripts/bootstrap.ps1` and `scripts/bootstrap.sh` install the required collection
- `scripts/lint.py` provides a cross-platform lint entrypoint for local use and pre-commit
- `scripts/lint.ps1` and `scripts/lint.sh` run the same local lint and syntax checks used in CI
- `scripts/run-playbook.ps1` wraps common `ansible-playbook` commands for PowerShell users
- `CONTRIBUTING.md` documents the expected contribution and validation workflow
- `SECURITY.md` documents how to report vulnerabilities and handle security-sensitive information

If `ansible-lint` is installed on your controller:

```bash
ansible-lint
```

For the full local lint pass:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

To enable the same checks before each commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Next Extensions

Common follow-up improvements you may want later:

- FreeIPA sudo rules
- Packer image pipeline for IPA-ready Linux templates
- AWX job templates and schedules
- separate Proxmox tenant and pool models
- Windows or AD-trust flow for RDP-oriented environments

## License

Released under the [MIT License](LICENSE).
