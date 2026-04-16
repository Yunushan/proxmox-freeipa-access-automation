# خودکارسازی دسترسی Proxmox + FreeIPA

این صفحه یک ترجمه کاملِ ساختاری از [README.md](../../README.md) ارائه می‌کند. نسخه انگلیسی منبع canonical باقی می‌ماند، اما این فایل همان بخش‌های اصلی را برای خواننده فارسی پوشش می‌دهد.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## زبان‌ها

نسخه انگلیسی منبع canonical این مستندات است. READMEهای ترجمه‌شده کامل دیگر را می‌توانید در فهرست ترجمه‌ها ببینید.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [نمایه ترجمه‌ها](README.md) | [راهنمای ترجمه](TRANSLATION_GUIDE.md)

این repository، **FreeIPA را منبع حقیقت** برای هویت و دسترسی در نظر می‌گیرد. Proxmox این دایرکتوری را از طریق LDAP realm مصرف می‌کند، مهمان‌های Linux با role بالادستی `ipaclient` به FreeIPA می‌پیوندند، و دسترسی به‌جای پراکندگی در حساب‌های محلی هر ماشین، از طریق گروه‌های syncشده، HBAC و قوانین `sudo` متمرکز می‌ماند.

> [!IMPORTANT]
> این پروژه **از FreeRADIUS به‌عنوان منبع هویت استفاده نمی‌کند**، **داخل هر VM کاربر محلی نمی‌سازد**، و **قصد ندارد همه edge caseهای ممکن در permissionهای Proxmox را پوشش دهد**.

## چرا این پروژه وجود دارد

از این مخزن زمانی استفاده کنید که از قبل داشته باشید:

- یک محیط سالم FreeIPA
- یک کلاستر Proxmox VE
- مهمان‌های Linux که باید احراز هویت متمرکز داشته باشند
- یک حساب سرویس اختصاصی برای LDAP bind در Proxmox
- یک مدل روشن از گروه‌های ادمین و اپراتور

ایده اصلی این است که FreeIPA منبع حقیقت برای هویت و دسترسی باشد. Proxmox این دایرکتوری را از طریق LDAP realm مصرف می‌کند، مهمان‌های Linux با role `ipaclient` به FreeIPA می‌پیوندند، و کنترل SSH، HBAC و `sudo` متمرکز باقی می‌ماند.

این repository زمانی انتخاب مناسبی است که بخواهید onboarding و offboarding تقریباً این‌گونه پیش برود:

1. ساختن یا به‌روزرسانی userها و groupها در FreeIPA
2. sync کردن این هویت‌ها به Proxmox
3. اعمال roleها و ACLهای Proxmox بر اساس groupهای syncشده
4. دادن دسترسی به مهمان‌های Linux از طریق login در FreeIPA، قوانین HBAC و `sudo`

## چه چیزی دریافت می‌کنید

- مدیریت گروه‌های کاربری، hostgroupها، قوانین HBAC و قوانین `sudo` در FreeIPA
- login-shellهای پیش‌فرض خودکار FreeIPA برای userهای ادمین Linux
- پیکربندی Proxmox LDAP realm در برابر FreeIPA
- همگام‌سازی دوره‌ای realm از یک گره مشخص کلاستر
- RBAC bindings در Proxmox برای گروه‌های همگام‌شده
- enrollment لینوکس از inventory ایستا، تعریف‌های دستی یا Proxmox discovery
- SSH bootstrap اختیاری بدون reboot از طریق QEMU Guest Agent
- فعال‌سازی اختیاری ارتباط guest-agent از سمت Proxmox برای مهمان‌های Linux که پشت Proxmox هستند
- نصب اختیاری QEMU Guest Agent از طریق SSH یا WinRM برای مهمان‌های قابل دسترس
- گزارش readiness اختیاری Linux برای وضعیت SSH و QEMU Guest Agent در Proxmox
- workflow اختیاری و جداگانه برای Windows domain membership روی مهمان‌های Windows 10/11 و Windows Server از طریق Active Directory
- workflow اختیاری و محدودِ helperهای آگاه از FreeIPA برای Windows جهت IPA CA trust، hosts bootstrap و بررسی reachability
- bootstrap اختیاری کلید عمومی SSH برای first-touch
- refresh خودکار کش SSSD پس از تغییرات مدل دسترسی
- onboarding اختیاری event-driven برای `post-start` و `post-migrate`

## دامنه

| شامل | شامل نمی‌شود |
| --- | --- |
| مدل دسترسی FreeIPA | استقرار FreeRADIUS |
| راه‌اندازی Proxmox LDAP realm | ایجاد کامل چرخه عمر کاربر در FreeIPA |
| Proxmox RBAC از گروه‌های sync شده | پوشش کامل همه سناریوهای multi-tenant در Proxmox |
| Linux IPA enrollment | login بومی Windows مستقیماً در برابر FreeIPA |
| workflow جداگانه Windows AD domain-membership | GPO یا اتوماسیون گسترده‌تر چرخه عمر objectهای AD |
| workflow محدود helperهای FreeIPA-aware برای Windows | وانمود کردن به این‌که helperهای FreeIPA-only برای Windows معادل AD هستند |

## فرایند کاری ویندوز

Windows در این repository یک workflow مستقل و محدودتر از Linux دارد.

