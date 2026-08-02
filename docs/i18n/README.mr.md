# Proxmox + FreeIPA प्रवेश स्वयंचलन

हे पृष्ठ [README.md](../../README.md) चे पूर्ण, रचनात्मकदृष्ट्या समतुल्य मराठी भाषांतर आहे. इंग्रजी आवृत्ती canonical source राहते, पण ही मराठी आवृत्तीही त्याच operational scope साठी ठेवली आहे.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## भाषा

पूर्ण दस्तऐवजीकरणाचा canonical source म्हणजे इंग्रजी README. आणखी 20 भाषांमध्ये पूर्ण translated README सुद्धा उपलब्ध आहेत.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

ही repository identity आणि access साठी **FreeIPA ला source of truth** मानते. Proxmox LDAP realm मार्फत त्या directory ला consume करतो, Linux guest upstream `ipaclient` role द्वारे FreeIPA मध्ये join होतात, आणि access synced groups, HBAC, आणि sudo rules मार्फत centrally managed राहते; प्रत्येक VM मधल्या local account sprawl द्वारे नाही.

> [!IMPORTANT]
> हा प्रकल्प **FreeRADIUS ला identity source म्हणून वापरत नाही**, **प्रत्येक VM मध्ये local users तयार करत नाही**, आणि **Proxmox permission चे सर्व edge case हाताळण्याचा प्रयत्न करत नाही**.

## हा प्रकल्प का अस्तित्वात आहे

ही repository तेव्हा वापरा जेव्हा तुमच्याकडे आधीपासून खालील गोष्टी आहेत:

- एक निरोगी FreeIPA deployment
- एक Proxmox VE cluster
- centralized authentication लागणारे Linux guest
- Proxmox LDAP bind साठी dedicated service account
- admins आणि operators साठी स्पष्ट group model

मुख्य तत्त्व असे आहे की identity आणि access साठी FreeIPA ला source of truth मानायचे. Proxmox त्याच directory ला LDAP realm म्हणून consume करतो, Linux guest upstream `ipaclient` role च्या माध्यमातून FreeIPA मध्ये join होतात, आणि SSH, HBAC, आणि `sudo` नियंत्रण प्रत्येक VM वरच्या local account मध्ये विखुरले जाण्याऐवजी centrally managed राहते.

तुम्हाला onboarding आणि offboarding साधारणपणे पुढील क्रमाने चालवायचे असल्यास ही repository योग्य ठरते:

1. FreeIPA मध्ये users आणि groups तयार करणे किंवा update करणे
2. त्या identity ना Proxmox मध्ये sync करणे
3. synced groups मधून Proxmox roles आणि ACL लागू करणे
4. FreeIPA login, HBAC, आणि `sudo` rules द्वारे Linux guest access देणे

## तुम्हाला काय मिळते

- FreeIPA user groups, hostgroups, HBAC rules, आणि `sudo` rules चे व्यवस्थापन
- Linux administrators साठी FreeIPA default login shell चे व्यवस्थापन
- FreeIPA कडे निर्देश करणारे Proxmox LDAP realm configuration
- एका निश्चित cluster node वरून periodic Proxmox realm sync
- synced directory groups साठी Proxmox RBAC bindings
- static inventory, IP-based targets, किंवा Proxmox VM discovery द्वारे Linux guest चे FreeIPA enrollment
- Proxmox QEMU Guest Agent मार्फत reboot शिवाय optional SSH bootstrap
- Proxmox-managed Linux guest साठी Proxmox side वर guest agent communication channel enable करण्याची optional क्षमता
- अशा guest वर SSH किंवा WinRM मार्फत optional QEMU Guest Agent installation जे आधीच reachable आहेत, bootstrap नंतर reachable होतात, किंवा Linux enrollment नंतर पुन्हा retry करता येतात
- SSH reachability आणि Proxmox QEMU Guest Agent status तपासण्यासाठी optional Linux readiness report
- Active Directory आधारित Windows 10/11 आणि Windows Server domain membership साठी वेगळा optional workflow
- IPA CA trust, hosts file bootstrap, आणि IPA service reachability validation पुरता मर्यादित FreeIPA-aware Windows helper workflow
- Linux guest साठी first-touch SSH public-key bootstrap
- FreeIPA access model बदलल्यानंतर managed Linux clients वर automatic SSSD cache refresh
- Proxmox VM hook आणि webhook trigger मार्फत optional event-driven Linux onboarding

## व्याप्ती

| समाविष्ट | समाविष्ट नाही |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm configuration | FreeIPA user lifecycle चे संपूर्ण निर्माण |
| synced groups मधून Proxmox RBAC | Proxmox multi-tenant edge case ची पूर्ण कव्हरेज |
| Linux client IPA enrollment | FreeIPA विरुद्ध Windows native login |
| Windows साठी AD domain membership workflow | AD object किंवा GPO चे व्यापक automation |
| Windows साठी मर्यादित FreeIPA helper workflow | FreeIPA-based Windows helper ला AD च्या बरोबरीचे समजणे |

## विंडोज कार्यप्रवाह

Windows support ला Linux IPA enrollment flow मध्ये मिसळलेले नाही. ते स्वतंत्र workflow म्हणून implement केले आहे.

