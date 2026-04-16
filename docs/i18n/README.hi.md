# Proxmox + FreeIPA अभिगम स्वचालन

यह पृष्ठ [README.md](../../README.md) का पूर्ण, संरचनात्मक रूप से समतुल्य हिन्दी अनुवाद है। अंग्रेजी संस्करण canonical स्रोत बना रहता है, लेकिन यह हिन्दी संस्करण भी वही परिचालन कवरेज देने के लिए है।

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## भाषाएँ

पूर्ण दस्तावेज़ का canonical स्रोत अंग्रेज़ी README है। 20 अतिरिक्त भाषाओं में भी पूर्ण translated README उपलब्ध हैं।

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

यह repository identity और access के लिए **FreeIPA को source of truth** मानती है। Proxmox उसी directory को LDAP realm के रूप में consume करता है, Linux guest upstream `ipaclient` role के माध्यम से FreeIPA में join होते हैं, और access synced groups, HBAC, तथा sudo rules के ज़रिए centrally managed रहता है, न कि हर VM में local account sprawl के रूप में।

> [!IMPORTANT]
> यह प्रोजेक्ट **FreeRADIUS को identity source की तरह उपयोग नहीं करता**, **हर VM के अंदर local users नहीं बनाता**, और **Proxmox permission के हर संभव edge case को manage करने की कोशिश नहीं करता**।

## यह प्रोजेक्ट क्यों मौजूद है

इस रिपॉजिटरी का उपयोग तब करें जब आपके पास पहले से:

- एक स्वस्थ FreeIPA deployment
- एक Proxmox VE cluster
- ऐसे Linux guest जिन्हें centralized authentication चाहिए
- Proxmox LDAP bind के लिए एक dedicated service account
- admins और operators के लिए एक स्पष्ट group model

मुख्य सिद्धांत यह है कि identity और access के लिए FreeIPA को source of truth माना जाए। Proxmox उसी directory को LDAP realm के रूप में consume करता है, Linux guest upstream `ipaclient` role के माध्यम से FreeIPA में शामिल होते हैं, और SSH, HBAC, तथा `sudo` नियंत्रण हर VM पर local accounts में बिखरने के बजाय centrally managed रहते हैं।

यह repository तब खास तौर पर उपयुक्त है जब आप onboarding और offboarding को लगभग इस क्रम में चलाना चाहते हों:

1. FreeIPA में users और groups बनाना या update करना
2. उन identities को Proxmox में sync करना
3. synced groups से Proxmox roles और ACLs लागू करना
4. FreeIPA login, HBAC, और sudo rules के माध्यम से Linux guest access देना

## आपको क्या मिलता है

- FreeIPA user groups, hostgroups, HBAC rules, और `sudo` rules का प्रबंधन
- Linux administrators के लिए FreeIPA default login shell का प्रबंधन
- FreeIPA से जुड़ा हुआ Proxmox LDAP realm configuration
- एक निर्दिष्ट cluster node से periodic Proxmox realm sync
- synced directory groups के लिए Proxmox RBAC bindings
- static inventory, IP-based targets, या Proxmox VM discovery के माध्यम से Linux guests का FreeIPA enrollment
- Proxmox QEMU Guest Agent के माध्यम से reboot रहित optional SSH bootstrap
- Proxmox-managed Linux guests के लिए Proxmox side पर guest agent communication channel enable करने की optional क्षमता
- ऐसे guests पर SSH या WinRM के माध्यम से optional QEMU Guest Agent install जो पहले से reachable हों, bootstrap के बाद reachable हों, या Linux enrollment के बाद फिर से retry किए जा सकें
- SSH reachability और Proxmox QEMU Guest Agent status के लिए optional Linux readiness report
- Active Directory आधारित Windows 10/11 और Windows Server domain membership के लिए अलग optional workflow
- IPA CA trust, hosts file bootstrap, और IPA service reachability validation के लिए सीमित FreeIPA-aware Windows helper workflow
- Linux guests के लिए first-touch SSH public-key bootstrap
- FreeIPA access model बदलने के बाद managed Linux clients पर automatic SSSD cache refresh
- Proxmox VM hook और webhook trigger के ज़रिए optional event-driven Linux onboarding

## दायरा

| शामिल है | शामिल नहीं है |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm configuration | FreeIPA user lifecycle का पूर्ण निर्माण |
| synced groups से Proxmox RBAC | सभी Proxmox multi-tenant edge cases की पूर्ण कवरेज |
| Linux client IPA enrollment | FreeIPA के विरुद्ध Windows native login |
| Windows के लिए AD domain membership workflow | AD object या GPO का व्यापक automation |
| Windows के लिए सीमित FreeIPA helper workflow | FreeIPA-based Windows helper को AD के बराबर मान लेना |

## विंडोज़ कार्यप्रवाह

Windows support को Linux IPA enrollment flow में मिलाया नहीं गया है। इसे एक अलग workflow के रूप में लागू किया गया है।

