# Proxmox + FreeIPA యాక్సెస్ ఆటోమేషన్

ఈ పేజీ [README.md](../../README.md) యొక్క పూర్తి నిర్మాణాత్మక తెలుగు అనువాదాన్ని అందిస్తుంది. ఇంగ్లీష్ వెర్షన్‌నే ప్రామాణిక మూలంగా పరిగణించాలి, అయితే ఈ ఫైల్ కూడా అదే ప్రధాన విభాగాలన్నింటినీ కవర్ చేస్తుంది.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## భాషలు

ఇంగ్లీష్ README ఈ పత్రానికి ప్రామాణిక మూలం. ఇతర పూర్తి అనువాద README ఫైళ్లు అనువాద సూచికలో అందుబాటులో ఉన్నాయి.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

## ఈ ప్రాజెక్ట్ ఎందుకు ఉంది

ఈ ప్రాజెక్ట్‌ను ఉపయోగించాల్సిన సరైన సందర్భం:

- స్థిరమైన FreeIPA పరిసరం
- Proxmox VE క్లస్టర్
- కేంద్రీకృత ప్రమాణీకరణ అవసరమైన Linux guestలు
- Proxmox LDAP bind కోసం ప్రత్యేక సేవా ఖాతా
- admins మరియు operators కోసం స్పష్టమైన గుంపు నమూనా

మీకు onboarding మరియు offboarding ఎక్కువగా ఈ క్రమంలో జరగాలి అనుకుంటే ఈ ప్రాజెక్ట్ బాగా సరిపోతుంది:

1. FreeIPA లో users మరియు groups ను సృష్టించండి లేదా నవీకరించండి
2. ఆ identities ను Proxmox లోకి sync చేయండి
3. synced groups ఆధారంగా Proxmox roles మరియు ACLs ను వర్తింపజేయండి
4. FreeIPA login, HBAC, మరియు sudo rules ద్వారా Linux guest access ను అనుమతించండి

## మీకు లభించేవి

- FreeIPA user groups, hostgroups, HBAC rules, `sudo` rules నిర్వహణ
- Linux admin users కోసం automatic FreeIPA login-shell defaults
- FreeIPA ఆధారిత Proxmox LDAP realm ఆకృతీకరణ
- నిర్ణయించిన cluster node నుండి కాలానుగుణ realm sync
- synced groups కోసం Proxmox RBAC bindings
- static inventory, manual host నిర్వచనలు లేదా Proxmox గుర్తింపు ద్వారా Linux enrollment
- QEMU Guest Agent ద్వారా ఐచ్చిక no-reboot SSH bootstrap
- Proxmox-backed Linux guests కోసం ఐచ్చిక Proxmox-side guest-agent communication enablement
- ఇప్పటికే reachable గా ఉన్న guestలు, bootstrap తర్వాత reachable అయ్యే guestలు, లేదా Linux enrollment తర్వాత మళ్లీ ప్రయత్నించే guestల కోసం ఐచ్చిక SSH లేదా WinRM fallback QEMU Guest Agent installation
- SSH reachability మరియు Proxmox QEMU Guest Agent స్థితి కోసం ఐచ్చిక Linux readiness reporting
- Active Directory ద్వారా Windows 10/11 మరియు Windows Server guestల కోసం వేరుగా ఉన్న Windows domain-membership workflow
- IPA CA trust, hosts bootstrap, మరియు IPA reachability checks కోసం పరిమిత FreeIPA-aware Windows helper workflow
- first-touch కోసం ఐచ్చిక SSH public-key bootstrap
- FreeIPA access మార్పుల తర్వాత స్వయంచాలక SSSD refresh
- `post-start`, `post-migrate` కోసం ఐచ్చిక event-driven onboarding

## పరిధి

| ఇందులో ఉంది | ఇందులో లేదు |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm setup | FreeIPA user lifecycle creation |
| synced groups ద్వారా Proxmox RBAC | పూర్తి Proxmox multi-tenant policy coverage |
| Linux IPA client enrollment | FreeIPA కు నేరుగా native Windows logon |
| వేరుగా ఉన్న Windows AD domain-membership workflow | GPO లేదా మరింత విస్తృతమైన AD object lifecycle automation |
| పరిమిత FreeIPA-aware Windows helper workflow | FreeIPA-only Windows helpers ను AD కి సమానంగా భావించడం |

## విండోస్ వర్క్‌ఫ్లో

Windows support ను Linux IPA enrollment లో కలపకుండా, వేరే workflow గా అమలు చేస్తారు.

- `windows_qemu_guest_agent_clients` అనే group ఐచ్చిక QEMU Guest Agent helper tasks కోసం మాత్రమే ఉపయోగించబడుతుంది.
- workflow ను ప్రారంభించడానికి `10-features.yml` లో `windows_domain_membership_enabled: true` ను సెట్ చేయండి.
- `windows_management_clients` అనేది `playbooks/windows-management.yml` మరియు `playbooks/site.yml` లోని optional Windows stage ఉపయోగించే ప్రత్యేక Windows management group.
- నిజమైన Windows logon ను Active Directory domain membership ద్వారానే నిర్వహిస్తారు; FreeIPA కేంద్రంగా ఉన్న పరిసరాల్లో Windows hosts ను FreeIPA కు నేరుగా join చేయకుండా, FreeIPA-AD trust లోని AD వైపుకు join చేయాలి.

