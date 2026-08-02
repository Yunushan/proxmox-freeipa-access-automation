# Proxmox + FreeIPA அணுகல் தானியக்கம்

இந்தப் பக்கம் [README.md](../../README.md) கோப்பின் முழுமையான கட்டமைப்பு சார்ந்த தமிழ் மொழிபெயர்ப்பை வழங்குகிறது. ஆங்கில பதிப்பே பிரமாணமான மூலமாக இருக்கும், ஆனால் இந்த கோப்பு அதே முக்கிய பிரிவுகளனைத்தையும் உள்ளடக்குகிறது.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## மொழிகள்

ஆங்கில README இந்த ஆவணத்தின் பிரமாணமான மூலமாகும். மற்ற முழுமையான மொழிபெயர்க்கப்பட்ட README கோப்புகள் மொழிபெயர்ப்பு குறியீட்டில் கிடைக்கின்றன.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

## இந்த திட்டம் ஏன் உள்ளது

இந்த திட்டத்தை பயன்படுத்த வேண்டிய சரியான சூழல்:

- நிலையான FreeIPA சூழல்
- Proxmox VE கிளஸ்டர்
- மையப்படுத்தப்பட்ட அங்கீகாரம் தேவைப்படும் Linux guest-கள்
- Proxmox LDAP bind-க்கு தனியான சேவை கணக்கு
- admin/operator குழுக்களுக்கு தெளிவான குழு அமைப்பு

இந்த திட்டம் மிகவும் பொருத்தமானது, onboarding மற்றும் offboarding பெரும்பாலும் பின்வரும் படிகளாக அமைய வேண்டும் என்று நீங்கள் விரும்பினால்:

1. FreeIPA-வில் users மற்றும் groups-ஐ உருவாக்கவும் அல்லது புதுப்பிக்கவும்
2. அந்த identities-ஐ Proxmox-க்கு sync செய்யவும்
3. synced groups-இலிருந்து Proxmox roles மற்றும் ACLs-ஐப் பயன்படுத்தவும்
4. FreeIPA login, HBAC, மற்றும் sudo rules மூலம் Linux guest அணுகலை அனுமதிக்கவும்

## கிடைப்பவை

- FreeIPA user groups, hostgroups, HBAC rules மற்றும் `sudo` rules நிர்வகிப்பு
- Linux admin users-க்கு automatic FreeIPA login shell defaults
- FreeIPA அடிப்படையிலான Proxmox LDAP realm உள்ளமைவு
- ஒரு குறிப்பிட்ட cluster node-இலிருந்து காலமுறை realm sync
- synced groups க்கான Proxmox RBAC bindings
- static inventory, manual host definitions அல்லது Proxmox கண்டறிதல் மூலம் Linux enrollment
- QEMU Guest Agent வழியாக விருப்ப no-reboot SSH bootstrap
- Proxmox-backed Linux guest-களுக்கு Proxmox-side guest-agent communication enablement
- ஏற்கனவே reachable ஆன guest-கள், bootstrap-க்கு பின் reachable ஆகும் guest-கள், அல்லது Linux enrollment க்கு பின் மீண்டும் முயற்சி செய்யப்படும் guest-களுக்கு விருப்ப SSH அல்லது WinRM fallback QEMU Guest Agent installation
- SSH reachability மற்றும் Proxmox QEMU Guest Agent status க்கான விருப்ப Linux readiness reporting
- Active Directory மூலம் Windows 10/11 மற்றும் Windows Server guest-களுக்கு தனியான Windows domain-membership workflow
- IPA CA trust, hosts bootstrap, மற்றும் IPA reachability checks க்கான வரையறுக்கப்பட்ட FreeIPA-aware Windows helper workflow
- first-touch க்கான விருப்ப SSH public-key bootstrap
- FreeIPA access மாற்றங்களுக்குப் பிறகு தானியங்கி SSSD refresh
- `post-start` மற்றும் `post-migrate` க்கான விருப்ப event-driven onboarding

## வரம்பு

| இதில் அடங்குவது | இதில் அடங்காதது |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm setup | FreeIPA user lifecycle creation |
| synced groups மூலம் Proxmox RBAC | முழுமையான Proxmox multi-tenant policy coverage |
| Linux IPA client enrollment | FreeIPA-க்கு நேரடியாக native Windows logon |
| தனியான Windows AD domain-membership workflow | GPO அல்லது விரிவான AD object lifecycle automation |
| வரையறுக்கப்பட்ட FreeIPA-aware Windows helper workflow | FreeIPA-only Windows helpers-ஐ AD-க்கு சமமாகக் கருதுவது |

## விண்டோஸ் பணிச்சுற்று

Windows ஆதரவு Linux IPA enrollment-இன் உள்ளே கலக்கப்படாமல், தனியான workflow ஆக அமைக்கப்பட்டுள்ளது.

- `windows_qemu_guest_agent_clients` என்பது optional QEMU Guest Agent helper tasks-க்கு மட்டும் ஒதுக்கப்பட்ட குழுவாகவே இருக்கும்.
- workflow-ஐ இயக்க `10-features.yml`-இல் `windows_domain_membership_enabled: true` என்பதை அமைக்கவும்.
- `windows_management_clients` என்பது `playbooks/windows-management.yml` மற்றும் `playbooks/site.yml`-இன் optional Windows stage பயன்படுத்தும் தனியான Windows management group ஆகும்.
- உண்மையான Windows logon Active Directory domain membership மூலம் தான் செய்யப்படுகிறது; FreeIPA மையமாக உள்ள சூழல்களில் Windows hosts-ஐ FreeIPA-க்கு நேரடியாக join செய்ய முயற்சிக்காமல், FreeIPA-AD trust-இன் AD பக்கத்தில் join செய்ய வேண்டும்.