- `windows_qemu_guest_agent_clients` केवल optional QEMU Guest Agent helper tasks के लिए आरक्षित है।
- `10-features.yml` में `windows_domain_membership_enabled: true` सेट करके Windows workflow सक्षम होता है।
- `windows_management_clients` एक अलग Windows group है, जिसे `playbooks/windows-management.yml` और `playbooks/site.yml` के optional Windows चरण उपयोग करते हैं।
- वास्तविक Windows login को Active Directory domain membership के माध्यम से संभाला जाता है। FreeIPA-केंद्रित environment में Windows hosts को सीधे FreeIPA में join कराने के बजाय FreeIPA-AD trust के AD side में join करना चाहिए।

सिर्फ FreeIPA आधारित Windows join इस रिपॉजिटरी द्वारा समर्थित नहीं है। Active Directory या FreeIPA-AD trust के बिना Windows side का scope केवल helper tasks तक सीमित रहता है, जैसे पहले से reachable guests का management और optional QEMU Guest Agent installation।

यदि फिर भी आपको domain join के बिना एक सीमित FreeIPA-aware Windows path चाहिए, तो `windows_freeipa_helpers_enabled: true` सक्षम करें और `playbooks/windows-freeipa-helpers.yml` के साथ `windows_freeipa_helper_clients` का उपयोग करें। यह helper workflow IPA CA trust install कर सकता है, bootstrap के लिए IPA CA अपने आप fetch कर सकता है, expected CA thumbprint को optionally pin कर सकता है, hosts file entries को optionally manage कर सकता है, IPA DNS और महत्वपूर्ण TCP ports को validate कर सकता है, Windows से HTTPS reachability validate कर सकता है, IPA-संबंधित endpoints के विरुद्ध Windows time source validate कर सकता है, Windows local group membership manage कर सकता है, और OpenSSH Server को optionally install या expose कर सकता है, लेकिन यह FreeIPA के विरुद्ध Windows native login प्रदान नहीं करता।

यदि आप उसी helper group पर बिना कोई बदलाव किए readiness check चलाना चाहते हैं, तो `playbooks/windows-freeipa-validate.yml` चलाएँ। यह workflow validation और summary path को बनाए रखता है, लेकिन उस run के लिए CA import, hosts file changes, local group changes, और OpenSSH management को non-mutating बना देता है।

यह workflow WinRM या PSRP के माध्यम से reachable Windows 10/11 और Windows Server guests को target करता है।

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

अधिक विस्तृत design explanation [docs/ARCHITECTURE.md](../ARCHITECTURE.md) में उपलब्ध है।

## आवश्यकताएँ

### नियंत्रक

- Ansible Core 2.14 या नया
- Proxmox primary nodes, IPA servers, और Linux clients तक SSH reachability
- यदि आप Windows workflow का उपयोग करते हैं तो Windows guests तक WinRM या PSRP reachability
- आवश्यकता होने पर `sudo` या `root`
- यदि QGA SSH bootstrap सक्षम है, तो guest के अंदर QEMU Guest Agent पहले से चल रहा होना चाहिए
- यदि Windows के लिए guest-agent installation fallback सक्षम है, तो reachable Windows hosts `windows_qemu_guest_agent_clients` में होने चाहिए
- यदि Windows domain membership सक्षम है, तो reachable Windows hosts `windows_management_clients` में होने चाहिए और आपको AD join credentials प्रदान करने होंगे
- यदि Windows के लिए FreeIPA helper tasks सक्षम हैं, तो reachable Windows hosts `windows_freeipa_helper_clients` में होने चाहिए
- यदि Linux SSH bootstrap सक्षम है, तो controller के पास SSH keypair और guest account के लिए initial password-based login path होना चाहिए

### लक्ष्य

- `proxmox_primary` में Proxmox VE 6.x या उससे नया
- Proxmox और Linux clients से reachable FreeIPA
- Windows 10/11 और Windows Server guests को अलग Windows workflow से manage किया जा सकता है यदि वे WinRM या PSRP के माध्यम से reachable हों
- सही DNS और time synchronization
- `proxmox_primary` के लिए `root` या ऐसा SSH user जिसके पास `pveversion`, `pvesh`, और `pveum` के लिए `sudo` हो
- यदि आप Windows domain membership उपयोग करते हैं, तो target Windows guests संबंधित AD domain controllers तक पहुँच सकें
- यदि आप सीमित FreeIPA helper workflow for Windows उपयोग करते हैं, तो target Windows guests संबंधित IPA servers तक पहुँच सकें
- यदि आप Proxmox discovery उपयोग करते हैं, तो guests QEMU Guest Agent के माध्यम से usable IP expose करें

## नेटवर्क पोर्ट

यह तालिका उन network ports को सूचीबद्ध करती है जिन्हें इस repository का controller, Proxmox LDAP automation, और Linux IPA enrollment flow उपयोग करते हैं।
इसे जानबूझकर केवल उसी surface तक सीमित रखा गया है जिसे यह project वास्तव में उपयोग करता है; यह FreeIPA server-to-server replication matrix की पूर्ण सूची नहीं है।