- `playbooks/windows-management.yml` برای Windows domain membership با role `windows_domain_membership` استفاده می‌شود
- `playbooks/windows-freeipa-helpers.yml` برای helperهای آگاه از FreeIPA روی Windows استفاده می‌شود، مانند تست دسترسی DNS/HTTPS/TCP، نصب یا تنظیم OpenSSH، trust کردن CA، و entries محلی `hosts`
- `playbooks/windows-freeipa-validate.yml` مسیر helper-only را فقط validate می‌کند و تغییر واقعی روی guest اعمال نمی‌کند
- مسیر helper ویندوز برای login تعاملی domain از FreeIPA بدون Active Directory طراحی نشده است
- اگر به login واقعی ویندوز برای workstationها و serverها نیاز دارید، رویکرد توصیه‌شده Active Directory domain join یا FreeIPA-AD trust است
- `windows_qemu_guest_agent_clients` فقط برای نصب QEMU Guest Agent روی guestهای Windows قابل دسترس استفاده می‌شود
- `windows_management_clients` و `windows_freeipa_helper_clients` عمداً از گروه‌های Windows جدا نگه داشته شده‌اند تا playbooks از Linux enrollment مستقل بمانند

این workflow مهمان‌های Windows 10/11 و Windows Server را هدف می‌گیرد که از طریق WinRM یا PSRP قابل دسترس باشند.

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

برای توضیح طراحی مفصل‌تر، [docs/ARCHITECTURE.md](../ARCHITECTURE.md) را ببینید.

## پیش‌نیازها

### کنترلر

- Ansible Core 2.14+
- دسترسی SSH به گره اصلی Proxmox، سرورهای IPA و کلاینت‌های Linux
- وقتی workflow ویندوز را استفاده می‌کنید، دسترسی WinRM یا PSRP به مهمان‌های Windows
- `sudo` یا `root` در جاهایی که لازم است
- اگر QGA SSH bootstrap فعال است، QEMU Guest Agent باید از قبل در guest فعال باشد
- اگر Windows fallback فعال است، میزبان‌های قابل دسترس باید در `windows_qemu_guest_agent_clients` باشند
- اگر Windows domain membership فعال است، میزبان‌های قابل دسترس باید در `windows_management_clients` قرار بگیرند و باید credentialهای join به AD را هم فراهم کنید
- اگر helperهای FreeIPA برای Windows فعال هستند، میزبان‌های قابل دسترس باید در `windows_freeipa_helper_clients` قرار بگیرند
- اگر Linux SSH bootstrap فعال است، controller به SSH keypair و مسیر اولیه مبتنی بر گذرواژه نیاز دارد

### اهداف

- Proxmox VE 6.x یا جدیدتر روی میزبان `proxmox_primary`
- FreeIPA قابل دسترس از Proxmox و Linux clients
- مهمان‌های Windows 10/11 و Windows Server وقتی از طریق WinRM یا PSRP قابل دسترس باشند، می‌توانند با workflow مستقل ویندوز مدیریت شوند
- DNS و همگام‌سازی زمان درست
- برای `proxmox_primary` از `root` یا کاربری استفاده کنید که `pveversion`, `pvesh`, `pveum` را با `sudo` اجرا می‌کند
- اگر Windows domain membership را استفاده می‌کنید، مهمان‌های هدف Windows باید بتوانند به domain controllerهای AD مربوطه برسند
- اگر workflow محدود helperهای FreeIPA برای Windows را استفاده می‌کنید، مهمان‌های هدف Windows باید بتوانند به سرورهای IPA مربوطه برسند
- در Proxmox discovery، guest باید IP قابل استفاده از طریق QEMU Guest Agent ارائه کند

## پورت‌های شبکه

این جدول پورت‌های شبکه‌ای را نشان می‌دهد که controller این repository، automation مربوط به Proxmox LDAP و مسیر Linux IPA enrollment از آن‌ها استفاده می‌کنند.
این فهرست عمداً محدود به همین پروژه است، نه کل ماتریس replication بین سرورهای FreeIPA.

