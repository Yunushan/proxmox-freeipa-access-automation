# Proxmox + FreeIPA رسائی آٹومیشن

یہ صفحہ [README.md](../../README.md) میں موجود آپریشنل ساخت کا مکمل اردو ترجمہ فراہم کرتا ہے۔ انگریزی نسخہ آخری canonical ماخذ رہے گا، مگر یہ اردو نسخہ بھی انہی بنیادی حصوں کو کور کرتا ہے تاکہ آپ پورا پروجیکٹ اپنی زبان میں پڑھ سکیں۔

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## زبانیں

مکمل دستاویزات کے لیے انگریزی نسخہ canonical source ہے۔ مزید مکمل ترجمہ شدہ README فائلیں translation index میں دستیاب ہیں۔

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

یہ repository **FreeIPA کو source of truth** سمجھتی ہے برائے identity اور access۔ Proxmox اسی directory کو LDAP realm کے طور پر consume کرتا ہے، Linux guests upstream `ipaclient` role کے ذریعے FreeIPA میں join ہوتے ہیں، اور access مقامی accounts میں بکھرنے کے بجائے synced groups، HBAC، اور `sudo` rules کے ذریعے مرکزیت میں رہتی ہے۔

> [!IMPORTANT]
> یہ project **نہ** FreeRADIUS کو identity source کے طور پر استعمال کرتا ہے، **نہ** ہر VM کے اندر local users بناتا ہے، اور **نہ** Proxmox permission edge cases کے ہر ممکنہ زاویے کو manage کرنے کا دعویٰ کرتا ہے۔

## یہ منصوبہ کیوں موجود ہے

اس repository کو اس وقت استعمال کریں جب آپ کے پاس پہلے سے:

- ایک صحت مند FreeIPA deployment
- ایک Proxmox VE cluster
- ایسے Linux guests جو central authentication استعمال کریں
- Proxmox LDAP bind کے لیے FreeIPA میں dedicated service account
- admins اور operators کے لیے واضح group model

یہ project اس وقت بہترین fit بنتا ہے جب آپ onboarding اور offboarding کو زیادہ تر اس ترتیب سے چلانا چاہتے ہوں:

1. FreeIPA میں users اور groups بنانا یا اپڈیٹ کرنا
2. انہی identities کو Proxmox میں sync کرنا
3. synced groups کے ذریعے Proxmox roles اور ACLs apply کرنا
4. Linux guest access کو FreeIPA login، HBAC، اور `sudo` rules کے ذریعے allow کرنا

## آپ کو کیا ملتا ہے

- FreeIPA user groups، hostgroups، HBAC rules، اور `sudo` rules کا انتظام
- Linux admin users کے لیے FreeIPA login shell defaults کا خودکار انتظام
- FreeIPA کے خلاف Proxmox LDAP realm configuration
- ایک designated cluster node سے recurring Proxmox realm sync
- synced directory groups کے لیے Proxmox RBAC bindings
- static inventory، IP-only targets، یا Proxmox VM discovery کے ذریعے Linux guest enrollment
- Proxmox QEMU Guest Agent کے ذریعے optional no-reboot SSH bootstrap
- Proxmox-backed Linux guests کے لیے optional Proxmox-side guest-agent communication enablement
- ایسے guests کے لیے optional SSH یا WinRM fallback QEMU Guest Agent installation جو پہلے سے reachable ہوں یا bootstrap کے بعد reachable ہو جائیں
- SSH reachability اور Proxmox QEMU Guest Agent status کے لیے optional Linux readiness reporting
- Windows 10/11 اور Windows Server guests کے لیے Active Directory کے ذریعے optional separate Windows domain-membership workflow
- IPA CA trust، hosts bootstrap، اور IPA reachability checks کے لیے optional limited FreeIPA-aware Windows helper workflow
- Linux guests کے لیے optional first-touch SSH public-key bootstrap
- FreeIPA access-model changes کے بعد managed Linux clients پر automatic SSSD cache refresh
- Proxmox VM hook اور webhook triggers کے ذریعے optional event-driven Linux onboarding

## دائرہ کار

| شامل | شامل نہیں |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm setup | FreeIPA user lifecycle creation |
| synced groups سے Proxmox RBAC | مکمل Proxmox multi-tenant policy coverage |
| Linux IPA client enrollment | براہِ راست FreeIPA کے خلاف native Windows logon |
| Windows کے لیے الگ AD domain-membership workflow | GPO یا وسیع تر AD object lifecycle automation |
| محدود FreeIPA-aware Windows helper workflow | یہ دکھانا کہ FreeIPA-only Windows helpers، AD کے برابر ہیں |

## ونڈوز ورک فلو

Windows support کو Linux IPA enrollment میں ملایا نہیں گیا۔ اسے الگ workflow کے طور پر implement کیا گیا ہے۔

- `windows_qemu_guest_agent_clients` صرف optional QEMU Guest Agent helper tasks کے لیے مخصوص رہتی ہے۔
- `10-features.yml` میں `windows_domain_membership_enabled: true` کے ذریعے یہ workflow enable کریں۔
- `windows_management_clients` وہ الگ Windows management group ہے جسے `playbooks/windows-management.yml` اور `playbooks/site.yml` کا optional Windows stage استعمال کرتا ہے۔
- اصل Windows logon Active Directory domain membership کے ذریعے handle ہوتا ہے؛ FreeIPA-centered environment میں Windows hosts کو براہِ راست FreeIPA میں join کرنے کے بجائے FreeIPA-AD trust کی AD side میں join کریں۔