| नाम | पोर्ट | प्रोटोकॉल | स्रोत | गंतव्य | कब आवश्यक | उद्देश्य |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | हमेशा | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | जब Windows management सक्षम हो | Windows guests तक Ansible connectivity |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS server | जब Linux guests IPA DNS उपयोग करें | IPA records और external names resolve करना |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment और login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA server | Linux IPA enrollment और login | LDAP और FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port`, default `443` | `TCP` | Linux guest | IPA server | Linux IPA enrollment | client installation के दौरान IPA web/API verification |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment और password operations | Kerberos password और keytab operations |
| LDAPS | `636` | `TCP` | Primary Proxmox node | IPA या LDAP server | जब Proxmox LDAP realm default `ldaps` mode उपयोग करे | Proxmox LDAP realm connection |

नोट्स:

- `LDAPS 636/TCP` repository default है क्योंकि `proxmox_ldap_mode` का default `ldaps` है। यदि आप LDAP mode या port बदलते हैं, तो वही `proxmox_ldap_port` अनुमति दें जिसे आप वास्तव में उपयोग कर रहे हैं।
- `WinRM` सामान्यतः HTTPS के लिए `5986/TCP` या HTTP के लिए `5985/TCP` उपयोग करता है, यह आपकी Windows transport configuration पर निर्भर है।
- `DNS 53/TCP,UDP` केवल तब आवश्यक है जब Linux guests IPA servers को resolvers के रूप में उपयोग करते हों।
- `Kerberos 88` और `Kerberos Password 464` दोनों को `TCP` और `UDP` दोनों चाहिए।
- Active Directory domain join के लिए standard Windows-to-domain-controller ports भी आवश्यक होते हैं, लेकिन वे environment-specific होते हैं और यहाँ विस्तार से सूचीबद्ध नहीं हैं।
- Kerberos के विश्वसनीय रूप से काम करने के लिए time synchronization भी आवश्यक है, लेकिन NTP source environment-specific है और इस repository द्वारा manage नहीं किया जाता।

## अनुकूलता

इस repository में Proxmox automation `pveum` और `pvesh` interfaces के आसपास लिखा गया है, जिन्हें Proxmox VE 6.x और बाद के versions realm और RBAC के लिए उपयोग करते हैं।

- default supported majors: `6`, `7`, `8`, `9`, `10`
- validation `pveversion` के माध्यम से detected Proxmox version की जाँच करता है
- supported version list को `proxmox_supported_major_versions` के माध्यम से आपके environment के अनुसार संकीर्ण या विस्तृत किया जा सकता है
- `proxmox_allow_future_major_versions` का default `true` है, इसलिए highest tested version से ऊपर के major versions भी default रूप से validation पार कर लेते हैं
- future major versions को तब तक केवल compatibility candidates की तरह देखना चाहिए जब तक उनकी published Proxmox interfaces इस automation के साथ वास्तव में सत्यापित न हो जाएँ
- `1` से `5` जैसे पुराने versions को यह public repository tested support के रूप में दावा नहीं करता; यदि आप उन्हें locally जोड़ते हैं, तो उसे explicit compatibility override मानें और पहले lab में full workflow validate करें

legacy lab के लिए local override उदाहरण:

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

## त्वरित प्रारंभ

नीचे दिए गए उदाहरण shell commands का उपयोग करते हैं। जहाँ उपयुक्त है वहाँ PowerShell equivalents भी दिए गए हैं।

### 1. उदाहरण इन्वेंटरी और वॉल्ट टेम्पलेट्स कॉपी करें

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

### 2. पर्यावरण-विशिष्ट फाइलें संपादित करें

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- यदि आप Windows management उपयोग करते हैं तो `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- यदि आप Windows management उपयोग करते हैं तो `inventories/production/group_vars/all/vault-windows.yml`

IPA और Proxmox settings के अलावा, Linux guests के लिए एक source mode चुनें:

- `linux_ipa_clients` के तहत static inventory entries
- `group_vars/all/30-linux-clients.yml` में `linux_ipa_client_hosts` entries
- `linux_ipa_proxmox_discovery_enabled: true` के साथ Proxmox VM discovery

Linux IPA enrollment के लिए domain values और server lists में अंतर समझें:

- `ipaclient_domain` shared IPA DNS domain है, उदाहरण `example.com`
- `linux_ipa_servers` IPA server hostnames की सूची है, उदाहरण `ipa01.example.com`

यदि आप Proxmox तक `root` के बजाय ऐसे सामान्य user से SSH करना चाहते हैं जिसके पास `sudo` हो, तो उसे `hosts.yml` के `proxmox_primary` में सेट करें और sudo password को `vault-proxmox.yml` में रखें:

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

इस configuration में `vault_proxmox_become_password` वही password है जो आप सामान्यतः Proxmox host पर `sudo` चलाते समय टाइप करते हैं।

### 3. वॉल्ट फाइलें एन्क्रिप्ट करें

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

