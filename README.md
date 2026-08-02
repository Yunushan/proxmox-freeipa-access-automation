<div align="center">

# Proxmox + FreeIPA Access Automation

**FreeIPA-first Ansible automation for Proxmox VE access, LDAP realm sync, RBAC, and Linux guest enrollment.**

<p>
  <img src="https://img.shields.io/badge/Ansible-Core%202.14%2B-EE0000?style=for-the-badge&logo=ansible&logoColor=white" alt="Ansible Core 2.14+" />
  <img src="https://img.shields.io/badge/Proxmox-VE%206.x%2B-E57000?style=for-the-badge" alt="Proxmox VE 6.x+" />
  <img src="https://img.shields.io/badge/FreeIPA-Source%20of%20Truth-1778F2?style=for-the-badge" alt="FreeIPA Source of Truth" />
  <img src="https://img.shields.io/badge/Linux-IPA%20Enrollment-0B7D69?style=for-the-badge&logo=linux&logoColor=white" alt="Linux IPA Enrollment" />
  <img src="https://img.shields.io/badge/Secrets-Ansible%20Vault-4C9A2A?style=for-the-badge" alt="Ansible Vault" />
  <img src="https://img.shields.io/badge/PowerShell-Friendly-5391FE?style=for-the-badge&logo=powershell&logoColor=white" alt="PowerShell Friendly" />
</p>

<p>
  <a href="#quick-start">Quick Start</a> •
  <a href="#rollout-order">Rollout Order</a> •
  <a href="#inventory-model">Inventory Model</a> •
  <a href="docs/EVENT_DRIVEN_VM_ONBOARDING.md">Event Hooks</a> •
  <a href="docs/VARIABLES.md">Variables</a> •
  <a href="#verification">Verification</a> •
  <a href="#development">Development</a> •
  <a href="CONTRIBUTING.md">Contributing</a> •
  <a href="SECURITY.md">Security</a>
</p>

</div>

## Languages

English is the canonical source for the full documentation. Full translated README files are available in 20 additional languages.

[English](README.md) | [العربية](docs/i18n/README.ar.md) | [বাংলা](docs/i18n/README.bn.md) | [简体中文](docs/i18n/README.zh-CN.md) | [Français](docs/i18n/README.fr.md)

[Deutsch](docs/i18n/README.de.md) | [हिन्दी](docs/i18n/README.hi.md) | [Bahasa Indonesia](docs/i18n/README.id.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md)

[मराठी](docs/i18n/README.mr.md) | [فارسی](docs/i18n/README.fa.md) | [Português](docs/i18n/README.pt.md) | [ਪੰਜਾਬੀ](docs/i18n/README.pa.md) | [Русский](docs/i18n/README.ru.md)

[Español](docs/i18n/README.es.md) | [தமிழ்](docs/i18n/README.ta.md) | [తెలుగు](docs/i18n/README.te.md) | [Türkçe](docs/i18n/README.tr.md) | [اردو](docs/i18n/README.ur.md)

[Tiếng Việt](docs/i18n/README.vi.md) | [Translation Index](docs/i18n/README.md) | [Translation Guide](docs/i18n/TRANSLATION_GUIDE.md)

This repository treats **FreeIPA as the source of truth** for identity and access. Proxmox consumes that directory through an LDAP realm, Linux guests join FreeIPA through the upstream `ipaclient` role, and access stays centralized through synced groups, HBAC, and sudo rules instead of local account sprawl.

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
4. allow Linux guest access through FreeIPA login, HBAC, and sudo rules

## What You Get