ఈ repository FreeIPA-only Windows domain join ను support చేయదు. Active Directory లేదా FreeIPA-AD trust లేకపోతే, Windows workflow అనేది reachable guest management మరియు optional QEMU Guest Agent installation వంటి helper tasks కు మాత్రమే పరిమితమవుతుంది.

Domain join లేకుండానే పరిమిత FreeIPA-aware Windows path కావాలనుకుంటే, `windows_freeipa_helpers_enabled: true` ను enable చేసి `windows_freeipa_helper_clients` group ను `playbooks/windows-freeipa-helpers.yml` తో ఉపయోగించండి. ఆ helper workflow IPA CA ను trust చేయగలదు, bootstrap కోసం IPA CA ను auto-fetch చేయగలదు, ఆశించిన IPA CA thumbprint ను pin చేయగలదు, optional hosts-file bootstrap entries ను నిర్వహించగలదు, IPA DNS మరియు ముఖ్య TCP ports ను validate చేయగలదు, Windows నుంచి HTTPS reachability ను validate చేయగలదు, IPA కు సంబంధించిన endpoint తో Windows time source ను validate చేయగలదు, local Windows group memberships ను నిర్వహించగలదు, మరియు ఐచ్చికంగా OpenSSH Server ను install లేదా expose చేయగలదు. అయితే ఇది FreeIPA కు native Windows logon ను అందించదు.

అదే helper group కోసం మార్పులు చేయని readiness check కావాలంటే `playbooks/windows-freeipa-validate.yml` ను నడపండి. అది validation మరియు summary మార్గాన్ని అలాగే ఉంచి, ఆ run లో CA import, hosts-file changes, local-group changes, మరియు OpenSSH management ను బలవంతంగా ఆపేస్తుంది.

ఈ workflow WinRM లేదా PSRP ద్వారా చేరుకోగల Windows 10/11 మరియు Windows Server guestలను లక్ష్యంగా ఉంచుతుంది.

## ఆర్కిటెక్చర్

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

పెద్ద రూపకల్పన వివరణ కోసం [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) చూడండి.

## అవసరాలు

### కంట్రోలర్

- Ansible Core 2.14+
- Proxmox primary node, IPA servers, Linux clients వరకు SSH ద్వారా చేరుకోగలగడం
- Windows workflow ఉపయోగించినప్పుడు Windows guests వరకు WinRM లేదా PSRP ద్వారా చేరుకోగలగడం
- అవసరమైన చోట `sudo` లేదా `root`
- QGA SSH bootstrap వాడితే guest లో QEMU Guest Agent ముందే నడుస్తూ ఉండాలి
- Windows fallback వాడితే hostలు `windows_qemu_guest_agent_clients` లో ఉండాలి
- Windows domain membership enable చేసినప్పుడు reachable Windows hosts `windows_management_clients` లో ఉండాలి మరియు మీరు AD join credentials ఇవ్వాలి
- Windows FreeIPA helper tasks enable చేసినప్పుడు reachable Windows hosts `windows_freeipa_helper_clients` లో ఉండాలి
- Linux SSH bootstrap కోసం SSH keypair మరియు ప్రారంభ password మార్గం అవసరం

### లక్ష్యాలు

- `proxmox_primary` host పై Proxmox VE 6.x లేదా అంతకంటే కొత్త version
- Proxmox మరియు Linux clients నుండి reachable FreeIPA
- WinRM లేదా PSRP ద్వారా చేరుకోగలిగితే, Windows 10/11 మరియు Windows Server guests ను వేరుగా ఉన్న Windows workflow ద్వారా నిర్వహించవచ్చు
- సరైన DNS మరియు సమయ సమకాలీకరణ
- `proxmox_primary` కోసం `root` లేదా `pveversion`, `pvesh`, `pveum` ను `sudo` తో నడపగల user
- Windows domain membership ఉపయోగిస్తే, లక్ష్య Windows guests సంబంధిత AD domain controllers ను చేరుకోగలగాలి
- పరిమిత Windows FreeIPA helper workflow ఉపయోగిస్తే, లక్ష్య Windows guests సంబంధిత IPA servers ను చేరుకోగలగాలి
- Proxmox discovery mode లో guest ఉపయోగించగల IP ను QEMU Guest Agent ద్వారా report చేయాలి

## నెట్‌వర్క్ పోర్టులు

ఈ repository controller, Proxmox LDAP automation, మరియు Linux IPA enrollment flow ఉపయోగించే network ports ను ఈ పట్టిక చూపిస్తుంది. ఇది ఈ ప్రాజెక్ట్‌కు సంబంధించిన పరిధిలోనే ఉంటుంది; FreeIPA server-to-server replication యొక్క పూర్తి matrix కాదు.