| نام | پورت | پروتکل | مبدأ | مقصد | زمان نیاز | هدف |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | کنترلر Ansible | گره Proxmox، سرور IPA، مهمان Linux | همیشه | اتصال Ansible |
| WinRM | `5985`, `5986` | `TCP` | کنترلر Ansible | مهمان Windows | وقتی Windows management فعال است | اتصال Ansible به مهمان‌های Windows |
| DNS | `53` | `TCP`, `UDP` | مهمان Linux | سرورهای IPA DNS | وقتی مهمان‌های Linux از IPA DNS استفاده می‌کنند | resolve کردن رکوردهای IPA و نام‌های بیرونی |
| Kerberos | `88` | `TCP`, `UDP` | مهمان Linux | سرورهای IPA | Linux IPA enrollment و login | احراز هویت Kerberos |
| LDAP | `389` | `TCP` | مهمان Linux | سرورهای IPA | Linux IPA enrollment و login | LDAP و FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port` با پیش‌فرض `443` | `TCP` | مهمان Linux | سرورهای IPA | Linux IPA enrollment | راستی‌آزمایی IPA web/API هنگام نصب client |
| Kerberos Password | `464` | `TCP`, `UDP` | مهمان Linux | سرورهای IPA | Linux IPA enrollment و عملیات گذرواژه | عملیات Kerberos password و keytab |
| LDAPS | `636` | `TCP` | گره اصلی Proxmox | سرورهای IPA/LDAP | Proxmox LDAP realm در حالت پیش‌فرض `ldaps` | اتصال Proxmox LDAP realm |

نکات:

- `LDAPS 636/TCP` مقدار پیش‌فرض repository است، چون `proxmox_ldap_mode` به‌طور پیش‌فرض `ldaps` است. اگر mode یا port مربوط به LDAP را تغییر دهید، به‌جای آن باید `proxmox_ldap_port` پیکربندی‌شده را باز کنید.
- بسته به transport ویندوز شما، `WinRM` معمولاً برای HTTPS از `5986/TCP` و برای HTTP از `5985/TCP` استفاده می‌کند.
- `DNS 53/TCP,UDP` فقط وقتی لازم است که مهمان‌های Linux از سرورهای IPA به‌عنوان DNS resolver استفاده کنند.
- `Kerberos 88` و `Kerberos Password 464` هر دو به `TCP` و `UDP` نیاز دارند.
- Windows domain join به Active Directory همچنین به مجموعه معمول پورت‌های Windows-to-domain-controller نیاز دارد، اما این ماتریس به‌شدت environment-specific است و عمداً اینجا به‌صورت کامل فهرست نشده است.
- همگام‌سازی زمان همچنان برای کارکرد قابل اعتماد Kerberos لازم است، اما منبع NTP وابسته به محیط است و توسط این repository مدیریت نمی‌شود.

## سازگاری

- automation مربوط به Proxmox در این repository حول interfaceهای realm و RBAC در `pveum` و `pvesh` نوشته شده که در Proxmox VE 6.x و نسخه‌های بعدی استفاده می‌شوند
- نسخه‌های major پیش‌فرض: `6`, `7`, `8`, `9`, `10`
- validation نسخه تشخیص‌داده‌شده Proxmox را با `pveversion` بررسی می‌کند
- اگر لازم باشد فهرست نسخه‌های پشتیبانی‌شده را در محیط خود محدودتر یا گسترده‌تر کنید، می‌توانید آن را با `proxmox_supported_major_versions` override کنید
- `proxmox_allow_future_major_versions` به‌طور پیش‌فرض `true` است
- بنابراین majorهایی که از بالاترین نسخه تست‌شده فهرست‌شده جدیدتر باشند نیز به‌صورت پیش‌فرض از validation عبور می‌کنند
- major versionهای آینده همچنان باید تا زمانی که interface واقعی Proxmox در آن release با این automation سنجیده شود، صرفاً compatibility candidate در نظر گرفته شوند
- majorهای قدیمی‌تر مانند `1` تا `5` در این repository عمومی به‌عنوان پشتیبانی‌شده و تست‌شده ادعا نمی‌شوند؛ اگر آن‌ها را به‌صورت محلی اضافه می‌کنید، این کار را یک compatibility override صریح بدانید و ابتدا کل workflow را در lab validate کنید

نمونه override محلی برای یک محیط آزمایشگاهی legacy:

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

## شروع سریع

نمونه‌های زیر از shell commands استفاده می‌کنند. در جاهایی که مهم است، معادل PowerShell هم آمده است.

### 1. فایل‌های نمونه اینونتوری و والت را کپی کنید

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

### 2. فایل‌های وابسته به محیط را ویرایش کنید

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` وقتی از Windows management استفاده می‌کنید
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` وقتی از Windows management استفاده می‌کنید

علاوه بر تنظیمات IPA و Proxmox، یکی از حالت‌های منبع مهمان Linux را انتخاب کنید:

- ورودی‌های ایستا زیر `linux_ipa_clients`
- تعریف‌های `linux_ipa_client_hosts` در `group_vars/all/30-linux-clients.yml`
- Proxmox VM discovery با `linux_ipa_proxmox_discovery_enabled: true`

برای Linux IPA enrollment، مقدار domain و server را از هم جدا نگه دارید:

- `ipaclient_domain` دامنه مشترک DNS در IPA است، مانند `example.com`
- `linux_ipa_servers` شامل hostnameهای سرور IPA است، مانند `ipa01.example.com`

اگر می‌خواهید به‌جای `root` با یک کاربر معمولیِ sudo-capable به Proxmox وصل شوید، آن را در `hosts.yml` زیر `proxmox_primary` تنظیم کنید و گذرواژه sudo را در `vault-proxmox.yml` نگه دارید:

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

در این setup، `vault_proxmox_become_password` همان گذرواژه‌ای است که معمولاً برای `sudo` روی میزبان Proxmox وارد می‌کنید.

### 3. فایل‌های والت را رمزگذاری کنید

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

اگر workflow اختیاری Windows را فعال می‌کنید، `inventories/production/group_vars/all/vault-windows.yml` را هم به همین command اضافه کنید.

یا از wrapperهای helper استفاده کنید که به‌طور پیش‌فرض vault IDهای جداگانه دارند و در صورت نیاز فایل‌های working vault را از templateهای نمونه می‌سازند:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

اگر هنگام اجرای playbookها برای هر domain گذرواژه جداگانه می‌خواهید، vault IDها را به `--ask-vault-pass` ترجیح دهید:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

اگر workflow اختیاری Windows هم گذرواژه vault مستقل دارد، `windows@prompt` را هم به همان command اضافه کنید.

فقط وقتی از `-AskVaultPass` استفاده کنید که همه vault fileهای مورد استفاده در آن playbook یک گذرواژه مشترک داشته باشند.

### 4. کالکشن مورد نیاز را نصب کنید

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

یا مستقیم:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

اگر `freeipa.ansible_freeipa` را قبل از اضافه شدن patch سازگاری در این repository نصب کرده‌اید، یکی از helperهای bootstrap را دوباره اجرا کنید یا `python .\scripts\patch_freeipa_collection.py` را یک بار به‌صورت دستی اجرا کنید تا نصب موجود هم patch شود.

وقتی از `scripts/run-playbook.ps1` استفاده می‌کنید، helper patch قبل از `ansible-playbook` به‌صورت خودکار اجرا می‌شود.

### 5. ابتدا اعتبارسنجی را اجرا کنید

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

اگر می‌خواهید فقط مسیر helper-only مربوط به Windows FreeIPA را validate کنید، بدون اعمال تغییر روی host:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

اگر یک audit فقط-خواندنی Linux readiness می‌خواهید که نشان دهد کدام guestهای runtime از طریق SSH reachable هستند و کدام guestهای کشف‌شده از Proxmox از طریق QEMU Guest Agent پاسخ می‌دهند:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

گزارش readiness به‌طور پیش‌فرض در `.ansible/linux-readiness-report.json` نوشته می‌شود.
فیلدهای اصلی را این‌گونه تفسیر کنید:

- `ssh.ready=true`: مسیر SSH تنظیم‌شده فعلی برای Ansible از سمت controller جواب داده است
- `ssh.promptless=true`: probe مربوط به SSH بدون `ansible_password` موفق شده، پس مسیر برای Ansible غیرتعاملی است
- `ssh.auth_mode=password_configured`: چون host دارای `ansible_password` بوده، probe از `sshpass` استفاده کرده است
- `ssh.auth_mode=key_or_agent`: probe در حالت batch و بدون `ansible_password` موفق شده است
- `qga.status=available`: دستور `qm guest ping` روی گره صاحب VM موفق بوده است
- `qga.status=disabled`: در تنظیمات Proxmox برای آن VM، QEMU Guest Agent فعال نیست
- `qga.status=configured_unresponsive`: guest agent در تنظیمات Proxmox فعال است، ولی پاسخ نمی‌دهد
- `qga.status=node_unreachable`: controller برای probe نتوانسته به گره Proxmox صاحب آن VM برسد
- `qga.status=not_applicable`: host از طریق Proxmox discovery ساخته نشده، پس probe مربوط به QGA انجام نشده است

نمونه بازرسی سریع:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. اختیاری: تغییرات برنامه‌ریزی‌شده را preview کنید

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> check mode را یک preview جزئی در نظر بگیرید، نه یک شبیه‌سازی کامل. این repository بخشی از پیکربندی Proxmox را با CLI مستقیم و Linux enrollment را با role بالادستی FreeIPA client انجام می‌دهد، بنابراین `--check` مفید است ولی authoritative نیست.
>
> برای FreeIPA HBAC rules، check mode مرحله تعریف rule را validate می‌کند ولی action بعدیِ enable یا disable را skip می‌کند. این کار از failureهای کاذب جلوگیری می‌کند؛ جاهایی که FreeIPA در dry run به‌دلیل ساخته‌نشدن واقعی rule آن را missing گزارش می‌کند.
>
> role مربوط به Proxmox realm sync timer هم در check mode آخرین مرحله enable یا start کردن `systemd` را skip می‌کند، چون در dry run فایل‌های unit diff می‌شوند ولی واقعاً نوشته نمی‌شوند.
>
> Linux IPA enrollment هم در check mode اجرا نمی‌شود. repository همچنان discovery، hostname resolution و input validation را انجام می‌دهد، اما role بالادستی `ipaclient` در dry run اجرا نمی‌شود.

### 7. پیکربندی کامل را اعمال کنید

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

اگر workflow اختیاری Windows فعال باشد و `vault-windows.yml` گذرواژه جداگانه داشته باشد، همین playbook را با `--vault-id windows@prompt` اجرا کنید یا در wrapper پاورشل از `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` استفاده کنید، نه `--ask-vault-pass`.

## ترتیب rollout

برای اولین deployment، stack را به این ترتیب اعمال کنید:

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

این ترتیب troubleshooting را خیلی ساده‌تر از اجرای هم‌زمان همه چیز می‌کند.

برای یک rollout محدود در PowerShell، مثلاً فقط یک مهمان Linux:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

کنترل‌های rollout پیش‌فرض محافظه‌کارانه هستند:

- تغییرات FreeIPA access با `serial: 1` اجرا می‌شوند
- تغییرات Proxmox با `serial: 1` اجرا می‌شوند
- hostname resolution، validation و enrollment برای Linux با `serial: 10` اجرا می‌شوند
- تغییرات Windows management با `serial: 10` اجرا می‌شوند
- همه مسیرهای rollout به‌طور پیش‌فرض `max_fail_percentage: 0` دارند

این مقادیر را در `inventories/production/group_vars/all/15-rollout.yml` تنظیم کنید.

## مدل tag

به‌جای ساخت playbookهای بیشتر، از tagها برای هدف‌گیری sliceهای پایدار rollout استفاده کنید.

- دامنه‌های اصلی: `freeipa`, `proxmox`, `linux`, `validate`
- دامنه Windows: `windows`, `windows_domain`
- Windows FreeIPA helpers: `windows`, `windows_freeipa`
- مدل FreeIPA: `freeipa_access`
- زیرمجموعه‌های Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- آماده‌سازی Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- enrollment لینوکس: `linux_enroll`
- مدیریت VM مبتنی بر رویداد: `event`, `linux_refresh`

نمونه‌ها:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## VM onboarding مبتنی بر رویداد

اگر می‌خواهید Proxmox بلافاصله پس از start یا migration یک VM، Linux discovery و IPA enrollment را trigger کند، از workflow اختیاری hook/webhook که در [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../../docs/EVENT_DRIVEN_VM_ONBOARDING.md) توضیح داده شده استفاده کنید.

این workflow از یک event playbook مستقل در `playbooks/proxmox-vm-event.yml` استفاده می‌کند تا مسیر trigger فقط سمت Linux و FreeIPA را برای guestها handle کند. بنابراین در هر VM event، دوباره automation مربوط به Proxmox LDAP realm یا RBAC اجرا نمی‌شود.

این repository اکنون می‌تواند همین stack اختیاری hook/webhook را از `site.yml` یا `proxmox.yml` هم deploy کند، به‌شرط آن‌که `proxmox_vm_event_onboarding_enabled: true` باشد و متغیرهای لازم برای webhook هم تنظیم شده باشند.

hookهای Proxmox برای VM یک phase مستقل به نام `create` ارائه نمی‌کنند. در عمل، VMهای جدید در اولین `post-start` گرفته می‌شوند و hookهای migration می‌توانند هم روی source node و هم target node trigger شوند.

## مدل اینونتوری

این repository از شش inventory group ازپیش‌تعریف‌شده و یک runtime group تولیدشده استفاده می‌کند:

- `ipa_servers`: یک یا چند FreeIPA server
- `proxmox_primary`: یک گره Proxmox که برای ownership تنظیمات realm و timer همگام‌سازی دوره‌ای انتخاب می‌شود
- `linux_ipa_clients`: گروه source declarative برای مهمان‌های Linux
- `linux_ipa_clients_runtime`: گروه runtime تولیدشده که از inventory ایستا، تعریف‌های دستی و Proxmox discovery اختیاری ساخته می‌شود
- `windows_qemu_guest_agent_clients`: گروه اختیاری Windows برای نصب QEMU Guest Agent
- `windows_management_clients`: گروه اختیاری Windows برای workflow مستقل domain membership
- `windows_freeipa_helper_clients`: گروه اختیاری Windows برای workflow محدود helperهای آگاه از FreeIPA

شما می‌توانید inventory groupهای خودتان را هم اضافه کنید و آن‌ها را در تعریف hostgroupهای FreeIPA reference کنید. وقتی می‌خواهید کل مجموعه آماده‌شده مهمان‌های Linux را در hostgroupهای FreeIPA استفاده کنید، `linux_ipa_clients_runtime` را reference کنید.

> [!IMPORTANT]
> FreeIPA همچنان به hostname نهایی هر guest نیاز دارد. اگر از targetهای IP-only یا Proxmox discovery استفاده می‌کنید، یا `ipa_hostname` را explicit تنظیم کنید یا مطمئن شوید که `hostname -f` روی خود guest، FQDN نهایی را برمی‌گرداند. playbookها اکنون قبل از ساختن membership مربوط به FreeIPA hostgroup، آن hostname را resolve می‌کنند.

> [!TIP]
> یک golden template قابل‌استفاده مجدد را داخل FreeIPA enroll نکنید. ابتدا VM را clone کنید، hostname نهایی را بدهید و سپس guest حاصل را enroll کنید.

### حالت‌های منبع Linux

شما می‌توانید `linux_ipa_clients` را به سه روش مختلف populate کنید.

#### 1. میزبان‌های ایستا در inventory

وقتی از قبل نام guestها را می‌دانید، از ورودی‌های معمولی inventory در Ansible استفاده کنید:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. تعریف‌های دستی میزبان در متغیرها

وقتی می‌خواهید guestها را بیرون از `hosts.yml` نگه دارید یا فقط IP در اختیار دارید، از `linux_ipa_client_hosts` استفاده کنید:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

نکته‌ها:

- اگر `name` یک hostname یا FQDN قابل resolve باشد، `ansible_host` اختیاری است
- اگر فقط IP را می‌دانید، برای `name` هر alias پایدار و قابل‌تشخیصی را استفاده کنید
- وقتی `ipa_hostname` تنظیم نشده باشد، playbook از `hostname -f` روی خود guest استفاده می‌کند

#### 3. کشف خودکار Proxmox VM

وقتی می‌خواهید playbook مهمان‌های Linux را از یک یا چند گره Proxmox به‌صورت خودکار بخواند، discovery را استفاده کنید:

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

نکته‌ها:

- discovery، VMها را به همان گروه `linux_ipa_clients_runtime` اضافه می‌کند که سایر playbookها استفاده می‌کنند
- کشف IP به داده interfaceهای شبکه که توسط QEMU guest agent گزارش می‌شود وابسته است
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` فقط به نام VMهایی اعتماد می‌کند که از قبل FQDN باشند
- اگر می‌خواهید نام‌های کوتاه و امن Proxmox مانند `Teleport-Server-1` به‌طور خودکار از طریق `linux_ipa_identity_hostname_suffix` به hintهایی مانند `teleport-server-1.example.com` تبدیل شوند، `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` را تنظیم کنید
- `linux_ipa_proxmox_discovery_vmids` اختیاری است و بیشتر برای محدود کردن discovery در workflow مبتنی بر event به یک یا چند VMID مشخص استفاده می‌شود
- guest همچنان باید hostname نهایی داشته باشد؛ یا از قبل داخل VM تنظیم شده باشد یا با `ipa_hostname` در تعریف دستی داده شود
- hostname واقعی سیستم guest هم باید برای enrollment معتبر باشد؛ مقادیر placeholder مانند `localhost.localdomain` باید قبل از اجرای `linux-clients` یا `site` روی خود VM اصلاح شوند
- وقتی guestها از hostnameهای کوتاه مانند `app-server-01` استفاده می‌کنند، می‌توانید `linux_ipa_identity_hostname_suffix` و در صورت نیاز `linux_freeipa_enroll_manage_hostname: true` را تنظیم کنید تا پروژه پیش از enrollment یک hostname کامل مانند `app-server-01.example.net` را resolve و اعمال کند
- وقتی DNS مربوط به hostnames مهمان‌ها به‌صورت authoritative در FreeIPA مدیریت می‌شود، می‌توانید `linux_freeipa_enroll_manage_authoritative_dns: true` را تنظیم کنید تا پروژه رکوردهای A و PTR همان guest را repair کند و رکوردهای AAAA مربوط به `fe80::/10` را قبل از enrollment حذف کند
- وقتی DNS هنوز آماده نیست، می‌توانید `linux_ipa_manage_etc_hosts: true` را همراه با `linux_ipa_etc_hosts_entries` استفاده کنید تا role یک block مدیریت‌شده در `/etc/hosts` برای serverهای IPA و FQDNهای guest بسازد
- `guest_qemu_agent_install_enabled` روی guestهایی که از قبل از طریق SSH یا WinRM reachable هستند QEMU Guest Agent را نصب می‌کند، بعداً در همان workflow روی guestهای Linux که تازه reachable شده‌اند دوباره تلاش می‌کند، و پس از Linux enrollment هم یک بار دیگر retry می‌کند
- برای اینکه discovery روشن بماند اما فقط subset محدودی از guestها وارد inventory runtime لینوکس شوند، `linux_ipa_proxmox_discovery_allowlist_enabled: true` را تنظیم کنید؛ allowlist می‌تواند بر اساس VMID، IP و name دقیق match کند
- وقتی روی همان nodeهای discovery-enabled، VMهای زیرساختی مثل firewall یا DNS server هم وجود دارند که نباید هرگز Linux IPA automation دریافت کنند، از `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips` یا `linux_ipa_proxmox_discovery_blacklist_names` استفاده کنید؛ blacklist همیشه نسبت به broad discovery یا allowlist اولویت دارد
- برای مهمان‌های Linux کشف‌شده از Proxmox که هنوز guest agent کاری ندارند، `linux_ipa_proxmox_discovery_ansible_user` و یکی از `linux_ipa_proxmox_discovery_ansible_password` یا `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` را تنظیم کنید تا repository یک مسیر first-touch SSH برای نصب QEMU Guest Agent داشته باشد
- اگر آن مهمان‌های کشف‌شده از SSH non-root استفاده می‌کنند، `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method` و `linux_ipa_proxmox_discovery_ansible_become_password` را هم تنظیم کنید، مگر اینکه آن حساب از قبل passwordless sudo داشته باشد
- `guest_qemu_agent_install_manage_proxmox_vm_agent` ارتباط guest-agent در سمت Proxmox (`qm set <vmid> --agent 1`) را هم برای مهمان‌های Linux مبتنی بر Proxmox قبل از نصب guest-side فعال می‌کند
- اگر این گزینه در Proxmox برای یک VM روشنِ در حال اجرا تغییر کند، repository به‌طور پیش‌فرض فقط warning می‌دهد، چون ممکن است Proxmox برای استفاده از کانال guest-agent به یک start تازه نیاز داشته باشد؛ اگر می‌خواهید repository این VMهای در حال اجرا را خودکار reboot کند، `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` را تنظیم کنید
- `linux_ipa_ssh_host_key_policy` برای اتصال‌های Linux guest به‌طور پیش‌فرض `accept_new` است تا بتوان با VMهای تازه کشف‌شده تماس گرفت بی‌آنکه host key checking کاملاً غیرفعال شود؛ host keyهای تغییرکرده همچنان fail می‌شوند و نیازمند review اپراتور هستند
- `linux_ipa_qga_ssh_bootstrap_enabled` مسیر ترجیحی bootstrap بدون reboot برای guestهای Proxmox-backed است، چون می‌تواند از طریق QEMU Guest Agent و بدون SSH login اولیه، یک کاربر automation مبتنی بر کلید بسازد
- `linux_ipa_qga_ssh_bootstrap_qm_path` به‌طور پیش‌فرض `qm` است و این flow قبل از fail شدن، چند مسیر fallback رایج را روی گره Proxmox probe می‌کند
- guestهایی که `guest-ping` را می‌پذیرند اما `guest-exec` را رد می‌کنند، به‌طور پیش‌فرض در QGA bootstrap skip می‌شوند؛ برای آن‌ها باید یک مسیر SSH دیگر نگه دارید، یا برای fail سریع از `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` استفاده کنید
- `linux_ipa_ssh_bootstrap_enabled` به‌طور اختیاری کلید عمومی SSH controller را پیش از hostname resolution و enrollment روی مهمان‌های Linux نصب می‌کند؛ `linux_ipa_ssh_bootstrap_password` حتی وقتی key bootstrap غیرفعال باشد، به‌عنوان fallback password مشترک برای first-touch هم استفاده می‌شود
- Linux IPA enrollment joinهای client بالادستی را که با timeout در JSON-RPC مربوط به FreeIPA fail شده‌اند، retry می‌کند و `linux_ipaclient_kinit_attempts` را برای محیط‌های کندتر یا شلوغ‌تر expose می‌کند
- Linux IPA enrollment به‌طور پیش‌فرض hostnameهای inventory مربوط به `ipa_servers` را هم به فهرست join serverها merge می‌کند تا clientها بتوانند به‌جای یک endpoint واحد از کل مجموعه serverهای IPA استفاده کنند
- وقتی بیش از یک IPA server در دسترس باشد، هر pass از retry در Linux client enrollment این candidateها را یکی‌یکی امتحان می‌کند
- workflow ترکیبی `site` ابتدا FreeIPA hostgroupها را می‌سازد و سپس بعد از enrollment لینوکس، hostهای runtime enroll‌شده را اضافه می‌کند تا اجراهای pre-enrollment به‌خاطر membership مهمان‌هایی که هنوز enroll نشده‌اند fail نشوند

