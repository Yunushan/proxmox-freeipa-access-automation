# Proxmox + FreeIPA Access Automation

Reusable Ansible project to:

- model FreeIPA user groups, hostgroups, and HBAC rules,
- configure a Proxmox VE LDAP realm backed by FreeIPA,
- schedule recurring Proxmox realm sync on one cluster node,
- apply Proxmox RBAC from synced directory groups,
- enroll Linux VMs or templates into FreeIPA with the upstream `ipaclient` role.

This project intentionally treats **FreeIPA as the source of truth**.
It does **not** try to use FreeRADIUS as the identity source or create local users inside every VM.
FreeRADIUS can keep using the same FreeIPA directory for network AAA, while Proxmox and Linux guests consume identity directly from FreeIPA.

## What this project is for

Use this project when you already have:

- Proxmox VE cluster
- FreeIPA deployed and healthy
- Linux VMs or templates that should authenticate centrally
- a service account in FreeIPA for Proxmox LDAP bind
- a clear group model for admins/operators

It is a good fit for environments where you want predictable onboarding/offboarding:

1. create or update users and groups in FreeIPA,
2. Proxmox sync imports relevant users/groups,
3. Linux guests accept access based on FreeIPA login + HBAC,
4. no host-local user sprawl.

## What this project does not do

- It does not domain-join Windows guests.
- It does not configure FreeRADIUS itself.
- It does not create FreeIPA users.
- It does not manage every possible Proxmox permission edge case.

## Repository layout

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
    └── bootstrap.sh
```

## Design choices

- **FreeIPA is authoritative** for identities and policy.
- **Proxmox uses a direct LDAP realm** against FreeIPA.
- **Proxmox group/user sync** is scheduled with a systemd timer on a single chosen PVE node.
- **Linux clients join FreeIPA** using the upstream `freeipa.ansible_freeipa.ipaclient` role.
- **HBAC controls Linux login authorization** instead of pushing local accounts everywhere.
- **Ansible Vault** is used for sensitive values.

## Prerequisites

Controller:

- Ansible Core 2.14+
- SSH reachability to your Proxmox primary node, IPA server, and Linux clients
- sudo/root privileges where required

Targets:

- Proxmox VE 9.x on the host in `proxmox_primary`
- FreeIPA reachable from Proxmox and Linux clients
- DNS and time sync already sane

## Quick start

### 1. Copy the example inventory and vars

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault.yml.example inventories/production/group_vars/all/vault.yml
```

### 2. Edit your environment values

Update:

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/main.yml`
- `inventories/production/group_vars/all/vault.yml`

### 3. Encrypt the vault file

```bash
ansible-vault encrypt inventories/production/group_vars/all/vault.yml
```

### 4. Install the required collection

```bash
./scripts/bootstrap.sh
```

### 5. Run validation first

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

### 6. Apply the full configuration

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## Recommended rollout order

For a first deployment, use this sequence:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

That makes troubleshooting easier than running the whole stack at once.

## Inventory model

This project uses three main inventory groups:

- `ipa_servers`: one or more FreeIPA servers
- `proxmox_primary`: one Proxmox node chosen to own realm configuration and sync timer
- `linux_ipa_clients`: Linux guests to enroll into FreeIPA

You can add other inventory groups for your own grouping logic and reference them from FreeIPA hostgroup definitions.

## Variable model

Most values live in:

- `inventories/production/group_vars/all/main.yml`
- `inventories/production/group_vars/all/vault.yml`

A few important variables:

### FreeIPA access model

- `freeipa_user_groups`
- `freeipa_hostgroups`
- `freeipa_hbac_rules`

### Proxmox LDAP realm

- `proxmox_ldap_realm_id`
- `proxmox_ldap_server1`
- `proxmox_ldap_base_dn`
- `proxmox_ldap_group_dn`
- `proxmox_ldap_bind_dn`
- `proxmox_ldap_bind_password`
- `proxmox_ldap_sync_attributes`
- `proxmox_ldap_sync_defaults`

### Proxmox RBAC

- `proxmox_custom_roles`
- `proxmox_acl_bindings`

### Linux IPA client enrollment

- `ipaclient_domain`
- `ipaclient_realm`
- `linux_ipa_servers`
- `linux_ipaclient_mkhomedir`
- `linux_ipasssd_permit`

## Example group strategy

A simple pattern that scales reasonably well:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- Proxmox ACL binding for synced group `proxmox-admins-ipa`

Remember that Proxmox LDAP sync creates synced groups with the suffix:

```text
<group-name>-<realm>
```

So if your FreeIPA group is `proxmox-admins` and the Proxmox realm is `ipa`, the synced PVE group name becomes:

```text
proxmox-admins-ipa
```

## Security notes

- Store all secrets in `vault.yml`, not in `main.yml`.
- Prefer a dedicated **read-only** LDAP bind account for Proxmox.
- Prefer TLS (`ldaps` or `ldap+starttls`) and certificate verification.
- Do not reuse your IPA admin user as the Proxmox LDAP bind account.
- Review `proxmox_ldap_filter` and `proxmox_ldap_group_filter` before production rollout to avoid syncing too much.

## Idempotency notes

This project is written to be reusable and mostly idempotent, but you should still review changes carefully in a lab first.

Known caveats:

- Proxmox CLI output varies slightly across releases.
- FreeIPA data modeling is flexible, so LDAP filters may need tuning for your tree.
- If you already hand-managed PVE ACLs and roles, compare before applying.

## Suggested next improvements

Common extensions you may want later:

- FreeIPA sudo rules
- Packer image pipeline for IPA-ready Linux templates
- AWX job templates and schedules
- separate Proxmox tenant/pool models
- Windows/AD trust flow for RDP logins

## License

MIT