இந்த repository, FreeIPA-only Windows domain join-ஐ ஆதரிக்காது. Active Directory அல்லது FreeIPA-AD trust இல்லாதபோது, Windows workflow என்பது reachable guest management மற்றும் optional QEMU Guest Agent installation போன்ற helper tasks வரை மட்டுப்படுத்தப்படுகிறது.

Windows-க்கு domain join இல்லாமல் வரையறுக்கப்பட்ட FreeIPA-aware path வேண்டுமெனில், `windows_freeipa_helpers_enabled: true` என்பதை இயக்கி `windows_freeipa_helper_clients` குழுவை `playbooks/windows-freeipa-helpers.yml` உடன் பயன்படுத்தவும். அந்த helper workflow IPA CA-ஐ நம்ப வைக்கலாம், bootstrap க்காக IPA CA-ஐ auto-fetch செய்யலாம், எதிர்பார்க்கப்படும் IPA CA thumbprint-ஐ pin செய்யலாம், optional hosts-file bootstrap entries-ஐ நிர்வகிக்கலாம், IPA DNS மற்றும் முக்கிய TCP ports-ஐ validate செய்யலாம், Windows-இலிருந்து HTTPS reachability-ஐ validate செய்யலாம், IPA தொடர்புடைய endpoint-ஐ ஒப்பிட்டு Windows time source-ஐ validate செய்யலாம், local Windows group memberships-ஐ நிர்வகிக்கலாம், மற்றும் OpenSSH Server-ஐ install அல்லது expose செய்யலாம். ஆனால் இது FreeIPA-க்கு எதிராக native Windows logon வழங்காது.

அதே helper group-க்கு மாற்றமற்ற readiness check வேண்டுமெனில் `playbooks/windows-freeipa-validate.yml`-ஐ இயக்கவும். அது validation மற்றும் summary path-ஐ வைத்துக்கொண்டு, அந்த ஓட்டத்தில் CA import, hosts-file changes, local-group changes, மற்றும் OpenSSH management ஆகியவற்றை force off செய்கிறது.

இந்த workflow, WinRM அல்லது PSRP மூலம் reachable ஆகும் Windows 10/11 மற்றும் Windows Server guest-களை நோக்கமாகக் கொண்டுள்ளது.

## கட்டமைப்பு

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

விரிவான வடிவமைப்பு விளக்கத்திற்கு [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) ஐப் பார்க்கவும்.

## தேவைகள்

### கட்டுப்பாட்டு இயந்திரம்

- Ansible Core 2.14+
- Proxmox primary node, IPA servers, Linux clients ஆகியவற்றிற்கு SSH அணுகல்
- Windows workflow பயன்படுத்தினால் Windows guest-களுக்கு WinRM அல்லது PSRP அணுகல்
- தேவைப்பட்டால் `sudo` அல்லது `root`
- QGA SSH bootstrap பயன்பாட்டில் இருந்தால் guest-இல் QEMU Guest Agent முன்பே இயங்க வேண்டும்
- Windows fallback பயன்படுத்தினால் host-கள் `windows_qemu_guest_agent_clients`-இல் இருக்க வேண்டும்
- Windows domain membership பயன்படுத்தினால் host-கள் `windows_management_clients`-இல் இருக்க வேண்டும்; மேலும் AD join credentials வழங்கப்பட வேண்டும்
- Windows FreeIPA helper tasks பயன்படுத்தினால் host-கள் `windows_freeipa_helper_clients`-இல் இருக்க வேண்டும்
- Linux SSH bootstrap பயன்படுத்தினால் SSH keypair மற்றும் ஆரம்ப password path வேண்டும்

### இலக்குகள்

- `proxmox_primary` host-இல் Proxmox VE 6.x அல்லது அதற்கு மேற்பட்ட version
- Proxmox மற்றும் Linux clients-இலிருந்து reachable FreeIPA
- WinRM அல்லது PSRP மூலம் reachable ஆகும் போது Windows 10/11 மற்றும் Windows Server guest-களை தனியான Windows workflow மூலம் நிர்வகிக்கலாம்
- சரியான DNS மற்றும் நேர ஒத்திசைவு
- `proxmox_primary` க்கு `root` அல்லது `pveversion`, `pvesh`, `pveum` ஆகியவற்றை `sudo` உடன் இயக்கக்கூடிய user
- Windows domain membership பயன்படுத்தினால், தொடர்புடைய AD domain controllers-ஐ target Windows guest-கள் reach செய்ய வேண்டும்
- வரையறுக்கப்பட்ட Windows FreeIPA helper workflow பயன்படுத்தினால், தொடர்புடைய IPA servers-ஐ target Windows guest-கள் reach செய்ய வேண்டும்
- Proxmox discovery mode-இல் guest பயன்படக்கூடிய IP-ஐ QEMU Guest Agent மூலம் report செய்ய வேண்டும்

## நெட்வொர்க் போர்ட்கள்