- `windows_qemu_guest_agent_clients` हे फक्त optional QEMU Guest Agent helper task साठी राखीव आहे.
- `10-features.yml` मध्ये `windows_domain_membership_enabled: true` सेट केल्याने Windows workflow सक्षम होते.
- `windows_management_clients` हा स्वतंत्र Windows group आहे, जो `playbooks/windows-management.yml` आणि `playbooks/site.yml` मधील optional Windows टप्पे वापरतात.
- वास्तविक Windows login हे Active Directory domain membership द्वारे हाताळले जाते. FreeIPA-केंद्रित environment मध्ये Windows hosts ला थेट FreeIPA मध्ये join करण्याऐवजी FreeIPA-AD trust च्या AD side मध्ये join करणे योग्य आहे.

फक्त FreeIPA वर आधारित Windows join या repository च्या support मध्ये नाही. Active Directory किंवा FreeIPA-AD trust नसल्यास Windows side चा scope फक्त helper task पर्यंत मर्यादित राहतो, जसे already reachable guests चे management आणि optional QEMU Guest Agent installation.

तरीही जर तुम्हाला domain join शिवाय मर्यादित FreeIPA-aware Windows path हवी असेल, तर `windows_freeipa_helpers_enabled: true` सक्षम करा आणि `playbooks/windows-freeipa-helpers.yml` सोबत `windows_freeipa_helper_clients` वापरा. हा helper workflow IPA CA trust install करू शकतो, bootstrap साठी IPA CA आपोआप fetch करू शकतो, expected CA thumbprint optionally pin करू शकतो, hosts file entries optionally manage करू शकतो, IPA DNS आणि महत्त्वाचे TCP ports validate करू शकतो, Windows मधून HTTPS reachability validate करू शकतो, IPA-संबंधित endpoints विरुद्ध Windows time source validate करू शकतो, Windows local group membership manage करू शकतो, आणि OpenSSH Server optionally install किंवा expose करू शकतो, पण तो FreeIPA विरुद्ध Windows native login देत नाही.

जर तुम्हाला त्याच helper group वर कोणतेही बदल न करता फक्त readiness check चालवायची असेल, तर `playbooks/windows-freeipa-validate.yml` चालवा. हा workflow validation आणि summary path कायम ठेवतो, पण त्या run साठी CA import, hosts file changes, local group changes, आणि OpenSSH management non-mutating बनवतो.

हा workflow WinRM किंवा PSRP मार्फत reachable Windows 10/11 आणि Windows Server guest ला target करतो.

## आर्किटेक्चर

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

अधिक सविस्तर design explanation [docs/ARCHITECTURE.md](../ARCHITECTURE.md) मध्ये आहे.

## आवश्यकता

### कंट्रोलर

- Ansible Core 2.14 किंवा नवीन
- Proxmox primary nodes, IPA servers, आणि Linux clients पर्यंत SSH reachability
- तुम्ही Windows workflow वापरत असाल तर Windows guest पर्यंत WinRM किंवा PSRP reachability
- गरजेनुसार `sudo` किंवा `root`
- QGA SSH bootstrap enabled असल्यास guest च्या आत QEMU Guest Agent आधीपासून चालू असणे आवश्यक
- Windows साठी guest-agent installation fallback enabled असल्यास reachable Windows hosts `windows_qemu_guest_agent_clients` मध्ये असणे आवश्यक
- Windows domain membership enabled असल्यास reachable Windows hosts `windows_management_clients` मध्ये असणे आवश्यक आणि AD join credentials द्यावी लागतात
- Windows साठी FreeIPA helper task enabled असल्यास reachable Windows hosts `windows_freeipa_helper_clients` मध्ये असणे आवश्यक
- Linux SSH bootstrap enabled असल्यास controller कडे SSH keypair आणि guest account साठी initial password-based login path असणे आवश्यक

### लक्ष्ये

- `proxmox_primary` मध्ये Proxmox VE 6.x किंवा त्यापेक्षा नवीन
- Proxmox आणि Linux clients मधून reachable FreeIPA
- Windows 10/11 आणि Windows Server guest हे WinRM किंवा PSRP द्वारे reachable असतील तर वेगळ्या Windows workflow मधून manage करता येतात
- योग्य DNS आणि time synchronization
- `proxmox_primary` साठी `root` किंवा `pveversion`, `pvesh`, आणि `pveum` साठी `sudo` असलेला SSH user
- तुम्ही Windows domain membership वापरत असाल तर target Windows guests संबंधित AD domain controllers पर्यंत पोहोचू शकले पाहिजेत
- तुम्ही Windows साठी मर्यादित FreeIPA helper workflow वापरत असाल तर target Windows guests संबंधित IPA servers पर्यंत पोहोचू शकले पाहिजेत
- तुम्ही Proxmox discovery वापरत असाल तर guests नी QEMU Guest Agent मार्फत usable IP expose करायला हव्यात

## नेटवर्क पोर्ट

ही तालिका त्या network ports ची यादी देते जी या repository चा controller, Proxmox LDAP automation, आणि Linux IPA enrollment flow वापरतात.
ही जाणूनबुजून केवळ त्या surface पुरती मर्यादित आहे जी हा project प्रत्यक्ष वापरतो; ती FreeIPA server-to-server replication matrix ची पूर्ण सूची नाही.