यदि आप Windows workflow enable करते हैं, तो उसी command में `inventories/production/group_vars/all/vault-windows.yml` भी जोड़ें।

वैकल्पिक रूप से helper wrapper का उपयोग करें, जो default रूप से domain-separated vault IDs का उपयोग करता है और आवश्यकता होने पर example templates से working vault files बनाता है:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

यदि आप playbook runs के लिए domain-specific passwords चाहते हैं, तो `--ask-vault-pass` के बजाय vault IDs का उपयोग करें:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

यदि optional Windows workflow भी अपना अलग vault password उपयोग करता है, तो उसी command में `windows@prompt` जोड़ें।

`-AskVaultPass` केवल तभी उपयोग करें जब उस playbook द्वारा उपयोग की जाने वाली सभी vault files एक ही password साझा करती हों।

### 4. आवश्यक कलेक्शन इंस्टॉल करें

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

या सीधे:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

यदि आपने इस repository द्वारा compatibility patch जोड़ने से पहले `freeipa.ansible_freeipa` install किया था, तो bootstrap helper को फिर से चलाएँ या `python .\scripts\patch_freeipa_collection.py` एक बार चलाएँ ताकि user-level collection installation भी patch हो जाए।

जब आप `scripts/run-playbook.ps1` उपयोग करते हैं, तो वह `ansible-playbook` चलाने से पहले इस patch helper को automatically चलाता है।

### 5. पहले सत्यापन चलाएँ

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

यदि आप केवल Windows FreeIPA helper-only path को बिना कोई बदलाव किए validate करना चाहते हैं:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

यदि आप read-only Linux readiness audit चाहते हैं जो बताए कि कौन से runtime guests SSH से reachable हैं और कौन से Proxmox-discovered guests QEMU Guest Agent के माध्यम से respond कर रहे हैं:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

readiness report default रूप से `.ansible/linux-readiness-report.json` में लिखा जाता है।
मुख्य fields की व्याख्या इस प्रकार करें:

- `ssh.ready=true`: वर्तमान Ansible SSH path controller से सफल है
- `ssh.promptless=true`: SSH probe `ansible_password` के बिना सफल हुआ, इसलिए यह path Ansible के लिए non-interactive है
- `ssh.auth_mode=password_configured`: probe ने `sshpass` का उपयोग किया क्योंकि host के पास `ansible_password` configured है
- `ssh.auth_mode=key_or_agent`: probe `ansible_password` के बिना SSH batch mode में सफल हुआ
- `qga.status=available`: VM के मालिक Proxmox node पर `qm guest ping` सफल हुआ
- `qga.status=disabled`: Proxmox VM configuration में QEMU Guest Agent enabled नहीं है
- `qga.status=configured_unresponsive`: guest agent Proxmox configuration में enabled है लेकिन respond नहीं कर रहा
- `qga.status=node_unreachable`: controller संबंधित Proxmox node तक नहीं पहुँच सका, इसलिए probe नहीं हो पाया
- `qga.status=not_applicable`: host Proxmox discovery से नहीं बना है, इसलिए QGA probe प्रयास नहीं किया गया

त्वरित inspection उदाहरण:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. वैकल्पिक: योजनाबद्ध परिवर्तनों का पूर्वावलोकन करें

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> check mode को पूर्ण simulation नहीं, बल्कि partial preview मानें। यह repository कुछ Proxmox configuration के लिए direct CLI commands और Linux enrollment के लिए upstream FreeIPA client role का उपयोग करती है, इसलिए `--check` उपयोगी है लेकिन पूर्ण authority नहीं है।
>
> FreeIPA HBAC rules के लिए check mode rule definition steps को validate करता है, लेकिन उसके बाद होने वाली enable या disable actions को skip कर देता है। इससे वह false failure नहीं होता जो तब आता जब FreeIPA dry run में वास्तव में न बनाए गए rule को missing बताता है।
>
> Proxmox realm sync timer role भी check mode में अंतिम `systemd` enable या start step को skip करता है, क्योंकि unit files diff में दिखाई देती हैं लेकिन dry run में वास्तव में लिखी नहीं जातीं।
>
> Linux IPA enrollment भी check mode में skip हो जाता है। repository discovery, hostname resolution, और input validation जारी रखती है, लेकिन upstream `ipaclient` role स्वयं dry run के दौरान execute नहीं होती।

### 7. पूर्ण कॉन्फ़िगरेशन लागू करें

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

यदि optional Windows workflow enabled है और `vault-windows.yml` अलग password उपयोग करता है, तो उसी playbook को `--ask-vault-pass` के बजाय `--vault-id windows@prompt` या PowerShell wrapper के `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` के साथ चलाएँ।

## रोलआउट क्रम

पहली deployment के लिए stack को इस क्रम में apply करें:

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

यह क्रम troubleshooting को बहुत आसान बनाता है, बजाय सब कुछ एक साथ चलाने के।

उदाहरण के लिए, केवल एक Linux guest तक सीमित PowerShell rollout:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

