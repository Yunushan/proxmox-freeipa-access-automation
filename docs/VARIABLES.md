# Variables

This repository splits environment variables by domain under `inventories/<env>/group_vars/all/`.

## File layout

- `10-features.yml`: top-level feature toggles
- `15-rollout.yml`: rollout serial and failure-budget settings
- `20-freeipa.yml`: FreeIPA admin/API values, groups, hostgroups, HBAC, and sudo rules
- `30-linux-clients.yml`: Linux enrollment, manual client definitions, and Proxmox discovery
- `40-proxmox-ldap.yml`: Proxmox LDAP realm configuration
- `50-proxmox-sync.yml`: recurring Proxmox realm-sync timer settings
- `60-proxmox-rbac.yml`: Proxmox custom roles and ACL bindings
- `vault-freeipa.yml`: encrypted FreeIPA admin secret
- `vault-proxmox.yml`: encrypted Proxmox LDAP bind secret and optional sudo password

`main.yml` remains as a directory index only.

## Rollout controls

The repository exposes play-level rollout controls through `15-rollout.yml`.

- `freeipa_access_serial`
- `freeipa_access_max_fail_percentage`
- `proxmox_rollout_serial`
- `proxmox_rollout_max_fail_percentage`
- `linux_freeipa_enroll_serial`
- `linux_freeipa_enroll_max_fail_percentage`

Those values drive the FreeIPA access play, the Proxmox play, Linux hostname resolution, Linux validation, and Linux enrollment.

## Source and runtime groups

- `linux_ipa_clients`: declarative source inventory group
- `linux_ipa_clients_runtime`: generated runtime group used by Linux preparation, validation, and enrollment playbooks
- `windows_qemu_guest_agent_clients`: optional inventory group used only for QEMU Guest Agent installation on reachable Windows guests

Use `linux_ipa_clients_runtime` when a FreeIPA hostgroup should include the full prepared Linux guest set.

## Hostname resolution rules

FreeIPA still needs each guest's final hostname.

The runtime flow resolves hostnames in this order:

1. `freeipa_hostgroup_hostname` when already set
2. `ipa_hostname` when explicitly declared
3. `ipa_hostname` or the guest short hostname with `linux_ipa_identity_hostname_suffix` when that suffix is set
4. the inventory hostname when it is already an FQDN
5. `hostname -f` on the guest during the combined `site` or `linux-clients` flows

For `freeipa.yml`, rely on declarative values such as FQDN inventory names or `ipa_hostname`.

Relevant Linux enrollment hostname controls:

- `linux_ipa_identity_hostname_suffix`: optional suffix used to turn short hostnames such as `app-server-01` into FQDNs such as `app-server-01.example.net`
- `linux_freeipa_enroll_manage_hostname`: when `true`, the Linux enrollment role updates the guest system hostname to the resolved FQDN before IPA enrollment
- `linux_ipa_manage_etc_hosts`: when `true`, the Linux enrollment role manages a bootstrap block in `/etc/hosts` before IPA connectivity and hostname verification
- `linux_ipa_etc_hosts_entries`: list of `{ ip, names }` mappings for `/etc/hosts`, useful when IPA DNS is not reachable yet or when a guest FQDN must be pinned locally during bootstrap
- `guest_qemu_agent_install_enabled`: when `true`, reachable Linux enrollment targets and optional `windows_qemu_guest_agent_clients` hosts install and start QEMU Guest Agent before later bootstrap steps
- `guest_qemu_agent_install_windows_package_path`: MSI path or URL used for Windows QEMU Guest Agent installation; defaults to the Fedora virtio-win direct-download `latest-qemu-ga` MSI path for `x86_64`
- `linux_ipa_ssh_host_key_policy`: SSH host key behavior for Linux guest connections; `accept_new` is the repository default for Linux runtime targets, while `strict` requires pre-populated `known_hosts` entries and `disabled` turns host key checking off for those Linux guest connections
- `linux_ipa_qga_ssh_bootstrap_enabled`: when `true`, Proxmox-backed Linux runtime guests use the QEMU Guest Agent to create a dedicated key-only automation user before SSH-based hostname resolution or enrollment
- `linux_ipa_qga_ssh_bootstrap_user`: username created inside Proxmox-backed Linux guests for QGA-based SSH bootstrap
- `linux_ipa_qga_ssh_bootstrap_shell`: login shell assigned to the QGA bootstrap user
- `linux_ipa_qga_ssh_bootstrap_public_key_file`: controller SSH public key installed through the QEMU Guest Agent bootstrap path
- `linux_ipa_qga_ssh_bootstrap_private_key_file`: controller SSH private key paired with the QGA bootstrap public key and used for later SSH connections
- `linux_ipa_qga_ssh_bootstrap_install_sudo`: when `true`, the QGA bootstrap path installs `sudo` if missing before creating the bootstrap sudoers entry
- `linux_ipa_qga_ssh_bootstrap_timeout`: timeout passed to `qm guest exec` during the QGA bootstrap path
- `linux_ipa_qga_ssh_bootstrap_qm_path`: Proxmox CLI command or absolute path used for Proxmox-side `qm guest ...` calls; defaults to `qm`
- `linux_ipa_qga_ssh_bootstrap_qm_fallback_paths`: common absolute `qm` locations probed on the Proxmox node before failing; defaults to `/usr/sbin/qm`, `/usr/bin/qm`, and `/sbin/qm`
- `linux_ipa_qga_ssh_bootstrap_delegate_python_interpreter`: Python interpreter forced for delegated Proxmox-side `qm guest ...` tasks; defaults to `/usr/bin/python3`
- `linux_ipa_ssh_bootstrap_enabled`: when `true`, the Linux workflows install the controller SSH public key onto the Linux guest account used for Ansible connections before hostname resolution and enrollment
- `linux_ipa_ssh_bootstrap_password`: optional shared first-touch password used as a fallback `ansible_password` for runtime Linux guests during SSH key bootstrap; keep this in vaulted variables when used
- `linux_ipa_ssh_bootstrap_public_key_file`: controller SSH public key path installed onto Linux guests during SSH bootstrap
- `linux_ipa_ssh_bootstrap_private_key_file`: controller SSH private key path preferred for subsequent Linux guest plays after SSH bootstrap
- `linux_sssd_refresh_enabled`: when `true`, the `freeipa.yml` and `site.yml` workflows clear SSSD caches and restart `sssd` on managed Linux clients after FreeIPA access-model changes so new sudo and HBAC policy is visible immediately
- `linux_ipa_proxmox_discovery_vmids`: optional VMID filter list for Proxmox discovery, mainly useful for event-driven runs such as the Proxmox hook/webhook workflow

Linux enrollment naming rules:

- `ipaclient_domain` is the shared IPA DNS domain, for example `example.com`
- `linux_ipa_servers` contains IPA server hostnames, for example `ipa01.example.com`
- do not set `ipaclient_domain` to one of the IPA server hostnames
- use YAML list syntax for `linux_ipa_servers` when possible, even though the role also normalizes comma-separated strings

## FreeIPA access model

- `freeipa_user_groups`: user groups created in FreeIPA
- `freeipa_hostgroups`: hostgroups built from declarative inventory groups or hostnames
- `freeipa_hbac_rules`: login and service-access rules such as SSH access
- `freeipa_sudo_rules`: sudo authorization rules evaluated by IPA-enrolled Linux clients
