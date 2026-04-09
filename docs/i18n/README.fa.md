# خودکارسازی دسترسی Proxmox + FreeIPA

این صفحه یک ترجمه کاملِ ساختاری از [README.md](../../README.md) ارائه می‌کند. نسخه انگلیسی منبع canonical باقی می‌ماند، اما این فایل همان بخش‌های اصلی را برای خواننده فارسی پوشش می‌دهد.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## چرا این پروژه وجود دارد

از این مخزن زمانی استفاده کنید که از قبل داشته باشید:

- یک محیط سالم FreeIPA
- یک کلاستر Proxmox VE
- مهمان‌های Linux که باید احراز هویت متمرکز داشته باشند
- یک حساب سرویس اختصاصی برای LDAP bind در Proxmox
- یک مدل روشن از گروه‌های ادمین و اپراتور

ایده اصلی این است که FreeIPA منبع حقیقت برای هویت و دسترسی باشد. Proxmox این دایرکتوری را از طریق LDAP realm مصرف می‌کند، مهمان‌های Linux با role `ipaclient` به FreeIPA می‌پیوندند، و کنترل SSH، HBAC و `sudo` متمرکز باقی می‌ماند.

## چه چیزی دریافت می‌کنید

- مدیریت گروه‌های کاربری، hostgroupها، قوانین HBAC و قوانین `sudo` در FreeIPA
- پیکربندی Proxmox LDAP realm در برابر FreeIPA
- همگام‌سازی دوره‌ای realm از یک گره مشخص کلاستر
- RBAC bindings در Proxmox برای گروه‌های همگام‌شده
- enrollment لینوکس از inventory ایستا، تعریف‌های دستی یا Proxmox discovery
- SSH bootstrap اختیاری بدون reboot از طریق QEMU Guest Agent
- نصب اختیاری QEMU Guest Agent از طریق SSH یا WinRM برای مهمان‌های قابل دسترس
- bootstrap اختیاری کلید عمومی SSH برای first-touch
- refresh خودکار کش SSSD پس از تغییرات مدل دسترسی
- onboarding اختیاری event-driven برای `post-start` و `post-migrate`

## دامنه

| شامل | شامل نمی‌شود |
| --- | --- |
| مدل دسترسی FreeIPA | Windows domain join |
| راه‌اندازی Proxmox LDAP realm | استقرار FreeRADIUS |
| Proxmox RBAC از گروه‌های sync شده | ایجاد کامل چرخه عمر کاربر در FreeIPA |
| Linux IPA enrollment | همه edge caseهای multi-tenant در Proxmox |

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

## پیش‌نیازها

### Controller

- Ansible Core 2.14+
- دسترسی SSH به گره اصلی Proxmox، سرورهای IPA و کلاینت‌های Linux
- `sudo` یا `root` در جاهایی که لازم است
- اگر QGA SSH bootstrap فعال است، QEMU Guest Agent باید از قبل در guest فعال باشد
- اگر Windows fallback فعال است، میزبان‌های قابل دسترس باید در `windows_qemu_guest_agent_clients` باشند
- اگر Linux SSH bootstrap فعال است، controller به SSH keypair و مسیر اولیه مبتنی بر گذرواژه نیاز دارد

### Targets

- Proxmox VE 6.x یا جدیدتر روی میزبان `proxmox_primary`
- FreeIPA قابل دسترس از Proxmox و Linux clients
- DNS و همگام‌سازی زمان درست
- برای `proxmox_primary` از `root` یا کاربری استفاده کنید که `pveversion`, `pvesh`, `pveum` را با `sudo` اجرا می‌کند
- در Proxmox discovery، guest باید IP قابل استفاده از طریق QEMU Guest Agent ارائه کند

## پورت‌های شبکه

- `22/TCP` برای SSH
- `53/TCP,UDP` برای IPA DNS
- `88/TCP,UDP` و `464/TCP,UDP` برای Kerberos
- `389/TCP` برای LDAP
- `linux_freeipa_enroll_https_port` با مقدار پیش‌فرض `443/TCP`
- `636/TCP` برای `ldaps`

