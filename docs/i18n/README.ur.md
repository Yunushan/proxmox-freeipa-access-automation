# Proxmox + FreeIPA رسائی آٹومیشن

یہ صفحہ [README.md](../../README.md) کی مکمل ساختی اردو ترجمہ فراہم کرتا ہے۔ انگریزی ورژن canonical ماخذ رہے گا، لیکن یہ فائل وہی اہم حصے کور کرتی ہے۔

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## یہ منصوبہ کیوں موجود ہے

اس repository کو اس وقت استعمال کریں جب آپ کے پاس پہلے سے:

- ایک صحت مند FreeIPA deployment
- ایک Proxmox VE cluster
- ایسے Linux guest جو مرکزی authentication استعمال کریں
- Proxmox LDAP bind کے لیے dedicated service account
- admins اور operators کے لیے واضح group model

بنیادی خیال یہ ہے کہ FreeIPA کو identity اور access کے لیے source of truth بنایا جائے۔ Proxmox اسے LDAP realm کے طور پر استعمال کرتا ہے، Linux guests `ipaclient` role کے ذریعے FreeIPA میں شامل ہوتے ہیں، اور SSH، HBAC اور `sudo` کنٹرول مرکزی رہتا ہے۔

## آپ کو کیا ملتا ہے

- FreeIPA user groups, hostgroups, HBAC rules اور `sudo` rules کا انتظام
- FreeIPA کے خلاف Proxmox LDAP realm configuration
- ایک مقررہ cluster node سے periodic realm sync
- synced groups کے لیے Proxmox RBAC bindings
- static inventory، manual host definitions یا Proxmox discovery سے Linux enrollment
- QEMU Guest Agent کے ذریعے optional no-reboot SSH bootstrap
- reachable guests کے لیے optional SSH یا WinRM guest-agent install
- first-touch کے لیے optional SSH public-key bootstrap
- FreeIPA access changes کے بعد automatic SSSD refresh
- `post-start` اور `post-migrate` کے لیے optional event-driven onboarding

## دائرہ کار

| شامل | شامل نہیں |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| synced groups سے Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | تمام Proxmox multi-tenant edge cases |

## معماری

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## ضروریات

### Controller

- Ansible Core 2.14+
- Proxmox primary node، IPA servers اور Linux clients تک SSH رسائی
- ضرورت کے مطابق `sudo` یا `root`
- اگر QGA SSH bootstrap فعال ہو تو guest کے اندر QEMU Guest Agent پہلے سے چل رہا ہو
- اگر Windows fallback فعال ہو تو host `windows_qemu_guest_agent_clients` میں ہوں
- اگر Linux SSH bootstrap فعال ہو تو controller کے پاس SSH keypair اور initial password path ہو

### Targets

- `proxmox_primary` میں Proxmox VE 6.x یا اس سے نیا
- Proxmox اور Linux clients سے reachable FreeIPA
- درست DNS اور time sync
- `proxmox_primary` کے لیے `root` یا ایسا sudo-capable user جو `pveversion`, `pvesh`, `pveum` چلا سکے
- discovery کے لیے QEMU Guest Agent سے usable IP

## نیٹ ورک پورٹس

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` اور `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, default `443/TCP`
- `636/TCP` for `ldaps`

## مطابقت

- Proxmox VE 6.x اور بعد کے ورژنز کے لیے
- default supported major: `6`, `7`, `8`, `9`, `10`
- `proxmox_supported_major_versions` سے override کیا جا سکتا ہے
- `proxmox_allow_future_major_versions` default `true`

## فوری آغاز

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

اپنے ماحول کے مطابق `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, اور `vault-proxmox.yml` کو edit کریں۔

## Rollout ترتیب

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Defaults جان بوجھ کر conservative ہیں: FreeIPA اور Proxmox کے لیے `serial: 1`، Linux کے لیے `serial: 10`، اور `max_fail_percentage: 0`.

## Tag ماڈل

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

اگر آپ چاہتے ہیں کہ Proxmox `post-start` یا `post-migrate` کے بعد فوراً Linux discovery اور IPA enrollment trigger کرے تو [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) میں بیان کردہ optional hook/webhook workflow استعمال کریں۔ یہ راستہ `playbooks/proxmox-vm-event.yml` استعمال کرتا ہے، ہر event پر LDAP realm یا RBAC دوبارہ نہیں چلاتا، اور نئے VM کو پہلے `post-start` پر پکڑ لیتا ہے۔

## Inventory ماڈل

اہم گروپس:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only یا Proxmox discovery کے ساتھ بھی guest کو final FQDN چاہیے، `ipa_hostname` یا `hostname -f` کے ذریعے۔

### Linux source modes

1. static inventory hosts
2. `linux_ipa_client_hosts` میں manual definitions
3. `linux_ipa_proxmox_discovery_*` کے ذریعے Proxmox discovery

اہم نوٹس: discovery QEMU Guest Agent network data پر منحصر ہے، `linux_ipa_proxmox_discovery_vmids` event path میں مددگار ہے، short names کے لیے `linux_ipa_identity_hostname_suffix` مفید ہے، authoritative DNS repair کے لیے `linux_freeipa_enroll_manage_authoritative_dns: true` استعمال ہو سکتا ہے، اور DNS تیار نہ ہونے پر `/etc/hosts` bootstrap دستیاب ہے۔

## Configuration surface

اہم فائلیں:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## مثال group strategy

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## سیکیورٹی

- secrets صرف vault files میں رکھیں
- Proxmox کے لیے dedicated read-only LDAP bind account کو ترجیح دیں
- certificate verification کے ساتھ TLS کو ترجیح دیں
- disposable lab کے باہر SSH host key checking بند نہ کریں

## Idempotency اور caveats

یہ repository repeatable run کے لیے لکھی گئی ہے، لیکن production سے پہلے lab validation ضروری ہے۔ معلوم حدود میں Proxmox CLI output differences، LDAP filter tuning، discovery کا QGA اور running guests پر انحصار، اور IP-based targets کے لیے valid final hostname کی ضرورت شامل ہے۔

## تصدیق

- FreeIPA میں groups, hostgroups, HBAC اور `sudo` verify کریں
- Proxmox میں LDAP realm, sync اور ACL bindings verify کریں
- Linux guest پر allowed login, denied HBAC case, `sudo -l` اور home creation چیک کریں

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

## ترقی

Repository میں `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflows, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, اور `scripts/vault.*` شامل ہیں۔

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## اگلی توسیعات

- IPA-ready Linux templates کے لیے Packer pipeline
- AWX job templates اور schedules
- الگ Proxmox tenant اور pool models
- RDP-oriented ماحول کے لیے Windows یا AD-trust flow

## لائسنس

یہ منصوبہ [MIT License](../../LICENSE) کے تحت جاری کیا گیا ہے۔
