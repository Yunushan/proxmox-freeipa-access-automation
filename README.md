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
  <a href="docs/VARIABLES.md">Variables</a> •
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
- Linux guest enrollment into FreeIPA with static inventory, IP-only targets, or Proxmox VM discovery

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
- if you use Proxmox VM auto-discovery, discovered guests must expose a usable IP through the QEMU guest agent

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

### 1. Copy the example inventory and vault templates

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
```

### 2. Edit the environment-specific files

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

Choose one Linux guest source mode in addition to the IPA and Proxmox settings:

- static inventory entries under `linux_ipa_clients`
- `linux_ipa_client_hosts` entries in `group_vars/all/30-linux-clients.yml`
- Proxmox VM discovery with `linux_ipa_proxmox_discovery_enabled: true`

For Linux IPA enrollment, keep the domain and server values distinct:

- `ipaclient_domain` is the shared IPA DNS domain, such as `example.com`
- `linux_ipa_servers` contains IPA server hostnames, such as `ipa01.example.com`

If you want to SSH to Proxmox with a regular sudo-capable user instead of `root`, set that under `proxmox_primary` in `hosts.yml` and keep the sudo password in `vault-proxmox.yml`:

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

### 3. Encrypt the vault files

```bash
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
```

```powershell
ansible-vault encrypt `
  inventories/production/group_vars/all/vault-freeipa.yml `
  inventories/production/group_vars/all/vault-proxmox.yml
```

Or use the helper wrappers, which default to separate vault IDs and create the working vault files from the example templates if needed:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

If you want separate passwords per domain when running playbooks, prefer vault IDs over `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Use `-AskVaultPass` only when both vault files share the same password.

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
>
> The Proxmox realm sync timer role also skips the final `systemd` enable or start step in check mode, because unit files are diffed but not actually written during the dry run.
>
> Linux IPA enrollment is also skipped in check mode. The repository still performs discovery, hostname resolution, and input validation, but the upstream `ipaclient` role is not executed during a dry run.

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

Default rollout controls are conservative:

- FreeIPA access changes run with `serial: 1`
- Proxmox changes run with `serial: 1`
- Linux hostname resolution, validation, and enrollment run with `serial: 10`
- all rollout paths default to `max_fail_percentage: 0`

Tune those values in `inventories/production/group_vars/all/15-rollout.yml`.

## Tag Model

Use tags to target stable rollout slices instead of creating more playbooks.

- Core domains: `freeipa`, `proxmox`, `linux`, `validate`
- FreeIPA model: `freeipa_access`
- Proxmox subsets: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`

Examples:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
```

## Inventory Model

This repository uses three declared inventory groups plus one generated runtime group:

- `ipa_servers`: one or more FreeIPA servers
- `proxmox_primary`: one Proxmox node chosen to own realm configuration and the recurring sync timer
- `linux_ipa_clients`: the declarative source inventory group for Linux guests
- `linux_ipa_clients_runtime`: the generated runtime group built from static inventory, manual host definitions, and optional Proxmox discovery

You can add your own inventory groups and reference them from FreeIPA hostgroup definitions. When you want the full prepared Linux guest set in FreeIPA hostgroups, reference `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> FreeIPA still needs each guest's final hostname. If you use IP-only targets or Proxmox discovery, either set `ipa_hostname` explicitly or make sure `hostname -f` on the guest returns the final FQDN. The playbooks now resolve that hostname before FreeIPA hostgroup membership is built.

> [!TIP]
> Do not enroll a reusable golden template into FreeIPA. Clone the VM first, assign the final hostname, and enroll the resulting guest instead.

### Linux Guest Source Modes

You can populate `linux_ipa_clients` in three different ways.

#### 1. Static inventory hosts

Use normal Ansible inventory entries when you already know the guest names:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. Manual host definitions in variables

Use `linux_ipa_client_hosts` when you want to keep guests out of `hosts.yml` or when all you have is an IP:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Notes:

- if `name` is a resolvable hostname or FQDN, `ansible_host` is optional
- if you only know the IP, use any stable alias for `name`
- when `ipa_hostname` is omitted, the playbook falls back to `hostname -f` on the guest

#### 3. Proxmox VM auto-discovery

Use discovery when you want the playbook to pull Linux guests from one or more Proxmox nodes:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
```

Notes:

- discovery adds VMs to the same `linux_ipa_clients_runtime` group used by the rest of the playbooks
- IP discovery depends on the QEMU guest agent reporting network interfaces
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` only trusts VM names that are already FQDNs
- the guest still needs a final hostname, either already configured inside the VM or provided with `ipa_hostname` through a manual definition
- the guest's real system hostname must also be valid for enrollment; placeholder values such as `localhost.localdomain` must be replaced on the VM before running `linux-clients` or `site`
- when guests use short hostnames such as `app-server-01`, you can set `linux_ipa_identity_hostname_suffix` and optionally `linux_freeipa_enroll_manage_hostname: true` so the project resolves and applies a full hostname such as `app-server-01.example.net` before enrollment

## Configuration Surface

Most values live in:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

For the file-by-file layout, see [docs/VARIABLES.md](docs/VARIABLES.md).

Key variable families:

| Area | Variables |
| --- | --- |
| FreeIPA access model | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules` |
| Rollout controls | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_ipa_client_hosts`, `linux_ipa_proxmox_discovery_*` |
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

- store all secrets in `vault-freeipa.yml` and `vault-proxmox.yml`, not in plaintext inventory variable files
- prefer a dedicated read-only LDAP bind account for Proxmox
- prefer TLS with certificate verification enabled
- keep SSH host key checking enabled outside disposable lab environments
- do not reuse the IPA admin account as the Proxmox LDAP bind account
- review `proxmox_ldap_filter` and `proxmox_ldap_group_filter` before production rollout to avoid importing too much

For a disposable lab where you explicitly want to bypass SSH host verification, opt out per shell session instead of changing repository defaults:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Idempotency and Caveats

This project is written to be reusable and mostly idempotent, but it should still be tested in a lab before production rollout.

Known caveats:

- Proxmox CLI output can vary slightly across releases
- FreeIPA directory layouts are flexible, so LDAP filters may need tuning for your tree
- existing hand-managed PVE ACLs and roles should be compared before applying automation over them
- Proxmox VM auto-discovery depends on running guests and QEMU guest-agent network data
- IP-only guest definitions still require a valid final hostname inside the guest, or an explicit `ipa_hostname`
- the Proxmox plays run with privilege escalation, so a non-root SSH user must have working `sudo` and you must supply a become password with `-K` unless that user has passwordless sudo
- if you store `ansible_become_password` in `vault-proxmox.yml`, you can skip `-K` because Ansible will read the sudo password from the encrypted variable instead

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
├── .editorconfig
├── CHANGELOG.md
├── LICENSE
├── README.md
├── ansible.cfg
├── requirements.yml
├── tests/
│   ├── README.md
│   └── smoke/
│       └── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   └── VARIABLES.md
├── inventories/
│   └── production/
│       ├── hosts.yml.example
│       └── group_vars/
│           └── all/
│               ├── 10-features.yml
│               ├── 15-rollout.yml
│               ├── 20-freeipa.yml
│               ├── 30-linux-clients.yml
│               ├── 40-proxmox-ldap.yml
│               ├── 50-proxmox-sync.yml
│               ├── 60-proxmox-rbac.yml
│               ├── main.yml
│               ├── vault-freeipa.yml.example
│               └── vault-proxmox.yml.example
├── playbooks/
│   ├── includes/
│   │   ├── prepare_linux_inventory.yml
│   │   └── resolve_linux_hostnames.yml
│   ├── freeipa.yml
│   ├── linux-clients.yml
│   ├── proxmox.yml
│   ├── site.yml
│   └── validate.yml
├── roles/
│   ├── freeipa_access_model/
│   ├── linux_ipa_host_identity/
│   ├── linux_ipa_inventory_prepare/
│   ├── linux_freeipa_enroll/
│   ├── proxmox_linux_vm_discovery/
│   ├── proxmox_ldap_realm/
│   ├── proxmox_rbac/
│   └── proxmox_realm_sync_timer/
└── scripts/
    ├── bootstrap.ps1
    ├── lint.py
    ├── lint.ps1
    ├── lint.sh
    ├── smoke-test.py
    ├── run-playbook.ps1
    ├── vault.ps1
    ├── vault.sh
    └── bootstrap.sh
```

</details>

## Development

Repository helper files included here:

- `.editorconfig` keeps whitespace, encoding, and line-ending defaults consistent across editors
- `.gitattributes` keeps common text files on LF line endings
- `.gitignore` keeps generated inventory, vault data, local collections, and editor files out of Git
- `.ansible-lint` excludes vendored collections and suppresses only the YAML line-length rule
- `.yamllint` keeps YAML formatting checks consistent across playbooks, inventories, and workflow files
- `.github/CODEOWNERS` routes review ownership for the main repository areas
- `.github/workflows/ci.yml` runs repository lint checks and smoke validation on pushes and pull requests
- `.pre-commit-config.yaml` runs the fast lint hook before commits when `pre-commit` is installed
- `CHANGELOG.md` tracks notable repository changes in a single place
- `docs/VARIABLES.md` explains the split inventory variable layout
- `scripts/bootstrap.ps1` and `scripts/bootstrap.sh` install the required collection
- `scripts/lint.py` provides the cross-platform lint entrypoint for local use, CI, and pre-commit
- `scripts/smoke-test.py` validates the example inventory and runs syntax checks without touching real infrastructure
- `scripts/lint.ps1` and `scripts/lint.sh` run the combined local lint and smoke workflow
- `scripts/run-playbook.ps1` wraps common `ansible-playbook` commands for PowerShell users
- `scripts/vault.ps1` and `scripts/vault.sh` wrap common split-vault operations for FreeIPA and Proxmox secrets
- `tests/` holds the repository verification surface, starting with smoke-test documentation
- `CONTRIBUTING.md` documents the expected contribution and validation workflow
- `SECURITY.md` documents how to report vulnerabilities and handle security-sensitive information

If `ansible-lint` is installed on your controller:

```bash
ansible-lint
```

To run the repository smoke checks directly:

```bash
python scripts/smoke-test.py
```

```powershell
python .\scripts\smoke-test.py
```

For the full local lint pass:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

To enable the fast lint hook before each commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

The PowerShell playbook wrapper now also supports common operator options directly:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
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