## سطح پیکربندی

بیشتر مقادیر در این فایل‌ها قرار دارند:

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

برای دیدن layout فایل‌به‌فایل، [docs/VARIABLES.md](../../docs/VARIABLES.md) را ببینید.

خانواده‌های مهم متغیر:

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

## نمونه راهبرد گروه

یک الگوی ساده که به‌خوبی scale می‌کند:

- گروه کاربری FreeIPA با نام `proxmox-admins`
- گروه کاربری FreeIPA با نام `linux-ssh-admins`
- hostgroup با نام `linux-all`
- قانون HBAC با نام `allow-linux-ssh-admins`
- قانون `sudo` با نام `allow-linux-ssh-admins-sudo`
- ACL binding در Proxmox برای گروه syncشده `proxmox-admins-ipa`

وقتی می‌خواهید اجرای ترکیبی `site.yml` به‌صورت خودکار به userهای مشخص IPA از طریق گروه مدیریت‌شده `linux-ssh-admins` دسترسی SSH و sudo روی Linux بدهد، `freeipa_linux_admin_users` را در [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) پر کنید.

یادتان باشد که Proxmox LDAP sync، گروه‌های syncشده را با این suffix ایجاد می‌کند:

```text
<group-name>-<realm>
```

اگر گروه FreeIPA شما `proxmox-admins` باشد و realm پروکسماکس `ipa` باشد، گروه syncشده در PVE چنین می‌شود:

