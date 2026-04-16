# أتمتة الوصول بين Proxmox و FreeIPA

توفر هذه الصفحة ترجمة عربية كاملة للبنية التشغيلية الموجودة في [README.md](../../README.md). تبقى النسخة الإنجليزية هي المصدر المرجعي النهائي، لكن هذه النسخة العربية تغطي نفس الأقسام الرئيسية حتى يتمكن المشغلون من متابعة المشروع بالكامل باللغة العربية.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-15

## اللغات

تظل اللغة الإنجليزية هي المصدر المرجعي الكامل للتوثيق. تتوفر ملفات README مترجمة بالكامل بلغات إضافية ضمن فهرس الترجمات.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [فهرس الترجمات](README.md) | [دليل الترجمة](TRANSLATION_GUIDE.md)

يتعامل هذا المستودع مع **FreeIPA باعتباره مصدر الحقيقة** للهوية والوصول. يستهلك Proxmox ذلك الدليل من خلال LDAP realm، وتنضم ضيوف Linux إلى FreeIPA عبر دور `ipaclient` upstream، ويبقى الوصول مركزيا من خلال المجموعات المتزامنة وقواعد HBAC و`sudo` بدلا من الحسابات المحلية المتفرقة.

> [!IMPORTANT]
> هذا المشروع **لا** يستخدم FreeRADIUS كمصدر الهوية، و**لا** ينشئ مستخدمين محليين داخل كل آلة افتراضية، و**لا** يحاول معالجة كل حالة حافة ممكنة في صلاحيات Proxmox.

## لماذا يوجد هذا المشروع

استخدم هذا المستودع عندما يكون لديك بالفعل:

- بيئة FreeIPA سليمة
- عنقود Proxmox VE
- ضيوف Linux ينبغي أن تعتمد على مصادقة مركزية
- حساب خدمة مخصص في FreeIPA لربط Proxmox مع LDAP
- نموذج واضح لمجموعات الإداريين والمشغلين

يصبح هذا المستودع مناسبا عندما تريد أن تكون عمليات onboarding وoffboarding بالشكل الآتي غالبا:

1. إنشاء المستخدمين والمجموعات أو تحديثهم داخل FreeIPA
2. مزامنة تلك الهويات إلى Proxmox
3. تطبيق أدوار Proxmox وACLs من خلال المجموعات المتزامنة
4. منح وصول ضيوف Linux من خلال تسجيل دخول FreeIPA وHBAC وقواعد `sudo`

## ما الذي ستحصل عليه

- إدارة مجموعات المستخدمين ومجموعات المضيفين وقواعد HBAC وقواعد `sudo` داخل FreeIPA
- إدارة افتراضية لقذائف تسجيل الدخول لمشرفي Linux في FreeIPA
- إعداد LDAP realm في Proxmox أمام FreeIPA
- مزامنة دورية لـ Proxmox realm من عقدة عنقود واحدة محددة
- ربط RBAC في Proxmox بالمجموعات القادمة من الدليل
- إلحاق ضيوف Linux إلى FreeIPA عبر جرد ثابت أو أهداف IP فقط أو اكتشاف Proxmox VM
- تمهيد SSH اختياري بلا إعادة تشغيل عبر Proxmox QEMU Guest Agent
- تمكين اختياري للاتصال بعامل الضيف من جهة Proxmox للضيوف المدعومين
- تثبيت اختياري لـ QEMU Guest Agent عبر SSH أو WinRM عندما يكون الضيف قابلا للوصول أو يصبح قابلا للوصول لاحقا
- تقرير جاهزية اختياري لـ Linux يوضح حالة SSH وحالة QEMU Guest Agent
- سير عمل مستقل اختياري لإدارة عضوية Windows في Active Directory لأجهزة Windows 10/11 وWindows Server
- سير عمل مساعد اختياري محدود لـ Windows مرتبط بـ FreeIPA من أجل الثقة بشهادة IPA والتحقق من الوصول
- تمهيد اختياري لمفتاح SSH العام للاتصال الأول مع ضيوف Linux
- تحديث تلقائي لذاكرة SSSD المؤقتة بعد تغييرات نموذج الوصول في FreeIPA
- إلحاق Linux اختياري معتمد على أحداث Proxmox من خلال hook وwebhook

## النطاق

| مشمول | غير مشمول |
| --- | --- |
| نموذج وصول FreeIPA | نشر FreeRADIUS |
| إعداد LDAP realm في Proxmox | إنشاء دورة حياة المستخدمين داخل FreeIPA |
| RBAC في Proxmox من المجموعات المتزامنة | تغطية كاملة لكل حالات multi-tenant في Proxmox |
| إلحاق عملاء Linux بـ IPA | تسجيل دخول Windows الأصلي مباشرة ضد FreeIPA |
| سير عمل منفصل لعضوية Windows في AD | أتمتة GPO أو دورة حياة كائنات AD الأوسع |
| سير عمل Windows المساعد المرتبط بـ FreeIPA | الادعاء بأن FreeIPA-only helpers تعادل Active Directory |

## سير عمل Windows

يتم تنفيذ دعم Windows في هذا المستودع كسير عمل مستقل بدلا من دمجه داخل إلحاق Linux مع IPA.