| नाव | पोर्ट | प्रोटोकॉल | स्रोत | गंतव्य | केव्हा आवश्यक | उद्देश |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | नेहमी | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | Windows management enabled असताना | Windows guest पर्यंत Ansible connectivity |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS server | Linux guest IPA DNS वापरत असताना | IPA records आणि external names resolve करणे |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment आणि login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA server | Linux IPA enrollment आणि login | LDAP आणि FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port`, default `443` | `TCP` | Linux guest | IPA server | Linux IPA enrollment | client installation दरम्यान IPA web/API verification |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment आणि password operations | Kerberos password आणि keytab operations |
| LDAPS | `636` | `TCP` | Primary Proxmox node | IPA किंवा LDAP server | Proxmox LDAP realm default `ldaps` mode वापरत असताना | Proxmox LDAP realm connection |

नोट्स:

- `LDAPS 636/TCP` हे repository default आहे कारण `proxmox_ldap_mode` चे default `ldaps` आहे. तुम्ही LDAP mode किंवा port बदलल्यास, तुम्ही प्रत्यक्ष वापरत असलेला `proxmox_ldap_port` allow करा.
- `WinRM` सहसा HTTPS साठी `5986/TCP` किंवा HTTP साठी `5985/TCP` वापरतो; हे तुमच्या Windows transport configuration वर अवलंबून असते.
- `DNS 53/TCP,UDP` फक्त तेव्हाच आवश्यक असते जेव्हा Linux guest IPA servers ला resolvers म्हणून वापरतात.
- `Kerberos 88` आणि `Kerberos Password 464` दोन्हींना `TCP` आणि `UDP` दोन्ही लागतात.
- Active Directory domain join साठी standard Windows-to-domain-controller ports देखील आवश्यक असतात, परंतु त्या environment-specific असल्याने येथे सविस्तर सूची दिलेली नाही.
- Kerberos विश्वासार्हपणे काम करण्यासाठी time synchronization आवश्यक आहे, पण NTP source environment-specific आहे आणि ही repository ते manage करत नाही.

## सुसंगतता

या repository मधील Proxmox automation `pveum` आणि `pvesh` interface भोवती लिहिलेले आहे, जे Proxmox VE 6.x आणि नंतरच्या versions मध्ये realm आणि RBAC साठी वापरले जातात.

- default supported majors: `6`, `7`, `8`, `9`, `10`
- validation `pveversion` द्वारे detected Proxmox version तपासते
- supported version list `proxmox_supported_major_versions` द्वारे तुमच्या environment नुसार कमी किंवा जास्त करता येते
- `proxmox_allow_future_major_versions` चे default `true` आहे, त्यामुळे highest tested version पेक्षा वरच्या major versions ही default ने validation पार करतात
- future major versions ना compatibility candidates म्हणूनच पाहिले पाहिजे जोपर्यंत त्यांच्या published Proxmox interfaces या automation सोबत प्रत्यक्ष validate होत नाहीत
- `1` ते `5` सारख्या जुन्या versions ना ही public repository tested support म्हणून घोषित करत नाही; तुम्ही त्यांना locally जोडत असाल तर त्याला explicit compatibility override माना आणि आधी lab मध्ये full workflow validate करा

legacy lab साठी local override उदाहरण:

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

## जलद प्रारंभ

खालील उदाहरणे shell commands वापरतात. जिथे योग्य आहे तिथे PowerShell equivalents देखील दिले आहेत.

### 1. उदाहरण इन्व्हेंटरी आणि वॉल्ट टेम्पलेट्स कॉपी करा

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Optional if you plan to manage Windows guests:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Optional if you plan to manage Windows guests:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. वातावरण-विशिष्ट फाइल्स संपादित करा

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- तुम्ही Windows management वापरत असाल तर `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- तुम्ही Windows management वापरत असाल तर `inventories/production/group_vars/all/vault-windows.yml`

IPA आणि Proxmox settings व्यतिरिक्त, Linux guest साठी एक source mode निवडा:

- `linux_ipa_clients` अंतर्गत static inventory entries
- `group_vars/all/30-linux-clients.yml` मधील `linux_ipa_client_hosts` entries
- `linux_ipa_proxmox_discovery_enabled: true` सह Proxmox VM discovery

Linux IPA enrollment साठी domain values आणि server lists यातील फरक समजून घ्या:

- `ipaclient_domain` हा shared IPA DNS domain आहे, उदाहरण `example.com`
- `linux_ipa_servers` ही IPA server hostnames ची यादी आहे, उदाहरण `ipa01.example.com`

जर तुम्हाला `root` ऐवजी `sudo` असलेल्या सामान्य user ने Proxmox वर SSH करायचे असेल, तर ते `hosts.yml` मधील `proxmox_primary` मध्ये सेट करा आणि sudo password `vault-proxmox.yml` मध्ये ठेवा:

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

या configuration मध्ये `vault_proxmox_become_password` म्हणजे Proxmox host वर `sudo` चालवताना तुम्ही नेहमी देत असलेला password.

### 3. वॉल्ट फाइल्स एन्क्रिप्ट करा

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

तुम्ही Windows workflow enable करत असाल तर त्याच command मध्ये `inventories/production/group_vars/all/vault-windows.yml` देखील जोडा.