- FreeIPA user group, hostgroup, HBAC, and sudo rule management
- automatic FreeIPA login-shell defaults for Linux admin users
- Proxmox LDAP realm configuration against FreeIPA
- recurring Proxmox realm sync from one designated cluster node
- Proxmox RBAC bindings for synced directory groups
- Linux guest enrollment into FreeIPA with static inventory, IP-only targets, or Proxmox VM discovery
- optional no-reboot SSH bootstrap through the Proxmox QEMU Guest Agent
- optional Proxmox-side guest-agent communication enablement for Proxmox-backed Linux guests
- optional SSH or WinRM fallback installation of QEMU Guest Agent for guests that are already reachable, become reachable after bootstrap, or are retried again after Linux enrollment
- optional Linux readiness reporting for SSH reachability and Proxmox QEMU Guest Agent status
- optional separate Windows domain-membership workflow for Windows 10/11 and Windows Server guests through Active Directory
- optional limited FreeIPA-aware Windows helper workflow for IPA CA trust, hosts bootstrap, and IPA reachability checks
- optional first-touch SSH public-key bootstrap for Linux guests
- automatic SSSD cache refresh on managed Linux clients after FreeIPA access-model changes
- optional event-driven Linux onboarding from Proxmox VM hook and webhook triggers

## Scope

| Included | Not Included |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm setup | FreeIPA user lifecycle creation |
| Proxmox RBAC from synced groups | Full Proxmox multi-tenant policy coverage |
| Linux IPA client enrollment | Native Windows logon directly against FreeIPA |
| Separate Windows AD domain-membership workflow | GPO or broader AD object lifecycle automation |
| Limited FreeIPA-aware Windows helper workflow | Pretending FreeIPA-only Windows helpers are equivalent to AD |

## Windows Workflow

Windows support is implemented as a separate workflow instead of being folded into Linux IPA enrollment.

- `windows_qemu_guest_agent_clients` stays dedicated to optional QEMU Guest Agent helper tasks.
- enable the workflow with `windows_domain_membership_enabled: true` in `10-features.yml`
- `windows_management_clients` is the separate Windows management group used by `playbooks/windows-management.yml` and by the optional Windows stage in `playbooks/site.yml`.
- actual Windows logon is handled through Active Directory domain membership; in FreeIPA-centered environments, join Windows hosts to the AD side of a FreeIPA-AD trust instead of trying to join Windows directly to FreeIPA

FreeIPA-only Windows domain join is not supported by this repository. Without Active Directory or a FreeIPA-AD trust, the Windows workflow is limited to helper tasks such as reachable guest management and optional QEMU Guest Agent installation.

If you still want a limited FreeIPA-aware path for Windows without domain join, enable `windows_freeipa_helpers_enabled: true` and use `windows_freeipa_helper_clients` with `playbooks/windows-freeipa-helpers.yml`. That helper workflow can trust the IPA CA, optionally auto-fetch the IPA CA for bootstrap, optionally pin the expected IPA CA thumbprint, manage optional hosts-file bootstrap entries, validate IPA DNS and key TCP ports, validate HTTPS reachability from Windows, validate a Windows time source against an IPA-related endpoint, manage local Windows group memberships, and optionally install or expose OpenSSH Server, but it does not provide native Windows logon against FreeIPA.

When you want a non-mutating readiness check for that same helper group, run `playbooks/windows-freeipa-validate.yml`. It keeps the validation and summary path but forces CA import, hosts-file changes, local-group changes, and OpenSSH management off for that run.

This workflow targets Windows 10/11 and Windows Server guests reached through WinRM or PSRP.

## Architecture

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> Windows management clients --> AD domain membership --> Windows logon
        |
        +--> Windows FreeIPA helper clients --> CA trust/IPA reachability --> helper-only integration
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

For the longer design explanation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Requirements

### Controller

- Ansible Core 2.14+
- SSH reachability to your Proxmox primary node, IPA server, and Linux clients
- WinRM or PSRP reachability to Windows guests when you use the Windows workflow
- sudo or root where required
- when Linux QGA SSH bootstrap is enabled, the Proxmox guest agent must already be active in the guest
- when guest-agent fallback installation is enabled for Windows, reachable Windows hosts must be placed in `windows_qemu_guest_agent_clients`
- when Windows domain membership is enabled, reachable Windows hosts must be placed in `windows_management_clients` and you must provide AD join credentials
- when Windows FreeIPA helper tasks are enabled, reachable Windows hosts must be placed in `windows_freeipa_helper_clients`
- when Linux SSH bootstrap is enabled, a controller SSH keypair and an initial password-capable login path for the guest account used by Ansible

