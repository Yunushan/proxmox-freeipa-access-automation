# Proxmox + FreeIPA ਐਕਸੈੱਸ ਆਟੋਮੇਸ਼ਨ

ਇਹ ਸਫ਼ਾ [README.md](../../README.md) ਦੀ ਪੂਰੀ ਸੰਰਚਨਾਤਮਕ ਪੰਜਾਬੀ ਰੂਪਾਂਤਰਨ ਵਰਜਨ ਦਿੰਦਾ ਹੈ। ਅੰਗਰੇਜ਼ੀ ਸੰਸਕਰਣ canonical source ਰਹਿੰਦਾ ਹੈ, ਪਰ ਇਹ ਫਾਇਲ ਉਹੀ ਮੁੱਖ ਭਾਗ ਕਵਰ ਕਰਦੀ ਹੈ।

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## ਇਹ ਪ੍ਰੋਜੈਕਟ ਕਿਉਂ ਹੈ

ਇਸ repository ਨੂੰ ਤਦੋਂ ਵਰਤੋਂ ਜਦੋਂ ਤੁਹਾਡੇ ਕੋਲ ਪਹਿਲਾਂ ਹੀ ਹੋਵੇ:

- ਇੱਕ ਸਿਹਤਮੰਦ FreeIPA deployment
- ਇੱਕ Proxmox VE cluster
- ਅਜੇਹੇ Linux guest ਜਿਨ੍ਹਾਂ ਨੂੰ central authentication ਚਾਹੀਦੀ ਹੈ
- Proxmox LDAP bind ਲਈ dedicated service account
- admins ਅਤੇ operators ਲਈ ਸਾਫ group model

ਮੁੱਖ ਵਿਚਾਰ ਇਹ ਹੈ ਕਿ FreeIPA ਨੂੰ identity ਅਤੇ access ਲਈ source of truth ਬਣਾਇਆ ਜਾਵੇ। Proxmox ਇਸਨੂੰ LDAP realm ਰਾਹੀਂ ਵਰਤਦਾ ਹੈ, Linux guest `ipaclient` role ਰਾਹੀਂ FreeIPA ਵਿੱਚ enroll ਹੁੰਦੇ ਹਨ, ਅਤੇ SSH, HBAC, `sudo` ਕੰਟਰੋਲ centralized ਰਹਿੰਦਾ ਹੈ।

## ਤੁਹਾਨੂੰ ਕੀ ਮਿਲਦਾ ਹੈ

- FreeIPA user groups, hostgroups, HBAC rules ਅਤੇ `sudo` rules ਦਾ ਪ੍ਰਬੰਧਨ
- FreeIPA ਦੇ ਖਿਲਾਫ Proxmox LDAP realm configuration
- ਨਿਰਧਾਰਤ cluster node ਤੋਂ periodic realm sync
- synced groups ਲਈ Proxmox RBAC bindings
- static inventory, manual host definitions ਜਾਂ Proxmox discovery ਤੋਂ Linux enrollment
- QEMU Guest Agent ਰਾਹੀਂ optional no-reboot SSH bootstrap
- reachable guest ਲਈ optional SSH/WinRM guest-agent install
- first-touch ਲਈ optional SSH public-key bootstrap
- FreeIPA access changes ਤੋਂ ਬਾਅਦ automatic SSSD refresh
- `post-start` ਅਤੇ `post-migrate` ਲਈ optional event-driven onboarding

## ਦਾਇਰਾ

| ਸ਼ਾਮਲ | ਸ਼ਾਮਲ ਨਹੀਂ |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| synced groups ਤੋਂ Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | ਸਾਰੇ Proxmox multi-tenant edge cases |

## ਆਰਕੀਟੈਕਚਰ

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## ਲੋੜਾਂ

- Ansible Core 2.14+
- Proxmox primary node, IPA servers ਅਤੇ Linux clients ਤੱਕ SSH ਪਹੁੰਚ
- ਲੋੜ ਅਨੁਸਾਰ `sudo` ਜਾਂ `root`
- QGA SSH bootstrap ਲਈ guest ਵਿੱਚ QEMU Guest Agent ਪਹਿਲਾਂ ਤੋਂ ਚਾਲੂ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ
- Windows fallback ਲਈ host `windows_qemu_guest_agent_clients` ਵਿੱਚ ਹੋਣ
- Linux SSH bootstrap ਲਈ SSH keypair ਅਤੇ initial password path