இந்த repository-யின் controller, Proxmox LDAP automation, மற்றும் Linux IPA enrollment flow பயன்படுத்தும் network ports இவை. இது முழு FreeIPA server-to-server replication matrix அல்ல; இந்த திட்டத்துக்குச் சம்பந்தமான பகுதி மட்டும்.

| பெயர் | போர்ட் | நெறிமுறை | மூலம் | இலக்கு | எப்போது தேவை | நோக்கம் |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | எப்போதும் | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | Windows management இயக்கப்பட்டால் | Windows guest-களுக்கான Ansible connectivity |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS servers | Linux guest-கள் IPA DNS பயன்படுத்தும் போது | IPA records மற்றும் external names resolve செய்ய |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment மற்றும் login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA servers | Linux IPA enrollment மற்றும் login | LDAP மற்றும் FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port` (default `443`) | `TCP` | Linux guest | IPA servers | Linux IPA enrollment | client install நேரத்தில் IPA web/API verification |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment மற்றும் password operations | Kerberos password மற்றும் keytab operations |
| LDAPS | `636` | `TCP` | Proxmox primary node | IPA/LDAP servers | default `ldaps` mode-இல் Proxmox LDAP realm | Proxmox LDAP realm connection |

குறிப்புகள்:

- repository default `LDAPS 636/TCP`; காரணம் `proxmox_ldap_mode` இயல்பாக `ldaps` ஆகும். நீங்கள் LDAP mode அல்லது port மாற்றினால், அமைக்கப்பட்ட `proxmox_ldap_port`-ஐ அனுமதிக்கவும்.
- உங்கள் Windows transport அமைப்பைப் பொறுத்து, `WinRM` பொதுவாக HTTPS க்கு `5986/TCP` அல்லது HTTP க்கு `5985/TCP` பயன்படுத்தும்.
- `DNS 53/TCP,UDP` என்பது Linux guest-கள் IPA servers-ஐ DNS resolvers ஆக பயன்படுத்தும் போது மட்டுமே தேவை.
- `Kerberos 88` மற்றும் `Kerberos Password 464` க்கு `TCP` மற்றும் `UDP` இரண்டும் தேவை.
- Active Directory domain join க்கு, Windows-to-domain-controller port set கூட தேவைப்படும்; அது சூழல்-சார்ந்ததால் இங்கு முழுமையாக பட்டியலிடப்படவில்லை.
- Kerberos நம்பகமாக இயங்க நேர ஒத்திசைவு இன்னும் அவசியம்; ஆனால் NTP source சூழல்-சார்ந்தது, இந்த repository அதைப் நிர்வகிக்காது.

## இணக்கத்தன்மை

- இந்த repository-யில் உள்ள Proxmox automation, Proxmox VE 6.x மற்றும் அதற்கு அப்பாற்பட்ட releases-இல் பயன்படுத்தப்படும் `pveum` மற்றும் `pvesh` realm மற்றும் RBAC interfaces-ஐ மையமாகக் கொண்டு எழுதப்பட்டுள்ளது
- இந்த repository Proxmox VE 6.x மற்றும் அதற்கு அப்பாற்பட்ட major releases-ஐ முன்னிட்டு எழுதப்பட்டுள்ளது
- default supported major versions: `6`, `7`, `8`, `9`, `10`
- validation `pveversion` மூலம் கண்டறியப்பட்ட Proxmox version-ஐச் சரிபார்க்கிறது
- சூழலுக்கேற்ப பட்டியலைக் குறைக்க அல்லது விரிவாக்க `proxmox_supported_major_versions` மூலம் இந்த பட்டியலை மாற்றலாம்
- `proxmox_allow_future_major_versions` இயல்பாக `true` ஆக இருப்பதால் எதிர்கால major releases கூட சாதாரணமாக pass ஆகலாம்
- வெளியான Proxmox interface இந்த automation உடன் சரிபார்க்கப்படும் வரை, எதிர்கால major versions-ஐ compatibility candidates ஆகவே கருத வேண்டும்
- `1` முதல் `5` வரை உள்ள பழைய legacy majors இங்கு tested support எனக் கூறப்படவில்லை; அவற்றை local override ஆகச் சேர்த்தால், அதை explicit compatibility override ஆகக் கருதி, முழு workflow-ஐ lab-இல் validate செய்யவும்

பழைய lab சூழலுக்கான local override உதாரணம்:

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

## விரைவு தொடக்கம்

கீழே shell command உதாரணங்கள் கொடுக்கப்பட்டுள்ளன. தேவையான இடங்களில் PowerShell equivalents-வும் சேர்க்கப்பட்டுள்ளன.

### 1. உதாரண இன்வென்டரி மற்றும் வால்ட் டெம்ப்ளேட்-களை நகலெடுக்கவும்

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

### 2. சூழலுக்கு உரிய கோப்புகளைத் திருத்தவும்

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

Linux guest source mode-களில் ஒன்றைத் தேர்வு செய்யவும்:

- static inventory entries under `linux_ipa_clients`
- `linux_ipa_client_hosts` entries in `group_vars/all/30-linux-clients.yml`
- Proxmox VM discovery with `linux_ipa_proxmox_discovery_enabled: true`

Linux IPA enrollment-க்கு:

- `ipaclient_domain` shared IPA DNS domain, உதாரணம் `example.com`
- `linux_ipa_servers` IPA server hostnames பட்டியல், உதாரணம் `ipa01.example.com`

`root`-க்கு பதிலாக சாதாரண `sudo`-சாத்தியமான user மூலம் Proxmox-க்கு SSH செய்ய விரும்பினால், அதை `hosts.yml`-இல் `proxmox_primary` கீழ் அமைத்து, `sudo` password-ஐ `vault-proxmox.yml`-இல் வைத்திருங்கள்:

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

அந்த அமைப்பில் `vault_proxmox_become_password` என்பது Proxmox host-இல் `sudo` செய்ய நீங்கள் சாதாரணமாக টাইப் செய்யும் password ஆகும்.

### 3. வால்ட் கோப்புகளை குறியாக்கம் செய்யவும்

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

Windows பணிச்சுற்றை enable செய்யும் போது `vault-windows.yml`-யையும் சேர்க்கவும்.

அல்லது helper wrappers-ஐ பயன்படுத்தவும்; அவை இயல்பாக தனித்த vault ID-களைப் பயன்படுத்தும், மேலும் தேவையானபோது example templates-இலிருந்து working vault files-ஐ உருவாக்கும்:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Playbook-களை இயக்கும்போது domain ஒன்றுக்கு ஒரு password வேண்டும் என்றால் `--ask-vault-pass`-ஐ விட vault ID-களை முன்னுரிமையாகப் பயன்படுத்தவும்:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Optional Windows workflow-க்கும் தனி vault password இருந்தால், அதே command-இல் `windows@prompt`-ஐச் சேர்க்கவும்.

அந்த playbook பயன்படுத்தும் vault files அனைத்தும் ஒரே password பகிர்ந்தால் மட்டுமே `-AskVaultPass`-ஐப் பயன்படுத்தவும்.

### 4. தேவையான கலெக்ஷனை நிறுவவும்

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

அல்லது நேரடியாக:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

### 5. முதலில் சரிபார்ப்பை இயக்கவும்

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Helper-only Windows FreeIPA பாதைக்கு:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Linux readiness audit-க்கு:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Readiness report இயல்பாக `.ansible/linux-readiness-report.json` எழுதுகிறது.

- `ssh.ready=true`: configured SSH path வேலை செய்தது
- `ssh.promptless=true`: `ansible_password` இன்றி probe வெற்றி பெற்றது
- `ssh.auth_mode=password_configured`: `sshpass` பயன்படுத்தப்பட்டது
- `ssh.auth_mode=key_or_agent`: SSH batch mode password இன்றி வேலை செய்தது
- `qga.status=available`: `qm guest ping` owning Proxmox node-இல் வெற்றியடைந்தது
- `qga.status=disabled`: QEMU Guest Agent Proxmox config-இல் enable செய்யப்படவில்லை
- `qga.status=configured_unresponsive`: config-இல் enable ஆனாலும் பதில் இல்லை
- `qga.status=node_unreachable`: controller owning node-ஐ reach செய்யவில்லை
- `qga.status=not_applicable`: host Proxmox discovery மூலம் உருவாக்கப்படவில்லை

விரைவு ஆய்வு:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. விருப்பமாக: திட்டமிட்ட மாற்றங்களை முன்கூட்டியே பார்க்கவும்

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Check mode-ஐ முழுமையான simulation ஆக அல்ல, partial preview ஆகக் கருதுங்கள். சில Proxmox configuration-கள் direct CLI command-கள் மூலம் செய்யப்படுகின்றன; Linux enrollment க்கு upstream FreeIPA client role பயன்படுத்தப்படுகிறது.

### 7. முழு கட்டமைப்பை செயல்படுத்தவும்

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

## ரோல்அவுட் வரிசை

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

இந்த வரிசை troubleshooting-ஐ எளிதாக்குகிறது.

PowerShell வரையறுக்கப்பட்ட rollout உதாரணம்:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

இயல்புநிலை rollout கட்டுப்பாடுகள் கவனமாக அமைக்கப்பட்டுள்ளன:

- FreeIPA access changes க்கு `serial: 1`
- Proxmox changes க்கு `serial: 1`
- Linux hostname resolution, validation, enrollment க்கு `serial: 10`
- Windows management changes க்கு `serial: 10`
- அனைத்து rollout paths-க்கும் `max_fail_percentage: 0`

## டேக் மாதிரி

- `freeipa`, `proxmox`, `linux`, `validate`
- `windows`, `windows_domain`
- `windows`, `windows_freeipa`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

உதாரணங்கள்:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## நிகழ்வு வழிநடத்தும் VM ஆன்போர்டிங்

`post-start` அல்லது `post-migrate` க்கு பின் உடனடியாக Proxmox Linux discovery மற்றும் IPA enrollment trigger செய்ய வேண்டும் என்றால் [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../../docs/EVENT_DRIVEN_VM_ONBOARDING.md) உள்ள optional hook/webhook workflow ஐ பயன்படுத்தவும்.

இந்தப் பாதை `playbooks/proxmox-vm-event.yml` ஐப் பயன்படுத்துகிறது; Linux மற்றும் FreeIPA guest side மட்டும் handle செய்கிறது. ஒவ்வொரு VM event-க்கும் Proxmox LDAP realm அல்லது RBAC மறுபடியும் இயங்காது.

## இன்வென்டரி மாதிரி

இந்த repository ஆறு declared groups மற்றும் ஒரு generated runtime group-ஐப் பயன்படுத்துகிறது:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

IP-only அல்லது Proxmox discovery இருந்தாலும் guest-க்கு final FQDN தேவை; அது `ipa_hostname` அல்லது `hostname -f` மூலம் கிடைக்க வேண்டும்.

### லினக்ஸ் கெஸ்ட் மூல முறைகள்

`linux_ipa_clients`-ஐ மூன்று விதங்களில் நிரப்பலாம்.

#### 1. Static inventory hosts

guest பெயர்கள் ஏற்கனவே தெரிந்திருந்தால், சாதாரண Ansible inventory entries-ஐப் பயன்படுத்தவும்:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. variables-இல் கையால் host வரையறைகள்

guest-களை `hosts.yml`-க்கு வெளியே வைத்திருக்க விரும்பினால், அல்லது உங்களிடம் IP மட்டுமே இருந்தால், `linux_ipa_client_hosts`-ஐப் பயன்படுத்தவும்:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

குறிப்புகள்:

- `name` resolvable hostname அல்லது FQDN ஆக இருந்தால், `ansible_host` விருப்பமானது
- IP மட்டும் தெரிந்தால், `name` க்காக ஏதாவது நிலையான alias-ஐப் பயன்படுத்தவும்
- `ipa_hostname` விடுபட்டால், playbook guest-இல் `hostname -f`-ஐ fallback ஆகப் பயன்படுத்தும்

#### 3. Proxmox VM தானியங்கி கண்டறிதல்

ஒரு அல்லது அதற்கு மேற்பட்ட Proxmox node-களிலிருந்து Linux guest-களை playbook இழுத்து வர வேண்டும் என்றால் discovery-ஐப் பயன்படுத்தவும்:

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

குறிப்புகள்:

- discovery, மற்ற playbook-கள் பயன்படுத்தும் அதே `linux_ipa_clients_runtime` குழுவில் VM-களைச் சேர்க்கிறது
- IP discovery என்பது QEMU Guest Agent network interfaces report செய்வதின்மீது சார்ந்துள்ளது
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` என்பது ஏற்கனவே FQDN ஆன VM name-களை மட்டும் நம்பும்
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` அமைத்தால், `Teleport-Server-1` போன்ற பாதுகாப்பான short Proxmox VM names-ஐ `linux_ipa_identity_hostname_suffix` மூலம் `teleport-server-1.example.com` போன்ற hostname hints ஆக மாற்றலாம்
- `linux_ipa_proxmox_discovery_vmids` விருப்பமானது; event-driven hook/webhook workflow-இல் discovery-ஐ ஒரு அல்லது அதற்கு மேற்பட்ட VMID-களுக்கு வரையறுக்க அதிகம் பயன்படும்
- guest-க்கு இறுதி hostname இன்னும் தேவைப்படும்; அது VM-இல் ஏற்கனவே அமைக்கப்பட்டிருக்கலாம் அல்லது manual definition-இல் `ipa_hostname` மூலம் வழங்கப்பட்டிருக்கலாம்
- guest-இன் உண்மையான system hostname enrollment-க்கு செல்லுபடியாக இருக்க வேண்டும்; `localhost.localdomain` போன்ற placeholder values-ஐ `linux-clients` அல்லது `site` இயக்குவதற்கு முன் VM-இல் மாற்ற வேண்டும்
- guest-கள் `app-server-01` போன்ற short hostname-களைப் பயன்படுத்தினால், `linux_ipa_identity_hostname_suffix` மற்றும் விருப்பமாக `linux_freeipa_enroll_manage_hostname: true` அமைத்து, enrollment-க்கு முன் `app-server-01.example.net` போன்ற முழு hostname-ஐ தீர்மானித்து பயன்படுத்தலாம்
- உங்கள் guest hostnames-க்கு FreeIPA DNS authoritative ஆக இருந்தால், `linux_freeipa_enroll_manage_authoritative_dns: true` அமைத்து குறிப்பிட்ட guest A மற்றும் PTR records-ஐ சரிசெய்யவும், enrollment-க்கு முன் link-local `fe80::/10` AAAA records-ஐ அகற்றவும்
- DNS இன்னும் தயாராக இல்லாவிட்டால், `linux_ipa_manage_etc_hosts: true` மற்றும் `linux_ipa_etc_hosts_entries` மூலம் IPA servers மற்றும் guest FQDNs க்கான managed `/etc/hosts` bootstrap block-ஐ enrollment checks க்கு முன் சேர்க்கலாம்
- `guest_qemu_agent_install_enabled` ஏற்கனவே SSH அல்லது WinRM மூலம் reachable ஆன guest-களில் QEMU Guest Agent-ஐ install செய்கிறது; அதே workflow-இல் பின்னர் reachable ஆகும் Linux guest-களில் மீண்டும் முயற்சிக்கிறது; Linux enrollment-க்கு பிறகும் மீண்டும் முயற்சிக்கிறது
- discovery இயங்கியபடியே இருக்கட்டும், ஆனால் நெருக்கமாக அங்கீகரிக்கப்பட்ட சில Proxmox guest-களே Linux runtime inventory-க்குள் செல்ல வேண்டும் என்றால் `linux_ipa_proxmox_discovery_allowlist_enabled: true` அமைக்கவும்; allowlist துல்லியமான VMID, IP, மற்றும் name அடிப்படையில் match செய்யும்
- discovery-enabled node-களில் firewall அல்லது DNS server போன்ற infrastructure VM-கள் இருந்தால், அவை Linux IPA automation பெறக்கூடாது; அதற்காக `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, அல்லது `linux_ipa_proxmox_discovery_blacklist_names`-ஐப் பயன்படுத்தவும்; broad discovery அல்லது allowlist மூலம் admission இருந்தாலும் blacklist match எப்போதும் மேலோங்கும்
- ஏற்கனவே இயங்கும் guest agent இல்லாத Proxmox-discovered Linux guest-களுக்கு, QEMU Guest Agent install செய்ய repository-க்கு usable first-touch SSH path தேவைப்படும்; அதற்காக `linux_ipa_proxmox_discovery_ansible_user` மற்றும் `linux_ipa_proxmox_discovery_ansible_password` அல்லது `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` அமைக்கவும்
- அவை non-root SSH user பயன்படுத்தினால், passwordless sudo ஏற்கனவே இல்லாவிட்டால் `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, மற்றும் `linux_ipa_proxmox_discovery_ansible_become_password` ஆகியவற்றையும் அமைக்கவும்
- `guest_qemu_agent_install_manage_proxmox_vm_agent` guest-side install க்கு முன் Proxmox-side guest-agent communication (`qm set <vmid> --agent 1`) ஐயும் இயலுமைப்படுத்தும்
- இயங்கிக்கொண்டிருக்கும் VM-இல் அந்த Proxmox VM option மாறினால், Proxmox host guest-agent channel-ஐப் பயன்படுத்த புதிய VM start தேவைப்படலாம்; repository default-ஆக warning மட்டும் தரும்; அப்படிப்பட்ட running VM-களை தானாக reboot செய்ய வேண்டுமெனில் `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` அமைக்கவும்
- `linux_ipa_ssh_host_key_policy` இயல்பாக `accept_new`; அதனால் புதியதாக கண்டறியப்பட்ட VM-களை host key checking முற்றிலுமாக அணைக்காமல் தொடர்பு கொள்ளலாம்; ஆனால் மாறிய host keys இன்னும் fail ஆகும், operator review தேவைப்படும்
- `linux_ipa_qga_ssh_bootstrap_enabled` என்பது Proxmox-backed guest-களுக்கான விருப்ப no-reboot bootstrap path; எந்த SSH login-மும் இன்னும் இல்லாதபோது கூட QEMU Guest Agent வழியாக key-only automation user-ஐ உருவாக்க முடியும்
- `linux_ipa_qga_ssh_bootstrap_qm_path` இயல்பாக `qm`; bootstrap flow தோல்வியடைவதற்கு முன் Proxmox node-இல் பொதுவான fallback paths-ஐயும் probe செய்கிறது
- `guest-ping` அனுமதித்து `guest-exec` மறுக்கும் guest-கள் இயல்பாக QGA bootstrap-இல் skip செய்யப்படுகின்றன; அவற்றுக்கு மற்றொரு SSH path வைத்திருக்கவும், அல்லது உடனே fail ஆக வேண்டுமெனில் `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` அமைக்கவும்
- `linux_ipa_ssh_bootstrap_enabled` hostname resolution மற்றும் enrollment-க்கு முன் controller SSH public key-ஐ Linux guest-களில் install செய்ய விருப்பமாக அனுமதிக்கும்; key bootstrap முடக்கப்பட்டிருந்தாலும் runtime Linux guest-களுக்கு shared first-touch password fallback ஆக `linux_ipa_ssh_bootstrap_password` பயன்படுத்தப்படுகிறது
- FreeIPA JSON-RPC timeout காரணமாக தோல்வியடைந்த upstream client joins-ஐ Linux IPA enrollment மீண்டும் முயற்சிக்கும்; மெதுவான அல்லது busier IPA சூழல்களுக்கு `linux_ipaclient_kinit_attempts` வழங்கப்படுகிறது
- Linux IPA enrollment இயல்பாக `ipa_servers` inventory hostnames-ஐ join server list-இல் merge செய்கிறது; அதனால் client-கள் ஒரு server மட்டும் அல்லாமல் முழு IPA server set-ஐப் பயன்படுத்த முடியும்
- ஒன்றுக்கு மேற்பட்ட IPA server-கள் இருந்தால், ஒவ்வொரு retry pass-உம் அவற்றை ஒன்றன்பின் ஒன்றாக முயற்சிக்கும்
- combined `site` workflow முதலில் FreeIPA hostgroups-ஐ உருவாக்கி, Linux enrollment-க்கு பின் enrolled runtime hosts-ஐச் சேர்க்கிறது; அதனால் இன்னும் enrolled ஆகாத guest-கள் காரணமாக hostgroup membership build தோல்வியடையாது

## கட்டமைப்பு வரம்பு

பெரும்பாலான மதிப்புகள் இந்த file-களில் இருக்கும்:

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

முக்கிய variable குடும்பங்கள்:

| Area | Variables |
| --- | --- |
| FreeIPA access model | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Rollout controls | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Windows management | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helpers | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |

## குழு தந்திர உதாரணம்

நன்றாக அளவுபடுத்தக்கூடிய ஒரு எளிய மாதிரி:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- Sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa` க்கான Proxmox ACL binding

