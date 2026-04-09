# Proxmox + FreeIPA அணுகல் தானியக்கம்

இந்தப் பக்கம் [README.md](../../README.md) கோப்பின் முழுமையான கட்டமைப்பு சார்ந்த தமிழ் பதிப்பை வழங்குகிறது. ஆங்கில பதிப்பு canonical source ஆகவே இருக்கும், ஆனால் இந்த கோப்பு அதே முக்கிய பிரிவுகளை உள்ளடக்குகிறது.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## இந்த திட்டம் ஏன் உள்ளது

பின்வரும் சூழலில் இந்த repository பொருத்தமானது:

- நிலையான FreeIPA சூழல்
- Proxmox VE cluster
- centralized authentication தேவைப்படும் Linux guest-கள்
- Proxmox LDAP bind-க்கு dedicated service account
- admin/operator குழுக்களுக்கு தெளிவான group model

FreeIPA-ஐ identity மற்றும் access க்கான source of truth ஆக வைத்திருப்பதே மையக் கொள்கை. Proxmox அதை LDAP realm ஆகப் பயன்படுத்துகிறது, Linux guest-கள் `ipaclient` role மூலம் FreeIPA-வில் enroll ஆகின்றன, SSH, HBAC, `sudo` கட்டுப்பாடு மையமாகவே இருக்கும்.

## கிடைப்பவை

- FreeIPA user groups, hostgroups, HBAC rules மற்றும் `sudo` rules நிர்வகிப்பு
- FreeIPA அடிப்படையிலான Proxmox LDAP realm configuration
- ஒரு குறிப்பிட்ட cluster node-இலிருந்து periodic realm sync
- synced groups க்கான Proxmox RBAC bindings
- static inventory, manual host definitions அல்லது Proxmox discovery மூலம் Linux enrollment
- QEMU Guest Agent வழியாக optional no-reboot SSH bootstrap
- reachable guest களுக்கு optional SSH/WinRM guest-agent install
- first-touch க்கான optional SSH public-key bootstrap
- FreeIPA access மாற்றங்களுக்குப் பிறகு automatic SSSD refresh
- `post-start` மற்றும் `post-migrate` க்கான optional event-driven onboarding

## வரம்பு

| இதில் உள்ளது | இதில் இல்லை |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| synced groups மூலம் Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | அனைத்து Proxmox multi-tenant edge cases |

## கட்டமைப்பு

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## தேவைகள்

- Ansible Core 2.14+
- Proxmox primary node, IPA servers, Linux clients ஆகியவற்றிற்கு SSH அணுகல்
- தேவைப்பட்டால் `sudo` அல்லது `root`
- QGA SSH bootstrap பயன்பாட்டில் இருந்தால் guest-இல் QEMU Guest Agent முன்பே இயங்க வேண்டும்
- Windows fallback பயன்படுத்தினால் host-கள் `windows_qemu_guest_agent_clients`-இல் இருக்க வேண்டும்
- Linux SSH bootstrap பயன்படுத்தினால் SSH keypair மற்றும் initial password path வேண்டும்

## நெட்வொர்க் போர்ட்கள்

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` மற்றும் `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, default `443/TCP`
- `636/TCP` for `ldaps`

## விரைவு தொடக்கம்

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

உங்கள் சூழலுக்கு ஏற்ப `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, `vault-proxmox.yml` ஆகியவற்றைத் திருத்தவும்.

## Rollout வரிசை

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Defaults பாதுகாப்பானவை: FreeIPA மற்றும் Proxmox க்கு `serial: 1`, Linux க்கு `serial: 10`, மற்றும் `max_fail_percentage: 0`.

## Tag மாதிரி

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

`post-start` அல்லது `post-migrate` உடனேயே Proxmox Linux discovery மற்றும் IPA enrollment ஐ trigger செய்ய வேண்டும் என்றால் [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) உள்ள optional hook/webhook workflow ஐ பயன்படுத்தவும். இது `playbooks/proxmox-vm-event.yml` ஐப் பயன்படுத்துகிறது, ஒவ்வொரு event-க்கும் LDAP realm அல்லது RBAC ஐ மீண்டும் இயக்காது, புதிய VM-களை முதல் `post-start` இல் பிடிக்கும்.

## Inventory மாதிரி

முக்கிய group-கள்:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only அல்லது Proxmox discovery இருந்தாலும் guest-க்கு இறுதி FQDN தேவை; அது `ipa_hostname` அல்லது `hostname -f` மூலம் கிடைக்க வேண்டும்.

## Configuration surface

முக்கிய file-கள்:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Group strategy உதாரணம்

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## பாதுகாப்பு

- secrets ஐ vault files-ல் மட்டும் வைத்திருங்கள்
- Proxmox க்கு dedicated read-only LDAP bind account பயன்படுத்தவும்
- certificate verification உடன் TLS ஐ முன்னுரிமையாக்கவும்
- disposable lab அல்லாத இடங்களில் SSH host key checking ஐ அணைக்க வேண்டாம்

## சரிபார்ப்பு

- FreeIPA-வில் groups, hostgroups, HBAC, `sudo` ஐ சரிபார்க்கவும்
- Proxmox-வில் LDAP realm, sync, ACL bindings ஐ சரிபார்க்கவும்
- Linux guest-இல் allowed login, denied HBAC case, `sudo -l`, home creation ஆகியவற்றைச் சோதிக்கவும்

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

## மேம்பாடு

இந்த repository-யில் `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflows, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, மற்றும் `scripts/vault.*` அடங்கும்.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## அடுத்த விரிவாக்கங்கள்

- IPA-ready Linux templates க்கான Packer pipeline
- AWX job templates மற்றும் schedules
- தனித்த Proxmox tenant/pool models
- RDP-oriented சூழல்களுக்கு Windows அல்லது AD-trust flow

## உரிமம்

இந்த திட்டம் [MIT License](../../LICENSE) கீழ் வெளியிடப்பட்டுள்ளது.
