# أتمتة الوصول بين Proxmox و FreeIPA

توفر هذه الصفحة ترجمة كاملة لبنية [README.md](../../README.md). تبقى النسخة الإنجليزية هي المرجع النهائي عند وجود أي تعارض، لكن هذه الصفحة تغطي جميع الأقسام الرئيسية نفسها حتى يتمكن المشغلون من قراءة المستند كاملاً باللغة العربية.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## لماذا يوجد هذا المشروع

استخدم هذا المستودع عندما يكون لديك بالفعل:

- بيئة FreeIPA سليمة
- عنقود Proxmox VE
- ضيوف Linux يجب أن يعتمدوا على مصادقة مركزية
- حساب خدمة مخصص لربط Proxmox مع LDAP
- نموذج واضح للمجموعات الإدارية والتشغيلية

الفكرة الأساسية هي جعل FreeIPA مصدر الحقيقة للهوية والوصول، بينما يستهلك Proxmox هذا الدليل من خلال LDAP realm، وتنضم أجهزة Linux إلى FreeIPA عبر دور `ipaclient`، وتبقى قواعد SSH و`sudo` وHBAC مركزية بدلاً من الحسابات المحلية المتناثرة.

## ما الذي ستحصل عليه

- إدارة مجموعات المستخدمين ومجموعات المضيفين وقواعد HBAC وقواعد `sudo` في FreeIPA
- إعداد LDAP realm في Proxmox وربط RBAC بالمجموعات المتزامنة
- مؤقت مزامنة دوري لـ Proxmox من عقدة عنقود واحدة محددة
- إلحاق ضيوف Linux بـ FreeIPA من جرد ثابت أو تعريفات يدوية أو اكتشاف Proxmox
- تمهيد SSH اختياري عبر QEMU Guest Agent من دون إعادة تشغيل
- تثبيت اختياري لـ QEMU Guest Agent عبر SSH أو WinRM للضيوف القابلين للوصول
- تمهيد اختياري لمفتاح SSH العام للاتصال الأول
- تحديث تلقائي لذاكرة SSSD المؤقتة بعد تغييرات نموذج الوصول
- إلحاق اختياري معتمد على أحداث `post-start` و`post-migrate`

## النطاق

| مشمول | غير مشمول |
| --- | --- |
| نموذج وصول FreeIPA | ضم Windows إلى الدومين |
| إعداد LDAP realm في Proxmox | نشر FreeRADIUS |
| RBAC في Proxmox من المجموعات المتزامنة | إنشاء دورة حياة المستخدمين داخل FreeIPA |
| إلحاق عملاء Linux بـ IPA | تغطية جميع حالات Proxmox متعددة المستأجرين |

## البنية

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