```text
proxmox-admins-ipa
```

## امنیت

- همه secrets را در `vault-freeipa.yml` و `vault-proxmox.yml` نگه دارید، نه در فایل‌های plaintext inventory
- برای Proxmox، یک حساب اختصاصی و فقط-خواندنی برای LDAP bind را ترجیح دهید
- TLS را با certificate verification فعال ترجیح دهید
- خارج از labهای موقت و disposable، SSH host key checking را فعال نگه دارید
- وقتی مهمان‌های Proxmox از قبل QEMU Guest Agent سالم دارند، `linux_ipa_qga_ssh_bootstrap_enabled` را به گذرواژه‌های موقت مشترک ترجیح دهید
- از `guest_qemu_agent_install_enabled` فقط وقتی استفاده کنید که repository از قبل یک مسیر مدیریتی معتبر به داخل guest داشته باشد؛ در حالت Proxmox discovery یعنی QGA از قبل کار می‌کند یا `linux_ipa_proxmox_discovery_ansible_user` به‌همراه password یا key access تنظیم شده است
- اگر Linux SSH bootstrap را فعال می‌کنید، هر گذرواژه bootstrap مشترک را در vault نگه دارید و پس از استقرار دسترسی مبتنی بر کلید آن را rotate یا حذف کنید
- حساب IPA admin را دوباره به‌عنوان حساب LDAP bind در Proxmox استفاده نکنید
- پیش از rollout در production، `proxmox_ldap_filter` و `proxmox_ldap_group_filter` را مرور کنید تا از import شدن بیش‌ازحد جلوگیری شود