default rollout controls जानबूझकर conservative हैं:

- FreeIPA access changes `serial: 1` के साथ चलती हैं
- Proxmox changes `serial: 1` के साथ चलती हैं
- hostname resolution, validation, और Linux enrollment `serial: 10` के साथ चलते हैं
- Windows management changes `serial: 10` के साथ चलती हैं
- सभी rollout paths default रूप से `max_fail_percentage: 0` उपयोग करते हैं

इन values को `inventories/production/group_vars/all/15-rollout.yml` में समायोजित करें।

## टैग मॉडल

लगातार नए playbooks बनाने के बजाय, stable rollout slices को target करने के लिए tags का उपयोग करें।

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

## इवेंट-चालित VM ऑनबोर्डिंग

यदि आप चाहते हैं कि Proxmox किसी VM के start होने या migration के बाद तुरंत Linux discovery और IPA enrollment trigger करे, तो [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) में वर्णित optional hook और webhook path का उपयोग करें।

यह path event-specific playbook `playbooks/proxmox-vm-event.yml` का उपयोग करता है, इसलिए trigger केवल Linux guest और FreeIPA side को संभालता है। यह हर VM event पर Proxmox LDAP realm automation या RBAC को दोबारा नहीं चलाता।

अब यह repository optional hook और webhook stack को `site.yml` या `proxmox.yml` के माध्यम से भी install कर सकती है, यदि `proxmox_vm_event_onboarding_enabled: true` सेट हो और आवश्यक webhook variables उपलब्ध हों।

Proxmox VM hook कोई अलग `create` phase प्रदान नहीं करता। व्यवहार में नया VM सामान्यतः पहले `post-start` event पर पकड़ा जाता है, जबकि migration hooks source node और destination node दोनों पर trigger हो सकते हैं।

## इन्वेंटरी मॉडल

यह repository छह परिभाषित inventory groups और एक runtime-generated group का उपयोग करती है:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

आप अपनी अतिरिक्त inventory groups भी परिभाषित कर सकते हैं और उन्हें FreeIPA hostgroup definitions में reference कर सकते हैं। यदि आप FreeIPA hostgroup side से तैयार Linux guest set पूरा उपयोग करना चाहते हैं, तो `linux_ipa_clients_runtime` group reference करें।

> [!IMPORTANT]
> FreeIPA को हर guest के लिए final hostname चाहिए। यदि आप IP-only targets या Proxmox discovery उपयोग करते हैं, तो `ipa_hostname` स्पष्ट रूप से दें या सुनिश्चित करें कि guest के अंदर `hostname -f` अंतिम FQDN लौटाता है। playbook FreeIPA hostgroup membership बनाने से पहले उसी hostname को resolve करती है।

> [!TIP]
> reusable golden templates को सीधे FreeIPA में enroll न करें। पहले VM clone करें, final hostname दें, फिर resulting guest को enroll करें।

### लिनक्स गेस्ट स्रोत मोड

आप `linux_ipa_clients` को तीन अलग-अलग तरीकों से populate कर सकते हैं।

#### 1. static inventory hosts

यदि आप पहले से guest names जानते हैं, तो सामान्य Ansible inventory entries उपयोग करें:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. variables में manual host definitions

यदि आप guests को `hosts.yml` से बाहर रखना चाहते हैं या आपके पास केवल IPs हैं, तो `linux_ipa_client_hosts` उपयोग करें:

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

- यदि `name` पहले से एक resolvable hostname या FQDN है, तो `ansible_host` optional है
- यदि आप केवल IP जानते हैं, तो `name` के लिए कोई भी स्थिर alias उपयोग करें
- यदि `ipa_hostname` छोड़ा जाता है, तो playbook guest के अंदर `hostname -f` पर fallback करती है

#### 3. Proxmox VM auto-discovery

यदि आप एक या अधिक Proxmox nodes से Linux guests खोजना चाहते हैं, तो discovery उपयोग करें:

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