FreeIPA-only Windows domain join اس repository میں supported نہیں ہے۔ Active Directory یا FreeIPA-AD trust کے بغیر Windows workflow صرف helper tasks تک محدود رہتا ہے، جیسے reachable guest management یا optional QEMU Guest Agent installation۔

اگر آپ domain join کے بغیر محدود FreeIPA-aware path چاہتے ہیں تو `windows_freeipa_helpers_enabled: true` enable کریں اور `playbooks/windows-freeipa-helpers.yml` کے ساتھ `windows_freeipa_helper_clients` استعمال کریں۔ یہ helper workflow IPA CA trust، ابتدائی bootstrap کے لیے IPA CA auto-fetch، optional hosts-file entries، DNS اور ports validation، اور HTTPS reachability validation کر سکتا ہے، لیکن **یہ Windows native logon against FreeIPA فراہم نہیں کرتا**۔

جب آپ اسی helper group کے لیے non-mutating readiness check چاہتے ہوں تو `playbooks/windows-freeipa-validate.yml` چلائیں۔ یہ validation اور summary path برقرار رکھتا ہے لیکن certificate import، hosts-file changes، اور OpenSSH management کو اس run کے لیے بند کر دیتا ہے۔

یہ workflow ایسے Windows 10/11 اور Windows Server guests کو target کرتا ہے جو WinRM یا PSRP کے ذریعے reachable ہوں۔

## معماری

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

طویل design explanation کے لیے [docs/ARCHITECTURE.md](../ARCHITECTURE.md) دیکھیں۔

## ضروریات

### کنٹرولر

- Ansible Core 2.14 یا اس سے نیا
- آپ کے Proxmox primary node، IPA servers، اور Linux clients تک SSH رسائی
- جب آپ Windows workflow استعمال کریں تو Windows guests تک WinRM یا PSRP رسائی
- ضرورت کے مطابق `sudo` یا `root`
- اگر Linux QGA SSH bootstrap enabled ہو تو guest کے اندر Proxmox guest agent پہلے سے active ہونا چاہیے
- اگر Windows کے لیے guest-agent fallback installation enabled ہو تو reachable Windows hosts کو `windows_qemu_guest_agent_clients` میں رکھنا ضروری ہے
- اگر Windows domain membership enabled ہو تو reachable Windows hosts کو `windows_management_clients` میں رکھنا اور AD join credentials فراہم کرنا ضروری ہے
- اگر Windows FreeIPA helper tasks enabled ہوں تو reachable Windows hosts کو `windows_freeipa_helper_clients` میں رکھنا ضروری ہے
- اگر Linux SSH bootstrap enabled ہو تو controller کے پاس SSH keypair اور guest account کے لیے ابتدائی password-capable login path ہونا چاہیے

### اہداف

- `proxmox_primary` میں Proxmox VE 6.x یا اس کے بعد کا ورژن
- Proxmox اور Linux clients سے reachable FreeIPA
- Windows 10/11 اور Windows Server guests الگ Windows workflow سے manage کیے جا سکتے ہیں اگر وہ WinRM یا PSRP کے ذریعے reachable ہوں
- درست DNS اور time synchronization
- `proxmox_primary` کے لیے یا تو `root` استعمال کریں یا ایسا SSH user جو `pveversion`, `pvesh`, اور `pveum` کے لیے `sudo` چلا سکے
- اگر آپ Windows domain membership استعمال کرتے ہیں تو target Windows guests متعلقہ AD domain controllers تک پہنچ سکیں
- اگر آپ limited Windows FreeIPA helper workflow استعمال کرتے ہیں تو target Windows guests متعلقہ IPA servers تک پہنچ سکیں
- اگر آپ Proxmox VM auto-discovery استعمال کرتے ہیں تو discovered guests کو QEMU guest agent کے ذریعے usable IP expose کرنا چاہیے

## نیٹ ورک پورٹس

یہ جدول ان ports کی فہرست دیتا ہے جو اس repository کی controller side، Proxmox LDAP automation، اور Linux IPA enrollment flow استعمال کرتے ہیں۔ یہ جان بوجھ کر اسی project کے دائرے تک محدود ہے، نہ کہ مکمل FreeIPA server-to-server replication matrix تک۔