برای یک lab موقت که عمداً می‌خواهید SSH host verification را bypass کنید، بهتر است به‌جای تغییر defaults repository، در همان shell session opt out کنید:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Idempotency و caveatها

این پروژه برای reuse و تا حد زیادی idempotent بودن نوشته شده است، اما هنوز هم باید قبل از rollout در production داخل lab آزمایش شود.

محدودیت‌ها و caveatهای شناخته‌شده:

- خروجی CLI در Proxmox ممکن است بین releaseها کمی تفاوت داشته باشد
- layoutهای دایرکتوری FreeIPA انعطاف‌پذیر هستند، بنابراین LDAP filterها ممکن است برای tree شما نیاز به تنظیم داشته باشند
- ACLها و roleهای PVE که قبلاً به‌صورت دستی مدیریت شده‌اند باید قبل از اعمال automation با وضعیت فعلی مقایسه شوند
- Proxmox VM auto-discovery به guestهای روشن و داده شبکه‌ی QEMU guest-agent وابسته است
- تعریف‌های guest مبتنی بر IP همچنان به hostname نهایی معتبر داخل guest یا یک `ipa_hostname` صریح نیاز دارند
- playهای Proxmox با privilege escalation اجرا می‌شوند؛ بنابراین اگر از یک کاربر SSH غیر root استفاده می‌کنید، باید `sudo` سالم داشته باشد و مگر آن‌که passwordless sudo داشته باشد، باید با `-K` گذرواژه become را بدهید
- اگر `ansible_become_password` را در `vault-proxmox.yml` ذخیره کرده باشید، می‌توانید `-K` را حذف کنید، چون Ansible گذرواژه sudo را از متغیر رمزگذاری‌شده می‌خواند

