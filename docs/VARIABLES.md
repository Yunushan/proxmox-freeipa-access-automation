# Variables

This repository splits environment variables by domain under `inventories/<env>/group_vars/all/`.

## File layout

- `10-features.yml`: top-level feature toggles
- `15-rollout.yml`: rollout serial and failure-budget settings
- `20-freeipa.yml`: FreeIPA admin/API values, groups, hostgroups, and HBAC
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

Linux enrollment naming rules:

- `ipaclient_domain` is the shared IPA DNS domain, for example `example.com`
- `linux_ipa_servers` contains IPA server hostnames, for example `ipa01.example.com`
- do not set `ipaclient_domain` to one of the IPA server hostnames
- use YAML list syntax for `linux_ipa_servers` when possible, even though the role also normalizes comma-separated strings