| పేరు | పోర్ట్ | ప్రోటోకాల్ | మూలం | గమ్యం | ఎప్పుడు అవసరం | ఉద్దేశ్యం |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | ఎల్లప్పుడూ | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | Windows management enable చేసినప్పుడు | Windows guests కు Ansible connectivity |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS servers | Linux guests IPA DNS ఉపయోగించినప్పుడు | IPA records మరియు external names ను resolve చేయడం |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment మరియు login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA servers | Linux IPA enrollment మరియు login | LDAP మరియు FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port` (default `443`) | `TCP` | Linux guest | IPA servers | Linux IPA enrollment | client install సమయంలో IPA web/API verification |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment మరియు password operations | Kerberos password మరియు keytab operations |
| LDAPS | `636` | `TCP` | Proxmox primary node | IPA/LDAP servers | default `ldaps` mode లో Proxmox LDAP realm | Proxmox LDAP realm connection |

గమనికలు:

- `proxmox_ldap_mode` default `ldaps` కావడంతో repository default `LDAPS 636/TCP`. మీరు LDAP mode లేదా port మార్చితే, మీరు configure చేసిన `proxmox_ldap_port` ను అనుమతించండి.
- Windows transport setup ను బట్టి `WinRM` సాధారణంగా HTTPS కోసం `5986/TCP`, HTTP కోసం `5985/TCP` ఉపయోగిస్తుంది.
- `DNS 53/TCP,UDP` అనేది Linux guests IPA servers ను DNS resolvers గా ఉపయోగించినప్పుడు మాత్రమే అవసరం.
- `Kerberos 88` మరియు `Kerberos Password 464` రెండింటికీ `TCP` మరియు `UDP` అవసరం.
- Active Directory domain join కు సాధారణ Windows-to-domain-controller port set కూడా అవసరమే, అయితే అది పరిసరానుసారంగా మారుతుంది కాబట్టి ఇక్కడ పూర్తి జాబితా ఇవ్వలేదు.
- Kerberos నమ్మదగిన విధంగా పని చేయడానికి time synchronization ఇంకా అవసరం; కానీ NTP source పరిసరానుసారమైనది, ఈ repository దాన్ని నిర్వహించదు.

## అనుకూలత

- ఈ repository లోని Proxmox automation, Proxmox VE 6.x మరియు తర్వాతి విడుదలల్లో ఉపయోగించే `pveum` మరియు `pvesh` realm మరియు RBAC interfaces ఆధారంగా రాయబడింది.
- ఈ repository Proxmox VE 6.x మరియు తదుపరి major releases కోసం రూపొందించబడింది
- default supported major versions: `6`, `7`, `8`, `9`, `10`
- validation `pveversion` ద్వారా గుర్తించిన Proxmox version ను check చేస్తుంది
- అవసరాన్ని బట్టి ఈ జాబితాను తగ్గించడానికి లేదా విస్తరించడానికి `proxmox_supported_major_versions` ను override చేయవచ్చు
- `proxmox_allow_future_major_versions` default `true` కావడంతో future major releases కూడా సాధారణంగా pass కావచ్చు
- విడుదలైన Proxmox interface ఈ automation తో సరిపోతుందో చూసే వరకు, future major versions ను compatibility candidates గా భావించాలి
- `1` నుంచి `5` వరకు ఉన్న పాత legacy majors ఈ public repository లో tested support గా చెప్పబడవు; వాటిని local గా జోడిస్తే దాన్ని explicit compatibility override గా పరిగణించి, పూర్తి workflow ను lab లో validate చేయాలి

పాత lab పరిసరానికి స్థానిక override ఉదాహరణ:

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

## త్వరిత ప్రారంభం

క్రింద shell command ఉదాహరణలు ఉన్నాయి. అవసరమైన చోట PowerShell equivalents కూడా చేర్చబడ్డాయి.

### 1. ఉదాహరణ ఇన్వెంటరీ మరియు వాల్ట్ టెంప్లేట్‌లను కాపీ చేయండి

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

### 2. పరిసరానికి సంబంధించిన ఫైళ్లను సవరించండి

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

Linux guest source విధానాల్లో ఒకదాన్ని ఎంచుకోండి:

- static inventory entries under `linux_ipa_clients`
- `linux_ipa_client_hosts` entries in `group_vars/all/30-linux-clients.yml`
- Proxmox VM discovery with `linux_ipa_proxmox_discovery_enabled: true`

Linux IPA enrollment కోసం:

- `ipaclient_domain` shared IPA DNS domain, ఉదాహరణకు `example.com`
- `linux_ipa_servers` IPA server hostnames జాబితా, ఉదాహరణకు `ipa01.example.com`

మీరు `root` బదులు సాధారణ `sudo` సామర్థ్యమున్న user తో Proxmox కు SSH చేయాలనుకుంటే, దాన్ని `hosts.yml` లో `proxmox_primary` కింద సెట్ చేసి, `sudo` password ను `vault-proxmox.yml` లో ఉంచండి:

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

ఆ setup లో `vault_proxmox_become_password` అనేది Proxmox host పై `sudo` కోసం మీరు సాధారణంగా టైప్ చేసే password.

### 3. వాల్ట్ ఫైళ్లను సంకేతీకరించండి

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

Windows వర్క్‌ఫ్లోను enable చేస్తే `vault-windows.yml` ను కూడా చేర్చండి.

లేదా helper wrappers ను ఉపయోగించండి; అవి సాధారణంగా వేరువేరు vault IDs ను ఉపయోగిస్తాయి మరియు అవసరమైతే example templates నుండి working vault files ను సృష్టిస్తాయి:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Playbooks నడుపుతున్నప్పుడు ప్రతి domain కు వేరు password కావాలనుకుంటే `--ask-vault-pass` కన్నా vault IDs ను ఉపయోగించడం మంచిది:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Optional Windows workflow కూడా తనదైన vault password ఉపయోగిస్తే, అదే command కు `windows@prompt` ను చేర్చండి.

ఆ playbook ఉపయోగించే అన్ని vault files ఒకే password పంచుకున్నప్పుడు మాత్రమే `-AskVaultPass` ను ఉపయోగించండి.

### 4. అవసరమైన కలెక్షన్ ను ఇన్‌స్టాల్ చేయండి

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

లేదా నేరుగా:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

### 5. ముందుగా ధృవీకరణను నడపండి

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Helper-only Windows FreeIPA మార్గం కోసం:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Linux readiness audit కోసం:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Readiness report సాధారణంగా `.ansible/linux-readiness-report.json` లో వ్రాస్తుంది.

- `ssh.ready=true`: configured SSH path పని చేసింది
- `ssh.promptless=true`: `ansible_password` లేకుండా probe విజయవంతమైంది
- `ssh.auth_mode=password_configured`: `sshpass` ఉపయోగించబడింది
- `ssh.auth_mode=key_or_agent`: password లేకుండా SSH batch mode పని చేసింది
- `qga.status=available`: owning Proxmox node పై `qm guest ping` విజయవంతమైంది
- `qga.status=disabled`: QEMU Guest Agent Proxmox config లో enable చేయబడలేదు
- `qga.status=configured_unresponsive`: config లో enable ఉన్నా స్పందించలేదు
- `qga.status=node_unreachable`: controller owning node ను చేరలేదు
- `qga.status=not_applicable`: host Proxmox discovery ద్వారా సృష్టించబడలేదు

త్వరిత పరిశీలన:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. ఐచ్చికంగా: ప్రణాళిక చేసిన మార్పులను ముందుగా చూడండి

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Check mode ను పూర్తి simulation గా కాకుండా partial preview గా చూడండి. కొన్ని Proxmox configuration steps direct CLI commands ద్వారా జరుగుతాయి, మరియు Linux enrollment కోసం upstream FreeIPA client role ఉపయోగించబడుతుంది.

### 7. పూర్తి కాన్ఫిగరేషన్‌ను అమలు చేయండి

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

## రోలౌట్ క్రమం

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

ఈ క్రమం troubleshooting ను సులభం చేస్తుంది.

PowerShell పరిమిత rollout ఉదాహరణ:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

డిఫాల్ట్ rollout నియంత్రణలు జాగ్రత్తగా ఉంచబడ్డాయి:

- FreeIPA access changes కోసం `serial: 1`
- Proxmox changes కోసం `serial: 1`
- Linux hostname resolution, validation, enrollment కోసం `serial: 10`
- Windows management changes కోసం `serial: 10`
- అన్ని rollout paths కు `max_fail_percentage: 0`

## ట్యాగ్ మోడల్

- `freeipa`, `proxmox`, `linux`, `validate`
- `windows`, `windows_domain`
- `windows`, `windows_freeipa`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

ఉదాహరణలు:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## ఈవెంట్ ఆధారిత VM ఆన్‌బోర్డింగ్

Proxmox `post-start` లేదా `post-migrate` తర్వాత వెంటనే Linux discovery మరియు IPA enrollment trigger చేయాలనుకుంటే [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../../docs/EVENT_DRIVEN_VM_ONBOARDING.md) లోని optional hook/webhook workflow ఉపయోగించండి.

ఈ workflow `playbooks/proxmox-vm-event.yml` అనే dedicated event playbook ను ఉపయోగిస్తుంది, కాబట్టి trigger path లో Linux మరియు FreeIPA guest వైపు మాత్రమే నిర్వహించబడుతుంది. ప్రతి VM event కు Proxmox LDAP realm లేదా RBAC automation మళ్లీ నడవదు.

`proxmox_vm_event_onboarding_enabled: true` మరియు అవసరమైన webhook variables సెట్ చేసినప్పుడు, ఈ repository `site.yml` లేదా `proxmox.yml` నుంచి కూడా ఆ optional hook/webhook stack ను deploy చేయగలదు.

Proxmox VM hooks లో standalone `create` phase ఉండదు. ప్రాక్టికల్‌గా కొత్త VMs తమ మొదటి `post-start` event లో గుర్తించబడతాయి, మరియు migration hooks source మరియు target nodes రెండింటిపై trigger కావచ్చు.

## ఇన్వెంటరీ మోడల్

ఈ repository ఆరు declared groups మరియు ఒక generated runtime group ను ఉపయోగిస్తుంది:

- `ipa_servers`: ఒకటి లేదా అంతకంటే ఎక్కువ FreeIPA servers
- `proxmox_primary`: realm configuration మరియు recurring sync timer బాధ్యత వహించే ఒక Proxmox node
- `linux_ipa_clients`: Linux guests కోసం declarative source inventory group
- `linux_ipa_clients_runtime`: static inventory, manual host definitions, మరియు optional Proxmox discovery ద్వారా నిర్మించబడే generated runtime group
- `windows_qemu_guest_agent_clients`: QEMU Guest Agent installation కోసం మాత్రమే ఉపయోగించే ఐచ్చిక Windows guest group
- `windows_management_clients`: వేరుగా ఉన్న Windows domain-membership workflow ఉపయోగించే ఐచ్చిక Windows guest group
- `windows_freeipa_helper_clients`: పరిమిత FreeIPA-aware helper workflow ఉపయోగించే ఐచ్చిక Windows guest group

మీ స్వంత inventory groups ను కూడా జోడించి వాటిని FreeIPA hostgroup definitions లో reference చేయవచ్చు. FreeIPA hostgroups లో పూర్తి సిద్ధమైన Linux guest set కావాలంటే `linux_ipa_clients_runtime` ను reference చేయండి.

> [!IMPORTANT]
> FreeIPA కి ప్రతి guest యొక్క final hostname ఇంకా అవసరమే. మీరు IP-only targets లేదా Proxmox discovery ఉపయోగిస్తే, `ipa_hostname` ను explicit గా ఇవ్వండి లేదా guest లో `hostname -f` final FQDN ను తిరిగి ఇవ్వాలని నిర్ధారించండి. ఇప్పుడు playbooks FreeIPA hostgroup membership నిర్మించే ముందు ఆ hostname ను resolve చేస్తాయి.

> [!TIP]
> మళ్లీ ఉపయోగించే golden template ను FreeIPA లో enroll చేయవద్దు. ముందుగా VM ను clone చేసి, final hostname కేటాయించి, ఆ guest ను enroll చేయండి.

### లినక్స్ గెస్ట్ మూల విధానాలు

`linux_ipa_clients` ను మూడు వేర్వేరు మార్గాల్లో నింపవచ్చు.

#### 1. Static inventory hosts

guest పేర్లు ముందే తెలిసి ఉంటే సాధారణ Ansible inventory entries ఉపయోగించండి:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. వేరియబుల్స్‌లో చేతితో host నిర్వచనలు

guests ను `hosts.yml` బయట ఉంచాలని అనుకుంటే, లేదా మీ వద్ద IP మాత్రమే ఉంటే `linux_ipa_client_hosts` ను ఉపయోగించండి:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

గమనికలు:

- `name` ఒక resolvable hostname లేదా FQDN అయితే `ansible_host` ఐచ్చికం
- మీకు IP మాత్రమే తెలిసి ఉంటే `name` కోసం ఏదైనా స్థిరమైన alias ఉపయోగించండి
- `ipa_hostname` ఇవ్వకపోతే playbook guest లోని `hostname -f` ను fallback గా ఉపయోగిస్తుంది

#### 3. Proxmox VM స్వయంచాలక గుర్తింపు

ఒకటి లేదా అంతకంటే ఎక్కువ Proxmox nodes నుంచి Linux guests ను playbook ద్వారా తీసుకురావాలనుకుంటే discovery ఉపయోగించండి:

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

గమనికలు:

- discovery మిగతా playbooks ఉపయోగించే అదే `linux_ipa_clients_runtime` group లో VMs ను చేర్చుతుంది
- IP discovery అనేది QEMU guest agent network interfaces ను report చేయడంపై ఆధారపడుతుంది
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` ఇప్పటికే FQDN గా ఉన్న VM names ను మాత్రమే నమ్ముతుంది
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` సెట్ చేస్తే, `Teleport-Server-1` వంటి safe short Proxmox VM names ను `linux_ipa_identity_hostname_suffix` ద్వారా `teleport-server-1.example.com` వంటి hostname hints గా ఆటోమేటిక్ గా మార్చవచ్చు
- `linux_ipa_proxmox_discovery_vmids` ఐచ్చికం; event-driven hook/webhook workflow లో discovery ను ఒకటి లేదా అంతకంటే ఎక్కువ ప్రత్యేక VMIDs కు scope చేయడానికి ప్రధానంగా ఉపయోగించబడుతుంది
- guest కు ఇంకా final hostname అవసరం; అది ఇప్పటికే VM లో configured అయి ఉండాలి లేదా manual definition లో `ipa_hostname` ద్వారా అందించాలి
- guest యొక్క నిజమైన system hostname enrollment కు కూడా చెల్లుబాటు అయ్యేదై ఉండాలి; `localhost.localdomain` వంటి placeholder values ను `linux-clients` లేదా `site` run చేసే ముందు VM లో మార్చాలి
- guests `app-server-01` వంటి short hostnames వాడితే, `linux_ipa_identity_hostname_suffix` మరియు ఐచ్చికంగా `linux_freeipa_enroll_manage_hostname: true` ను సెట్ చేసి enrollment ముందు `app-server-01.example.net` వంటి పూర్తి hostname ను resolve చేసి apply చేయవచ్చు
- మీ guest hostnames కు FreeIPA DNS authoritative అయితే, `linux_freeipa_enroll_manage_authoritative_dns: true` ను సెట్ చేసి ప్రత్యేక guest A మరియు PTR records ను సరిచేసి, enrollment ముందు link-local `fe80::/10` AAAA records ను తొలగించవచ్చు
- DNS ఇంకా సిద్ధంగా లేకపోతే, `linux_ipa_manage_etc_hosts: true` మరియు `linux_ipa_etc_hosts_entries` ను అందించి IPA servers మరియు guest FQDNs కోసం managed `/etc/hosts` bootstrap block ను enrollment checks ముందు జోడించవచ్చు
- `guest_qemu_agent_install_enabled` ఇప్పటికే SSH లేదా WinRM ద్వారా చేరుకోగల guestలపై QEMU Guest Agent ను install చేస్తుంది, తర్వాత అదే workflow లో చేరుకోగలిగే Linux guestలపై మళ్లీ ప్రయత్నిస్తుంది, మరియు Linux enrollment తర్వాత మరోసారి ప్రయత్నిస్తుంది
- `linux_ipa_proxmox_discovery_allowlist_enabled: true` సెట్ చేస్తే discovery కొనసాగుతూనే ఉంటుంది కానీ కచ్చితంగా ఆమోదించిన కొంతమంది Proxmox guests మాత్రమే Linux runtime inventory లో చేరతారు; allowlist exact VMIDs, IPs, మరియు names తో match చేయగలదు
- discovery-enabled nodes లో firewalls లేదా DNS servers వంటి infrastructure VMs ఉంటే అవి ఎప్పటికీ Linux IPA automation పొందకూడదు; దాని కోసం `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, లేదా `linux_ipa_proxmox_discovery_blacklist_names` ను ఉపయోగించండి; broad discovery లేదా allowlist ద్వారా admission ఉన్నా blacklist match ఎల్లప్పుడూ గెలుస్తుంది
- ఇప్పటికే పనిచేస్తున్న guest agent లేని Proxmox-discovered Linux guests కోసం, QEMU Guest Agent install చేయడానికి repository కు usable first-touch SSH path అవసరం; అందుకే `linux_ipa_proxmox_discovery_ansible_user` మరియు `linux_ipa_proxmox_discovery_ansible_password` లేదా `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` ను సెట్ చేయాలి
- అటువంటి discovered guests non-root SSH user ను ఉపయోగిస్తే, ఆ account కి ఇప్పటికే passwordless sudo లేకుంటే `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, మరియు `linux_ipa_proxmox_discovery_ansible_become_password` ను కూడా సెట్ చేయాలి
- `guest_qemu_agent_install_manage_proxmox_vm_agent` guest-side install path ప్రారంభమయ్యే ముందు Proxmox-side guest-agent communication (`qm set <vmid> --agent 1`) ను కూడా enable చేస్తుంది
- running VM లో ఆ Proxmox VM option మారితే, host guest-agent channel ఉపయోగించడానికి కొత్త VM start అవసరం కావచ్చు కాబట్టి repository default గా warning మాత్రమే ఇస్తుంది; అలాంటి running VMలను ఆటోమేటిక్ గా reboot చేయాలంటే `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` సెట్ చేయండి
- `linux_ipa_ssh_host_key_policy` default గా `accept_new`; దాని వల్ల కొత్తగా discover చేసిన VMs ను host key checking పూర్తిగా disable చేయకుండా సంప్రదించవచ్చు; కానీ మార్చబడిన host keys ఇంకా fail అవుతాయి మరియు operator review అవసరం
- `linux_ipa_qga_ssh_bootstrap_enabled` అనేది Proxmox-backed guests కోసం preferred no-reboot bootstrap path, ఎందుకంటే SSH login లేకముందే QEMU Guest Agent ద్వారా dedicated key-only automation user ను సృష్టించగలదు
- `linux_ipa_qga_ssh_bootstrap_qm_path` default గా `qm`; bootstrap flow fail అవ్వడానికి ముందు Proxmox node పై సాధారణ fallback paths ను కూడా పరీక్షిస్తుంది
- `guest-ping` ను అనుమతించి `guest-exec` ను తిరస్కరించే guests default గా QGA bootstrap లో skip అవుతాయి; వాటికి మరో SSH path సిద్ధంగా ఉంచండి లేదా వెంటనే fail కావాలంటే `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` సెట్ చేయండి
- `linux_ipa_ssh_bootstrap_enabled` hostname resolution మరియు enrollment ముందు controller SSH public key ను Linux guests పై install చేయడానికి ఐచ్చికంగా సహాయపడుతుంది; key bootstrap disable చేసినప్పటికీ runtime Linux guests కోసం shared first-touch password fallback గా `linux_ipa_ssh_bootstrap_password` కూడా ఉపయోగించబడుతుంది
- FreeIPA JSON-RPC timeout వల్ల fail అయ్యే upstream client joins ను Linux IPA enrollment మళ్లీ ప్రయత్నిస్తుంది; నెమ్మదిగా ఉండే లేదా busy IPA environments కోసం `linux_ipaclient_kinit_attempts` ను expose చేస్తుంది
- Linux IPA enrollment default గా `ipa_servers` inventory hostnames ను join server list లో merge చేస్తుంది, దాంతో clients ఒకే configured endpoint కు పరిమితం కాకుండా పూర్తి IPA server set ను ఉపయోగించగలవు
- ఒకటి కంటే ఎక్కువ IPA servers అందుబాటులో ఉంటే, ప్రతి retry pass లో వాటిని ఒక్కొక్కటిగా ప్రయత్నిస్తుంది
- combined `site` workflow మొదట FreeIPA hostgroups ను సృష్టించి, Linux enrollment తర్వాత enrolled runtime hosts ను చేర్చుతుంది; దాంతో ఇంకా enroll కాలేని guests వల్ల pre-enrollment hostgroup membership fail కాకుండా ఉంటుంది

## కాన్ఫిగరేషన్ పరిధి

చాలా విలువలు ఈ files లో ఉంటాయి:

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

file-by-file layout కోసం [docs/VARIABLES.md](../../docs/VARIABLES.md) చూడండి.

ప్రధాన variable కుటుంబాలు:

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

## గుంపు వ్యూహ ఉదాహరణ

- సులభంగా విస్తరించగల ఒక సరళ నమూనా:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- Sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa` కోసం Proxmox ACL binding