## ਨੈੱਟਵਰਕ ਪੋਰਟ

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` ਅਤੇ `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, default `443/TCP`
- `636/TCP` for `ldaps`

## ਤੇਜ਼ ਸ਼ੁਰੂਆਤ

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
./scripts/bootstrap.sh
ansible-playbook playbooks/validate.yml --ask-vault-pass
ansible-playbook playbooks/site.yml --ask-vault-pass
```

ਆਪਣੇ environment ਲਈ `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, ਅਤੇ `vault-proxmox.yml` ਸੋਧੋ।

## Rollout ਕ੍ਰਮ

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Defaults conservative ਹਨ: FreeIPA ਅਤੇ Proxmox ਲਈ `serial: 1`, Linux ਲਈ `serial: 10`, ਅਤੇ `max_fail_percentage: 0`.

## Tag ਮਾਡਲ

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

ਜੇ ਤੁਸੀਂ ਚਾਹੁੰਦੇ ਹੋ ਕਿ Proxmox `post-start` ਜਾਂ `post-migrate` ਤੋਂ ਬਾਅਦ ਤੁਰੰਤ Linux discovery ਅਤੇ IPA enrollment ਚਲਾਏ, ਤਾਂ [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) ਵਿੱਚ ਦਿੱਤਾ optional hook/webhook workflow ਵਰਤੋ। ਇਹ `playbooks/proxmox-vm-event.yml` ਵਰਤਦਾ ਹੈ, ਹਰ event ਤੇ LDAP realm ਜਾਂ RBAC ਮੁੜ ਨਹੀਂ ਚਲਾਉਂਦਾ ਅਤੇ ਨਵੇਂ VM ਨੂੰ ਪਹਿਲੇ `post-start` ਤੇ ਕੈਪਚਰ ਕਰਦਾ ਹੈ।

## Inventory ਮਾਡਲ

ਮੁੱਖ groups:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only ਜਾਂ Proxmox discovery ਹੋਣ ਦੇ ਬਾਵਜੂਦ guest ਨੂੰ final FQDN ਚਾਹੀਦਾ ਹੈ, `ipa_hostname` ਜਾਂ `hostname -f` ਰਾਹੀਂ।

## Configuration surface

ਮੁੱਖ ਫਾਇਲਾਂ:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Group strategy ਉਦਾਹਰਨ

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## ਸੁਰੱਖਿਆ

- secrets ਸਿਰਫ vault files ਵਿੱਚ ਰੱਖੋ
- Proxmox ਲਈ dedicated read-only LDAP bind account ਵਰਤੋ
- certificate verification ਦੇ ਨਾਲ TLS ਨੂੰ ਤਰਜੀਹ ਦਿਓ
- disposable lab ਤੋਂ ਬਾਹਰ SSH host key checking ਬੰਦ ਨਾ ਕਰੋ

## ਤਸਦੀਕ

- FreeIPA ਵਿੱਚ groups, hostgroups, HBAC ਅਤੇ `sudo` verify ਕਰੋ
- Proxmox ਵਿੱਚ LDAP realm, sync ਅਤੇ ACL bindings verify ਕਰੋ
- Linux guest ਉੱਤੇ allowed login, denied HBAC case, `sudo -l` ਅਤੇ home creation test ਕਰੋ

## Repository layout

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## Development

ਇਸ repository ਵਿੱਚ `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflows, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, ਅਤੇ `scripts/vault.*` ਸ਼ਾਮਲ ਹਨ।

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## ਅਗਲੇ ਵਿਸਥਾਰ

- IPA-ready Linux templates ਲਈ Packer pipeline
- AWX job templates ਅਤੇ schedules
- ਅਲੱਗ Proxmox tenant/pool models
- RDP-oriented environments ਲਈ Windows ਜਾਂ AD-trust flow

## ਲਾਇਸੈਂਸ

ਇਹ ਪ੍ਰੋਜੈਕਟ [MIT License](../../LICENSE) ਦੇ ਅਧੀਨ ਜਾਰੀ ਕੀਤਾ ਗਿਆ ਹੈ।