## راستی‌آزمایی

بعد از یک rollout موفق، به‌جای این‌که فرض کنید همه مسیرهای دسترسی درست هستند، وضعیت نهایی را verify کنید.

### در FreeIPA

- بررسی کنید که گروه‌های کاربری مورد انتظار وجود دارند
- بررسی کنید که hostgroupهای مورد انتظار وجود دارند
- بررسی کنید که HBAC ruleهای مورد انتظار وجود دارند و enabled هستند
- بررسی کنید که ruleهای `sudo` مورد انتظار وجود دارند و enabled هستند

### در Proxmox

- بررسی کنید که LDAP realm وجود دارد
- بررسی کنید که initial sync کاربرها یا گروه‌های مورد انتظار را import کرده است
- بررسی کنید که گروه syncشده موردنظر، ACL binding مورد انتظار را دارد

### روی یک مهمان Linux

- بررسی کنید که یک user مجاز IPA بتواند login کند
- بررسی کنید که یک user غیرمجاز توسط HBAC مسدود شود
- بررسی کنید که یک مدیر مجاز IPA بتواند `sudo -l` اجرا کند
- اگر `linux_ipaclient_mkhomedir` فعال است، بررسی کنید که در اولین login دایرکتوری home ساخته شود

## ساختار مخزن