managed `linux-ssh-admins` group ద్వారా combined `site.yml` run సమయంలో ప్రత్యేక IPA users కు Linux SSH మరియు sudo access ఆటోమేటిక్ గా ఇవ్వాలనుకుంటే [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) లో `freeipa_linux_admin_users` ను నింపండి.

Proxmox LDAP sync ఈ suffix తో synced groups ను సృష్టిస్తుందని గుర్తుంచుకోండి:

```text
<group-name>-<realm>
```

మీ FreeIPA group `proxmox-admins` మరియు Proxmox realm `ipa` అయితే, synced PVE group ఇలా మారుతుంది:

```text
proxmox-admins-ipa
```

## భద్రత

- plaintext inventory variable files లో కాకుండా, అన్ని secrets ను `vault-freeipa.yml` మరియు `vault-proxmox.yml` లో నిల్వ చేయండి
- Proxmox కోసం dedicated read-only LDAP bind account ఉపయోగించండి
- certificate verification ఉన్న TLS ను ప్రాధాన్యంగా వాడండి
- disposable lab కాని చోట SSH host key checking ను ఆపవద్దు
- QGA available అయితే shared temporary passwords కంటే `linux_ipa_qga_ssh_bootstrap_enabled` path ను ప్రాధాన్యంగా వాడండి
- `guest_qemu_agent_install_enabled` ను repository కి ఇప్పటికే guest లోకి చెల్లుబాటు అయ్యే management path ఉన్నప్పుడు మాత్రమే ఉపయోగించండి; Proxmox discovery లో అంటే QGA ఇప్పటికే నడుస్తూ ఉండాలి లేదా `linux_ipa_proxmox_discovery_ansible_user` తో password లేదా key access configure అయి ఉండాలి
- Linux SSH bootstrap enable చేస్తే, ఏ shared bootstrap password అయినా vaulted variables లో ఉంచి key-based access ఏర్పడిన తర్వాత దానిని rotate చేయండి లేదా తొలగించండి
- IPA admin account ను Proxmox LDAP bind account గా మళ్లీ ఉపయోగించవద్దు
- production rollout కు ముందు `proxmox_ldap_filter` మరియు `proxmox_ldap_group_filter` ను review చేసి అవసరానికి మించి import కాకుండా చూడండి