वैकल्पिकरित्या helper wrapper वापरा, जी default ने domain-separated vault IDs वापरते आणि गरज पडल्यास example templates मधून working vault files तयार करते:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

जर तुम्हाला playbook runs साठी domain-specific passwords हवे असतील, तर `--ask-vault-pass` ऐवजी vault IDs वापरा:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

जर optional Windows workflow देखील वेगळा vault password वापरत असेल, तर त्याच command मध्ये `windows@prompt` जोडा.

`-AskVaultPass` फक्त तेव्हाच वापरा जेव्हा त्या playbook ने वापरलेल्या सर्व vault files एकच password share करतात.

### 4. आवश्यक कलेक्शन इंस्टॉल करा

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

किंवा थेट:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

या repository ने compatibility patch जोडण्यापूर्वी जर तुम्ही `freeipa.ansible_freeipa` install केले असेल, तर bootstrap helper पुन्हा चालवा किंवा `python .\scripts\patch_freeipa_collection.py` एकदा चालवा, जेणेकरून user-level collection installation देखील patch होईल.

तुम्ही `scripts/run-playbook.ps1` वापरत असाल, तर ते `ansible-playbook` चालवण्यापूर्वी हा patch helper आपोआप चालवते.

### 5. आधी पडताळणी चालवा

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

जर तुम्हाला कोणताही बदल न करता फक्त Windows FreeIPA helper-only path validate करायची असेल:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

जर तुम्हाला असा read-only Linux readiness audit हवा असेल जो दाखवेल की कोणते runtime guest SSH ने reachable आहेत आणि कोणते Proxmox-discovered guest QEMU Guest Agent मार्फत respond करत आहेत:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

readiness report default ने `.ansible/linux-readiness-report.json` मध्ये लिहिला जातो.
मुख्य field चे अर्थ पुढीलप्रमाणे:

- `ssh.ready=true`: सध्याचा Ansible SSH path controller वरून यशस्वी आहे
- `ssh.promptless=true`: `ansible_password` शिवाय SSH probe यशस्वी झाला, म्हणजे हा path Ansible साठी non-interactive आहे
- `ssh.auth_mode=password_configured`: probe ने `sshpass` वापरले कारण host वर `ansible_password` configured आहे
- `ssh.auth_mode=key_or_agent`: probe `ansible_password` शिवाय SSH batch mode मध्ये यशस्वी झाला
- `qga.status=available`: त्या VM च्या मालक Proxmox node वर `qm guest ping` यशस्वी झाला
- `qga.status=disabled`: Proxmox VM configuration मध्ये QEMU Guest Agent enabled नाही
- `qga.status=configured_unresponsive`: guest agent Proxmox configuration मध्ये enabled आहे पण respond करत नाही
- `qga.status=node_unreachable`: controller संबंधित Proxmox node पर्यंत पोहोचू शकला नाही, म्हणून probe होऊ शकला नाही
- `qga.status=not_applicable`: host Proxmox discovery मधून आलेला नाही, त्यामुळे QGA probe चा प्रयत्नच झाला नाही

द्रुत inspection उदाहरण:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. ऐच्छिक: नियोजित बदलांचे पूर्वावलोकन पाहा

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> check mode ला पूर्ण simulation म्हणून नव्हे, तर partial preview म्हणून पहा. ही repository काही Proxmox configuration साठी direct CLI command वापरते आणि Linux enrollment साठी upstream FreeIPA client role वापरते, त्यामुळे `--check` उपयोगी आहे, पण अंतिम authority नाही.
>
> FreeIPA HBAC rule साठी check mode rule definition step validate करते, पण नंतरचे enable किंवा disable action skip करते. त्यामुळे dry run दरम्यान प्रत्यक्ष न बनलेल्या rule बद्दल FreeIPA false failure देत नाही.
>
> Proxmox realm sync timer role सुद्धा check mode मध्ये शेवटचे `systemd` enable किंवा start step skip करते, कारण unit files diff मध्ये दिसतात पण dry run दरम्यान प्रत्यक्ष लिहिल्या जात नाहीत.
>
> Linux IPA enrollment देखील check mode मध्ये skip होते. repository discovery, hostname resolution, आणि input validation चालू ठेवते, पण upstream `ipaclient` role dry run दरम्यान execute होत नाही.

### 7. पूर्ण कॉन्फिगरेशन लागू करा

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

जर optional Windows workflow enabled असेल आणि `vault-windows.yml` वेगळा password वापरत असेल, तर तोच playbook `--ask-vault-pass` ऐवजी `--vault-id windows@prompt` किंवा PowerShell wrapper मधील `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` सह चालवा.

## रोलआउट क्रम

पहिल्या deployment साठी stack या क्रमाने apply करा:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Optional if you manage Windows guests:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Optional if you want the limited Windows FreeIPA helper workflow:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Optional if you only want validation coverage for that helper workflow:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

हा क्रम troubleshooting खूप सोपे करतो, सर्व काही एकाच वेळी चालवण्यापेक्षा.

उदाहरणार्थ, फक्त एका Linux guest साठी मर्यादित PowerShell rollout:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

default rollout controls मुद्दाम conservative आहेत:

- FreeIPA access changes `serial: 1` ने चालतात
- Proxmox changes `serial: 1` ने चालतात
- hostname resolution, validation, आणि Linux enrollment `serial: 10` ने चालतात
- Windows management changes `serial: 10` ने चालतात
- सर्व rollout path default ने `max_fail_percentage: 0` वापरतात

या values `inventories/production/group_vars/all/15-rollout.yml` मध्ये समायोजित करा.

## टॅग मॉडेल

नवीन playbook सतत वाढवत बसण्यापेक्षा stable rollout slice target करण्यासाठी tags वापरा.

- core domain: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helper: `windows`, `windows_freeipa`
- FreeIPA access model: `freeipa_access`
- Proxmox subsets: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- event-driven VM handling: `event`, `linux_refresh`

उदाहरण:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## इव्हेंट-चालित VM ऑनबोर्डिंग

जर तुम्हाला Proxmox ने VM start झाल्यावर किंवा migration नंतर त्वरित Linux discovery आणि IPA enrollment trigger करावी असे वाटत असेल, तर [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) मध्ये वर्णन केलेला optional hook आणि webhook path वापरा.

हा path event-specific playbook `playbooks/proxmox-vm-event.yml` वापरतो, त्यामुळे trigger फक्त Linux guest side आणि FreeIPA side हाताळतो. तो प्रत्येक VM event वर Proxmox LDAP realm automation किंवा RBAC पुन्हा चालवत नाही.

आता ही repository optional hook आणि webhook stack स्वतः `site.yml` किंवा `proxmox.yml` मधून install करू शकते, जर `proxmox_vm_event_onboarding_enabled: true` सेट केलेले असेल आणि आवश्यक webhook variables उपलब्ध असतील.

Proxmox VM hook स्वतंत्र `create` phase देत नाही. प्रत्यक्षात नवीन VM साधारणपणे पहिल्या `post-start` event वर पकडला जातो, आणि migration hook source node आणि destination node दोन्ही ठिकाणी trigger होऊ शकतो.

## इन्व्हेंटरी मॉडेल

ही repository सहा defined inventory group आणि एक runtime-generated group वापरते:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

तुम्ही स्वतःचे additional inventory group देखील define करू शकता आणि FreeIPA hostgroup definition मध्ये त्यांना reference करू शकता. FreeIPA hostgroup side वरून संपूर्ण prepared Linux guest set वापरायचा असेल तर `linux_ipa_clients_runtime` group reference करा.

> [!IMPORTANT]
> FreeIPA ला प्रत्येक guest साठी final hostname आवश्यक असतो. तुम्ही IP-only target किंवा Proxmox discovery वापरत असाल तर `ipa_hostname` explicitly द्या किंवा guest मधील `hostname -f` final FQDN देतो याची खात्री करा. playbook FreeIPA hostgroup membership तयार करण्यापूर्वी तो hostname resolve करते.

> [!TIP]
> reusable golden templates थेट FreeIPA मध्ये enroll करू नका. आधी VM clone करा, final hostname द्या, आणि मग resulting guest enroll करा.

### लिनक्स गेस्ट स्रोत मोड

तुम्ही `linux_ipa_clients` तीन वेगवेगळ्या पद्धतींनी populate करू शकता.

#### 1. static inventory hosts

जर तुम्हाला guest names आधीच माहित असतील, तर सामान्य Ansible inventory entries वापरा:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. variables मध्ये manual host definitions

जर तुम्हाला guest `hosts.yml` च्या बाहेर ठेवायचे असतील, किंवा तुमच्याकडे फक्त IPs असतील, तर `linux_ipa_client_hosts` वापरा:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

नोट्स:

- `name` आधीच resolvable hostname किंवा FQDN असल्यास `ansible_host` optional आहे
- तुमच्याकडे फक्त IP असल्यास, `name` साठी कोणताही स्थिर alias वापरा
- `ipa_hostname` दिले नसल्यास playbook guest च्या आतल्या `hostname -f` वर fallback करते

#### 3. Proxmox VM auto-discovery

जर तुम्हाला एक किंवा अधिक Proxmox node मधून Linux guest pull करायचे असतील, तर discovery वापरा:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Optional: limit discovery-based automation to explicitly approved guests.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Optional: always exclude infrastructure or sensitive guests even when
# broader node discovery is enabled.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# Optional first-touch SSH settings for discovered guests when the guest
# agent is not running yet and the repository needs to SSH in to install it.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

नोट्स:

- discovery VMs ना त्याच `linux_ipa_clients_runtime` group मध्ये जोडते, जी इतर playbook देखील वापरतात
- IP discovery अशा QEMU guest agent वर अवलंबून असते जी network interface report करू शकते
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` फक्त आधीपासून FQDN असलेल्या VM name वर विश्वास ठेवते
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` सेट केल्यावर `Teleport-Server-1` सारख्या सुरक्षित short VM name ला `linux_ipa_identity_hostname_suffix` वापरून `teleport-server-1.example.com` सारख्या hostname hint मध्ये promote करता येते
- `linux_ipa_proxmox_discovery_vmids` optional आहे आणि मुख्यतः event-driven hook किंवा webhook workflow मध्ये discovery विशिष्ट VMID पर्यंत मर्यादित करण्यासाठी उपयोगी आहे
- guest ना अजूनही final hostname लागतो, जो VM मध्ये configured असेल किंवा manual definition मध्ये `ipa_hostname` म्हणून दिलेला असेल
- guest चा actual system hostname enrollment साठी valid असला पाहिजे; `localhost.localdomain` सारखी placeholder values `linux-clients` किंवा `site` चालवण्यापूर्वी VM च्या आत बदलली पाहिजेत
- guest `app-server-01` सारखा short hostname वापरत असल्यास, `linux_ipa_identity_hostname_suffix` आणि आवश्यक असल्यास `linux_freeipa_enroll_manage_hostname: true` सेट करून project ला enrollment आधी `app-server-01.example.net` सारखा full hostname resolve आणि apply करू देता येते
- FreeIPA DNS तुमच्या guest hostname साठी authoritative असल्यास, `linux_freeipa_enroll_manage_authoritative_dns: true` सेट करून project संबंधित A आणि PTR records दुरुस्त करू शकते आणि enrollment आधी link-local `fe80::/10` AAAA records काढू शकते
- DNS अजून तयार नसेल, तर `linux_ipa_manage_etc_hosts: true` आणि `linux_ipa_etc_hosts_entries` सेट करून role ला IPA server आणि guest FQDN साठी managed `/etc/hosts` bootstrap block जोडू देता येते
- `guest_qemu_agent_install_enabled` SSH किंवा WinRM ने आधीपासून reachable guest वर QEMU Guest Agent install करते, त्याच workflow मध्ये नंतर reachable होणाऱ्या Linux guest वर पुन्हा प्रयत्न करते, आणि Linux enrollment नंतरही retry करते, जेणेकरून agent-dependent Proxmox workflow ते वापरू शकतील
- `linux_ipa_proxmox_discovery_allowlist_enabled: true` सेट केल्यावर discovery सुरू राहते, पण फक्त explicitly approved Proxmox guest Linux runtime inventory मध्ये admit होतात; allowlist VMID, IP, आणि names वर exact matching करू शकते
- `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, किंवा `linux_ipa_proxmox_discovery_blacklist_names` सेट करा जर discovery-enabled node वर firewall, DNS server, किंवा इतर infrastructure VMs असतील ज्यांना Linux IPA automation पासून नेहमी वगळले पाहिजे; blacklist matching broad discovery आणि allowlist admission या दोहोंपेक्षा precedence घेते
- ज्या Proxmox-discovered Linux guest मध्ये functional guest agent अद्याप उपलब्ध नाही, त्यांच्यासाठी `linux_ipa_proxmox_discovery_ansible_user` आणि सोबत `linux_ipa_proxmox_discovery_ansible_password` किंवा `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` सेट करा, जेणेकरून repository ला QEMU Guest Agent install करण्यासाठी usable first-touch SSH path मिळेल
- जर असा discovered guest non-root SSH user वापरत असेल, तर `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, आणि `linux_ipa_proxmox_discovery_ansible_become_password` देखील सेट करा, जोपर्यंत त्या account कडे आधीपासून passwordless `sudo` नाही
- `guest_qemu_agent_install_manage_proxmox_vm_agent` Proxmox side वर guest agent communication (`qm set <vmid> --agent 1`) enable करते, त्यानंतर guest च्या आत installation path सुरू होते
- जेव्हा हा Proxmox VM option चालू VM वर बदलला जातो, तेव्हा repository default ने फक्त warning देते, कारण guest agent channel usable होण्यापूर्वी Proxmox ला VM restart लागू शकतो; जर repository ने असे चालू VM आपोआप reboot करावेत असे वाटत असेल, तर `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` सेट करा
- `linux_ipa_ssh_host_key_policy` default ने Linux guest connection साठी `accept_new` वापरते, त्यामुळे newly discovered VM पर्यंत host key checking पूर्णपणे disable न करता पोहोचता येते; बदललेले host keys तरीही fail होतील आणि operator review मागतील
- `linux_ipa_qga_ssh_bootstrap_enabled` हा Proxmox-based guest साठी preferred no-reboot bootstrap path आहे, कारण तो सामान्य SSH login आधी QEMU Guest Agent च्या मदतीने dedicated key-only automation user तयार करू शकतो
- `linux_ipa_qga_ssh_bootstrap_qm_path` चे default `qm` आहे, आणि bootstrap flow fail होण्यापूर्वी Proxmox node वरील common fallback path देखील तपासते
- जे guest `guest-ping` allow करतात पण `guest-exec` block करतात, त्यांना default ने QGA bootstrap दरम्यान skip केले जाते; अशांसाठी दुसरा SSH path द्या किंवा `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` सेट करून run त्वरित fail होऊ द्या
- `linux_ipa_ssh_bootstrap_enabled` hostname resolution आणि enrollment आधी controller ची public key Linux guest वर optionally install करते; `linux_ipa_ssh_bootstrap_password` shared first-touch password fallback म्हणून देखील वापरली जाते, जरी key-based bootstrap disabled असला तरी
- Linux IPA enrollment FreeIPA JSON-RPC timeout मुळे fail झालेल्या upstream client join वर retry करते, आणि धीम्या किंवा busy IPA environment साठी `linux_ipaclient_kinit_attempts` expose करते
- Linux IPA enrollment default ने inventory `ipa_servers` hostnames देखील join server list मध्ये merge करते, जेणेकरून client single endpoint ऐवजी संपूर्ण IPA server set वापरू शकेल
- जेव्हा एकापेक्षा अधिक IPA servers उपलब्ध असतात, तेव्हा प्रत्येक retry round enrollment दरम्यान त्या candidate IPA server ना क्रमाने प्रयत्न करते
- combined `site` workflow आधी FreeIPA hostgroup तयार करते, आणि त्यानंतर enrolled runtime hosts जोडते, त्यामुळे pre-enrollment run केवळ guest अजून enrolled नसल्यामुळे hostgroup membership step वर fail होत नाही