<details>
<summary>ساختار repository را نشان بده</summary>

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

## توسعه

فایل‌های helper مهم این repository:

- `.editorconfig` تنظیمات پیش‌فرض مربوط به whitespace، encoding و line-ending را بین editorهای مختلف سازگار نگه می‌دارد
- `.gitattributes` line ending فایل‌های متنی رایج را روی LF نگه می‌دارد
- `.gitignore` inventoryهای تولیدشده، داده‌های vault، collectionهای محلی و فایل‌های editor را از Git بیرون نگه می‌دارد
- `.ansible-lint` collectionهای vendored را exclude می‌کند و فقط rule مربوط به طول خط در YAML را suppress می‌کند
- `.yamllint` بررسی‌های formatting در YAML را بین playbookها، inventoryها و workflow fileها سازگار نگه می‌دارد
- `.github/CODEOWNERS` مسئولیت review را برای بخش‌های اصلی repository route می‌کند
- `.github/workflows/ci.yml` lint و smoke validation را روی pushها و pull requestها اجرا می‌کند
- `.pre-commit-config.yaml` وقتی `pre-commit` نصب باشد، hook سریع lint را قبل از commit اجرا می‌کند
- `CHANGELOG.md` تغییرات مهم repository را در یک محل track می‌کند
- `docs/VARIABLES.md` layout شکسته‌شده متغیرهای inventory را توضیح می‌دهد
- `docs/i18n/` شامل READMEهای ترجمه‌شده است که باید ساختار کامل بخش‌های نسخه انگلیسی را mirror کنند، درحالی‌که `README.md` منبع canonical باقی می‌ماند
- `docs/i18n/TRANSLATION_GUIDE.md` توضیح می‌دهد که READMEهای ترجمه‌شده چگونه باید همگام نگه داشته شوند
- `scripts/bootstrap.ps1` و `scripts/bootstrap.sh` collection لازم را در مسیر محلی `collections/` نصب می‌کنند و آن را برای سازگاری با ansible-core 2.24+ patch می‌کنند
- `scripts/patch_freeipa_collection.py` importهای deprecated را در collection پین‌شده FreeIPA بازنویسی می‌کند تا با releaseهای آینده ansible-core سازگار بماند
- `scripts/lint.py` ورودی cross-platform مربوط به lint را برای استفاده محلی، CI و pre-commit فراهم می‌کند
- `scripts/smoke-test.py` inventory نمونه را validate می‌کند و syntax checkها را بدون دست‌زدن به زیرساخت واقعی اجرا می‌کند، از جمله playbook مستقل Windows
- `scripts/check_translations.py` READMEهای ترجمه‌شده را از نظر metadata، برابری ساختار بخش‌ها و حداقل پوشش محتوایی نسبت به README canonical انگلیسی audit می‌کند
- `scripts/lint.ps1` و `scripts/lint.sh` workflow مشترک lint و smoke را اجرا می‌کنند
- `scripts/proxmox_event_webhook.py` webhook اختیاری سمت controller را برای eventهای Proxmox VM اجرا می‌کند
- `scripts/proxmox-vm-hook.pl` hookscript اختیاری Proxmox است که در `post-start` و `post-migrate` به webhook سمت controller اطلاع می‌دهد
- `scripts/run-playbook.ps1` commandهای رایج `ansible-playbook` را برای کاربران PowerShell wrap می‌کند، از جمله workflow مستقل Windows
- `scripts/vault.ps1` و `scripts/vault.sh` عملیات رایج split-vault را برای secretهای FreeIPA، Proxmox و Windows اختیاری wrap می‌کنند
- `tests/` سطح verification repository را نگه می‌دارد که فعلاً از مستندات smoke-test شروع می‌شود
- `CONTRIBUTING.md` workflow مورد انتظار برای contribution و validation را مستند می‌کند
- `SECURITY.md` نحوه report کردن آسیب‌پذیری‌ها و برخورد با اطلاعات حساس امنیتی را توضیح می‌دهد

```bash
ansible-lint
python scripts/smoke-test.py
python scripts/check_translations.py
python scripts/check_translations.py --strict
```

```powershell
python .\scripts\smoke-test.py
python .\scripts\check_translations.py
python .\scripts\check_translations.py --strict
```

برای اجرای کامل local lint:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

برای فعال کردن hook سریع lint قبل از هر commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

wrapper مربوط به playbook در PowerShell اکنون این گزینه‌های رایج عملیاتی را هم مستقیم پشتیبانی می‌کند:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## گسترش‌های بعدی

بهبودهای follow-up رایجی که بعداً شاید بخواهید:

- pipeline مبتنی بر Packer برای templateهای Linux آماده FreeIPA
- job templateها و scheduleهای AWX
- مدل‌های جداگانه tenant و pool در Proxmox
- integration گسترده‌تر با Windows local policy یا GPO

## مجوز

این پروژه تحت [MIT License](../../LICENSE) منتشر شده است.