| نام | پورٹ | پروٹوکول | ذریعہ | منزل | کب ضروری | مقصد |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node، IPA server، Linux guest | ہمیشہ | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | جب Windows management enabled ہو | Windows guests تک Ansible connectivity |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS servers | جب Linux guests IPA DNS استعمال کریں | IPA records اور external names resolve کرنا |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment اور login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA servers | Linux IPA enrollment اور login | LDAP اور FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port` (default `443`) | `TCP` | Linux guest | IPA servers | Linux IPA enrollment | client install کے دوران IPA web/API verification |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment اور password operations | Kerberos password اور keytab operations |
| LDAPS | `636` | `TCP` | Proxmox primary node | IPA/LDAP servers | جب Proxmox LDAP realm default `ldaps` mode میں ہو | Proxmox LDAP realm connection |

نوٹس:

- `LDAPS 636/TCP` repository default ہے کیونکہ `proxmox_ldap_mode` کا default `ldaps` ہے۔ اگر آپ mode یا port بدلیں تو configured `proxmox_ldap_port` allow کریں۔
- `WinRM` عام طور پر HTTPS کے لیے `5986/TCP` یا HTTP کے لیے `5985/TCP` استعمال کرتا ہے، یہ آپ کے Windows transport setup پر منحصر ہے۔
- `DNS 53/TCP,UDP` صرف اس وقت ضروری ہے جب Linux guests IPA servers کو اپنے DNS resolvers کے طور پر استعمال کریں۔
- `Kerberos 88` اور `Kerberos Password 464` دونوں کو `TCP` اور `UDP` دونوں چاہیے۔
- Active Directory domain join کے لیے Windows-to-domain-controller port set بھی درکار ہوتا ہے، مگر وہ environment-specific ہے اس لیے یہاں exhaustively درج نہیں کیا گیا۔
- Kerberos کے قابلِ اعتماد طریقے سے کام کرنے کے لیے time synchronization ضروری ہے، مگر NTP source اس repository کے دائرے میں شامل نہیں۔

## مطابقت

اس repository میں Proxmox automation `pveum` اور `pvesh` کے realm اور RBAC interfaces کے گرد لکھی گئی ہے، جو Proxmox VE 6.x اور بعد کے releases میں استعمال ہوتے ہیں۔

- default supported major versions: `6`, `7`, `8`, `9`, `10`
- validation، detected Proxmox version کو `pveversion` کے ذریعے check کرتی ہے
- اگر آپ کو اپنے environment میں version list کو narrow یا extend کرنا ہو تو `proxmox_supported_major_versions` استعمال کریں
- `proxmox_allow_future_major_versions` کا default `true` ہے، اس لیے سب سے بلند tested version سے اوپر والے majors بھی default کے تحت validation pass کر لیتے ہیں
- future major versions کو تب تک compatibility candidates سمجھا جانا چاہیے جب تک ان کے released Proxmox interfaces اس automation کے خلاف check نہ ہو جائیں
- پرانے major versions جیسے `1` سے `5` تک کو یہ public repository tested support کے طور پر claim نہیں کرتی؛ اگر آپ انہیں locally شامل کریں تو اسے explicit compatibility override سمجھیں اور پورا workflow پہلے lab میں validate کریں

legacy lab environment کے لیے local override مثال:

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

## فوری آغاز

نیچے دی گئی مثالیں shell commands استعمال کرتی ہیں۔ جہاں یہ اہم ہو سکتا ہے وہاں PowerShell equivalents بھی شامل ہیں۔

### 1. مثال انوینٹری اور والٹ ٹیمپلیٹس کاپی کریں

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

### 2. ماحول-مخصوص فائلیں ایڈٹ کریں

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` جب آپ Windows management استعمال کریں
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` جب آپ Windows management استعمال کریں

IPA اور Proxmox settings کے علاوہ Linux guest source mode میں سے ایک منتخب کریں:

- `linux_ipa_clients` کے تحت static inventory entries
- `group_vars/all/30-linux-clients.yml` میں `linux_ipa_client_hosts` entries
- `linux_ipa_proxmox_discovery_enabled: true` کے ساتھ Proxmox VM discovery

Linux IPA enrollment کے لیے domain اور server values کو الگ رکھیں:

- `ipaclient_domain` مشترک IPA DNS domain ہوتا ہے، جیسے `example.com`
- `linux_ipa_servers` میں IPA server hostnames ہوتے ہیں، جیسے `ipa01.example.com`

اگر آپ `root` کے بجائے Proxmox تک کسی عام sudo-capable user سے SSH کرنا چاہتے ہیں، تو اسے `hosts.yml` میں `proxmox_primary` کے تحت set کریں اور sudo password کو `vault-proxmox.yml` میں رکھیں:

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

اس setup میں `vault_proxmox_become_password` وہ password ہے جو آپ عام طور پر Proxmox host پر `sudo` کے لیے manually type کرتے ہیں۔

### 3. والٹ فائلیں انکرپٹ کریں

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

جب آپ Windows workflow enable کریں تو اسی command میں `inventories/production/group_vars/all/vault-windows.yml` بھی شامل کریں۔

یا helper wrappers استعمال کریں، جو default طور پر separate vault IDs استعمال کرتے ہیں اور ضرورت پڑنے پر example templates سے working vault files بنا دیتے ہیں:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

اگر آپ playbooks چلاتے وقت ہر domain کے لیے الگ passwords چاہتے ہیں، تو `--ask-vault-pass` کے بجائے vault IDs کو ترجیح دیں:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

اگر optional Windows workflow بھی اپنا الگ vault password استعمال کرتا ہے تو اسی command میں `windows@prompt` بھی شامل کریں۔

`-AskVaultPass` صرف تب استعمال کریں جب اس playbook میں استعمال ہونے والی تمام vault files ایک ہی password share کرتی ہوں۔

### 4. مطلوبہ کلیکشن انسٹال کریں

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

یا براہِ راست:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

اگر آپ نے `freeipa.ansible_freeipa` اس سے پہلے انسٹال کیا تھا کہ repository نے compatibility patch شامل کیا، تو bootstrap helpers میں سے ایک دوبارہ چلائیں یا `python .\scripts\patch_freeipa_collection.py` ایک بار manually چلا دیں تاکہ موجودہ user-level collection install بھی patch ہو جائے۔

جب آپ `scripts/run-playbook.ps1` استعمال کرتے ہیں تو یہ `ansible-playbook` سے پہلے patch helper خودکار طور پر چلا دیتا ہے۔

### 5. پہلے تصدیق چلائیں

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

اگر آپ صرف helper-only Windows FreeIPA path کو validate کرنا چاہتے ہیں، بغیر host changes کے:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

اگر آپ ایک read-only Linux readiness audit چاہتے ہیں جو یہ report کرے کہ کون سے runtime guests SSH پر reachable ہیں اور کون سے Proxmox-discovered guests QEMU Guest Agent کے ذریعے جواب دیتے ہیں:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

readiness report default طور پر `.ansible/linux-readiness-report.json` لکھتا ہے۔
اہم fields کو اس طرح سمجھیں:

- `ssh.ready=true`: controller سے موجودہ configured Ansible SSH path کامیاب رہا
- `ssh.promptless=true`: SSH probe `ansible_password` کے بغیر کامیاب ہوا، یعنی Ansible کے لیے path non-interactive ہے
- `ssh.auth_mode=password_configured`: probe نے `sshpass` استعمال کیا کیونکہ host پر `ansible_password` موجود تھا
- `ssh.auth_mode=key_or_agent`: probe، `ansible_password` کے بغیر SSH batch mode میں کامیاب ہوا
- `qga.status=available`: owning Proxmox node پر `qm guest ping` کامیاب ہوا
- `qga.status=disabled`: Proxmox VM config میں QEMU Guest Agent enabled نہیں ہے
- `qga.status=configured_unresponsive`: guest agent Proxmox config میں enabled ہے مگر جواب نہیں دے رہا
- `qga.status=node_unreachable`: controller probe کے لیے owning Proxmox node تک نہیں پہنچ سکا
- `qga.status=not_applicable`: host Proxmox discovery سے create نہیں ہوا تھا، اس لیے کوئی QGA probe نہیں ہوا

فوری inspection کی مثال:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. اختیاری طور پر منصوبہ بند تبدیلیوں کا پیش منظر دیکھیں

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> check mode کو مکمل simulation نہیں بلکہ ایک جزوی preview سمجھیں۔ یہ repository Proxmox configuration کے کچھ حصوں کے لیے direct CLI commands اور Linux enrollment کے لیے upstream FreeIPA client role استعمال کرتی ہے، اس لیے `--check` مفید ہے مگر مکمل authority نہیں رکھتا۔
>
> FreeIPA HBAC rules کے لیے check mode rule-definition step کو validate کرتی ہے مگر بعد والا enable یا disable action چھوڑ دیتی ہے۔ اس سے وہ false failures نہیں آتے جہاں FreeIPA dry run کے دوران rule واقعی create نہ ہونے کی وجہ سے اسے missing بتاتی ہے۔
>
> Proxmox realm sync timer role بھی check mode میں آخری `systemd` enable یا start step چھوڑ دیتی ہے، کیونکہ dry run میں unit files diff تو ہو جاتی ہیں مگر واقعی لکھی نہیں جاتیں۔
>
> Linux IPA enrollment بھی check mode میں skip ہو جاتا ہے۔ repository پھر بھی discovery، hostname resolution، اور input validation کرتی ہے، مگر upstream `ipaclient` role dry run کے دوران execute نہیں ہوتا۔

### 7. مکمل کنفیگریشن نافذ کریں

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

اگر optional Windows workflow enabled ہو اور `vault-windows.yml` الگ password استعمال کرتا ہو، تو اسی playbook کو `--vault-id windows@prompt` کے ساتھ چلائیں یا PowerShell wrapper میں `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` استعمال کریں، `--ask-vault-pass` کے بجائے۔

## رول آؤٹ ترتیب

پہلی deployment کے لیے stack کو اس ترتیب میں apply کریں:

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

یہ ترتیب ایک ساتھ سب کچھ چلانے کے مقابلے میں troubleshooting کو بہت آسان بناتی ہے۔

محدود PowerShell rollout کی مثال، مثلاً ایک Linux guest:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

default rollout controls محتاط رکھے گئے ہیں:

- FreeIPA access changes `serial: 1` کے ساتھ چلتی ہیں
- Proxmox changes `serial: 1` کے ساتھ چلتی ہیں
- Linux hostname resolution، validation، اور enrollment `serial: 10` کے ساتھ چلتے ہیں
- Windows management changes `serial: 10` کے ساتھ چلتی ہیں
- تمام rollout paths کا default `max_fail_percentage: 0` ہے

ان values کو `inventories/production/group_vars/all/15-rollout.yml` میں tune کریں۔

## ٹیگ ماڈل

مزید playbooks بنانے کے بجائے stable rollout slices کو target کرنے کے لیے tags استعمال کریں۔

- Core domains: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helpers: `windows`, `windows_freeipa`
- FreeIPA model: `freeipa_access`
- Proxmox subsets: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- Event-driven VM handling: `event`, `linux_refresh`

مثالیں:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## ایونٹ سے چلنے والی VM آن بورڈنگ

اگر آپ چاہتے ہیں کہ Proxmox VM start یا migration کے فوراً بعد Linux discovery اور IPA enrollment trigger کرے، تو [docs/EVENT_DRIVEN_VM_ONBOARDING.md](docs/EVENT_DRIVEN_VM_ONBOARDING.md) میں documented optional hook/webhook workflow استعمال کریں۔

یہ workflow `playbooks/proxmox-vm-event.yml` میں موجود dedicated event playbook استعمال کرتا ہے، تاکہ trigger path صرف Linux اور FreeIPA guest side کو handle کرے۔ یہ ہر VM event پر Proxmox LDAP realm یا RBAC automation دوبارہ نہیں چلاتا۔

اب repository یہ optional hook/webhook stack `site.yml` یا `proxmox.yml` سے بھی deploy کر سکتی ہے، بشرطیکہ `proxmox_vm_event_onboarding_enabled: true` ہو اور مطلوبہ webhook variables set ہوں۔

Proxmox VM hooks الگ سے `create` phase expose نہیں کرتے۔ عملی طور پر نئے VMs اپنی پہلی `post-start` event پر pick up ہوتے ہیں، اور migration hooks source اور target دونوں nodes پر trigger ہو سکتے ہیں۔

## انوینٹری ماڈل

یہ repository چھ declared inventory groups اور ایک generated runtime group استعمال کرتی ہے:

- `ipa_servers`: ایک یا ایک سے زیادہ FreeIPA servers
- `proxmox_primary`: ایک Proxmox node جسے realm configuration اور recurring sync timer own کرنے کے لیے منتخب کیا جاتا ہے
- `linux_ipa_clients`: Linux guests کے لیے declarative source inventory group
- `linux_ipa_clients_runtime`: generated runtime group جو static inventory، manual host definitions، اور optional Proxmox discovery سے بنتا ہے
- `windows_qemu_guest_agent_clients`: optional Windows guest group جو صرف QEMU Guest Agent installation کے لیے استعمال ہوتا ہے
- `windows_management_clients`: optional Windows guest group جو الگ Windows domain-membership workflow استعمال کرتا ہے
- `windows_freeipa_helper_clients`: optional Windows guest group جو محدود FreeIPA-aware helper workflow استعمال کرتا ہے

آپ اپنے inventory groups بھی شامل کر سکتے ہیں اور انہیں FreeIPA hostgroup definitions میں reference کر سکتے ہیں۔ جب آپ کو FreeIPA hostgroups میں مکمل prepared Linux guest set چاہیے ہو، تو `linux_ipa_clients_runtime` کو reference کریں۔

> [!IMPORTANT]
> FreeIPA کو اب بھی ہر guest کا آخری hostname چاہیے ہوتا ہے۔ اگر آپ IP-only targets یا Proxmox discovery استعمال کرتے ہیں، تو یا تو `ipa_hostname` کو explicit طور پر set کریں یا یہ یقینی بنائیں کہ guest پر `hostname -f` آخری FQDN واپس دے۔ playbooks اب FreeIPA hostgroup membership build ہونے سے پہلے وہ hostname resolve کرتی ہیں۔

> [!TIP]
> reusable golden template کو FreeIPA میں enroll نہ کریں۔ پہلے VM clone کریں، آخری hostname assign کریں، پھر حاصل ہونے والے guest کو enroll کریں۔

### لینکس گیسٹ ماخذ کے طریقے

آپ `linux_ipa_clients` کو تین مختلف طریقوں سے populate کر سکتے ہیں۔

#### 1. Static inventory hosts

جب آپ کو guest names پہلے سے معلوم ہوں تو عام Ansible inventory entries استعمال کریں:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. Variables میں manual host definitions

جب آپ guests کو `hosts.yml` سے باہر رکھنا چاہتے ہوں یا آپ کے پاس صرف IP ہو تو `linux_ipa_client_hosts` استعمال کریں:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

نوٹس:

- اگر `name` ایک resolvable hostname یا FQDN ہو، تو `ansible_host` optional ہے
- اگر آپ کو صرف IP معلوم ہو، تو `name` کے لیے کوئی بھی stable alias استعمال کریں
- جب `ipa_hostname` omit ہو، تو playbook guest پر `hostname -f` کو fallback کے طور پر استعمال کرتی ہے

#### 3. Proxmox VM auto-discovery

جب آپ چاہتے ہوں کہ playbook ایک یا ایک سے زیادہ Proxmox nodes سے Linux guests خود نکالے، تو discovery استعمال کریں:

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

نوٹس:

- discovery، باقی playbooks میں استعمال ہونے والے اسی `linux_ipa_clients_runtime` group میں VMs شامل کرتی ہے
- IP discovery، QEMU guest agent کی network interface reporting پر منحصر ہوتی ہے
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` صرف انہی VM names پر اعتماد کرتی ہے جو پہلے سے FQDN ہوں
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` set کریں اگر آپ چاہتے ہوں کہ محفوظ short Proxmox VM names جیسے `Teleport-Server-1` خودکار طور پر `linux_ipa_identity_hostname_suffix` کے ذریعے `teleport-server-1.example.com` جیسے hostname hints میں promote ہو جائیں
- `linux_ipa_proxmox_discovery_vmids` optional ہے اور زیادہ تر event-driven hook/webhook workflow میں discovery کو ایک یا زیادہ مخصوص VMIDs تک محدود کرنے کے لیے استعمال ہوتا ہے
- guest کو اب بھی آخری hostname چاہیے ہوتا ہے، یا تو پہلے سے VM کے اندر configured ہو یا manual definition کے ذریعے `ipa_hostname` کے ساتھ فراہم کیا گیا ہو
- guest کا اصل system hostname بھی enrollment کے لیے valid ہونا چاہیے؛ `localhost.localdomain` جیسی placeholder values کو `linux-clients` یا `site` چلانے سے پہلے VM پر بدلنا ضروری ہے
- جب guests short hostnames جیسے `app-server-01` استعمال کریں، تو آپ `linux_ipa_identity_hostname_suffix` اور اختیاری طور پر `linux_freeipa_enroll_manage_hostname: true` set کر سکتے ہیں تاکہ project enrollment سے پہلے `app-server-01.example.net` جیسا full hostname resolve اور apply کرے
- جب FreeIPA DNS آپ کے guest hostnames کے لیے authoritative ہو، تو آپ `linux_freeipa_enroll_manage_authoritative_dns: true` set کر سکتے ہیں تاکہ project enrollment سے پہلے مخصوص guest A اور PTR records کو repair کرے اور link-local `fe80::/10` AAAA records کو remove کرے
- جب DNS ابھی تیار نہ ہو، تو آپ `linux_ipa_manage_etc_hosts: true` set کر سکتے ہیں اور `linux_ipa_etc_hosts_entries` فراہم کر سکتے ہیں تاکہ role enrollment checks سے پہلے IPA servers اور guest FQDNs کے لیے managed `/etc/hosts` bootstrap block شامل کرے
- `guest_qemu_agent_install_enabled` ان guests پر QEMU Guest Agent انسٹال کرتا ہے جو پہلے ہی SSH یا WinRM سے reachable ہوں، انہی Linux guests پر دوبارہ کوشش کرتا ہے جو اسی workflow میں بعد میں reachable ہو جائیں، اور Linux enrollment کے بعد ایک بار پھر retry کرتا ہے تاکہ بعد کے Proxmox agent-dependent workflows اسے استعمال کر سکیں
- `linux_ipa_proxmox_discovery_allowlist_enabled: true` set کریں اگر آپ discovery کو on رکھنا چاہتے ہوں مگر صرف سختی سے approved subset ہی Linux runtime inventory میں داخل ہو؛ allowlist exact VMIDs، IPs، اور names سے match کر سکتی ہے
- `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, یا `linux_ipa_proxmox_discovery_blacklist_names` set کریں جب discovery-enabled nodes پر firewalls یا DNS servers جیسے infrastructure VMs بھی ہوں جن پر Linux IPA automation کبھی نہیں چلنی چاہیے؛ blacklist matches broad discovery یا allowlist دونوں پر ہمیشہ فوقیت رکھتے ہیں
- ان Proxmox-discovered Linux guests کے لیے جن کے پاس پہلے سے working guest agent نہ ہو، `linux_ipa_proxmox_discovery_ansible_user` اور ساتھ میں `linux_ipa_proxmox_discovery_ansible_password` یا `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` set کریں تاکہ repository کے پاس QEMU Guest Agent install کرنے کے لیے usable first-touch SSH path ہو
- اگر وہ discovered guests non-root SSH user استعمال کرتے ہوں، تو `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, اور `linux_ipa_proxmox_discovery_ansible_become_password` بھی set کریں، جب تک کہ اس account کے پاس پہلے سے passwordless sudo نہ ہو
- `guest_qemu_agent_install_manage_proxmox_vm_agent` guest-side install path چلنے سے پہلے Proxmox-backed Linux guests کے لیے Proxmox side guest-agent communication (`qm set <vmid> --agent 1`) بھی enable کرتا ہے
- جب یہ Proxmox VM option کسی running VM پر بدلے، تو repository default طور پر صرف warning دیتی ہے کیونکہ Proxmox کو host کے guest-agent channel استعمال کرنے سے پہلے VM کو نئے سرے سے start کرنے کی ضرورت پڑ سکتی ہے؛ اگر آپ چاہتے ہیں کہ repository ایسے running VMs خودکار طور پر reboot کرے تو `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` set کریں
- `linux_ipa_ssh_host_key_policy` Linux guest connections کے لیے default طور پر `accept_new` ہے، تاکہ newly discovered VMs سے مکمل host key checking disable کیے بغیر رابطہ کیا جا سکے؛ changed host keys پھر بھی fail ہوں گی اور operator review درکار ہوگا
- `linux_ipa_qga_ssh_bootstrap_enabled` Proxmox-backed guests کے لیے پسندیدہ no-reboot bootstrap path ہے کیونکہ یہ کسی موجودہ SSH login کے بغیر بھی QEMU Guest Agent کے ذریعے dedicated key-only automation user create کر سکتا ہے
- `linux_ipa_qga_ssh_bootstrap_qm_path` کا default `qm` ہے، اور bootstrap flow fail ہونے سے پہلے Proxmox node پر عام fallback paths بھی probe کرتا ہے
- جو guests `guest-ping` allow کرتے ہیں مگر `guest-exec` reject کرتے ہیں، وہ default طور پر QGA bootstrap کے دوران skip ہو جاتے ہیں؛ ان کے لیے کوئی دوسرا SSH path دستیاب رکھیں، یا fast failure کے لیے `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` set کریں
- `linux_ipa_ssh_bootstrap_enabled` اختیاری طور پر hostname resolution اور enrollment سے پہلے controller SSH public key کو Linux guests پر install کرتا ہے؛ `linux_ipa_ssh_bootstrap_password` وہ shared first-touch password fallback بھی ہے جو runtime Linux guests کے لیے key bootstrap disabled ہونے پر بھی استعمال ہو سکتا ہے
- Linux IPA enrollment، FreeIPA JSON-RPC timeout کے ساتھ fail ہونے والے upstream client joins کو retry کرتی ہے، اور سست یا مصروف IPA environments کے لیے `linux_ipaclient_kinit_attempts` expose کرتی ہے
- Linux IPA enrollment default طور پر `ipa_servers` inventory hostnames کو بھی join server list میں merge کرتی ہے، تاکہ clients ایک single configured endpoint کے بجائے پورا IPA server set استعمال کر سکیں
- جب ایک سے زیادہ IPA servers دستیاب ہوں، تو Linux client enrollment کے دوران ہر retry pass ان IPA server candidates کو ایک ایک کر کے آزمانے کی کوشش کرتا ہے
- combined `site` workflow پہلے FreeIPA hostgroups create کرتی ہے، پھر Linux enrollment کے بعد enrolled runtime hosts کو ان میں شامل کرتی ہے، تاکہ pre-enrollment runs ان guests کے لیے hostgroup membership پر fail نہ ہوں جو ابھی enroll نہیں ہوئے

## کنفیگریشن کا دائرہ

زیادہ تر values یہاں رہتی ہیں:

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

file-by-file layout کے لیے [docs/VARIABLES.md](../../docs/VARIABLES.md) دیکھیں۔

اہم variable families:

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

## گروپ حکمت عملی کی مثال

ایک سادہ pattern جو اچھی طرح scale کرتا ہے:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- Sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa` کے لیے Proxmox ACL binding