managed `linux-ssh-admins` குழுவின் மூலம் குறிப்பிட்ட IPA user-களுக்கு Linux SSH மற்றும் sudo access தானாக வழங்க `freeipa_linux_admin_users`-ஐ [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) இல் நிரப்பவும்.

Proxmox LDAP sync, suffix உடன் synced groups-ஐ உருவாக்கும் என்பதை நினைவில் கொள்ளவும்:

```text
<group-name>-<realm>
```

உங்கள் FreeIPA group `proxmox-admins`, மேலும் Proxmox realm `ipa` என்றால், synced PVE group ஆக மாறுவது:

```text
proxmox-admins-ipa
```

## பாதுகாப்பு

- எல்லா secrets-ஐயும் plaintext inventory variable files-ல் அல்ல, `vault-freeipa.yml` மற்றும் `vault-proxmox.yml` இல் வைத்திருங்கள்
- Proxmox க்கு dedicated read-only LDAP bind account பயன்படுத்தவும்
- certificate verification உடன் TLS ஐ முன்னுரிமையாக்கவும்
- disposable lab அல்லாத இடங்களில் SSH host key checking ஐ அணைக்க வேண்டாம்
- QGA available ஆக இருந்தால் shared temporary password களைவிட `linux_ipa_qga_ssh_bootstrap_enabled` path-ஐ முன்னுரிமையாக்கவும்
- repository-க்கு ஏற்கனவே guest-க்குள் செல்ல செல்லுபடியாகும் management path இருந்தால் மட்டுமே `guest_qemu_agent_install_enabled`-ஐப் பயன்படுத்தவும்; Proxmox discovery இல் அதாவது QGA ஏற்கனவே இயங்கிக் கொண்டிருக்க வேண்டும் அல்லது `linux_ipa_proxmox_discovery_ansible_user` மற்றும் password அல்லது key access அமைக்கப்பட்டிருக்க வேண்டும்
- Linux SSH bootstrap இயக்கப்பட்டால், shared bootstrap password-ஐ vaulted variables-இல் வைத்து, key-based access உருவான பிறகு அதை rotate செய்யவும் அல்லது அகற்றவும்
- IPA admin account-ஐ Proxmox LDAP bind account ஆக மீண்டும் பயன்படுத்த வேண்டாம்
- production rollout-க்கு முன் `proxmox_ldap_filter` மற்றும் `proxmox_ldap_group_filter` மதிப்புகளை review செய்து, தேவையற்ற அளவு import ஆகாதபடி கவனிக்கவும்