### Targets

- Proxmox VE 6.x and later on the host in `proxmox_primary`
- FreeIPA reachable from Proxmox and Linux clients
- Windows 10/11 and Windows Server guests can be managed by the separate Windows workflow when they are reachable through WinRM or PSRP
- sane DNS and time synchronization
- for `proxmox_primary`, either connect as `root` or use an SSH user that can run `sudo` for `pveversion`, `pvesh`, and `pveum`
- if you use Windows domain membership, the target Windows guests must be able to reach the relevant AD domain controllers
- if you use the limited Windows FreeIPA helper workflow, the target Windows guests must be able to reach the relevant IPA servers
- if you use Proxmox VM auto-discovery, discovered guests must expose a usable IP through the QEMU guest agent

## Network Ports

This table lists the network ports used by this repository's controller, Proxmox LDAP automation, and Linux IPA enrollment flow.
It is intentionally scoped to this project, not the full FreeIPA server-to-server replication matrix.

| Name | Port | Protocol | Source | Destination | Required When | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | Always | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | When Windows management is enabled | Ansible connectivity to Windows guests |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS servers | When Linux guests use IPA DNS | Resolve IPA records and external names through IPA DNS |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment and login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA servers | Linux IPA enrollment and login | LDAP and FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port` (default `443`) | `TCP` | Linux guest | IPA servers | Linux IPA enrollment | IPA web/API verification during client install |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment and password operations | Kerberos password and keytab operations |
| LDAPS | `636` | `TCP` | Proxmox primary node | IPA/LDAP servers | Proxmox LDAP realm in default `ldaps` mode | Proxmox LDAP realm connection |

Notes:

- `LDAPS 636/TCP` is the repository default because `proxmox_ldap_mode` defaults to `ldaps`. If you change the LDAP mode or port, allow the configured `proxmox_ldap_port` instead.
- `WinRM` commonly uses `5986/TCP` for HTTPS or `5985/TCP` for HTTP, depending on your Windows transport setup.
- `DNS 53/TCP,UDP` is only needed when Linux guests use the IPA servers as their DNS resolvers.
- `Kerberos 88` and `Kerberos Password 464` need both `TCP` and `UDP`.
- Active Directory domain join also requires the normal Windows-to-domain-controller port set, but that matrix is environment-specific and intentionally not exhaustively listed here.
- Time synchronization is still required for Kerberos to work reliably, but the NTP source is environment-specific and is not managed by this repository.

## Compatibility

The Proxmox automation in this repository is written around the `pveum` and `pvesh` realm and RBAC interfaces used by Proxmox VE 6.x and later releases.

- Supported major versions by default: `6`, `7`, `8`, `9`, `10`
- Validation checks the detected Proxmox version with `pveversion`
- The supported version list can be overridden with `proxmox_supported_major_versions` if you need to narrow or extend it in your environment
- `proxmox_allow_future_major_versions` defaults to `true`, so majors newer than the highest listed tested version also pass validation by default
- Future major versions should still be treated as compatibility candidates until the released Proxmox interface is checked against this automation
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
proxmox_allow_future_major_versions: false
```

## Quick Start

Examples below use shell commands. PowerShell equivalents are included where that is likely to matter.

### 1. Copy the example inventory and vault templates

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Optional when you plan to manage Windows guests:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Optional when you plan to manage Windows guests:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Edit the environment-specific files

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` when you use Windows management
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` when you use Windows management

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

Add `inventories/production/group_vars/all/vault-windows.yml` to the same command when you enable the Windows workflow.

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

If the optional Windows workflow also uses its own vault password, add `windows@prompt` to the same command.

Use `-AskVaultPass` only when all vault files used by that playbook share the same password.

### 4. Install the required collection

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Or directly:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