جب آپ چاہتے ہوں کہ combined `site.yml` run مخصوص IPA users کو managed `linux-ssh-admins` group کے ذریعے خودکار طور پر Linux SSH اور sudo access دے، تو [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) میں `freeipa_linux_admin_users` populate کریں۔

یاد رکھیں کہ Proxmox LDAP sync، suffix کے ساتھ synced groups بناتی ہے:

```text
<group-name>-<realm>
```

اگر آپ کی FreeIPA group `proxmox-admins` ہو اور Proxmox realm `ipa` ہو، تو synced PVE group یہ بنے گی:

```text
proxmox-admins-ipa
```

## سکیورٹی

- تمام secrets کو plaintext inventory variable files کے بجائے `vault-freeipa.yml` اور `vault-proxmox.yml` میں رکھیں
- Proxmox کے لیے dedicated read-only LDAP bind account کو ترجیح دیں
- TLS کو certificate verification enabled کے ساتھ ترجیح دیں
- disposable lab environments کے باہر SSH host key checking کو enabled رکھیں
- جب Proxmox guests میں پہلے سے working QEMU Guest Agent موجود ہو تو shared temporary passwords کے بجائے `linux_ipa_qga_ssh_bootstrap_enabled` کو ترجیح دیں
- `guest_qemu_agent_install_enabled` صرف اسی وقت استعمال کریں جب repository کے پاس پہلے سے guest کے اندر جانے کا valid management path ہو؛ Proxmox discovery میں اس کا مطلب ہے کہ QGA پہلے سے چل رہی ہو یا `linux_ipa_proxmox_discovery_ansible_user` کے ساتھ password یا key access configured ہو
- اگر آپ Linux SSH bootstrap enable کرتے ہیں، تو کسی بھی shared bootstrap password کو vaulted variables میں رکھیں اور key-based access قائم ہونے کے بعد اسے rotate یا remove کر دیں
- IPA admin account کو Proxmox LDAP bind account کے طور پر دوبارہ استعمال نہ کریں
- production rollout سے پہلے `proxmox_ldap_filter` اور `proxmox_ldap_group_filter` کو review کریں تاکہ بہت زیادہ objects import نہ ہو جائیں