## कॉन्फिगरेशन परिघ

बहुतेक values खालील ठिकाणी आढळतात:

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

प्रत्येक file नुसार layout साठी [docs/VARIABLES.md](../VARIABLES.md) पहा.

मुख्य variable family:

| क्षेत्र | Variables |
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

## गट धोरणाचे उदाहरण

एक साधा पण चांगला scale होणारा pattern:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa` साठी Proxmox ACL binding

जर तुम्हाला combined `site.yml` run ने काही IPA users ना automatically Linux SSH आणि sudo access द्यावी असे वाटत असेल, तर [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) मधील `freeipa_linux_admin_users` भरा, जेणेकरून managed `linux-ssh-admins` group मार्फत access दिली जाईल.

हे लक्षात ठेवा की Proxmox LDAP sync suffix सहित group तयार करते:

```text
<group-name>-<realm>
```

जर तुमचा FreeIPA group `proxmox-admins` असेल आणि Proxmox realm `ipa` असेल, तर resulting synced PVE group असा असेल:

```text
proxmox-admins-ipa
```

## सुरक्षा

- सर्व secrets plaintext inventory variable file ऐवजी `vault-freeipa.yml` आणि `vault-proxmox.yml` मध्ये ठेवा
- Proxmox साठी dedicated read-only LDAP bind account ला प्राधान्य द्या
- certificate verification enabled ठेवून TLS ला प्राधान्य द्या
- temporary lab वगळता SSH host key checking सुरू ठेवा
- तुमच्या Proxmox guest मध्ये QEMU Guest Agent आधीपासून functional असेल, तर shared temporary password पेक्षा `linux_ipa_qga_ssh_bootstrap_enabled` ला प्राधान्य द्या
- `guest_qemu_agent_install_enabled` फक्त तेव्हाच वापरा जेव्हा repository कडे guest च्या आत जाण्यासाठी valid management path आधीपासून असेल; Proxmox discovery साठी याचा अर्थ QGA आधीपासून चालू असेल किंवा `linux_ipa_proxmox_discovery_ansible_user` आणि password किंवा key access configured असेल
- तुम्ही Linux SSH bootstrap enable करत असाल, तर shared bootstrap password encrypted variable मध्ये ठेवा आणि key-based access स्थापन झाल्यावर ती rotate किंवा remove करा
- IPA admin account ला Proxmox LDAP bind account म्हणून reuse करू नका
- production rollout आधी `proxmox_ldap_filter` आणि `proxmox_ldap_group_filter` पुनरावलोकन करा, जेणेकरून जास्त object import होणार नाहीत

जर तुम्हाला disposable lab मध्ये जाणूनबुजून SSH host key verification disable करायची असेल, तर repository defaults बदलण्याऐवजी shell session level वर opt-out करा:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## आइडेम्पोटेंसी आणि सावधगिरी

ही repository पुन्हा पुन्हा चालवता येण्याजोगी लिहिली आहे आणि बहुतांश भाग idempotent आहेत, पण production rollout आधी lab मध्ये validate करणे आवश्यक आहे.

ज्ञात caveat:

- Proxmox CLI output release नुसार थोडे बदलू शकते
- FreeIPA directory layout flexible असल्याने LDAP filters तुमच्या tree नुसार tune करावे लागू शकतात
- आधीपासून manually managed PVE ACL आणि role यांची तुलना automation लागू करण्यापूर्वी करणे योग्य
- Proxmox VM auto-discovery ही running guest आणि QEMU guest agent network data वर अवलंबून असते
- IP-based guest definition ला देखील guest च्या आत valid final hostname किंवा explicit `ipa_hostname` आवश्यक असते
- Proxmox play privilege escalation सह चालतात, त्यामुळे non-root SSH users कडे working `sudo` असावे, आणि जर त्या account कडे passwordless `sudo` नसेल तर `-K` सह become password द्यावी लागते
- तुम्ही `ansible_become_password` `vault-proxmox.yml` मध्ये ठेवले असल्यास `-K` वगळता येते, कारण Ansible encrypted variable मधून sudo password वाचू शकते

## पडताळणी

rollout यशस्वी झाल्यानंतर final state verify करा; सर्व access path आपोआप बरोबर झाले असे गृहित धरू नका.

### FreeIPA मध्ये

- expected user groups अस्तित्वात आहेत याची खात्री करा
- expected hostgroups अस्तित्वात आहेत याची खात्री करा
- expected HBAC rules अस्तित्वात आणि enabled आहेत याची खात्री करा
- expected `sudo` rules अस्तित्वात आणि enabled आहेत याची खात्री करा

### Proxmox मध्ये

- LDAP realm अस्तित्वात आहे याची खात्री करा
- initial sync ने expected users किंवा groups import केले आहेत याची खात्री करा
- target synced groups वर expected ACL bindings आहेत याची खात्री करा

### लिनक्स गेस्ट वर

- allowed IPA users login करू शकतात याची खात्री करा
- disallowed users ना HBAC block करते याची खात्री करा
- allowed IPA admin `sudo -l` चालवू शकतात याची खात्री करा
- `linux_ipaclient_mkhomedir` enabled असल्यास पहिल्या login वेळी home directory तयार होते याची खात्री करा

## रिपॉझिटरी रचना

<details>
<summary>Repository layout दाखवा</summary>

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
    ├── check_translations.py
    └── bootstrap.sh
```