SSH host verification ను ఉద్దేశపూర్వకంగా bypass చేయాలనుకునే disposable lab కోసం, repository defaults మార్చకుండా ప్రతి shell session స్థాయిలో మాత్రమే opt out చేయండి:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## ఐడెంపోటెన్సీ మరియు జాగ్రత్తలు

ఈ project ప్రధానంగా idempotent గా రాయబడింది. అయినప్పటికీ production ముందు lab లో validate చేయాలి.

- Proxmox CLI output release ను బట్టి కొద్దిగా మారవచ్చు
- FreeIPA LDAP filters మీ directory tree కు tuning అవసరం కావచ్చు
- existing hand-managed PVE ACLs మరియు roles automation కు ముందు compare చేయాలి
- Proxmox VM auto-discovery running guests మరియు QEMU guest-agent data పై ఆధారపడుతుంది
- IP-only guest definitions కు valid final hostname లేదా explicit `ipa_hostname` అవసరం
- non-root Proxmox SSH user వాడితే working `sudo` తప్పనిసరి; passwordless sudo లేకపోతే `-K` ద్వారా become password ఇవ్వాలి
- `ansible_become_password` ను `vault-proxmox.yml` లో నిల్వ చేస్తే `-K` అవసరం ఉండదు, ఎందుకంటే Ansible encrypted variable నుంచే sudo password ను చదువుతుంది