SSH host verification-ஐ நினைத்தே bypass செய்ய வேண்டிய disposable lab களுக்கு, repository defaults-ஐ மாற்றாமல் shell session அளவில் opt out செய்யவும்:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## இடெம்போட்டென்சி மற்றும் கவனிக்க வேண்டியவை

இந்த project பெரும்பாலும் idempotent ஆக எழுதப்பட்டுள்ளது. ஆனாலும் production க்கு முன் lab-இல் validate செய்வது அவசியம்.

- Proxmox CLI output release-ஐப் பொறுத்து சிறிது மாறலாம்
- FreeIPA LDAP filters உங்கள் directory tree க்கு tuning தேவைப்படலாம்
- existing hand-managed PVE ACLs மற்றும் roles automation க்கு முன் compare செய்யப்பட வேண்டும்
- Proxmox VM auto-discovery running guests மற்றும் QEMU guest-agent data மீது சார்ந்துள்ளது
- IP-only guest definitions க்கு valid final hostname அல்லது explicit `ipa_hostname` தேவை
- non-root Proxmox SSH user பயன்படுத்தினால் working `sudo` அவசியம்; passwordless sudo இல்லாவிட்டால் `-K` மூலம் become password கொடுக்க வேண்டும்

## சரிபார்ப்பு