If you installed `freeipa.ansible_freeipa` before this repository added the compatibility patch, rerun one of the bootstrap helpers or run `python .\scripts\patch_freeipa_collection.py` once to patch the existing user-level collection install as well.

When you use `scripts/run-playbook.ps1`, it runs the patch helper automatically before `ansible-playbook`.

### 5. Run validation first

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

If you want to validate only the helper-only Windows FreeIPA path without making host changes:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

If you want a read-only Linux readiness audit that reports which runtime guests are reachable over SSH and which Proxmox-discovered guests respond through QEMU Guest Agent:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

The readiness report writes `.ansible/linux-readiness-report.json` by default.
Interpret the main fields like this:

- `ssh.ready=true`: the currently configured Ansible SSH path worked from the controller
- `ssh.promptless=true`: the SSH probe succeeded without `ansible_password`, so the path is non-interactive for Ansible
- `ssh.auth_mode=password_configured`: the probe used `sshpass` because the host had `ansible_password`
- `ssh.auth_mode=key_or_agent`: the probe succeeded in SSH batch mode without `ansible_password`
- `qga.status=available`: `qm guest ping` succeeded on the owning Proxmox node
- `qga.status=disabled`: the Proxmox VM config does not enable QEMU Guest Agent
- `qga.status=configured_unresponsive`: the guest agent is enabled in Proxmox config but did not respond
- `qga.status=node_unreachable`: the controller could not reach the owning Proxmox node for the probe
- `qga.status=not_applicable`: the host was not created by Proxmox discovery, so no QGA probe was attempted

Example quick inspection:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
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

If the optional Windows workflow is enabled and `vault-windows.yml` uses a separate password, run the same playbook with `--vault-id windows@prompt` or the PowerShell wrapper `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` instead of `--ask-vault-pass`.

## Rollout Order

For the first deployment, apply the stack in this order:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Optional when you manage Windows guests:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Optional when you want the limited Windows FreeIPA helper workflow:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Optional when you want validation-only coverage for the helper workflow:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
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
- Windows management changes run with `serial: 10`
- all rollout paths default to `max_fail_percentage: 0`

Tune those values in `inventories/production/group_vars/all/15-rollout.yml`.

## Tag Model

Use tags to target stable rollout slices instead of creating more playbooks.

- Core domains: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helpers: `windows`, `windows_freeipa`
- FreeIPA model: `freeipa_access`
- Proxmox subsets: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- Event-driven VM handling: `event`, `linux_refresh`

Examples:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Event-Driven VM Onboarding

If you want Proxmox to trigger Linux discovery and IPA enrollment immediately after VM starts or migrations, use the optional hook/webhook workflow documented in [docs/EVENT_DRIVEN_VM_ONBOARDING.md](docs/EVENT_DRIVEN_VM_ONBOARDING.md).

That workflow uses a dedicated event playbook at `playbooks/proxmox-vm-event.yml` so the trigger path only handles the Linux and FreeIPA guest side. It does not rerun the Proxmox LDAP realm or RBAC automation on every VM event.

The repository can now also deploy that optional hook/webhook stack from `site.yml` or `proxmox.yml` when `proxmox_vm_event_onboarding_enabled: true` and the required webhook variables are set.

Proxmox VM hooks do not expose a standalone `create` phase. In practice, new VMs are picked up on their first `post-start` event, and migration hooks can trigger on both source and target nodes.

## Inventory Model

This repository uses six declared inventory groups plus one generated runtime group:

- `ipa_servers`: one or more FreeIPA servers
- `proxmox_primary`: one Proxmox node chosen to own realm configuration and the recurring sync timer
- `linux_ipa_clients`: the declarative source inventory group for Linux guests
- `linux_ipa_clients_runtime`: the generated runtime group built from static inventory, manual host definitions, and optional Proxmox discovery
- `windows_qemu_guest_agent_clients`: optional Windows guest group used only for QEMU Guest Agent installation
- `windows_management_clients`: optional Windows guest group used by the separate Windows domain-membership workflow
- `windows_freeipa_helper_clients`: optional Windows guest group used by the limited FreeIPA-aware helper workflow

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
# Optional: gate discovery-driven automation to approved guests only.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Optional: always exclude infrastructure or sensitive guests even when broad
# node discovery is enabled.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# Optional first-touch SSH settings for discovered guests when the guest agent
# is not running yet and the repository must connect over SSH to install it.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