للتفسير التصميمي الأطول راجع [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## المتطلبات

### وحدة التحكم

- Ansible Core 2.14 أو أحدث
- إمكانية SSH إلى العقدة الأساسية في Proxmox وخوادم IPA وضيوف Linux
- صلاحيات `sudo` أو `root` عند الحاجة
- عند استخدام تمهيد SSH عبر QGA يجب أن يكون QEMU Guest Agent نشطاً داخل الضيف
- عند تمكين تثبيت عامل الضيف للويندوز يجب وضع الأجهزة القابلة للوصول داخل `windows_qemu_guest_agent_clients`
- عند تمكين تمهيد SSH التقليدي تحتاج إلى زوج مفاتيح SSH ومسار دخول أولي بكلمة مرور

### الأهداف

- Proxmox VE 6.x أو أحدث على المضيف الموجود في `proxmox_primary`
- FreeIPA قابل للوصول من Proxmox وضيوف Linux
- DNS ومزامنة وقت سليمان
- على `proxmox_primary` استخدم `root` أو مستخدماً يمكنه تنفيذ `sudo` لأوامر `pveversion` و`pvesh` و`pveum`
- عند استخدام اكتشاف Proxmox يجب أن يقدّم الضيف IP صالحاً عبر QEMU Guest Agent

## منافذ الشبكة

المصفوفة المرجعية الكاملة موجودة في README الإنجليزي. أهم المنافذ المستخدمة في هذا المشروع هي:

- `22/TCP` للاتصال عبر SSH من وحدة التحكم إلى Proxmox وFreeIPA وضيوف Linux
- `53/TCP,UDP` من ضيوف Linux إلى خوادم IPA DNS عند استخدام DNS الخاص بـ IPA
- `88/TCP,UDP` و`464/TCP,UDP` لـ Kerberos ومهام كلمة المرور
- `389/TCP` لـ LDAP الخاص بعملاء IPA
- `linux_freeipa_enroll_https_port` والقيمة الافتراضية له `443/TCP` للتحقق من واجهة IPA أثناء الإلحاق
- `636/TCP` كافتراضي لاتصال Proxmox LDAP عندما يكون `proxmox_ldap_mode=ldaps`

## التوافق

- الإعدادات تستهدف Proxmox VE 6.x وما بعده
- الإصدارات المدعومة افتراضياً: `6`, `7`, `8`, `9`, `10`
- يمكن تجاوز قائمة الإصدارات عبر `proxmox_supported_major_versions`
- المتغير `proxmox_allow_future_major_versions` افتراضياً `true`

## البدء السريع

### 1. انسخ جرد المثال وملفات vault

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
```

### 2. عدّل الملفات الخاصة ببيئتك

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

اختر كذلك وضع مصدر ضيوف Linux: إدخالات جرد ثابتة، أو `linux_ipa_client_hosts`، أو اكتشاف Proxmox عبر `linux_ipa_proxmox_discovery_enabled: true`.

### 3. شفّر ملفات vault

```bash
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
```

### 4. ثبّت الـ collection المطلوبة

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

### 5. شغّل التحقق أولاً

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

### 6. معاينة التغييرات اختيارياً

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

### 7. طبّق الإعداد الكامل

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## ترتيب الإطلاق

في أول نشر يفضّل التشغيل بهذا الترتيب:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

الإعدادات الافتراضية محافظة:

- تغييرات FreeIPA تعمل مع `serial: 1`
- تغييرات Proxmox تعمل مع `serial: 1`
- اكتشاف وإلحاق Linux يعمل افتراضياً مع `serial: 10`
- جميع المسارات تستخدم `max_fail_percentage: 0`

## نموذج الوسوم

استخدم الوسوم لاستهداف أجزاء مستقرة من الإطلاق:

- المجالات الأساسية: `freeipa`, `proxmox`, `linux`, `validate`
- نموذج وصول FreeIPA: `freeipa_access`
- أجزاء Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- تحضير Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- إلحاق Linux: `linux_enroll`
- الأحداث: `event`, `linux_refresh`

## إلحاق الآلات الافتراضية المعتمد على الأحداث

إذا أردت أن يطلق Proxmox اكتشاف Linux وإلحاقه بـ IPA مباشرة بعد تشغيل الآلة أو هجرتها، فاستخدم سير hook/webhook الاختياري المشروح في [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

- يستخدم هذا المسار `playbooks/proxmox-vm-event.yml`
- لا يعيد تشغيل LDAP realm أو RBAC في Proxmox عند كل حدث
- لا توجد مرحلة `create` منفصلة في hooks الخاصة بـ Proxmox؛ عادةً يتم الالتقاط عند أول `post-start`
- يمكن أيضاً تفعيل نشر هذا المكدس الاختياري من `site.yml` أو `proxmox.yml`

## نموذج الجرد

المجموعات الأساسية هي:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

إذا استخدمت IP فقط أو اكتشاف Proxmox، فيجب أن يكون لدى الضيف اسم مضيف نهائي صحيح، إما عبر `ipa_hostname` أو عبر نتيجة `hostname -f`.

### أوضاع مصادر ضيوف Linux

1. مضيفون ثابتون داخل الجرد الاعتيادي.
2. تعريفات يدوية داخل `linux_ipa_client_hosts`.
3. اكتشاف آلي من Proxmox عبر `linux_ipa_proxmox_discovery_*`.

ملاحظات مهمة:

- الاكتشاف يعتمد على QEMU Guest Agent لإرجاع الشبكة
- `linux_ipa_proxmox_discovery_vmids` مفيد خصوصاً لمسار الأحداث
- يمكن استخدام `linux_ipa_identity_hostname_suffix` مع `linux_freeipa_enroll_manage_hostname: true`
- عند إدارة DNS الموثوق يمكن استخدام `linux_freeipa_enroll_manage_authoritative_dns: true`
- عندما لا يكون DNS جاهزاً بعد، استخدم `linux_ipa_manage_etc_hosts: true` مع `linux_ipa_etc_hosts_entries`
- `linux_ipa_qga_ssh_bootstrap_enabled` هو المسار المفضل للتمهيد من دون إعادة تشغيل

## سطح الإعداد

تتركز معظم القيم في الملفات التالية:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

راجع [docs/VARIABLES.md](../VARIABLES.md) للحصول على الشرح التفصيلي.

## مثال على استراتيجية المجموعات

نمط بسيط وقابل للتوسع:

- مجموعة مستخدمين `proxmox-admins`
- مجموعة مستخدمين `linux-ssh-admins`
- مجموعة مضيفين `linux-all`
- قاعدة HBAC باسم `allow-linux-ssh-admins`
- قاعدة `sudo` باسم `allow-linux-ssh-admins-sudo`
- ربط ACL في Proxmox للمجموعة المتزامنة `proxmox-admins-ipa`

## الأمان

- خزّن الأسرار داخل ملفات vault فقط
- استخدم حساب LDAP للقراءة فقط في Proxmox متى أمكن
- فضّل TLS مع التحقق من الشهادات
- أبقِ التحقق من مفاتيح SSH مفعلاً خارج المختبرات المؤقتة
- استخدم `linux_ipa_qga_ssh_bootstrap_enabled` بدلاً من كلمات المرور المشتركة عندما يكون QGA جاهزاً

## الاعتمادية والملاحظات

المشروع قابل لإعادة الاستخدام إلى حد كبير، لكن اختبره دائماً في مختبر قبل الإنتاج. من القيود المعروفة:

- قد يختلف خرج CLI الخاص بـ Proxmox قليلاً بين الإصدارات
- قد تحتاج مرشحات LDAP إلى ضبط حسب شجرتك
- اكتشاف Proxmox يعتمد على الضيوف المشغلين وعلى QEMU Guest Agent
- التعريفات المبنية على IP فقط تحتاج اسم مضيف نهائي صالح

## التحقق

بعد نجاح الإطلاق تحقّق من الحالة الناتجة:

- في FreeIPA: المجموعات وقواعد HBAC و`sudo` وتمكينها
- في Proxmox: وجود LDAP realm والمزامنة والـ ACLs المطلوبة
- على ضيف Linux: دخول مستخدم مسموح، منع مستخدم مرفوض، نجاح `sudo -l`، وإنشاء المنزل عند أول دخول إذا كان `mkhomedir` مفعلاً

## بنية المستودع

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

البنية الكاملة المطابقة للمستودع موضحة في README الإنجليزي.

## التطوير

يتضمن المستودع ملفات مساعدة للتطوير مثل:

- `.editorconfig`, `.gitattributes`, `.gitignore`
- `.ansible-lint`, `.yamllint`
- `.github/workflows/ci.yml`
- `scripts/bootstrap.ps1`, `scripts/bootstrap.sh`
- `scripts/lint.py`, `scripts/lint.ps1`, `scripts/lint.sh`
- `scripts/smoke-test.py`
- `scripts/proxmox_event_webhook.py`
- `scripts/proxmox-vm-hook.pl`
- `scripts/run-playbook.ps1`
- `scripts/vault.ps1`, `scripts/vault.sh`

أوامر مفيدة:

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
.\scripts\lint.ps1
```

## الامتدادات التالية

تحسينات شائعة لاحقاً:

- خط Packer لقوالب Linux الجاهزة لـ IPA
- قوالب وظائف وجداول AWX
- نماذج منفصلة للمستأجرين والمجموعات في Proxmox
- مسار Windows أو AD-trust لبيئات تعتمد على RDP

## الرخصة

هذا المشروع منشور تحت [رخصة MIT](../../LICENSE).