ایسی disposable lab کے لیے جہاں آپ واضح طور پر SSH host verification bypass کرنا چاہتے ہوں، repository defaults بدلنے کے بجائے فی shell session opt out کریں:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## آئیڈیمپوٹنسی اور احتیاطیں

یہ project دوبارہ قابلِ استعمال اور زیادہ تر idempotent رہنے کے لیے لکھی گئی ہے، مگر production rollout سے پہلے اسے lab میں test کرنا پھر بھی ضروری ہے۔

معروف caveats:

- Proxmox CLI output مختلف releases میں معمولی فرق رکھ سکتی ہے
- FreeIPA directory layouts لچکدار ہوتی ہیں، اس لیے LDAP filters کو آپ کے tree کے لیے tune کرنے کی ضرورت پڑ سکتی ہے
- موجودہ hand-managed PVE ACLs اور roles کو automation apply کرنے سے پہلے compare کیا جانا چاہیے
- Proxmox VM auto-discovery running guests اور QEMU guest-agent network data پر منحصر ہوتی ہے
- IP-only guest definitions کو پھر بھی guest کے اندر valid final hostname یا explicit `ipa_hostname` چاہیے ہوتا ہے
- Proxmox plays privilege escalation کے ساتھ چلتی ہیں، اس لیے non-root SSH user کے پاس working `sudo` ہونا چاہیے اور جب تک اس user کے پاس passwordless sudo نہ ہو آپ کو `-K` کے ساتھ become password دینا ہوگا
- اگر آپ `ansible_become_password` کو `vault-proxmox.yml` میں store کرتے ہیں تو `-K` چھوڑ سکتے ہیں، کیونکہ Ansible encrypted variable سے sudo password خود پڑھ لے گی