Notes:

- discovery adds VMs to the same `linux_ipa_clients_runtime` group used by the rest of the playbooks
- IP discovery depends on the QEMU guest agent reporting network interfaces
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` only trusts VM names that are already FQDNs
- set `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` when you also want safe short Proxmox VM names such as `Teleport-Server-1` promoted automatically to hostname hints such as `teleport-server-1.example.com` through `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` is optional and mainly used by the event-driven hook/webhook workflow to scope discovery to one or more specific VMIDs
- the guest still needs a final hostname, either already configured inside the VM or provided with `ipa_hostname` through a manual definition
- the guest's real system hostname must also be valid for enrollment; placeholder values such as `localhost.localdomain` must be replaced on the VM before running `linux-clients` or `site`
- when guests use short hostnames such as `app-server-01`, you can set `linux_ipa_identity_hostname_suffix` and optionally `linux_freeipa_enroll_manage_hostname: true` so the project resolves and applies a full hostname such as `app-server-01.example.net` before enrollment
- when FreeIPA DNS is authoritative for your guest hostnames, you can set `linux_freeipa_enroll_manage_authoritative_dns: true` so the project repairs the specific guest A and PTR records and removes link-local `fe80::/10` AAAA records before enrollment
- when DNS is not ready yet, you can set `linux_ipa_manage_etc_hosts: true` and provide `linux_ipa_etc_hosts_entries` so the role adds a managed `/etc/hosts` bootstrap block for IPA servers and guest FQDNs before enrollment checks
- `guest_qemu_agent_install_enabled` installs QEMU Guest Agent on guests that are already reachable over SSH or WinRM, retries on Linux guests that become reachable later in the same workflow, and retries again after Linux enrollment, so later Proxmox agent-dependent workflows can use it
- set `linux_ipa_proxmox_discovery_allowlist_enabled: true` when you want discovery to remain on but only a tightly approved subset of Proxmox guests should enter the Linux runtime inventory; the allowlist can match exact VMIDs, IPs, and names
- set `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, or `linux_ipa_proxmox_discovery_blacklist_names` when discovery-enabled nodes also host infrastructure VMs such as firewalls or DNS servers that must never receive Linux IPA automation; blacklist matches always win over admission through broad discovery or the allowlist
- for Proxmox-discovered Linux guests that do not already have a working guest agent, set `linux_ipa_proxmox_discovery_ansible_user` and either `linux_ipa_proxmox_discovery_ansible_password` or `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` so the repository has a usable first-touch SSH path to install QEMU Guest Agent
- when those discovered guests use a non-root SSH user, also set `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, and `linux_ipa_proxmox_discovery_ansible_become_password` unless that account already has passwordless sudo
- `guest_qemu_agent_install_manage_proxmox_vm_agent` also enables Proxmox-side guest-agent communication (`qm set <vmid> --agent 1`) for Proxmox-backed Linux guests before the guest-side install path runs
- when that Proxmox VM option changes on a running VM, the repository only warns by default because Proxmox may require a fresh VM start before the host can use the guest-agent channel; set `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` if you want the repository to reboot those running VMs automatically
- `linux_ipa_ssh_host_key_policy` defaults to `accept_new` for Linux guest connections so newly discovered VMs can be contacted without disabling host key checking entirely; changed host keys still fail and require operator review
- `linux_ipa_qga_ssh_bootstrap_enabled` is the preferred no-reboot bootstrap path for Proxmox-backed guests because it can create a dedicated key-only automation user through the QEMU Guest Agent before any SSH login exists
- `linux_ipa_qga_ssh_bootstrap_qm_path` defaults to `qm`, and the bootstrap flow also probes common fallback paths on the Proxmox node before failing
- `linux_ipa_qga_ssh_bootstrap_exec_shell` defaults to `/bin/sh` and controls which in-guest shell path the QGA bootstrap launches
- guests that allow `guest-ping` but reject `guest-exec` are skipped by default during QGA bootstrap; keep another SSH path available for them, or set `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` to fail fast instead
- guests that allow `guest-ping` but cannot launch the configured QGA bootstrap shell are also skipped by default; keep another SSH path available for them, override `linux_ipa_qga_ssh_bootstrap_exec_shell` if the guest uses a different shell path, or set `linux_ipa_qga_ssh_bootstrap_fail_on_exec_shell_missing: true` to fail fast instead
- `linux_ipa_ssh_bootstrap_enabled` optionally installs the controller SSH public key onto Linux guests before hostname resolution and enrollment; `linux_ipa_ssh_bootstrap_password` is also used as the shared first-touch password fallback for runtime Linux guests even when key bootstrap is disabled
- Linux IPA enrollment retries upstream client joins that fail with a FreeIPA JSON-RPC timeout, and exposes `linux_ipaclient_kinit_attempts` for slower or busier IPA environments
- Linux IPA enrollment also merges the `ipa_servers` inventory hostnames into the join server list by default, so clients can use the full IPA server set instead of a single configured endpoint
- when more than one IPA server is available, each retry pass tries those IPA server candidates one at a time during Linux client enrollment
- the combined `site` workflow creates FreeIPA hostgroups before Linux enrollment, then adds the enrolled runtime hosts afterward so pre-enrollment runs do not fail on hostgroup membership for not-yet-enrolled guests

## Configuration Surface

Most values live in:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml`