## سازگاری

- برای Proxmox VE 6.x و نسخه‌های جدیدتر طراحی شده است
- نسخه‌های major پیش‌فرض: `6`, `7`, `8`, `9`, `10`
- با `proxmox_supported_major_versions` قابل override است
- `proxmox_allow_future_major_versions` به‌طور پیش‌فرض `true` است

## شروع سریع

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

فایل‌های `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml` و `vault-proxmox.yml` را متناسب با محیط خود ویرایش کنید.

## ترتیب rollout

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

پیش‌فرض‌ها محافظه‌کارانه هستند: `serial: 1` برای FreeIPA و Proxmox، `serial: 10` برای Linux و `max_fail_percentage: 0`.

## مدل tag

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## VM onboarding مبتنی بر رویداد

اگر می‌خواهید Proxmox بلافاصله بعد از `post-start` یا `post-migrate`، Linux discovery و IPA enrollment را اجرا کند، از workflow اختیاری hook/webhook در [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) استفاده کنید. این مسیر از `playbooks/proxmox-vm-event.yml` استفاده می‌کند، در هر event دوباره LDAP realm یا RBAC را اجرا نمی‌کند و VMهای جدید را در اولین `post-start` می‌گیرد.

## مدل inventory

گروه‌های اصلی:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

حتی در حالت IP-only یا Proxmox discovery، guest همچنان به FQDN نهایی از طریق `ipa_hostname` یا `hostname -f` نیاز دارد.

### حالت‌های منبع Linux

1. میزبان‌های ایستا در inventory
2. تعریف‌های دستی در `linux_ipa_client_hosts`
3. Proxmox discovery از طریق `linux_ipa_proxmox_discovery_*`

نکات مهم: discovery به داده شبکه QEMU Guest Agent وابسته است، `linux_ipa_proxmox_discovery_vmids` برای event path مفید است، نام‌های کوتاه را می‌توان با `linux_ipa_identity_hostname_suffix` تکمیل کرد، DNS authoritative را می‌توان با `linux_freeipa_enroll_manage_authoritative_dns` ترمیم کرد، و هنگام آماده نبودن DNS می‌توان از `/etc/hosts` bootstrap استفاده کرد.

## سطح پیکربندی

فایل‌های اصلی:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## نمونه راهبرد گروه

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## امنیت

- همه secrets را فقط در vault نگه دارید
- برای Proxmox از حساب LDAP bind فقط-خواندنی و اختصاصی استفاده کنید
- TLS با certificate verification را ترجیح دهید
- خارج از آزمایشگاه موقت، SSH host key checking را غیرفعال نکنید

## Idempotency و caveatها

این مخزن برای اجراهای تکراری طراحی شده است، اما باید پیش از production در lab اعتبارسنجی شود. محدودیت‌های شناخته‌شده شامل تفاوت خروجی CLI در Proxmox، نیاز به تنظیم LDAP filter، وابستگی discovery به guestهای روشن و QGA، و نیاز به hostname نهایی معتبر برای هدف‌های مبتنی بر IP است.

## راستی‌آزمایی

- در FreeIPA، گروه‌ها، hostgroupها، HBAC و `sudo` را بررسی کنید
- در Proxmox، LDAP realm، sync و ACL bindings را بررسی کنید
- روی Linux guest، login مجاز، deny شدن توسط HBAC، `sudo -l` و ساخت home را تست کنید

## ساختار مخزن

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## توسعه

مخزن شامل `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflowها، `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1` و `scripts/vault.*` است.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## گسترش‌های بعدی

- Packer pipeline برای Linux templateهای IPA-ready
- AWX job template و schedule
- مدل‌های جداگانه tenant و pool در Proxmox
- جریان Windows یا AD-trust برای محیط‌های RDP-oriented

## مجوز

این پروژه تحت [MIT License](../../LICENSE) منتشر شده است.