## ధృవీకరణ

rollout విజయవంతంగా పూర్తయ్యాక, ప్రతి access path సరిగానే ఉందని ఊహించకుండా ఏర్పడిన state ను verify చేయండి.

### FreeIPA లో

- expected user groups ఉన్నాయి అని నిర్ధారించండి
- expected hostgroups ఉన్నాయి అని నిర్ధారించండి
- expected HBAC rules ఉన్నాయి మరియు enable అయ్యాయి అని నిర్ధారించండి
- expected sudo rules ఉన్నాయి మరియు enable అయ్యాయి అని నిర్ధారించండి

### Proxmox లో

- LDAP realm ఉంది అని నిర్ధారించండి
- initial sync expected users లేదా groups ను import చేసిందా అని నిర్ధారించండి
- intended synced group కు ఆశించిన ACL binding ఉందా అని నిర్ధారించండి

### లినక్స్ గెస్ట్ లో

- అనుమతించబడిన IPA user log in చేయగలడా అని నిర్ధారించండి
- అనుమతించని user ను HBAC block చేస్తున్నదా అని నిర్ధారించండి
- అనుమతించబడిన IPA admin `sudo -l` నడపగలడా అని నిర్ధారించండి
- `linux_ipaclient_mkhomedir` enable అయితే first login లో home directory సృష్టించబడిందా అని నిర్ధారించండి