For the file-by-file layout, see [docs/VARIABLES.md](docs/VARIABLES.md).

Key variable families:

| Area | Variables |
| --- | --- |
| FreeIPA access model | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Rollout controls | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Linux readiness reporting | `linux_readiness_report_*` |
| Windows management | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helpers | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Ansible connection secrets | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Example Group Strategy

A simple pattern that scales well:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- Sudo rule `allow-linux-ssh-admins-sudo`
- Proxmox ACL binding for synced group `proxmox-admins-ipa`

Populate `freeipa_linux_admin_users` in [`inventories/production/group_vars/all/20-freeipa.yml`](inventories/production/group_vars/all/20-freeipa.yml) when you want the combined `site.yml` run to grant specific IPA users Linux SSH and sudo access automatically through the managed `linux-ssh-admins` group.

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
- prefer `linux_ipa_qga_ssh_bootstrap_enabled` over shared temporary passwords when your Proxmox guests already have a working QEMU Guest Agent
- use `guest_qemu_agent_install_enabled` only when the repository already has a valid management path into the guest; for Proxmox discovery that means QGA is already running or `linux_ipa_proxmox_discovery_ansible_user` plus password or key access is configured
- if you enable Linux SSH bootstrap, store any shared bootstrap password in vaulted variables and rotate or remove it once key-based access is established
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
- confirm the expected sudo rules exist and are enabled

### In Proxmox

- confirm the LDAP realm exists
- confirm the initial sync imported the expected users or groups
- confirm the intended synced group has the expected ACL binding

### On a Linux Guest