### FreeIPA-வில்

- expected user groups ஐச் சரிபார்க்கவும்
- expected hostgroups ஐச் சரிபார்க்கவும்
- expected HBAC rules ஐச் சரிபார்க்கவும்
- expected sudo rules ஐச் சரிபார்க்கவும்

### Proxmox-வில்

- LDAP realm ஐச் சரிபார்க்கவும்
- initial sync expected users/groups ஐ import செய்ததா என்று பாருங்கள்
- intended synced group க்கு ACL binding சரியாக உள்ளதா எனச் சரிபார்க்கவும்

### லினக்ஸ் கெஸ்ட்-இல்

- allowed IPA user login சோதிக்கவும்
- denied HBAC case verify செய்யவும்
- `sudo -l` சோதிக்கவும்
- `linux_ipaclient_mkhomedir` enable ஆனால் முதல் login-இல் home creation verify செய்யவும்

## களஞ்சிய அமைப்பு

<details>
<summary>Repository கட்டமைப்பைக் காட்டு</summary>

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
├── scripts/
│   ├── bootstrap.ps1
│   ├── lint.py
│   ├── lint.ps1
│   ├── lint.sh
│   ├── patch_freeipa_collection.py
│   ├── proxmox-event-webhook.env.example
│   ├── proxmox-event-webhook.service.example
│   ├── proxmox-vm-hook.conf.example
│   ├── proxmox-vm-hook.pl
│   ├── proxmox_event_webhook.py
│   ├── smoke-test.py
│   ├── run-playbook.ps1
│   ├── vault.ps1
│   ├── vault.sh
│   └── bootstrap.sh
```

</details>

## மேம்பாடு

இந்த repository-யில் பின்வரும் helper files அடங்கும்:

- `.editorconfig` பல editor-களில் whitespace, encoding, மற்றும் line-ending defaults-ஐ ஒரே மாதிரியாக வைத்திருக்கிறது
- `.gitattributes` பொதுவான text files-ஐ LF line endings-இல் வைத்திருக்கிறது
- `.gitignore` generated inventory, vault data, local collections, மற்றும் editor files ஆகியவை Git-இல் செல்லாதபடி காக்கிறது
- `.ansible-lint` vendored collections-ஐ விலக்கி, YAML line-length rule ஒன்றையே மட்டும் suppress செய்கிறது
- `.yamllint` playbooks, inventories, மற்றும் workflow files முழுவதும் YAML formatting checks ஒரே மாதிரி இருக்கச் செய்கிறது
- `.github/CODEOWNERS` repository-யின் முக்கிய பகுதிகளுக்கான review ownership-ஐ வழிமாற்றுகிறது
- `.github/workflows/ci.yml` push மற்றும் pull request நேரங்களில் repository lint checks மற்றும் smoke validation ஐ இயக்குகிறது
- `.pre-commit-config.yaml` `pre-commit` நிறுவப்பட்டிருக்கும்போது commit க்களுக்கு முன் fast lint hook-ஐ இயக்குகிறது
- `CHANGELOG.md` repository-யின் முக்கியமான மாற்றங்களை ஒரு இடத்தில் பதிவு செய்கிறது
- `docs/VARIABLES.md` split inventory variable layout-ஐ விளக்குகிறது
- `docs/i18n/` மொழிபெயர்க்கப்பட்ட README கோப்புகளை வைத்திருக்கிறது; `README.md` canonical source ஆக இருக்கும் போது அவை முழு English section structure-ஐ பிரதிபலிக்க வேண்டும்
- `docs/i18n/TRANSLATION_GUIDE.md` மொழிபெயர்க்கப்பட்ட README கோப்புகளை எவ்வாறு ஒத்திசைக்க வேண்டும் என்பதை விளக்குகிறது
- `scripts/bootstrap.ps1` மற்றும் `scripts/bootstrap.sh` தேவையான collection-ஐ repo-local `collections/` பாதையில் நிறுவி, ansible-core 2.24+ இணக்கத்தன்மைக்காக patch செய்கின்றன
- `scripts/patch_freeipa_collection.py` pinned FreeIPA collection-இல் deprecated import-களை rewrite செய்து, எதிர்கால ansible-core releases உடனும் அது வேலை செய்யும் படி செய்கிறது
- `scripts/lint.py` local use, CI, மற்றும் pre-commit க்கு cross-platform lint entrypoint-ஐ வழங்குகிறது
- `scripts/smoke-test.py` உதாரண inventory-ஐ validate செய்து, உண்மையான infrastructure-ஐத் தொடாமல் syntax checks-ஐ இயக்குகிறது; தனியான Windows playbook-யும் இதில் அடங்கும்
- `scripts/check_translations.py` canonical English README-க்கு எதிராக metadata, section-structure parity, மற்றும் minimum content coverage ஆகியவற்றுக்காக மொழிபெயர்க்கப்பட்ட README கோப்புகளை audit செய்கிறது
- `scripts/lint.ps1` மற்றும் `scripts/lint.sh` இணைந்த local lint மற்றும் smoke workflow-ஐ இயக்குகின்றன
- `scripts/proxmox_event_webhook.py` Proxmox VM events க்கான optional controller-side webhook-ஐ இயக்குகிறது
- `scripts/proxmox-vm-hook.pl` `post-start` மற்றும் `post-migrate` சமயங்களில் controller webhook-ஐ அறிவிக்கும் optional Proxmox VM hookscript ஆகும்
- `scripts/run-playbook.ps1` தனியான Windows workflow உட்பட, PowerShell பயனர்களுக்கான பொதுவான `ansible-playbook` command-களை wrap செய்கிறது
- `scripts/vault.ps1` மற்றும் `scripts/vault.sh` FreeIPA, Proxmox, மற்றும் optional Windows secrets க்கான பொதுவான split-vault operations-ஐ wrap செய்கின்றன
- `tests/` repository verification surface-ஐ வைத்திருக்கிறது; அது smoke-test documentation-இல் இருந்து தொடங்குகிறது
- `CONTRIBUTING.md` எதிர்பார்க்கப்படும் contribution மற்றும் validation workflow-ஐ ஆவணப்படுத்துகிறது
- `SECURITY.md` பாதிப்பு அறிக்கைகள் மற்றும் security-sensitive தகவல்களை எவ்வாறு கையாள வேண்டும் என்பதை ஆவணப்படுத்துகிறது

உங்கள் controller-இல் `ansible-lint` நிறுவப்பட்டிருந்தால்:

```bash
ansible-lint
```

Repository smoke checks-ஐ நேரடியாக இயக்க:

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

முழுமையான local lint pass-க்கு:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

ஒவ்வொரு commit-க்கும் முன் fast lint hook-ஐ enable செய்ய:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell wrapper உதாரணங்கள்:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## அடுத்த விரிவாக்கங்கள்

- IPA-ready Linux templates க்கான Packer pipeline
- AWX job templates மற்றும் schedules
- தனித்த Proxmox tenant/pool models
- மேலும் விரிவான Windows local policy அல்லது GPO ஒருங்கிணைப்பு

## உரிமம்

இந்த திட்டம் [0BSD License](../../LICENSE) கீழ் வெளியிடப்பட்டுள்ளது.