## تصدیق

کامیاب rollout کے بعد یہ فرض کرنے کے بجائے کہ ہر access path درست ہے، نتیجے میں بننے والی state کو verify کریں۔

### FreeIPA میں

- تصدیق کریں کہ متوقع user groups موجود ہیں
- تصدیق کریں کہ متوقع hostgroups موجود ہیں
- تصدیق کریں کہ متوقع HBAC rules موجود اور enabled ہیں
- تصدیق کریں کہ متوقع sudo rules موجود اور enabled ہیں

### Proxmox میں

- تصدیق کریں کہ LDAP realm موجود ہے
- تصدیق کریں کہ initial sync نے متوقع users یا groups import کیے ہیں
- تصدیق کریں کہ مطلوبہ synced group کے پاس متوقع ACL binding ہے

### لینکس گیسٹ پر

- تصدیق کریں کہ allowed IPA user login کر سکتا ہے
- تصدیق کریں کہ disallowed user کو HBAC بلاک کرتی ہے
- تصدیق کریں کہ allowed IPA admin `sudo -l` چلا سکتا ہے
- تصدیق کریں کہ اگر `linux_ipaclient_mkhomedir` enabled ہو تو پہلی login پر home directory create ہو جاتی ہے

## ریپوزٹری ساخت

<details>
<summary>Repository layout دکھائیں</summary>

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

