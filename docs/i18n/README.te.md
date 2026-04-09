# Proxmox + FreeIPA యాక్సెస్ ఆటోమేషన్

ఈ పేజీ [README.md](../../README.md) యొక్క పూర్తి నిర్మాణాత్మక తెలుగు వెర్షన్‌ను అందిస్తుంది. ఇంగ్లీష్ వెర్షన్ canonical source గానే ఉంటుంది, కానీ ఈ ఫైల్ కూడా అదే ప్రధాన విభాగాలను కవర్ చేస్తుంది.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## ఈ ప్రాజెక్ట్ ఎందుకు ఉంది

ఈ repository క్రింది పరిస్థితుల్లో ఉపయోగించేందుకు రూపొందించబడింది:

- స్థిరమైన FreeIPA environment
- Proxmox VE cluster
- centralized authentication అవసరమైన Linux guestలు
- Proxmox LDAP bind కోసం dedicated service account
- admins, operators కోసం స్పష్టమైన group model

ప్రధాన ఆలోచన FreeIPA ను identity మరియు access కోసం source of truth గా ఉపయోగించడం. Proxmox దాన్ని LDAP realm ద్వారా ఉపయోగిస్తుంది, Linux guestలు `ipaclient` role ద్వారా FreeIPA లో enroll అవుతాయి, మరియు SSH, HBAC, `sudo` నియంత్రణ centralized గా ఉంటుంది.

## మీకు లభించేవి

- FreeIPA user groups, hostgroups, HBAC rules, `sudo` rules నిర్వహణ
- FreeIPA ఆధారిత Proxmox LDAP realm configuration
- నిర్ణయించిన cluster node నుండి periodic realm sync
- synced groups కోసం Proxmox RBAC bindings
- static inventory, manual host definitions లేదా Proxmox discovery ద్వారా Linux enrollment
- QEMU Guest Agent ద్వారా optional no-reboot SSH bootstrap
- reachable guestలకు optional SSH/WinRM guest-agent install
- first-touch కోసం optional SSH public-key bootstrap
- FreeIPA access మార్పుల తర్వాత automatic SSSD refresh
- `post-start`, `post-migrate` కోసం optional event-driven onboarding

## పరిధి

| ఇందులో ఉంది | ఇందులో లేదు |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| synced groups ద్వారా Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | అన్ని Proxmox multi-tenant edge cases |

## ఆర్కిటెక్చర్

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## అవసరాలు

- Ansible Core 2.14+
- Proxmox primary node, IPA servers, Linux clients వరకు SSH చేరుకోగలగడం
- అవసరమైన చోట `sudo` లేదా `root`
- QGA SSH bootstrap వాడితే guest లో QEMU Guest Agent ముందే రన్ అవుతూ ఉండాలి
- Windows fallback వాడితే hostలు `windows_qemu_guest_agent_clients` లో ఉండాలి
- Linux SSH bootstrap కోసం SSH keypair మరియు initial password path అవసరం

## నెట్‌వర్క్ పోర్టులు

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` మరియు `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, default `443/TCP`
- `636/TCP` for `ldaps`

## త్వరిత ప్రారంభం

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

మీ environment కు అనుగుణంగా `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, `vault-proxmox.yml` ఫైళ్లను మార్చండి.

## Rollout క్రమం

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Defaults conservative గా ఉంటాయి: FreeIPA, Proxmox కోసం `serial: 1`, Linux కోసం `serial: 10`, మరియు `max_fail_percentage: 0`.

## Tag మోడల్

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

Proxmox `post-start` లేదా `post-migrate` తర్వాత వెంటనే Linux discovery మరియు IPA enrollment trigger చేయాలనుకుంటే [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) లోని optional hook/webhook workflow ఉపయోగించండి. ఇది `playbooks/proxmox-vm-event.yml` ఉపయోగిస్తుంది, ప్రతి event కు LDAP realm లేదా RBAC మళ్లీ నడపదు, మరియు కొత్త VM ను మొదటి `post-start` వద్ద పట్టుకుంటుంది.

## Inventory మోడల్

ప్రధాన groups:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only లేదా Proxmox discovery ఉన్నా guest కు final FQDN అవసరం; అది `ipa_hostname` లేదా `hostname -f` ద్వారా రావాలి.

## Configuration surface

ప్రధాన files:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Group strategy ఉదాహరణ

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## భద్రత

- secrets ను vault files లో మాత్రమే ఉంచండి
- Proxmox కోసం dedicated read-only LDAP bind account ఉపయోగించండి
- certificate verification ఉన్న TLS ను ప్రాధాన్యంగా వాడండి
- disposable lab కాని చోట SSH host key checking ను ఆపవద్దు

## ధృవీకరణ

- FreeIPA లో groups, hostgroups, HBAC, `sudo` ను verify చేయండి
- Proxmox లో LDAP realm, sync, ACL bindings ను verify చేయండి
- Linux guest లో allowed login, denied HBAC case, `sudo -l`, home creation ను పరీక్షించండి

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

## అభివృద్ధి

ఈ repository లో `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflows, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, మరియు `scripts/vault.*` ఉన్నాయి.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## తదుపరి విస్తరణలు

- IPA-ready Linux templates కోసం Packer pipeline
- AWX job templates మరియు schedules
- వేరు చేసిన Proxmox tenant/pool models
- RDP-oriented environments కోసం Windows లేదా AD-trust flow

## లైసెన్స్

ఈ ప్రాజెక్ట్ [MIT License](../../LICENSE) కింద విడుదలైంది.