- تبقى المجموعة `windows_qemu_guest_agent_clients` مخصصة لمهام QEMU Guest Agent المساعدة الاختيارية.
- فعّل هذا المسار عبر `windows_domain_membership_enabled: true` داخل `10-features.yml`.
- المجموعة `windows_management_clients` هي مجموعة الإدارة المنفصلة التي تستخدمها `playbooks/windows-management.yml` والمرحلة الاختيارية داخل `playbooks/site.yml`.
- يتم التعامل مع تسجيل دخول Windows الفعلي عبر عضوية Active Directory domain membership؛ وفي البيئات المتمركزة حول FreeIPA ينبغي ضم أجهزة Windows إلى جهة AD ضمن FreeIPA-AD trust بدلا من محاولة ضمها مباشرة إلى FreeIPA.

الضم المباشر لـ Windows إلى FreeIPA غير مدعوم في هذا المستودع. بدون Active Directory أو FreeIPA-AD trust يبقى نطاق Windows محدودا في مهام مساعدة مثل إدارة الضيوف القابلين للوصول وتثبيت QEMU Guest Agent عندما يتوفر مسار الإدارة.

إذا أردت مع ذلك مسارا محدودا مرتبطا بـ FreeIPA من دون domain join، فعّل `windows_freeipa_helpers_enabled: true` واستخدم المجموعة `windows_freeipa_helper_clients` مع `playbooks/windows-freeipa-helpers.yml`. يستطيع هذا المسار الوثوق بشهادة IPA CA، وجلب الشهادة تلقائيا للتهيئة الأولية، وتثبيت إدخالات hosts اختيارية، والتحقق من DNS والمنافذ والاتصال عبر HTTPS، لكنه **لا** يوفر تسجيل دخول Windows أصليا ضد FreeIPA.

عندما تحتاج إلى تحقق non-mutating من هذا المسار نفسه، شغّل `playbooks/windows-freeipa-validate.yml`. فهو يبقي مسار التحقق والتلخيص لكنه يعطل استيراد الشهادة وتعديلات hosts وإدارة OpenSSH في تلك الجولة.

هذا السير موجه لضيوف Windows 10/11 وWindows Server القابلين للوصول عبر WinRM أو PSRP.

## البنية

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