- confirm an allowed IPA user can log in
- confirm a disallowed user is blocked by HBAC
- confirm an allowed IPA admin can run `sudo -l`
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
│   ├── EVENT_DRIVEN_VM_ONBOARDING.md
│   ├── i18n/
│   │   ├── README.md
│   │   └── README.<lang>.md
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
│               ├── 35-windows-clients.yml
│               ├── 40-proxmox-ldap.yml
│               ├── 50-proxmox-sync.yml
│               ├── 60-proxmox-rbac.yml
│               ├── main.yml
│               ├── vault-freeipa.yml.example
│               ├── vault-proxmox.yml.example
│               └── vault-windows.yml.example
├── playbooks/
│   ├── includes/
│   │   ├── bootstrap_linux_qga_ssh.yml
│   │   ├── bootstrap_linux_ssh.yml
│   │   ├── ensure_guest_qemu_agent.yml
│   │   ├── manage_windows_domain_membership.yml
│   │   ├── manage_windows_freeipa_helpers.yml
│   │   ├── prepare_linux_event_inventory.yml
│   │   ├── prepare_linux_inventory.yml
│   │   └── resolve_linux_hostnames.yml
│   ├── freeipa.yml
│   ├── linux-clients.yml
│   ├── linux-readiness-report.yml
│   ├── proxmox-vm-event.yml
│   ├── proxmox.yml
│   ├── site.yml
│   ├── validate.yml
│   ├── windows-freeipa-helpers.yml
│   ├── windows-freeipa-validate.yml
│   └── windows-management.yml
├── roles/
│   ├── freeipa_access_model/
│   ├── freeipa_runtime_hostgroup_membership/
│   ├── guest_qemu_agent_install/
│   ├── linux_ipa_host_identity/
│   ├── linux_ipa_inventory_prepare/
│   ├── linux_ipa_qga_ssh_bootstrap/
│   ├── linux_ipa_ssh_bootstrap/
│   ├── linux_readiness_report/
│   ├── linux_freeipa_enroll/
│   ├── linux_sssd_refresh/
│   ├── proxmox_linux_vm_discovery/
│   ├── proxmox_ldap_realm/
│   ├── proxmox_rbac/
│   ├── proxmox_realm_sync_timer/
│   ├── windows_domain_membership/
│   └── windows_freeipa_helpers/
└── scripts/
    ├── bootstrap.ps1
    ├── lint.py
    ├── lint.ps1
    ├── lint.sh
    ├── patch_freeipa_collection.py
    ├── proxmox-event-webhook.env.example
    ├── proxmox-event-webhook.service.example
    ├── proxmox-vm-hook.conf.example
    ├── proxmox-vm-hook.pl
    ├── proxmox_event_webhook.py
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
- `docs/i18n/` holds translated README files that should mirror the full English section structure while `README.md` remains the canonical source
- `docs/i18n/TRANSLATION_GUIDE.md` explains how translated README files should be kept in sync
- `scripts/bootstrap.ps1` and `scripts/bootstrap.sh` install the required collection into the repo-local `collections/` path and patch it for ansible-core 2.24+ compatibility
- `scripts/patch_freeipa_collection.py` rewrites deprecated imports in the pinned FreeIPA collection so it stays compatible with future ansible-core releases
- `scripts/lint.py` provides the cross-platform lint entrypoint for local use, CI, and pre-commit
- `scripts/smoke-test.py` validates the example inventory and runs syntax checks without touching real infrastructure, including the separate Windows playbook
- `scripts/check_translations.py` audits translated README files for metadata, section-structure parity, and minimum content coverage against the canonical English README
- `scripts/lint.ps1` and `scripts/lint.sh` run the combined local lint and smoke workflow
- `scripts/proxmox_event_webhook.py` runs the optional controller-side webhook for Proxmox VM events
- `scripts/proxmox-vm-hook.pl` is the optional Proxmox VM hookscript that notifies the controller webhook on `post-start` and `post-migrate`
- `scripts/run-playbook.ps1` wraps common `ansible-playbook` commands for PowerShell users, including the separate Windows workflow
- `scripts/vault.ps1` and `scripts/vault.sh` wrap common split-vault operations for FreeIPA, Proxmox, and optional Windows secrets
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
python scripts/check_translations.py
python scripts/check_translations.py --strict
```

```powershell
python .\scripts\smoke-test.py
python .\scripts\check_translations.py
python .\scripts\check_translations.py --strict
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
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Next Extensions

Common follow-up improvements you may want later:

- Packer image pipeline for IPA-ready Linux templates
- AWX job templates and schedules
- separate Proxmox tenant and pool models
- broader Windows local policy or GPO integration

## License

Released under the [0BSD License](LICENSE).