- discovery VMs को उसी `linux_ipa_clients_runtime` group में जोड़ती है जिसे अन्य playbooks उपयोग करते हैं
- IP discovery QEMU guest agent पर निर्भर करती है जो network interfaces report कर सके
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` केवल उन VM names पर भरोसा करता है जो पहले से FQDN हों
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` सेट करने पर `Teleport-Server-1` जैसे सुरक्षित short VM names को `linux_ipa_identity_hostname_suffix` के माध्यम से `teleport-server-1.example.com` जैसे hostname hints में promote किया जा सकता है
- `linux_ipa_proxmox_discovery_vmids` optional है और मुख्यतः event-driven hook या webhook workflows में discovery को खास VMIDs तक सीमित करने के लिए उपयोगी है
- guests को अभी भी final hostname चाहिए, जो या तो VM के अंदर configured हो या manual definitions में `ipa_hostname` के रूप में दिया गया हो
- guest का वास्तविक system hostname भी enrollment के लिए valid होना चाहिए; `localhost.localdomain` जैसे placeholder values को `linux-clients` या `site` चलाने से पहले VM के भीतर बदलना होगा
- जब guests `app-server-01` जैसे short hostnames उपयोग करते हैं, तो आप `linux_ipa_identity_hostname_suffix` और optionally `linux_freeipa_enroll_manage_hostname: true` सेट कर सकते हैं ताकि project enrollment से पहले उसे `app-server-01.example.net` जैसे full hostname में resolve और apply करे
- जब FreeIPA DNS आपके guest hostnames के लिए authoritative हो, तो आप `linux_freeipa_enroll_manage_authoritative_dns: true` सेट करके संबंधित A और PTR records repair कर सकते हैं और enrollment से पहले link-local `fe80::/10` AAAA records हटा सकते हैं
- यदि DNS अभी तैयार नहीं है, तो `linux_ipa_manage_etc_hosts: true` और `linux_ipa_etc_hosts_entries` सेट करके role IPA servers और guest FQDNs के लिए managed `/etc/hosts` bootstrap block जोड़ सकती है
- `guest_qemu_agent_install_enabled` उन guests पर QEMU Guest Agent install करता है जो पहले से SSH या WinRM के माध्यम से reachable हैं, उन Linux guests पर retry करता है जो उसी workflow में बाद में reachable हो जाते हैं, और Linux enrollment के बाद फिर से retry करता है ताकि agent-dependent Proxmox workflows इसका लाभ उठा सकें
- `linux_ipa_proxmox_discovery_allowlist_enabled: true` सेट करने पर discovery चालू रहती है लेकिन केवल explicitly approved Proxmox guests ही Linux runtime inventory में admit किए जाते हैं; allowlist VMID, IP, और names पर exact matching कर सकती है
- `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, या `linux_ipa_proxmox_discovery_blacklist_names` सेट करें यदि discovery-enabled nodes पर firewall, DNS servers, या अन्य infrastructure VMs भी मौजूद हों जिन्हें Linux IPA automation से हमेशा बाहर रखना चाहिए; blacklist matching broad discovery और allowlist admission दोनों पर precedence लेती है
- उन Proxmox-discovered Linux guests के लिए जिनमें functional guest agent अभी उपलब्ध नहीं है, `linux_ipa_proxmox_discovery_ansible_user` और साथ में `linux_ipa_proxmox_discovery_ansible_password` या `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` सेट करें ताकि repository QEMU Guest Agent install करने के लिए usable first-touch SSH path पा सके
- यदि ऐसा discovered guest non-root SSH user उपयोग करता है, तो `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, और `linux_ipa_proxmox_discovery_ansible_become_password` भी सेट करें, जब तक उस account के पास पहले से passwordless `sudo` न हो
- `guest_qemu_agent_install_manage_proxmox_vm_agent` Proxmox side पर guest agent communication भी enable करता है (`qm set <vmid> --agent 1`) इससे पहले कि guest के अंदर installation path शुरू हो
- जब वही Proxmox VM option running VM पर बदला जाता है, तो repository default रूप से केवल warning देती है क्योंकि Proxmox को guest agent channel usable बनने से पहले VM restart की आवश्यकता हो सकती है; यदि आप चाहते हैं कि repository ऐसे running VMs को automatically reboot करे, तो `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` सेट करें
- `linux_ipa_ssh_host_key_policy` default रूप से Linux guest connections के लिए `accept_new` उपयोग करता है ताकि newly discovered VMs तक host key checking पूरी तरह disable किए बिना पहुंचा जा सके; बदली हुई host keys फिर भी fail होंगी और operator review चाहेंगी
- `linux_ipa_qga_ssh_bootstrap_enabled` Proxmox-based guests के लिए पसंदीदा no-reboot bootstrap path है क्योंकि यह सामान्य SSH login से पहले QEMU Guest Agent के जरिए एक dedicated key-only automation user बना सकता है
- `linux_ipa_qga_ssh_bootstrap_qm_path` का default `qm` है, और bootstrap flow fail होने से पहले Proxmox node पर common fallback paths भी जाँचती है
- जो guests `guest-ping` allow करते हैं लेकिन `guest-exec` block करते हैं, उन्हें default रूप से QGA bootstrap के दौरान skip किया जाता है; उनके लिए अन्य SSH path दें या `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` सेट करें ताकि run तुरंत fail हो
- `linux_ipa_ssh_bootstrap_enabled` optionally controller की public key को hostname resolution और enrollment से पहले Linux guests पर install करता है; `linux_ipa_ssh_bootstrap_password` shared first-touch password fallback के रूप में भी उपयोग होती है, भले ही key-based bootstrap disabled हो
- Linux IPA enrollment उन upstream client joins को retry करती है जो FreeIPA JSON-RPC timeout के कारण fail हुए हों, और धीमे या व्यस्त IPA environments के लिए `linux_ipaclient_kinit_attempts` expose करती है
- Linux IPA enrollment default रूप से inventory `ipa_servers` hostnames को join server list में merge करती है, ताकि clients एक single endpoint के बजाय पूरे IPA server set का उपयोग कर सकें
- जब एक से अधिक IPA servers उपलब्ध हों, तो हर retry round enrollment के दौरान उन candidate IPA servers को क्रम से आज़माता है
- combined `site` workflow पहले FreeIPA hostgroups बनाती है और उसके बाद enrolled runtime hosts को जोड़ती है, ताकि pre-enrollment runs केवल इस वजह से hostgroup membership step पर fail न हों कि guests अभी तक enrolled नहीं हैं