## రిపోజిటరీ నిర్మాణం

<details>
<summary>రిపోజిటరీ నిర్మాణాన్ని చూపించు</summary>

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

## అభివృద్ధి

ఈ repository లో ఉన్న helper files:

- `.editorconfig` వేర్వేరు editors మధ్య whitespace, encoding, మరియు line-ending defaults ను సుసంబద్ధంగా ఉంచుతుంది
- `.gitattributes` సాధారణ text files ను LF line endings పై ఉంచుతుంది
- `.gitignore` generated inventory, vault data, local collections, మరియు editor files Git లోకి వెళ్లకుండా నిరోధిస్తుంది
- `.ansible-lint` vendored collections ను మినహాయించి YAML line-length rule ఒక్కటినే suppress చేస్తుంది
- `.yamllint` playbooks, inventories, మరియు workflow files అంతటా YAML formatting checks ను సుసంబద్ధంగా ఉంచుతుంది
- `.github/CODEOWNERS` ప్రధాన repository ప్రాంతాలకు review ownership ను మార్గనిర్దేశం చేస్తుంది
- `.github/workflows/ci.yml` pushes మరియు pull requests పై repository lint checks మరియు smoke validation ను నడుపుతుంది
- `.pre-commit-config.yaml` `pre-commit` install అయి ఉన్నప్పుడు commits కు ముందు fast lint hook ను నడుపుతుంది
- `CHANGELOG.md` ముఖ్యమైన repository మార్పులను ఒకేచోట నమోదు చేస్తుంది
- `docs/VARIABLES.md` split inventory variable layout ను వివరిస్తుంది
- `docs/i18n/` అనువదించిన README files ను ఉంచుతుంది; `README.md` canonical source గా ఉండగా ఇవి పూర్తి English section structure ను ప్రతిబింబించాలి
- `docs/i18n/TRANSLATION_GUIDE.md` అనువదించిన README files ను sync లో ఎలా ఉంచాలో వివరిస్తుంది
- `scripts/bootstrap.ps1` మరియు `scripts/bootstrap.sh` అవసరమైన collection ను repo-local `collections/` path లో install చేసి, ansible-core 2.24+ compatibility కోసం patch చేస్తాయి
- `scripts/patch_freeipa_collection.py` pinned FreeIPA collection లో deprecated imports ను rewrite చేసి, భవిష్యత్ ansible-core releases తో కూడా compatible గా ఉంచుతుంది
- `scripts/lint.py` local use, CI, మరియు pre-commit కోసం cross-platform lint entrypoint ను అందిస్తుంది
- `scripts/smoke-test.py` example inventory ను validate చేసి, నిజమైన infrastructure ను తాకకుండా syntax checks నడుపుతుంది; వేరే Windows playbook కూడా ఇందులో ఉంటుంది
- `scripts/check_translations.py` canonical English README తో పోల్చి metadata, section-structure parity, మరియు minimum content coverage కోసం translated README files ను audit చేస్తుంది
- `scripts/lint.ps1` మరియు `scripts/lint.sh` కలిపిన local lint మరియు smoke workflow ను నడుపుతాయి
- `scripts/proxmox_event_webhook.py` Proxmox VM events కోసం optional controller-side webhook ను నడుపుతుంది
- `scripts/proxmox-vm-hook.pl` `post-start` మరియు `post-migrate` వద్ద controller webhook కు తెలియజేసే optional Proxmox VM hookscript
- `scripts/run-playbook.ps1` వేరుగా ఉన్న Windows workflow సహా, PowerShell users కోసం సాధారణ `ansible-playbook` commands ను wrap చేస్తుంది
- `scripts/vault.ps1` మరియు `scripts/vault.sh` FreeIPA, Proxmox, మరియు optional Windows secrets కోసం సాధారణ split-vault operations ను wrap చేస్తాయి
- `tests/` repository verification surface ను కలిగి ఉంటుంది; ఇది smoke-test documentation తో ప్రారంభమవుతుంది
- `CONTRIBUTING.md` ఆశించిన contribution మరియు validation workflow ను documents చేస్తుంది
- `SECURITY.md` vulnerabilities ను ఎలా report చేయాలో మరియు security-sensitive సమాచారాన్ని ఎలా handle చేయాలో documents చేస్తుంది

మీ controller పై `ansible-lint` install అయి ఉంటే:

```bash
ansible-lint
```

Repository smoke checks ను నేరుగా నడపడానికి:

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

పూర్తి local lint pass కోసం:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

ప్రతి commit కు ముందు fast lint hook ను enable చేయడానికి:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell wrapper ఉదాహరణలు:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## తదుపరి విస్తరణలు

- IPA-ready Linux templates కోసం Packer pipeline
- AWX job templates మరియు schedules
- వేరు చేసిన Proxmox tenant/pool models
- మరింత విస్తృతమైన Windows local policy లేదా GPO అనుసంధానం

## లైసెన్స్

ఈ ప్రాజెక్ట్ [MIT License](../../LICENSE) కింద విడుదలైంది.