للتفسير التصميمي الأطول راجع [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## المتطلبات

### وحدة التحكم

- Ansible Core 2.14 أو أحدث
- وصول SSH من وحدة التحكم إلى عقدة Proxmox الأساسية وخوادم IPA وضيوف Linux
- وصول WinRM أو PSRP إلى ضيوف Windows عندما تستخدم سير عمل Windows
- صلاحيات `sudo` أو `root` عند الحاجة
- عند تمكين تمهيد Linux عبر QGA يجب أن يكون QEMU Guest Agent نشطا داخل الضيف
- عند تمكين تثبيت Guest Agent لضيوف Windows يجب وضع الأجهزة القابلة للوصول في `windows_qemu_guest_agent_clients`
- عند تمكين عضوية Windows في الدومين يجب وضع الأهداف في `windows_management_clients` مع توفير بيانات اعتماد الانضمام إلى AD
- عند تمكين مهام Windows المساعدة المرتبطة بـ FreeIPA يجب وضع الأهداف في `windows_freeipa_helper_clients`
- عند تمكين تمهيد Linux التقليدي عبر SSH تحتاج إلى زوج مفاتيح SSH ومسار دخول أولي يدعم كلمة المرور للحساب المستخدم بواسطة Ansible

### الأهداف

- Proxmox VE 6.x أو أحدث على المضيف الموجود في `proxmox_primary`
- FreeIPA قابل للوصول من Proxmox ومن ضيوف Linux
- يمكن إدارة ضيوف Windows 10/11 وWindows Server بالسير المنفصل عندما يكونون قابلين للوصول عبر WinRM أو PSRP
- DNS ومزامنة وقت سليمان
- بالنسبة إلى `proxmox_primary`، استخدم `root` أو مستخدما يملك `sudo` لأوامر `pveversion` و`pvesh` و`pveum`
- عند استخدام عضوية Windows في الدومين يجب أن تتمكن أجهزة Windows الهدف من الوصول إلى وحدات تحكم AD ذات الصلة
- عند استخدام مسار Windows المساعد المرتبط بـ FreeIPA يجب أن تتمكن تلك الأجهزة من الوصول إلى خوادم IPA ذات الصلة
- عند استخدام اكتشاف Proxmox VM تلقائيا يجب أن يقدّم الضيف IP صالحا عبر QEMU Guest Agent

## منافذ الشبكة

يسرد هذا الجدول المنافذ التي يستخدمها هذا المستودع بين وحدة التحكم وProxmox وFreeIPA وضيوف Linux وWindows. وهو مقصود به نطاق هذا المشروع فقط، وليس مصفوفة كاملة لكل منافذ FreeIPA أو Active Directory.

| الاسم | المنفذ | البروتوكول | المصدر | الوجهة | مطلوب عندما | الغرض |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | وحدة تحكم Ansible | عقدة Proxmox أو خادم IPA أو ضيف Linux | دائما | اتصال Ansible |
| WinRM | `5985`, `5986` | `TCP` | وحدة تحكم Ansible | ضيف Windows | عند تفعيل إدارة Windows | اتصال Ansible مع Windows |
| DNS | `53` | `TCP`, `UDP` | ضيف Linux | خوادم IPA DNS | عندما يستخدم Linux DNS الخاص بـ IPA | حل سجلات IPA والأسماء الخارجية |
| Kerberos | `88` | `TCP`, `UDP` | ضيف Linux | خوادم IPA | إلحاق Linux وتسجيل الدخول | مصادقة Kerberos |
| LDAP | `389` | `TCP` | ضيف Linux | خوادم IPA | إلحاق Linux وتسجيل الدخول | LDAP واكتشاف FreeIPA client |
| HTTPS | `linux_freeipa_enroll_https_port` (الافتراضي `443`) | `TCP` | ضيف Linux | خوادم IPA | إلحاق Linux | التحقق من واجهة IPA أو API أثناء الإلحاق |
| Kerberos Password | `464` | `TCP`, `UDP` | ضيف Linux | خوادم IPA | الإلحاق وعمليات كلمات المرور | keytab وكلمات مرور Kerberos |
| LDAPS | `636` | `TCP` | عقدة Proxmox الأساسية | خوادم IPA أو LDAP | عند استخدام LDAP realm في الوضع الافتراضي `ldaps` | اتصال LDAP الخاص بـ Proxmox |

ملاحظات:

- `LDAPS 636/TCP` هو الافتراضي لأن `proxmox_ldap_mode` يساوي `ldaps` افتراضيا. إذا غيّرت الوضع أو المنفذ فاسمح بالقيمة المضبوطة في `proxmox_ldap_port`.
- غالبا ما يستخدم WinRM المنفذ `5986/TCP` عند HTTPS أو `5985/TCP` عند HTTP وفق إعداد النقل في Windows.
- يحتاج `DNS 53/TCP,UDP` فقط عندما تستخدم ضيوف Linux خوادم IPA كمحللات DNS.
- يحتاج `Kerberos 88` و`Kerberos Password 464` إلى `TCP` و`UDP` معا.
- يتطلب ضم Windows إلى AD مجموعة المنافذ المعتادة بين Windows ووحدات التحكم في الدومين، لكن ذلك يعتمد على البيئة ولم يدرج هنا بشكل exhaustive.
- تبقى مزامنة الوقت مطلبا أساسيا لعمل Kerberos بشكل صحيح، لكن مصدر NTP نفسه ليس ضمن ما يديره هذا المستودع.

## التوافق

أتمتة Proxmox في هذا المستودع مبنية حول واجهات `pveum` و`pvesh` الخاصة بالـ realm وRBAC في Proxmox VE 6.x والإصدارات الأحدث.

- الإصدارات الرئيسية المدعومة افتراضيا: `6`, `7`, `8`, `9`, `10`
- يتحقق مسار validation من إصدار Proxmox المكتشف عبر `pveversion`
- يمكن تجاوز قائمة الإصدارات المدعومة عبر `proxmox_supported_major_versions` إذا احتجت إلى تضييقها أو توسيعها محليا
- المتغير `proxmox_allow_future_major_versions` مضبوط افتراضيا على `true`، لذلك تمر الإصدارات الأحدث من أعلى إصدار مختبر في التحقق افتراضيا
- يجب مع ذلك التعامل مع الإصدارات الرئيسية المستقبلية على أنها مرشحة توافق حتى تتم مراجعة الواجهة الفعلية فيها مقابل هذه الأتمتة
- لا يدّعي هذا المستودع دعما مختبرا للإصدارات القديمة جدا مثل `1` حتى `5` في صورته العامة؛ وإذا أضفتها محليا فاعتبر ذلك override مقصودا واختبر كامل المسار في مختبر أولا

مثال override محلي لبيئة اختبار قديمة:

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

## البدء السريع

الأمثلة التالية تستخدم shell commands. أضيفت مكافئات PowerShell عندما يكون ذلك مهما عمليا.

### 1. انسخ جرد المثال وملفات vault

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# اختياري إذا كنت ستدير ضيوف Windows:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# اختياري إذا كنت ستدير ضيوف Windows:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. عدّل الملفات الخاصة ببيئتك

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` عندما تستخدم Windows management
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` عندما تستخدم Windows management

اختر أيضا وضع مصدر ضيوف Linux إلى جانب إعدادات IPA وProxmox:

- إدخالات جرد ثابتة تحت `linux_ipa_clients`
- إدخالات `linux_ipa_client_hosts` داخل `group_vars/all/30-linux-clients.yml`
- اكتشاف Proxmox VM عبر `linux_ipa_proxmox_discovery_enabled: true`

احرص على إبقاء قيم نطاق IPA وقيم الخوادم منفصلة:

- `ipaclient_domain` هو نطاق DNS المشترك لـ IPA مثل `example.com`
- `linux_ipa_servers` تحتوي أسماء خوادم IPA مثل `ipa01.example.com`

إذا أردت الاتصال بـ Proxmox عبر مستخدم عادي يملك `sudo` بدلا من `root`، فاضبط ذلك داخل `proxmox_primary` في `hosts.yml` وضع كلمة مرور `sudo` في `vault-proxmox.yml`:

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

في هذا الإعداد تكون `vault_proxmox_become_password` هي كلمة المرور التي ستكتبها عادة عند تنفيذ `sudo` على مضيف Proxmox.

### 3. شفّر ملفات vault

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

أضف `inventories/production/group_vars/all/vault-windows.yml` إلى الأمر نفسه عندما تفعّل سير عمل Windows.

أو استخدم wrappers المساعدة، فهي تضبط vault IDs المنفصلة افتراضيا وتنشئ ملفات vault العملية من القوالب إذا لزم الأمر:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

إذا أردت كلمات مرور منفصلة لكل domain عند تشغيل playbooks، فالأفضل استخدام vault IDs بدلا من `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

إذا كان سير Windows الاختياري يستخدم كلمة مرور مختلفة أيضا، فأضف `windows@prompt` إلى الأمر نفسه.

استخدم `-AskVaultPass` فقط عندما تشترك كل ملفات vault المستخدمة في ذلك الـ playbook في كلمة مرور واحدة.

### 4. ثبّت المجموعة المطلوبة

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

أو مباشرة:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

إذا كنت قد ثبّت `freeipa.ansible_freeipa` قبل إضافة patch التوافق في هذا المستودع، فأعد تشغيل bootstrap helper أو شغّل `python .\scripts\patch_freeipa_collection.py` مرة واحدة حتى يتم patching للتثبيت الموجود محليا.

إذا كنت تستخدم `scripts/run-playbook.ps1` فسيشغّل ذلك الـ patch helper تلقائيا قبل تنفيذ `ansible-playbook`.

### 5. شغّل التحقق أولاً

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

إذا أردت فقط التحقق من مسار Windows FreeIPA helper من دون إجراء تغييرات:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

وإذا أردت تقرير جاهزية read-only لـ Linux يوضح أي ضيوف runtime قابلة للوصول عبر SSH وأي ضيوف Proxmox-discovered تستجيب عبر QEMU Guest Agent:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

يُكتب التقرير افتراضيا في `.ansible/linux-readiness-report.json`.
أهم الحقول تعني ما يلي:

- `ssh.ready=true`: مسار SSH الحالي الخاص بـ Ansible يعمل من وحدة التحكم
- `ssh.promptless=true`: نجح probing عبر SSH من دون `ansible_password`، أي أن المسار non-interactive
- `ssh.auth_mode=password_configured`: استخدم probe أداة `sshpass` لأن `ansible_password` مضبوطة للمضيف
- `ssh.auth_mode=key_or_agent`: نجح probe في batch mode من دون كلمة مرور مضبوطة في الجرد
- `qga.status=available`: نجح `qm guest ping` على عقدة Proxmox المالكة لذلك VM
- `qga.status=disabled`: خيار QEMU Guest Agent غير مفعّل في إعداد VM داخل Proxmox
- `qga.status=configured_unresponsive`: العامل مفعّل في Proxmox لكن لا يستجيب من داخل الضيف
- `qga.status=node_unreachable`: تعذر الوصول إلى عقدة Proxmox نفسها، لذلك لم يتم اختبار العامل
- `qga.status=not_applicable`: المضيف ليس قادما من اكتشاف Proxmox وبالتالي لا يوجد probe خاص بـ QGA

مثال quick inspection:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. عاين التغييرات اختياريا

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> لا تنظر إلى check mode باعتباره محاكاة كاملة، بل معاينة جزئية مفيدة. هذا المستودع يستخدم أوامر CLI مباشرة لبعض إعدادات Proxmox ويعتمد دور `ipaclient` upstream لإلحاق Linux، لذلك يفيد `--check` لكنه لا يمثل الحقيقة النهائية.
>
> عند قواعد HBAC في FreeIPA يتحقق check mode من تعريف القاعدة، لكنه يتجاوز خطوة enable أو disable اللاحقة حتى لا يعطي فشلا زائفا لقواعد لم تنشأ فعليا بعد.
>
> كما يتجاوز دور Proxmox realm sync timer خطوة `systemd` الأخيرة في check mode لأن الملفات قد تظهر في diff لكن لا تُكتب فعليا أثناء dry run.
>
> إلحاق Linux مع IPA يتجاوز التنفيذ الحقيقي أيضا في check mode. تستمر هذه الأتمتة في الاكتشاف وتحليل أسماء المضيفين والتحقق من المدخلات، لكن دور `ipaclient` نفسه لا ينفذ الإلحاق الحقيقي أثناء dry run.

### 7. طبّق الإعداد الكامل

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

إذا كان سير Windows الاختياري مفعلا وكانت `vault-windows.yml` تستخدم كلمة مرور مختلفة، فاستخدم `--vault-id windows@prompt` أو `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` بدلا من الاكتفاء بـ `--ask-vault-pass`.

## ترتيب الإطلاق

في أول نشر يُفضّل تطبيق المكدس بهذا الترتيب:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# اختياري إذا كنت تدير ضيوف Windows:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# اختياري إذا أردت فقط مسار Windows المساعد المرتبط بـ FreeIPA:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# اختياري إذا أردت التحقق فقط من هذا المسار:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

هذا الترتيب يجعل troubleshooting أسهل كثيرا من تشغيل كل شيء دفعة واحدة.

مثال PowerShell محدود على ضيف Linux واحد:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

الإعدادات الافتراضية محافظة عمدا:

- تغييرات FreeIPA تعمل مع `serial: 1`
- تغييرات Proxmox تعمل مع `serial: 1`
- اكتشاف Linux وحل الأسماء والإلحاق يعمل افتراضيا مع `serial: 10`
- تغييرات إدارة Windows تعمل مع `serial: 10`
- جميع المسارات تستخدم `max_fail_percentage: 0` افتراضيا

يمكنك ضبط هذه القيم في `inventories/production/group_vars/all/15-rollout.yml`.

## نموذج الوسوم

بدلا من إنشاء playbooks جديدة باستمرار، استخدم الوسوم لاستهداف شريحة مستقرة من الإطلاق.

- المجالات الأساسية: `freeipa`, `proxmox`, `linux`, `validate`
- نموذج وصول FreeIPA: `freeipa_access`
- أجزاء Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- تحضير Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- إلحاق Linux: `linux_enroll`
- أحداث VM: `event`, `linux_refresh`
- مجال Windows: `windows`, `windows_domain`
- Windows FreeIPA helper: `windows`, `windows_freeipa`

أمثلة:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## إلحاق الآلات الافتراضية المعتمد على الأحداث

إذا أردت أن يطلق Proxmox اكتشاف Linux وإلحاقه بـ IPA مباشرة بعد تشغيل VM أو بعد migration، فاستخدم مسار hook وwebhook الاختياري المشروح في [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

هذا المسار يستخدم playbook الحدثي `playbooks/proxmox-vm-event.yml`، لذلك فهو يعالج جانب ضيف Linux وجانب FreeIPA فقط. ولا يعيد تشغيل LDAP realm في Proxmox أو RBAC عند كل حدث VM.

يمكن لهذا المستودع الآن أيضا أن يثبّت stack الخاص بالـ hook والـ webhook من داخل `site.yml` أو `proxmox.yml` إذا ضُبط `proxmox_vm_event_onboarding_enabled: true` وتوفرت متغيرات الـ webhook المطلوبة.

لا توفر hooks في Proxmox مرحلة `create` مستقلة. عمليا غالبا ما يُلتقط VM الجديد عند أول حدث `post-start`، ويمكن أيضا أن ينطلق hook الخاص بالهجرة على العقدة المصدر والعقدة الوجهة معا.

## نموذج الجرد

يستخدم هذا المستودع ست مجموعات معرفة ومجموعة runtime مولدة ديناميكيا:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

يمكنك أيضا تعريف مجموعات inventory إضافية والإشارة إليها في تعريفات FreeIPA hostgroup. وإذا أردت استخدام كامل مجموعة ضيوف Linux الجاهزين من جهة FreeIPA، فاستخدم المجموعة `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> يحتاج FreeIPA إلى الاسم النهائي لكل ضيف. إذا كنت تستخدم أهدافا معتمدة على IP فقط أو اكتشاف Proxmox، فعليك إما تمرير `ipa_hostname` صراحة أو التأكد من أن `hostname -f` داخل الضيف يرجع FQDN النهائي. يقوم هذا المشروع بحل هذا الاسم قبل إنشاء عضوية hostgroup في FreeIPA.

> [!TIP]
> لا تقم بإلحاق golden templates القابلة لإعادة الاستخدام مباشرة بـ FreeIPA. استنسخ VM أولا، واضبط اسم المضيف النهائي، ثم قم بإلحاق الضيف الناتج.

### أوضاع مصادر ضيوف Linux

يمكنك ملء `linux_ipa_clients` بثلاث طرق رئيسية.

#### 1. مضيفون ثابتون داخل الجرد

إذا كنت تعرف أسماء الضيوف مسبقا، فاستخدم إدخالات جرد Ansible العادية:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

هذا النمط جيد للخوادم الثابتة والبيئات الحتمية والأساطيل التي تديرها يدويا.

#### 2. تعريفات مضيفين يدوية داخل المتغيرات

إذا أردت إبقاء الضيوف خارج `hosts.yml` أو كنت تملك IPs فقط، فاستخدم `linux_ipa_client_hosts`:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

ملاحظات:

- يكون `ansible_host` اختياريا عندما يكون `name` اسما قابلا للحل أو FQDN صالحا بالفعل
- إذا لم تملك إلا IP، فاستخدم أي alias ثابت في `name`
- إذا لم تزوّد `ipa_hostname` فسيعود المشروع إلى `hostname -f` داخل الضيف

#### 3. اكتشاف Proxmox VM تلقائيا

إذا أردت سحب ضيوف Linux من عقدة أو أكثر في Proxmox، فاستخدم الاكتشاف:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# اختياري: قصر الأتمتة المعتمدة على الاكتشاف على ضيوف محددين صراحة.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# اختياري: استبعاد ضيوف البنية التحتية دائما حتى مع تفعيل الاكتشاف الواسع.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# إعدادات SSH للاتصال الأولي بالضيوف المكتشفين عندما لا يكون عامل الضيف جاهزا بعد.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

ملاحظات:

- يضيف الاكتشاف الضيوف إلى المجموعة نفسها `linux_ipa_clients_runtime` التي تستخدمها بقية playbooks
- يعتمد اكتشاف IP على QEMU Guest Agent يمكنه إرجاع معلومات الواجهة الشبكية
- المتغير `linux_ipa_proxmox_discovery_use_vm_name_as_hint` يثق فقط في أسماء VM التي تكون FQDN بالفعل
- عندما تضبط `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` يمكن ترقية اسم VM قصير وآمن مثل `teleport-server-1` إلى hint مثل `teleport-server-1.example.com` باستخدام `linux_ipa_identity_hostname_suffix`
- المتغير `linux_ipa_proxmox_discovery_vmids` اختياري ويكون مفيدا خصوصا لمسار hook أو webhook المعتمد على الحدث عندما تريد قصر الاكتشاف على VMID محدد
- يحتاج الضيف مع ذلك إلى hostname نهائي، إما مضبوط داخل النظام أو معرّف يدويا عبر `ipa_hostname`
- يجب أن يكون hostname الفعلي داخل النظام صالحا للإلحاق؛ قيم placeholder مثل `localhost.localdomain` يجب تغييرها قبل تشغيل `linux-clients` أو `site`
- إذا استخدم الضيف اسما قصيرا مثل `app-server-01`، فاضبط `linux_ipa_identity_hostname_suffix` واستخدم `linux_freeipa_enroll_manage_hostname: true` عند الحاجة حتى يتمكن المشروع من حل الاسم الكامل وتطبيقه قبل الإلحاق
- إذا كان FreeIPA DNS authoritative لأسماء ضيوفك، فاضبط `linux_freeipa_enroll_manage_authoritative_dns: true` ليصلح المشروع سجلات A وPTR ذات الصلة ويزيل سجلات AAAA من نوع link-local قبل الإلحاق
- إذا لم يكن DNS جاهزا بعد، فاضبط `linux_ipa_manage_etc_hosts: true` مع `linux_ipa_etc_hosts_entries` ليضيف الدور block bootstrap مُدارا في `/etc/hosts`
- المتغير `guest_qemu_agent_install_enabled` يثبت QEMU Guest Agent على الضيوف التي أصبحت قابلة للوصول عبر SSH أو WinRM، ويعيد المحاولة على ضيوف Linux التي تصبح قابلة للوصول لاحقا في نفس المسار، ويعيد المحاولة أيضا بعد إلحاق Linux
- استخدم `linux_ipa_proxmox_discovery_allowlist_enabled: true` عندما تريد أن يبقى الاكتشاف مفعلا لكن لا يدخل جرد Linux runtime إلا subset معتمد بدقة من ضيوف Proxmox
- استخدم blacklist عبر `linux_ipa_proxmox_discovery_blacklist_vmids` أو `linux_ipa_proxmox_discovery_blacklist_names` أو `linux_ipa_proxmox_discovery_blacklist_ips` عندما تستضيف عقد الاكتشاف ضيوف بنية تحتية مثل firewalls أو DNS servers يجب ألا تتلقى أتمتة IPA أبدا
- إذا كان الضيوف المكتشفون لا يملكون QEMU Guest Agent فعالا بعد، فاضبط `linux_ipa_proxmox_discovery_ansible_user` ومعه `linux_ipa_proxmox_discovery_ansible_password` أو `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` حتى يتوفر مسار SSH صالح للاتصال الأول
- عندما يستخدم هؤلاء الضيوف مستخدم SSH غير root، فاضبط أيضا `linux_ipa_proxmox_discovery_ansible_become` و`linux_ipa_proxmox_discovery_ansible_become_method` و`linux_ipa_proxmox_discovery_ansible_become_password` ما لم يكن `sudo` بدون كلمة مرور متاحا
- يفعّل `guest_qemu_agent_install_manage_proxmox_vm_agent` أيضا خيار Proxmox الخاص بالعامل (`qm set <vmid> --agent 1`) للضيوف المدعومين قبل محاولة التثبيت داخل الضيف
- إذا تغيّر هذا الخيار على VM قيد التشغيل فالمشروع يكتفي بالتحذير افتراضيا لأن Proxmox قد يتطلب إعادة تشغيل جديدة للـ VM قبل أن يعمل channel الخاص بالعامل
- السياسة `linux_ipa_ssh_host_key_policy` مضبوطة افتراضيا على `accept_new` لاتصالات Linux guest حتى يمكن الوصول إلى VMs المكتشفة حديثا من دون تعطيل فحص المفاتيح بالكامل؛ لكن تغيير المفتاح لاحقا ما زال يفشل ويتطلب مراجعة المشغل
- يظل `linux_ipa_qga_ssh_bootstrap_enabled` هو مسار bootstrap المفضل بلا إعادة تشغيل للضيوف المدعومين عبر Proxmox لأنه يستطيع إنشاء مستخدم automation بمفتاح فقط من خلال QEMU Guest Agent قبل وجود أي SSH login عملي
- يضبط `linux_ipa_ssh_bootstrap_enabled` تثبيت المفتاح العام لوحدة التحكم على ضيوف Linux قبل حل الاسم والإلحاق، كما يُستخدم `linux_ipa_ssh_bootstrap_password` ككلمة مرور fallback مشتركة للمرة الأولى حتى عندما يكون bootstrap بالمفتاح معطلا
- يعيد إلحاق Linux مع IPA المحاولة عندما يفشل upstream join بسبب FreeIPA JSON-RPC timeout، ويكشف المتغير `linux_ipaclient_kinit_attempts` للبيئات البطيئة أو المزدحمة
- يدمج إلحاق Linux أيضا أسماء hosts من مجموعة `ipa_servers` داخل قائمة خوادم الانضمام افتراضيا حتى يستطيع العميل استخدام مجموعة خوادم IPA كاملة بدلا من endpoint واحدة
- عندما يتوفر أكثر من خادم IPA واحد، تُجرّب تلك الخوادم واحدا واحدا في كل جولة retry أثناء الإلحاق
- ينشئ سير `site` الموحّد FreeIPA hostgroups قبل إلحاق Linux ثم يضيف المضيفين الملحقين لاحقا، حتى لا تفشل التشغيلات المسبقة بسبب عضوية hostgroup للمضيفين غير الملحقين بعد

## سطح الإعداد

توجد أغلب القيم في:

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

للتقسيم الكامل ملفا بملف، راجع [docs/VARIABLES.md](../VARIABLES.md).

عائلات المتغيرات الأساسية:

| المجال | المتغيرات |
| --- | --- |
| نموذج وصول FreeIPA | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| ضوابط الإطلاق | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| LDAP realm في Proxmox | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| RBAC في Proxmox | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| إلحاق Linux بـ IPA | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| تقرير جاهزية Linux | `linux_readiness_report_*` |
| إدارة Windows | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helpers | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| أسرار الاتصال في Ansible | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## مثال على استراتيجية المجموعات

نمط بسيط وقابل للتوسع:

- مجموعة مستخدمين في FreeIPA باسم `proxmox-admins`
- مجموعة مستخدمين في FreeIPA باسم `linux-ssh-admins`
- مجموعة مضيفين في FreeIPA باسم `linux-all`
- قاعدة HBAC باسم `allow-linux-ssh-admins`
- قاعدة `sudo` باسم `allow-linux-ssh-admins-sudo`
- ACL binding في Proxmox للمجموعة المتزامنة `proxmox-admins-ipa`

املأ `freeipa_linux_admin_users` في [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) عندما تريد أن يمنح تشغيل `site.yml` الموحّد مستخدمين محددين في IPA صلاحية SSH و`sudo` على Linux تلقائيا من خلال المجموعة المُدارة `linux-ssh-admins`.

تذكّر أن مزامنة LDAP في Proxmox تنشئ المجموعات المتزامنة باللاحقة:

```text
<group-name>-<realm>
```

إذا كانت مجموعة FreeIPA لديك هي `proxmox-admins` وكان realm في Proxmox هو `ipa` فستصبح مجموعة PVE المتزامنة:

```text
proxmox-admins-ipa
```

## الأمان

- خزّن كل الأسرار داخل `vault-freeipa.yml` و`vault-proxmox.yml` و`vault-windows.yml` بدلا من ملفات الجرد النصية الصريحة
- استخدم حساب LDAP للقراءة فقط في Proxmox متى أمكن
- فضّل TLS مع التحقق من الشهادات مفعّلا
- أبقِ التحقق من مفاتيح SSH مفعّلا خارج المختبرات المؤقتة
- فضّل `linux_ipa_qga_ssh_bootstrap_enabled` على كلمات المرور المؤقتة المشتركة عندما يكون QEMU Guest Agent في ضيوف Proxmox جاهزا بالفعل
- استخدم `guest_qemu_agent_install_enabled` فقط عندما يمتلك المشروع بالفعل مسار إدارة صالحا داخل الضيف؛ وفي اكتشاف Proxmox يعني ذلك أن QGA يعمل أو أن `linux_ipa_proxmox_discovery_ansible_user` مع كلمة مرور أو مفتاح SSH مضبوط
- إذا فعّلت Linux SSH bootstrap فاحتفظ بأي كلمة مرور bootstrap مشتركة داخل vault وقم بتدويرها أو حذفها بعد تثبيت الوصول بالمفتاح
- لا تعِد استخدام حساب IPA admin كحساب bind لـ LDAP في Proxmox
- راجع `proxmox_ldap_filter` و`proxmox_ldap_group_filter` قبل الإطلاق الإنتاجي حتى لا تستورد كائنات أكثر من اللازم

إذا كنت في مختبر disposable وتريد تجاوز فحص مفاتيح SSH صراحة، فقم بذلك على مستوى جلسة shell لا بتغيير defaults الخاصة بالمستودع:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## الاعتمادية والملاحظات

هذا المشروع مكتوب ليكون قابلا لإعادة الاستخدام وفي معظمه idempotent، لكنه مع ذلك يحتاج إلى اختبار مختبري قبل الإطلاق الإنتاجي.

القيود المعروفة:

- قد يختلف خرج CLI الخاص بـ Proxmox قليلا بين الإصدارات
- بنية الدليل داخل FreeIPA مرنة، لذلك قد تحتاج مرشحات LDAP إلى ضبط حسب الشجرة لديك
- يجب مقارنة ACLs والأدوار الموجودة يدويا في PVE قبل إسقاط الأتمتة فوقها
- يعتمد اكتشاف Proxmox VM تلقائيا على الضيوف المشغلين وعلى بيانات الشبكة القادمة من QEMU Guest Agent
- التعريفات المعتمدة على IP فقط ما زالت تحتاج hostname نهائيا صالحا داخل الضيف أو `ipa_hostname` صريحا
- تعمل playbooks الخاصة بـ Proxmox مع privilege escalation، لذلك يجب أن يملك مستخدم SSH غير root `sudo` عاملا ويجب أن تمرر become password عبر `-K` ما لم يكن `sudo` بدون كلمة مرور متاحا
- إذا خزّنت `ansible_become_password` داخل `vault-proxmox.yml` فيمكنك تجاوز `-K` لأن Ansible سيقرأ كلمة مرور `sudo` من المتغير المشفّر

## التحقق

بعد نجاح الإطلاق تحقّق من الحالة الناتجة بدلا من افتراض أن كل مسار وصول أصبح صحيحا تلقائيا.

### في FreeIPA

- تأكد من وجود مجموعات المستخدمين المتوقعة
- تأكد من وجود مجموعات المضيفين المتوقعة
- تأكد من وجود قواعد HBAC المطلوبة وأنها مفعّلة
- تأكد من وجود قواعد `sudo` المطلوبة وأنها مفعّلة

### في Proxmox

- تأكد من وجود LDAP realm
- تأكد من أن المزامنة الأولية جلبت المستخدمين أو المجموعات المتوقعة
- تأكد من أن المجموعة المتزامنة المقصودة تحمل ACL binding المطلوبة

### على ضيف Linux

- تأكد من أن مستخدم IPA المسموح له يمكنه تسجيل الدخول
- تأكد من أن مستخدما غير مسموح به يُمنع بواسطة HBAC
- تأكد من أن مسؤول IPA المسموح له يستطيع تنفيذ `sudo -l`
- تأكد من أن مجلد المنزل يُنشأ عند أول دخول إذا كان `linux_ipaclient_mkhomedir` مفعّلا

## بنية المستودع

<details>
<summary>أظهر بنية المستودع</summary>

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

## التطوير

تشمل ملفات المساعدة المهمة في هذا المستودع:

- `.editorconfig` للحفاظ على اتساق المسافات وencoding ونهايات الأسطر بين المحررات
- `.gitattributes` للإبقاء على الملفات النصية الشائعة على نهايات أسطر LF
- `.gitignore` لمنع ملفات الجرد المولدة وبيانات vault والـ collections المحلية وملفات المحرر من الدخول إلى Git
- `.ansible-lint` لاستبعاد collections الموردة وكبت قاعدة طول أسطر YAML فقط
- `.yamllint` للحفاظ على اتساق فحوص تنسيق YAML عبر playbooks وinventories وworkflow files
- `.github/CODEOWNERS` لتوجيه ownership الخاص بالمراجعة في مناطق المستودع الرئيسية
- `.github/workflows/ci.yml` لتشغيل lint checks وsmoke validation عند الـ push وطلبات السحب
- `.pre-commit-config.yaml` لتشغيل lint hook السريع قبل commits عندما تكون `pre-commit` مثبتة
- `CHANGELOG.md` لتتبع التغييرات المهمة في مكان واحد
- `docs/VARIABLES.md` لشرح تخطيط المتغيرات المجزأ في الجرد
- `docs/i18n/` للاحتفاظ بملفات README المترجمة التي ينبغي أن تعكس هيكل الأقسام الكامل في README الإنجليزي بينما تبقى `README.md` المصدر المرجعي
- `docs/i18n/TRANSLATION_GUIDE.md` لشرح كيفية إبقاء الترجمات متزامنة
- `scripts/bootstrap.ps1` و`scripts/bootstrap.sh` لتثبيت الـ collection المطلوبة داخل مسار `collections/` المحلي في المستودع وتطبيق patch التوافق مع `ansible-core` 2.24+
- `scripts/patch_freeipa_collection.py` لإعادة كتابة imports المهملة داخل الـ collection المثبتة pinned حتى تبقى متوافقة مع إصدارات ansible-core القادمة
- `scripts/lint.py` لتقديم نقطة دخول lint متعددة المنصات للاستخدام المحلي وCI وpre-commit
- `scripts/smoke-test.py` للتحقق من جرد المثال وتشغيل syntax checks من دون لمس البنية التحتية الحقيقية، بما في ذلك playbooks الخاصة بـ Windows
- `scripts/check_translations.py` لمراجعة ملفات README المترجمة من حيث metadata وتكافؤ بنية الأقسام والحد الأدنى من تغطية المحتوى مقارنة بالمصدر الإنجليزي
- `scripts/lint.ps1` و`scripts/lint.sh` لتشغيل مسار lint وsmoke المحلي الموحّد
- `scripts/proxmox_event_webhook.py` لتشغيل webhook اختياري على جهة وحدة التحكم لأحداث Proxmox VM
- `scripts/proxmox-vm-hook.pl` كـ hookscript اختياري لـ Proxmox يُشعِر webhook على جهة وحدة التحكم عند `post-start` و`post-migrate`
- `scripts/run-playbook.ps1` لتغليف أوامر `ansible-playbook` الشائعة لمستخدمي PowerShell، بما في ذلك سير Windows المنفصل
- `scripts/vault.ps1` و`scripts/vault.sh` لتغليف عمليات split-vault الشائعة المتعلقة بأسرار FreeIPA وProxmox وWindows الاختيارية
- `tests/README.md` و`tests/smoke/README.md` لتوثيق مسار التحقق والدخان الخاص بالمستودع

إذا كانت `ansible-lint` مثبتة على وحدة التحكم:

```bash
ansible-lint
```

لتشغيل smoke checks الخاصة بالمستودع مباشرة:

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

ولتمرير lint local الكامل:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

ولتفعيل lint hook السريع قبل كل commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

كما أن wrapper الخاص بـ PowerShell يدعم الآن خيارات تشغيل شائعة مباشرة:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## الامتدادات التالية

تحسينات شائعة قد تحتاجها لاحقا:

- خط Packer لصناعة صور Linux الجاهزة لـ IPA
- قوالب وظائف AWX وجداولها
- نماذج منفصلة للمستأجرين وpool داخل Proxmox
- تكامل أوسع مع سياسات Windows المحلية أو GPO

## الرخصة

هذا المشروع منشور تحت [رخصة MIT](../../LICENSE).