## कॉन्फ़िगरेशन परिधि

अधिकांश values निम्न स्थानों पर रहती हैं:

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

प्रत्येक file के अनुसार layout के लिए [docs/VARIABLES.md](../VARIABLES.md) देखें।

मुख्य variable families:

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

## उदाहरण समूह रणनीति

एक सरल लेकिन अच्छी तरह scale होने वाला pattern:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa` के लिए Proxmox ACL binding

यदि आप चाहते हैं कि combined `site.yml` run कुछ IPA users को automatically Linux SSH और sudo access दे, तो [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) में `freeipa_linux_admin_users` भरें ताकि managed `linux-ssh-admins` group के ज़रिए वह access दिया जा सके।

ध्यान रखें कि Proxmox LDAP sync suffix के साथ groups बनाती है:

```text
<group-name>-<realm>
```

यदि आपका FreeIPA group `proxmox-admins` है और Proxmox realm `ipa` है, तो synced PVE group इस प्रकार बनेगा:

```text
proxmox-admins-ipa
```

## सुरक्षा

- सभी secrets को plaintext inventory variables के बजाय `vault-freeipa.yml` और `vault-proxmox.yml` में रखें
- Proxmox के लिए dedicated read-only LDAP bind account को प्राथमिकता दें
- certificate verification enabled रखते हुए TLS को प्राथमिकता दें
- temporary lab को छोड़कर SSH host key checking चालू रखें
- यदि आपके Proxmox guests में QEMU Guest Agent पहले से functional है, तो shared temporary passwords की तुलना में `linux_ipa_qga_ssh_bootstrap_enabled` को प्राथमिकता दें
- `guest_qemu_agent_install_enabled` का उपयोग केवल तब करें जब repository के पास guest के अंदर प्रवेश करने के लिए वैध management path पहले से हो; Proxmox discovery के लिए इसका अर्थ है कि या तो QGA पहले से चल रहा हो या `linux_ipa_proxmox_discovery_ansible_user` और password या key access configured हो
- यदि आप Linux SSH bootstrap enable करते हैं, तो shared bootstrap password को encrypted variable में रखें और key-based access स्थापित होने के बाद उसे rotate या remove करें
- IPA admin account को Proxmox LDAP bind account के रूप में reuse न करें
- production rollout से पहले `proxmox_ldap_filter` और `proxmox_ldap_group_filter` की समीक्षा करें ताकि अत्यधिक objects import न हो जाएँ

यदि आप disposable lab में जानबूझकर SSH host key verification disable करना चाहते हैं, तो repository defaults बदलने के बजाय shell session level पर opt-out करें:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## आइडेम्पोटेंसी और सावधानियाँ

यह repository दोबारा चलाए जाने के लिए लिखी गई है और अधिकांशतः idempotent है, लेकिन production rollout से पहले इसे lab में validate किया जाना चाहिए।

ज्ञात caveats:

- Proxmox CLI output releases के बीच थोड़ी बदल सकती है
- FreeIPA directory layout flexible होती है, इसलिए LDAP filters को आपकी tree के अनुसार tune करना पड़ सकता है
- पहले से manually managed PVE ACLs और roles की तुलना कर लेनी चाहिए, उसके बाद ही automation को उन पर लागू करें
- Proxmox VM auto-discovery running guests और QEMU guest agent network data पर निर्भर करती है
- IP-based guest definitions को अभी भी guest के अंदर valid final hostname या explicit `ipa_hostname` चाहिए
- Proxmox plays privilege escalation के साथ चलती हैं, इसलिए non-root SSH users के पास working `sudo` होना चाहिए, और यदि उस account के पास passwordless `sudo` नहीं है तो आपको `-K` के साथ become password देना होगा
- यदि आप `ansible_become_password` को `vault-proxmox.yml` में store करते हैं, तो `-K` छोड़ा जा सकता है क्योंकि Ansible encrypted variable से sudo password पढ़ लेगा

## सत्यापन

rollout सफल होने के बाद final state verify करें; यह मानकर न चलें कि सभी access paths अपने आप सही हो गए हैं।

### FreeIPA में

- सुनिश्चित करें कि अपेक्षित user groups मौजूद हैं
- सुनिश्चित करें कि अपेक्षित hostgroups मौजूद हैं
- सुनिश्चित करें कि अपेक्षित HBAC rules मौजूद और enabled हैं
- सुनिश्चित करें कि अपेक्षित `sudo` rules मौजूद और enabled हैं

### Proxmox में

- सुनिश्चित करें कि LDAP realm मौजूद है
- सुनिश्चित करें कि initial sync ने अपेक्षित users या groups import किए हैं
- सुनिश्चित करें कि target synced groups पर अपेक्षित ACL bindings मौजूद हैं

### लिनक्स गेस्ट पर

- सुनिश्चित करें कि allowed IPA users login कर सकते हैं
- सुनिश्चित करें कि disallowed users को HBAC block करता है
- सुनिश्चित करें कि allowed IPA admins `sudo -l` चला सकते हैं
- यदि `linux_ipaclient_mkhomedir` enabled है, तो पहले login पर home directories बनती हैं

## रिपॉजिटरी संरचना

<details>
<summary>रिपॉजिटरी लेआउट दिखाएँ</summary>

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

इस repository में शामिल मुख्य helper files:

- `.editorconfig`, ताकि editors के बीच spaces, encoding, और line endings के defaults consistent रहें
- `.gitattributes`, ताकि common text files पर `LF` line endings enforce की जा सकें
- `.gitignore`, ताकि generated inventory, vault data, local collections, और editor junk Git में शामिल न हों
- `.ansible-lint`, ताकि vendor collection paths को exclude किया जा सके और केवल YAML line-length rule को suppress किया जा सके
- `.yamllint`, ताकि playbooks, inventory, और workflows में YAML validation consistent रहे
- `.github/CODEOWNERS`, ताकि repository के मुख्य क्षेत्रों पर review ownership स्पष्ट रहे
- `.github/workflows/ci.yml`, ताकि push और pull request events पर lint और smoke validation चल सके
- `.pre-commit-config.yaml`, ताकि `pre-commit` install होने पर commit से पहले fast lint hooks चल सकें
- `CHANGELOG.md`, ताकि repository changes को एक ही जगह track किया जा सके
- `docs/VARIABLES.md`, ताकि split inventory variable structure समझाया जा सके
- `docs/i18n/`, जहाँ translated READMEs रखी जाती हैं; इन files को अंग्रेज़ी `README.md` की पूरी section structure reflect करनी चाहिए
- `docs/i18n/TRANSLATION_GUIDE.md`, ताकि translated READMEs को sync में रखने का तरीका समझाया जा सके
- `scripts/bootstrap.ps1` और `scripts/bootstrap.sh`, ताकि आवश्यक collections local `collections/` path पर install की जा सकें और ansible-core 2.24+ compatibility patch लागू किया जा सके
- `scripts/patch_freeipa_collection.py`, ताकि pinned FreeIPA collection के अंदर deprecated imports को rewrite किया जा सके और upcoming ansible-core versions के साथ compatibility बनी रहे
- `scripts/lint.py`, ताकि local, CI, और pre-commit के लिए cross-platform lint entry point उपलब्ध हो
- `scripts/smoke-test.py`, ताकि बिना वास्तविक infrastructure को छुए example inventory validation और syntax checks चलाए जा सकें, जिसमें अलग Windows playbooks की coverage भी शामिल हो
- `scripts/check_translations.py`, ताकि translated READMEs की metadata, section structure parity, और canonical English README के मुकाबले minimum content coverage verify की जा सके
- `scripts/lint.ps1` और `scripts/lint.sh`, ताकि local lint और smoke workflows को एक साथ चलाया जा सके
- `scripts/proxmox_event_webhook.py`, ताकि controller side optional webhook की तरह कार्य किया जा सके जो Proxmox VM events संभाले
- `scripts/proxmox-vm-hook.pl`, ताकि Proxmox nodes पर optional VM hook की तरह कार्य किया जा सके
- `scripts/run-playbook.ps1`, ताकि Windows और PowerShell environments के लिए consistent `ansible-playbook` wrapper उपलब्ध कराया जा सके
- `scripts/vault.ps1` और `scripts/vault.sh`, ताकि domain-separated vault files की creation, editing, viewing, और encryption आसान हो
- `tests/`, repository की verification surface को संभालता है, जिसकी शुरुआत smoke-test documentation से होती है
- `CONTRIBUTING.md`, अपेक्षित contribution और validation workflow को document करता है
- `SECURITY.md`, vulnerability reporting और security-sensitive जानकारी के सही handling को document करता है

यदि आपके controller पर `ansible-lint` install है:

```bash
ansible-lint
```

repository smoke checks सीधे चलाने के लिए:

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

पूर्ण local lint pass के लिए:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

हर commit से पहले fast lint hook enable करने के लिए:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper अब common operator options को भी सीधे support करता है:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## आगे के विस्तार

सामान्यतः अगले उपयोगी extensions:

- IPA-ready Linux templates के लिए Packer pipeline
- combined rollouts के लिए AWX या Automation Controller job templates और scheduling
- मजबूत Proxmox tenant और pool model
- Windows RDP या hybrid identity environments के लिए AD trust workflows

## लाइसेंस

यह repository [MIT License](../../LICENSE) के अंतर्गत जारी की जाती है।