## ترقی

اس repository میں شامل helper files:

- `.editorconfig` مختلف editors میں whitespace، encoding، اور line-ending defaults کو consistent رکھتی ہے
- `.gitattributes` عام text files کو LF line endings پر برقرار رکھتی ہے
- `.gitignore` generated inventory، vault data، local collections، اور editor files کو Git سے باہر رکھتی ہے
- `.ansible-lint` vendored collections کو exclude کرتی ہے اور صرف YAML line-length rule کو suppress کرتی ہے
- `.yamllint` playbooks، inventories، اور workflow files میں YAML formatting checks کو consistent رکھتی ہے
- `.github/CODEOWNERS` repository کے اہم حصوں کے لیے review ownership route کرتی ہے
- `.github/workflows/ci.yml` pushes اور pull requests پر repository lint checks اور smoke validation چلاتی ہے
- `.pre-commit-config.yaml` جب `pre-commit` installed ہو تو commits سے پہلے fast lint hook چلاتی ہے
- `CHANGELOG.md` repository کی notable changes کو ایک جگہ track کرتی ہے
- `docs/VARIABLES.md` split inventory variable layout کی وضاحت کرتی ہے
- `docs/i18n/` میں translated README files رکھی جاتی ہیں جنہیں مکمل English section structure کی mirror ہونا چاہیے، جبکہ `README.md` canonical source رہتی ہے
- `docs/i18n/TRANSLATION_GUIDE.md` بتاتی ہے کہ translated README files کو sync میں کیسے رکھا جائے
- `scripts/bootstrap.ps1` اور `scripts/bootstrap.sh` required collection کو repo-local `collections/` path میں install کرتے ہیں اور اسے ansible-core 2.24+ compatibility کے لیے patch کرتے ہیں
- `scripts/patch_freeipa_collection.py` pinned FreeIPA collection میں deprecated imports کو rewrite کرتی ہے تاکہ یہ future ansible-core releases کے ساتھ compatible رہے
- `scripts/lint.py` local use، CI، اور pre-commit کے لیے cross-platform lint entrypoint فراہم کرتی ہے
- `scripts/smoke-test.py` example inventory کو validate کرتی ہے اور اصل infrastructure کو چھوئے بغیر syntax checks چلاتی ہے، جس میں الگ Windows playbook بھی شامل ہے
- `scripts/check_translations.py` translated README files کی metadata، section-structure parity، اور canonical English README کے مقابلے minimum content coverage کا audit کرتی ہے
- `scripts/lint.ps1` اور `scripts/lint.sh` مشترک local lint اور smoke workflow چلاتی ہیں
- `scripts/proxmox_event_webhook.py` Proxmox VM events کے لیے optional controller-side webhook چلاتی ہے
- `scripts/proxmox-vm-hook.pl` optional Proxmox VM hookscript ہے جو `post-start` اور `post-migrate` پر controller webhook کو notify کرتی ہے
- `scripts/run-playbook.ps1` PowerShell users کے لیے common `ansible-playbook` commands wrap کرتی ہے، جس میں الگ Windows workflow بھی شامل ہے
- `scripts/vault.ps1` اور `scripts/vault.sh` FreeIPA، Proxmox، اور optional Windows secrets کے لیے عام split-vault operations wrap کرتی ہیں
- `tests/` repository کے verification surface کو رکھتا ہے، ابتداء smoke-test documentation سے ہوتی ہے
- `CONTRIBUTING.md` متوقع contribution اور validation workflow کو document کرتی ہے
- `SECURITY.md` vulnerabilities report کرنے اور security-sensitive information handle کرنے کا طریقہ document کرتی ہے

اگر `ansible-lint` آپ کے controller پر installed ہے:

```bash
ansible-lint
```

repository smoke checks کو براہِ راست چلانے کے لیے:

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

مکمل local lint pass کے لیے:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

ہر commit سے پہلے fast lint hook enable کرنے کے لیے:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper اب common operator options کو براہِ راست بھی support کرتی ہے:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## اگلی توسیعات

عام follow-up improvements جو آپ بعد میں چاہ سکتے ہیں:

- IPA-ready Linux templates کے لیے Packer image pipeline
- AWX job templates اور schedules
- الگ Proxmox tenant اور pool models
- زیادہ وسیع Windows local policy یا GPO integration

## لائسنس

یہ project [MIT License](../../LICENSE) کے تحت جاری کیا گیا ہے۔