</details>

## विकास

या repository मध्ये समाविष्ट मुख्य helper files:

- `.editorconfig`, जेणेकरून editor दरम्यान spaces, encoding, आणि line ending चे defaults consistent राहतील
- `.gitattributes`, जेणेकरून common text file वर `LF` line ending enforce करता येतील
- `.gitignore`, जेणेकरून generated inventory, vault data, local collections, आणि editor junk Git मध्ये जाऊ नये
- `.ansible-lint`, जेणेकरून vendor collection path exclude करता येतील आणि फक्त YAML line-length rule suppress करता येईल
- `.yamllint`, जेणेकरून playbook, inventory, आणि workflow भर YAML validation consistent राहील
- `.github/CODEOWNERS`, जेणेकरून repository च्या मुख्य भागांवर review ownership स्पष्ट राहील
- `.github/workflows/ci.yml`, जेणेकरून push आणि pull request event वर lint आणि smoke validation चालवता येईल
- `.pre-commit-config.yaml`, जेणेकरून `pre-commit` install असल्यास commit आधी fast lint hooks चालवता येतील
- `CHANGELOG.md`, जेणेकरून महत्त्वाचे repository change एका ठिकाणी track करता येतील
- `docs/VARIABLES.md`, जेणेकरून split inventory variable structure समजावता येईल
- `docs/i18n/`, जिथे translated README ठेवले जातात; या file मध्ये इंग्रजी `README.md` ची पूर्ण section structure reflect झाली पाहिजे
- `docs/i18n/TRANSLATION_GUIDE.md`, जेणेकरून translated README sync मध्ये ठेवण्याची पद्धत समजावता येईल
- `scripts/bootstrap.ps1` आणि `scripts/bootstrap.sh`, जेणेकरून आवश्यक collection local `collections/` path वर install करता येतील आणि ansible-core 2.24+ compatibility patch लागू करता येईल
- `scripts/patch_freeipa_collection.py`, जेणेकरून pinned FreeIPA collection मधील deprecated imports rewrite करून पुढील ansible-core versions सोबत compatibility राखता येईल
- `scripts/lint.py`, जेणेकरून local, CI, आणि pre-commit साठी cross-platform lint entry point देता येईल
- `scripts/smoke-test.py`, जेणेकरून प्रत्यक्ष infrastructure न छेडता example inventory validation आणि syntax checks चालवता येतील, ज्यात वेगळ्या Windows playbook ची coverage सुद्धा आहे
- `scripts/check_translations.py`, जेणेकरून translated README ची metadata, section structure parity, आणि canonical English README विरुद्ध minimum content coverage तपासता येईल
- `scripts/lint.ps1` आणि `scripts/lint.sh`, जेणेकरून local lint आणि smoke workflow एकत्र चालवता येतील
- `scripts/proxmox_event_webhook.py`, जेणेकरून controller side optional webhook म्हणून काम करता येईल जे Proxmox VM events हाताळते
- `scripts/proxmox-vm-hook.pl`, जेणेकरून Proxmox node वर optional VM hook म्हणून काम करता येईल
- `scripts/run-playbook.ps1`, जेणेकरून Windows आणि PowerShell environment साठी consistent `ansible-playbook` wrapper उपलब्ध होईल
- `scripts/vault.ps1` आणि `scripts/vault.sh`, जेणेकरून domain-separated vault files create, edit, view, आणि encrypt करणे सोपे होईल
- `tests/`, जे smoke-test documentation पासून सुरू होणारा repository verification surface जपते
- `CONTRIBUTING.md`, जे expected contribution आणि validation workflow document करते
- `SECURITY.md`, जे vulnerability reporting आणि security-sensitive माहिती हाताळण्याची पद्धत document करते

जर तुमच्या controller वर `ansible-lint` install असेल:

```bash
ansible-lint
```

repository smoke checks थेट चालवण्यासाठी:

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

पूर्ण local lint pass साठी:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

प्रत्येक commit आधी fast lint hook enable करण्यासाठी:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper आता common operator options सुद्धा थेट support करते:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## पुढील विस्तार

सामान्यपणे पुढची उपयुक्त extension:

- IPA-ready Linux templates साठी Packer pipeline
- combined rollout साठी AWX किंवा Automation Controller job template आणि scheduling
- अधिक मजबूत Proxmox tenant आणि pool model
- Windows RDP किंवा hybrid identity environment साठी AD trust workflow

## परवाना

ही repository [0BSD License](../../LICENSE) अंतर्गत प्रकाशित केली जाते.
