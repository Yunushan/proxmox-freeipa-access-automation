# Автоматизация доступа Proxmox + FreeIPA

Эта страница содержит полную и структурно эквивалентную русскую версию [README.md](../../README.md). Английский текст остается каноническим источником, но русская версия должна покрывать тот же операционный объем для русскоязычных операторов.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## Языки

Английская версия является каноническим источником полной документации. Также доступны полные переводы README еще на 20 языках.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

Этот repository рассматривает **FreeIPA как source of truth** для identity и access. Proxmox использует этот каталог через LDAP realm, Linux-гости вступают в FreeIPA через upstream-роль `ipaclient`, а доступ остается централизованным через synced groups, HBAC и sudo rules вместо расползания локальных учетных записей по каждой VM.

> [!IMPORTANT]
> Этот проект **не использует FreeRADIUS как identity source**, **не создает local users внутри каждой VM** и **не пытается охватить все возможные edge case прав доступа в Proxmox**.

## Зачем нужен этот проект

Используйте репозиторий, если у вас уже есть:

- рабочее развертывание FreeIPA
- кластер Proxmox VE
- Linux-гости, которым нужна централизованная аутентификация
- отдельная сервисная учетная запись для LDAP bind Proxmox
- понятная модель групп для администраторов и операторов

Проект делает FreeIPA источником истины для идентификации и доступа. Proxmox использует этот каталог через LDAP realm, Linux-гости вступают в FreeIPA через upstream-роль `ipaclient`, а SSH, HBAC и `sudo` остаются централизованными, а не распределенными по локальным учетным записям в каждой VM.

Этот repository особенно хорошо подходит, когда вы хотите, чтобы onboarding и offboarding в основном выглядели так:

1. создать или обновить users и groups в FreeIPA
2. синхронизировать эти identity в Proxmox
3. применить Proxmox roles и ACL на основе synced groups
4. дать Linux-гостям доступ через FreeIPA login, HBAC и `sudo` rules

## Что вы получаете

- управление группами пользователей, hostgroup, правилами HBAC и правилами `sudo` в FreeIPA
- значения login shell FreeIPA по умолчанию для Linux-администраторов
- настройку LDAP realm Proxmox на FreeIPA
- повторяющуюся синхронизацию realm Proxmox с одного назначенного узла кластера
- RBAC-привязки Proxmox для синхронизированных директорных групп
- enrollment Linux-гостей в FreeIPA через статический inventory, IP-only цели или discovery VM в Proxmox
- необязательный SSH bootstrap без перезагрузки через QEMU Guest Agent Proxmox
- необязательное включение коммуникации guest agent на стороне Proxmox для Linux-гостей, управляемых через Proxmox
- необязательную установку QEMU Guest Agent через SSH или WinRM как fallback для гостей, которые уже доступны, становятся доступны после bootstrap или повторно обрабатываются после Linux enrollment
- необязательный Linux readiness report для оценки SSH-доступности и состояния QEMU Guest Agent в Proxmox
- отдельный и необязательный workflow для domain membership Windows 10/11 и Windows Server через Active Directory
- ограниченный и необязательный Windows workflow с учетом FreeIPA для доверия к IPA CA, bootstrap hosts file и проверок доступности сервисов IPA
- необязательный bootstrap публичного SSH-ключа для первого доступа к Linux-гостям
- автоматическое обновление кэша SSSD на управляемых Linux-клиентах после изменений модели доступа FreeIPA
- необязательный Linux onboarding, управляемый событиями, через VM hooks Proxmox и webhook-триггеры

## Область охвата

| Включено | Не включено |
| --- | --- |
| Модель доступа FreeIPA | Развертывание FreeRADIUS |
| Настройка LDAP realm Proxmox | Полный жизненный цикл пользователей FreeIPA |
| RBAC Proxmox из синхронизированных групп | Полное покрытие всех multi-tenant edge case в Proxmox |
| Enrollment Linux IPA clients | Нативный логин Windows напрямую против FreeIPA |
| Отдельный workflow AD domain membership для Windows | Широкая автоматизация объектов AD или GPO |
| Ограниченный workflow Windows FreeIPA helpers | Попытка считать helper-путь на базе FreeIPA эквивалентом AD |

## Workflow Windows

Поддержка Windows реализована как отдельный workflow, а не встроена в Linux enrollment в IPA.

- `windows_qemu_guest_agent_clients` остается выделенной группой для необязательных helper-задач QEMU Guest Agent.
- включите workflow через `windows_domain_membership_enabled: true` в `10-features.yml`
- `windows_management_clients` — это отдельная группа управления Windows, используемая `playbooks/windows-management.yml` и необязательной стадией Windows внутри `playbooks/site.yml`
- реальный вход в Windows обрабатывается через membership в домене Active Directory; в инфраструктурах вокруг FreeIPA присоединяйте Windows-хосты к стороне AD trust-связи FreeIPA-AD вместо попытки вводить Windows напрямую в FreeIPA

Прямой Windows join только к FreeIPA этим репозиторием не поддерживается. Без Active Directory или trust FreeIPA-AD Windows-часть ограничена helper-задачами: управлением доступными гостями и необязательной установкой QEMU Guest Agent.

Если вам все же нужен ограниченный и aware-of-FreeIPA путь для Windows без domain join, включите `windows_freeipa_helpers_enabled: true` и используйте группу `windows_freeipa_helper_clients` с `playbooks/windows-freeipa-helpers.yml`. Этот helper-workflow может доверять IPA CA, автоматически забирать IPA CA для bootstrap, опционально фиксировать ожидаемый thumbprint CA, управлять записями hosts file, проверять IPA DNS и ключевые TCP-порты, валидировать HTTPS-доступность из Windows, проверять источник времени Windows относительно IPA-связанного endpoint, управлять членством в локальных Windows-группах и опционально устанавливать или публиковать OpenSSH Server, но он не дает нативный Windows login через FreeIPA.

Если вам нужен readiness-check без внесения изменений для этой helper-группы, запускайте `playbooks/windows-freeipa-validate.yml`. Он сохраняет логику проверки и сводки, но переводит импорт CA, изменения hosts file, изменения локальных групп и управление OpenSSH в безвредный режим только для этой проверки.

Этот workflow ориентирован на Windows 10/11 и Windows Server, доступные по WinRM или PSRP.

## Архитектура

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

Более подробное описание архитектуры приведено в [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Требования

### Контроллер

- Ansible Core 2.14 или новее
- SSH-доступ к основному узлу Proxmox, IPA-серверам и Linux-клиентам
- WinRM- или PSRP-доступ к Windows-гостям, если вы используете Windows workflow
- `sudo` или `root`, где это требуется
- при включенном QGA SSH bootstrap QEMU Guest Agent уже должен работать внутри гостя
- если включен fallback-установщик guest agent для Windows, доступные Windows-хосты должны находиться в `windows_qemu_guest_agent_clients`
- если включен Windows domain membership, доступные Windows-хосты должны находиться в `windows_management_clients`, и вы должны предоставить учетные данные для ввода в AD
- если включены FreeIPA helper-задачи для Windows, доступные Windows-хосты должны находиться в `windows_freeipa_helper_clients`
- если включен Linux SSH bootstrap, контроллеру нужна SSH key pair и начальный парольный путь входа для учетной записи гостя, которую использует Ansible

### Цели

- Proxmox VE 6.x и новее на хосте `proxmox_primary`
- доступный FreeIPA для Proxmox и Linux-клиентов
- Windows 10/11 и Windows Server могут управляться отдельным Windows workflow, если они доступны по WinRM или PSRP
- корректные DNS и синхронизация времени
- на `proxmox_primary` нужен `root` или SSH-пользователь с `sudo` для `pveversion`, `pvesh` и `pveum`
- если вы используете Windows domain membership, целевые Windows-гости должны уметь достигать соответствующих контроллеров домена AD
- если вы используете ограниченный Windows FreeIPA helper workflow, целевые Windows-гости должны уметь достигать соответствующих IPA-серверов
- при Proxmox discovery гость должен отдавать usable IP через QEMU Guest Agent

## Сетевые порты

Эта таблица перечисляет сетевые порты, которые использует контроллер этого репозитория, LDAP-автоматизация Proxmox и Linux IPA enrollment workflow.
Она намеренно ограничена поверхностью именно этого проекта, а не полной матрицей server-to-server репликации FreeIPA.

| Имя | Порт | Протокол | Источник | Назначение | Нужен когда | Назначение трафика |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible-контроллер | Узел Proxmox, IPA-сервер, Linux-гость | Всегда | Подключение Ansible |
| WinRM | `5985`, `5986` | `TCP` | Ansible-контроллер | Windows-гость | Когда включено Windows-управление | Подключение Ansible к Windows-гостям |
| DNS | `53` | `TCP`, `UDP` | Linux-гость | IPA DNS-серверы | Когда Linux-гости используют IPA DNS | Разрешение IPA-записей и внешних имен через IPA DNS |
| Kerberos | `88` | `TCP`, `UDP` | Linux-гость | IPA-серверы | Linux IPA enrollment и login | Kerberos-аутентификация |
| LDAP | `389` | `TCP` | Linux-гость | IPA-серверы | Linux IPA enrollment и login | LDAP и discovery клиента FreeIPA |
| HTTPS | `linux_freeipa_enroll_https_port`, по умолчанию `443` | `TCP` | Linux-гость | IPA-серверы | Linux IPA enrollment | Проверка IPA web/API при установке клиента |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux-гость | IPA-серверы | Linux IPA enrollment и операции с паролями | Kerberos password и keytab операции |
| LDAPS | `636` | `TCP` | Основной узел Proxmox | IPA- или LDAP-серверы | Когда LDAP realm Proxmox использует режим `ldaps` по умолчанию | Подключение LDAP realm Proxmox |

Примечания:

- `LDAPS 636/TCP` — стандартное значение репозитория, потому что `proxmox_ldap_mode` по умолчанию использует `ldaps`. Если вы меняете режим LDAP или порт, открывайте фактически настроенный `proxmox_ldap_port`.
- `WinRM` обычно использует `5986/TCP` для HTTPS или `5985/TCP` для HTTP, в зависимости от настроенного транспорта Windows.
- `DNS 53/TCP,UDP` нужен только когда Linux-гости используют IPA-серверы как resolvers.
- Для `Kerberos 88` и `Kerberos Password 464` требуются и `TCP`, и `UDP`.
- Ввод в домен Active Directory также требует стандартный набор Windows-to-domain-controller портов, но эта матрица зависит от среды и здесь специально не перечисляется полностью.
- Синхронизация времени по-прежнему обязательна для надежной работы Kerberos, но источник NTP зависит от среды и этим репозиторием не управляется.

## Совместимость

Автоматизация Proxmox в этом репозитории написана вокруг интерфейсов `pveum` и `pvesh` для realm и RBAC, используемых Proxmox VE 6.x и более новыми версиями.

- major-версии, поддерживаемые по умолчанию: `6`, `7`, `8`, `9`, `10`
- валидация проверяет обнаруженную версию Proxmox через `pveversion`
- список поддерживаемых major-версий можно переопределить через `proxmox_supported_major_versions`, если вам нужно сузить или расширить его под вашу среду
- `proxmox_allow_future_major_versions` по умолчанию равен `true`, поэтому major-версии выше последней протестированной также проходят валидацию по умолчанию
- будущие major-версии все равно следует рассматривать как кандидаты на совместимость, пока опубликованный интерфейс Proxmox не будет проверен против этой автоматизации
- старые legacy-major версии, например `1`–`5`, не объявляются как протестированная поддержка этим публичным репозиторием; если вы добавляете их локально, рассматривайте это как явный compatibility override и сначала валидируйте полный workflow в лаборатории

Пример локального override для legacy-лаборатории:

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

## Быстрый старт

Примеры ниже используют shell-команды. Там, где это важно, приведены эквиваленты PowerShell.

### 1. Скопируйте пример инвентаря и шаблоны vault

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Опционально, если вы планируете управлять Windows-гостями:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Опционально, если вы планируете управлять Windows-гостями:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Отредактируйте файлы, зависящие от среды

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml`, если вы используете управление Windows
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml`, если вы используете управление Windows

Помимо настроек IPA и Proxmox выберите один режим источника Linux-гостей:

- статические inventory entries под `linux_ipa_clients`
- элементы `linux_ipa_client_hosts` в `group_vars/all/30-linux-clients.yml`
- Proxmox VM discovery с `linux_ipa_proxmox_discovery_enabled: true`

Для Linux IPA enrollment разделяйте значения домена и списка серверов:

- `ipaclient_domain` — общий IPA DNS-домен, например `example.com`
- `linux_ipa_servers` содержит hostnames IPA-серверов, например `ipa01.example.com`

Если вы хотите подключаться к Proxmox по SSH обычным пользователем с `sudo`, а не `root`, настройте это под `proxmox_primary` в `hosts.yml` и храните пароль `sudo` в `vault-proxmox.yml`:

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

В этой схеме `vault_proxmox_become_password` — это пароль, который вы обычно вводили бы для `sudo` на Proxmox-хосте.

### 3. Зашифруйте vault-файлы

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

Добавьте `inventories/production/group_vars/all/vault-windows.yml` в ту же команду, если вы включаете Windows workflow.

Или используйте helper-wrapper'ы, которые по умолчанию применяют отдельные vault ID и при необходимости создают рабочие vault-файлы из example-шаблонов:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Если вы хотите отдельные пароли по доменам при запуске playbook, предпочитайте vault ID вместо `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Если необязательный Windows workflow тоже использует собственный пароль vault, добавьте `windows@prompt` в ту же команду.

Используйте `-AskVaultPass` только тогда, когда все vault-файлы, задействованные этим playbook, разделяют один пароль.

### 4. Установите нужную коллекцию

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Или напрямую:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

Если вы установили `freeipa.ansible_freeipa` до того, как этот репозиторий добавил compatibility patch, перезапустите один из bootstrap-helper'ов или один раз выполните `python .\scripts\patch_freeipa_collection.py`, чтобы пропатчить и существующую пользовательскую установку collection.

Когда вы используете `scripts/run-playbook.ps1`, он запускает этот patch-helper автоматически перед `ansible-playbook`.

### 5. Сначала запустите валидацию

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Если вы хотите проверить только helper-only Windows FreeIPA путь без внесения изменений в хосты:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Если вам нужен read-only аудит Linux readiness, который показывает, какие runtime-гости доступны по SSH и какие Proxmox-discovered гости отвечают через QEMU Guest Agent:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Readiness report по умолчанию записывает `.ansible/linux-readiness-report.json`.
Основные поля интерпретируются так:

- `ssh.ready=true`: текущий настроенный Ansible SSH-путь сработал с контроллера
- `ssh.promptless=true`: SSH-probe прошел без `ansible_password`, то есть путь не требует интерактива для Ansible
- `ssh.auth_mode=password_configured`: probe использовал `sshpass`, потому что у хоста был `ansible_password`
- `ssh.auth_mode=key_or_agent`: probe прошел в SSH batch mode без `ansible_password`
- `qga.status=available`: `qm guest ping` успешно выполнился на owning Proxmox node
- `qga.status=disabled`: конфигурация VM в Proxmox не включает QEMU Guest Agent
- `qga.status=configured_unresponsive`: guest agent включен в конфигурации Proxmox, но не ответил
- `qga.status=node_unreachable`: контроллер не смог достичь owning Proxmox node для этой проверки
- `qga.status=not_applicable`: хост не был создан через Proxmox discovery, поэтому QGA-probe не выполнялся

Пример быстрой проверки:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. Опционально: просмотрите планируемые изменения

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Относитесь к check mode как к частичному preview, а не к полной симуляции. Этот репозиторий использует прямые CLI-команды для части конфигурации Proxmox и upstream-роль клиента FreeIPA для Linux enrollment, поэтому `--check` полезен, но не является абсолютным источником истины.
>
> Для правил FreeIPA HBAC check mode валидирует этап определения правила, но пропускает последующее enable или disable действие. Это позволяет избежать ложных ошибок, когда FreeIPA сообщает, что правила нет, потому что оно не было реально создано в dry run.
>
> Роль таймера синхронизации realm Proxmox также пропускает финальный шаг `systemd` enable или start в check mode, потому что unit files отображаются в diff, но реально не записываются во время dry run.
>
> Linux IPA enrollment тоже пропускается в check mode. Репозиторий все равно выполняет discovery, resolution hostname и валидацию входных данных, но upstream-роль `ipaclient` не запускается в dry run.

### 7. Примените полную конфигурацию

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

Если необязательный Windows workflow включен, а `vault-windows.yml` использует отдельный пароль, запускайте тот же playbook с `--vault-id windows@prompt` или через PowerShell wrapper `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` вместо `--ask-vault-pass`.

## Порядок rollout

Для первого развертывания применяйте стек в таком порядке:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Опционально, если вы управляете Windows-гостями:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Опционально, если вам нужен ограниченный Windows FreeIPA helper-workflow:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Опционально, если вам нужен только validation-путь для helper-workflow:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

Такая последовательность значительно упрощает troubleshooting по сравнению с запуском всего сразу.

Пример ограниченного PowerShell rollout, например только для одного Linux-гостя:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Значения rollout по умолчанию консервативны:

- изменения модели доступа FreeIPA выполняются с `serial: 1`
- изменения Proxmox выполняются с `serial: 1`
- resolution hostname, validation и Linux enrollment выполняются с `serial: 10`
- изменения Windows management выполняются с `serial: 10`
- все rollout-пути по умолчанию используют `max_fail_percentage: 0`

Настройте эти значения в `inventories/production/group_vars/all/15-rollout.yml`.

## Модель тегов

Используйте теги, чтобы целиться в стабильные срезы rollout вместо создания все новых playbook.

- базовые домены: `freeipa`, `proxmox`, `linux`, `validate`
- Windows-домен: `windows`, `windows_domain`
- Windows FreeIPA helpers: `windows`, `windows_freeipa`
- модель FreeIPA: `freeipa_access`
- подмножества Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- подготовка Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- event-driven обработка VM: `event`, `linux_refresh`

Примеры:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Event-driven onboarding ВМ

Если вы хотите, чтобы Proxmox запускал Linux discovery и IPA enrollment сразу после старта VM или после миграции, используйте необязательный hook/webhook workflow из [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

Этот путь использует выделенный event-playbook `playbooks/proxmox-vm-event.yml`, поэтому триггер обрабатывает только Linux- и FreeIPA-часть гостя. Он не переисполняет автоматизацию LDAP realm и RBAC Proxmox на каждом VM event.

Репозиторий также умеет разворачивать этот необязательный hook/webhook stack через `site.yml` или `proxmox.yml`, когда `proxmox_vm_event_onboarding_enabled: true` задано и необходимые webhook-переменные заполнены.

Hooks VM в Proxmox не имеют отдельной фазы `create`. На практике новые VM обычно подхватываются при первом `post-start`, а migration hooks могут срабатывать и на source node, и на destination node.

## Модель инвентаря

Этот репозиторий использует шесть определенных inventory-групп и одну runtime-группу, создаваемую динамически:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Вы также можете определить собственные дополнительные inventory-группы и ссылаться на них в определениях hostgroup FreeIPA. Если вы хотите использовать полный набор подготовленных Linux-гостей на стороне hostgroup FreeIPA, ссылайтесь на группу `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> FreeIPA по-прежнему нужен финальный hostname для каждого гостя. Если вы используете IP-only цели или Proxmox discovery, задайте `ipa_hostname` явно либо убедитесь, что `hostname -f` внутри гостя возвращает финальный FQDN. Теперь playbook сначала резолвит это имя перед построением membership в hostgroup FreeIPA.

> [!TIP]
> Не enroll'ьте reusable golden template напрямую в FreeIPA. Сначала клонируйте VM, задайте финальный hostname и только затем enroll'ьте получившегося гостя.

### Источники Linux-гостей

Вы можете наполнить `linux_ipa_clients` тремя способами.

#### 1. Статические хосты в inventory

Если имена гостей вам уже известны, используйте обычные inventory entries Ansible:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. Ручные определения хостов в переменных

Используйте `linux_ipa_client_hosts`, когда вы хотите держать гостей вне `hosts.yml` или когда у вас есть только IP:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Примечания:

- если `name` уже является резолвимым hostname или FQDN, `ansible_host` необязателен
- если вы знаете только IP, используйте любой стабильный alias в поле `name`
- если `ipa_hostname` не задан, playbook откатывается к `hostname -f` внутри гостя

#### 3. Auto-discovery VM в Proxmox

Используйте discovery, если вы хотите, чтобы playbook подтягивал Linux-гостей с одного или нескольких узлов Proxmox:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Опционально: ограничьте automation по discovery только явно одобренными гостями.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Опционально: всегда исключайте инфраструктурные или чувствительные гости,
# даже когда широкое node discovery включено.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# Опциональные first-touch SSH-параметры для discovered-гостей, если guest
# agent еще не запущен и репозиторию нужно зайти по SSH, чтобы его установить.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

Примечания:

- discovery добавляет VM в ту же группу `linux_ipa_clients_runtime`, которую используют остальные playbook
- IP discovery зависит от того, что QEMU guest agent сообщает сетевые интерфейсы
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` доверяет только именам VM, которые уже являются FQDN
- задайте `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true`, если вы также хотите автоматически преобразовывать безопасные короткие имена VM Proxmox, такие как `Teleport-Server-1`, в hints hostname вроде `teleport-server-1.example.com` через `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` опционален и в основном используется event-driven hook/webhook workflow для ограничения discovery одним или несколькими конкретными VMID
- гостю все равно нужен финальный hostname — уже настроенный внутри VM или переданный через `ipa_hostname` в ручном определении
- реальный системный hostname гостя тоже должен быть валидным для enrollment; placeholder-значения вроде `localhost.localdomain` должны быть заменены на VM до запуска `linux-clients` или `site`
- если гости используют короткие hostnames, например `app-server-01`, вы можете задать `linux_ipa_identity_hostname_suffix` и опционально `linux_freeipa_enroll_manage_hostname: true`, чтобы проект вычислил и применил полное имя вроде `app-server-01.example.net` до enrollment
- если DNS FreeIPA является authoritative для hostname ваших гостей, вы можете задать `linux_freeipa_enroll_manage_authoritative_dns: true`, чтобы проект исправлял A- и PTR-записи конкретного гостя и удалял link-local AAAA-записи `fe80::/10` до enrollment
- если DNS еще не готов, задайте `linux_ipa_manage_etc_hosts: true` и предоставьте `linux_ipa_etc_hosts_entries`, чтобы роль добавила управляемый bootstrap-блок `/etc/hosts` для IPA-серверов и guest FQDN перед проверками enrollment
- `guest_qemu_agent_install_enabled` устанавливает QEMU Guest Agent на гостей, уже доступных по SSH или WinRM, повторяет попытку для Linux-гостей, которые становятся доступными позже в том же workflow, и еще раз после Linux enrollment, чтобы последующие agent-dependent workflow Proxmox могли его использовать
- задайте `linux_ipa_proxmox_discovery_allowlist_enabled: true`, если хотите сохранить discovery включенным, но допускать в Linux runtime inventory только строго одобренное подмножество Proxmox-гостей; allowlist умеет точно матчить VMID, IP и имена
- задайте `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips` или `linux_ipa_proxmox_discovery_blacklist_names`, если discovery-enabled узлы также содержат инфраструктурные VM, такие как firewalls или DNS servers, которые никогда не должны получать Linux IPA automation; совпадения blacklist всегда побеждают admission через широкое discovery или allowlist
- для Linux-гостей, обнаруженных в Proxmox и еще не имеющих рабочего guest agent, задайте `linux_ipa_proxmox_discovery_ansible_user` и также `linux_ipa_proxmox_discovery_ansible_password` или `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file`, чтобы репозиторий имел рабочий first-touch SSH path и мог установить QEMU Guest Agent
- если такие discovered-гости используют SSH-пользователя не `root`, задайте также `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method` и `linux_ipa_proxmox_discovery_ansible_become_password`, если только эта учетная запись уже не имеет passwordless sudo
- `guest_qemu_agent_install_manage_proxmox_vm_agent` также включает коммуникацию guest agent на стороне Proxmox (`qm set <vmid> --agent 1`) для Proxmox-backed Linux-гостей до запуска guest-side install path
- если этот Proxmox VM option меняется на работающей VM, по умолчанию репозиторий только предупреждает, потому что Proxmox может потребовать новый старт VM, прежде чем хост сможет использовать guest-agent channel; задайте `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true`, если хотите, чтобы репозиторий автоматически перезагружал такие работающие VM
- `linux_ipa_ssh_host_key_policy` по умолчанию использует `accept_new` для подключений к Linux-гостям, чтобы к newly discovered VM можно было подключаться без полного отключения host key checking; изменившиеся host keys все равно приводят к ошибке и требуют проверки оператором
- `linux_ipa_qga_ssh_bootstrap_enabled` — предпочтительный no-reboot bootstrap path для Proxmox-backed гостей, потому что он умеет создавать выделенного key-only automation user через QEMU Guest Agent до появления любого SSH-login
- `linux_ipa_qga_ssh_bootstrap_qm_path` по умолчанию равен `qm`, а bootstrap flow также проверяет распространенные fallback paths на Proxmox node перед окончательной ошибкой
- гости, которые позволяют `guest-ping`, но блокируют `guest-exec`, по умолчанию пропускаются в QGA bootstrap; держите для них другой SSH path или задайте `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` для fail-fast поведения
- `linux_ipa_ssh_bootstrap_enabled` опционально устанавливает SSH public key контроллера на Linux-гости до resolution hostname и enrollment; `linux_ipa_ssh_bootstrap_password` также используется как общий first-touch password fallback для runtime Linux-гостей даже при отключенном key-bootstrap
- Linux IPA enrollment повторяет upstream client joins, завершившиеся JSON-RPC timeout на FreeIPA, и раскрывает `linux_ipaclient_kinit_attempts` для более медленных или загруженных IPA-сред
- Linux IPA enrollment также по умолчанию добавляет inventory-hostnames из `ipa_servers` в список join servers, чтобы клиенты использовали полный набор IPA-серверов, а не одну настроенную точку
- когда доступно больше одного IPA-сервера, каждый retry-pass пытается эти кандидаты IPA-серверов по одному во время Linux client enrollment
- combined workflow `site` сначала создает hostgroup FreeIPA, а затем добавляет enrolled runtime hosts, чтобы pre-enrollment runs не падали на шаге membership в hostgroup из-за еще не enrolled-гостей

## Поверхность конфигурации

Большинство значений находится в:

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

Для структуры по файлам смотрите [docs/VARIABLES.md](../VARIABLES.md).

Ключевые семейства переменных:

| Область | Переменные |
| --- | --- |
| Модель доступа FreeIPA | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Контроль rollout | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| LDAP realm Proxmox | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| RBAC Proxmox | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Linux readiness reporting | `linux_readiness_report_*` |
| Управление Windows | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helpers | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Секреты Ansible-подключений | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Пример групповой стратегии

Простой паттерн, который хорошо масштабируется:

- группа пользователей FreeIPA `proxmox-admins`
- группа пользователей FreeIPA `linux-ssh-admins`
- hostgroup FreeIPA `linux-all`
- правило HBAC `allow-linux-ssh-admins`
- правило sudo `allow-linux-ssh-admins-sudo`
- ACL binding Proxmox для синхронизированной группы `proxmox-admins-ipa`

Заполните `freeipa_linux_admin_users` в [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml), если вы хотите, чтобы combined run `site.yml` автоматически выдавал конкретным пользователям IPA доступ по Linux SSH и sudo через управляемую группу `linux-ssh-admins`.

Помните, что Proxmox LDAP sync создает синхронизированные группы с суффиксом:

```text
<group-name>-<realm>
```

Если ваша группа FreeIPA называется `proxmox-admins`, а realm Proxmox — `ipa`, результирующая синхронизированная группа PVE будет:

```text
proxmox-admins-ipa
```

## Безопасность

- храните все секреты в `vault-freeipa.yml` и `vault-proxmox.yml`, а не в plaintext inventory-файлах переменных
- для Proxmox предпочтителен выделенный read-only LDAP bind account
- предпочитайте TLS с включенной проверкой сертификатов
- сохраняйте SSH host key checking включенным вне disposable-лабораторий
- предпочитайте `linux_ipa_qga_ssh_bootstrap_enabled` общим временным паролям, когда ваши Proxmox-гости уже имеют рабочий QEMU Guest Agent
- используйте `guest_qemu_agent_install_enabled` только если у репозитория уже есть валидный management path внутрь гостя; для Proxmox discovery это означает, что QGA уже работает или настроены `linux_ipa_proxmox_discovery_ansible_user` и доступ по паролю или ключу
- если вы включаете Linux SSH bootstrap, храните общий bootstrap password в зашифрованных переменных и меняйте или удаляйте его после установления key-based access
- не переиспользуйте IPA admin account как LDAP bind account для Proxmox
- перед production rollout проверьте `proxmox_ldap_filter` и `proxmox_ldap_group_filter`, чтобы не импортировать лишние объекты

Для disposable-лаборатории, где вы осознанно хотите отключить проверку SSH host key, делайте это на уровне shell session, а не изменением defaults репозитория:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Идемпотентность и ограничения

Проект написан так, чтобы быть переиспользуемым и в основном идемпотентным, но его все равно следует проверять в лаборатории перед production rollout.

Известные caveat'ы:

- вывод CLI Proxmox может слегка отличаться между версиями
- layout директорий FreeIPA гибок, поэтому LDAP filter может требовать подстройки под вашу tree
- ранее вручную созданные ACL и roles в PVE нужно сравнить перед применением автоматизации поверх них
- auto-discovery VM в Proxmox зависит от работающих гостей и сетевых данных QEMU guest agent
- IP-only определения гостей все равно требуют валидного финального hostname внутри гостя или явного `ipa_hostname`
- playbook'и Proxmox выполняются с privilege escalation, поэтому SSH-пользователь не `root` должен иметь рабочий `sudo`, и вы должны предоставить become password через `-K`, если только у этого пользователя нет passwordless sudo
- если вы храните `ansible_become_password` в `vault-proxmox.yml`, можно не использовать `-K`, потому что Ansible прочитает пароль sudo из зашифрованной переменной

## Проверка

После успешного rollout проверяйте итоговое состояние явно, а не предполагайте, что все пути доступа уже работают корректно.

### В FreeIPA

- подтвердите, что ожидаемые группы пользователей существуют
- подтвердите, что ожидаемые hostgroup существуют
- подтвердите, что ожидаемые правила HBAC существуют и включены
- подтвердите, что ожидаемые правила `sudo` существуют и включены

### В Proxmox

- подтвердите, что LDAP realm существует
- подтвердите, что initial sync импортировал ожидаемых пользователей или группы
- подтвердите, что нужная синхронизированная группа получила ожидаемый ACL binding

### На Linux-госте

- подтвердите, что разрешенный пользователь IPA может войти
- подтвердите, что запрещенный пользователь блокируется HBAC
- подтвердите, что разрешенный IPA-администратор может выполнить `sudo -l`
- подтвердите, что home directory создается при первом входе, если включен `linux_ipaclient_mkhomedir`

## Структура репозитория

<details>
<summary>Показать структуру репозитория</summary>

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

## Разработка

Основные helper-файлы, включенные в репозиторий:

- `.editorconfig`, чтобы поддерживать единые настройки пробелов, кодировки и окончаний строк между редакторами
- `.gitattributes`, чтобы фиксировать типичные текстовые файлы на `LF`
- `.gitignore`, чтобы generated inventory, vault data, локальные collection'ы и editor junk не попадали в Git
- `.ansible-lint`, чтобы исключать vendor collection paths и подавлять только правило длины строк YAML
- `.yamllint`, чтобы поддерживать единообразную YAML-валидацию для playbook, inventory и workflow-файлов
- `.github/CODEOWNERS`, чтобы направлять review ownership по основным областям репозитория
- `.github/workflows/ci.yml`, чтобы запускать lint и smoke validation на push и pull request
- `.pre-commit-config.yaml`, чтобы запускать быстрый lint hook перед commit, если установлен `pre-commit`
- `CHANGELOG.md`, чтобы отслеживать значимые изменения репозитория в одном месте
- `docs/VARIABLES.md`, чтобы объяснять разнесенную структуру inventory-переменных
- `docs/i18n/`, чтобы хранить переведенные README; эти файлы должны отражать полную секционную структуру английского `README.md`
- `docs/i18n/TRANSLATION_GUIDE.md`, чтобы объяснять, как поддерживать переведенные README синхронизированными
- `scripts/bootstrap.ps1` и `scripts/bootstrap.sh`, чтобы устанавливать необходимую collection в локальный путь `collections/` и применять compatibility patch для ansible-core 2.24+
- `scripts/patch_freeipa_collection.py`, чтобы переписывать deprecated imports внутри закрепленной FreeIPA collection и сохранять совместимость с будущими версиями ansible-core
- `scripts/lint.py`, чтобы предоставлять multiplatform lint entry point для локального использования, CI и pre-commit
- `scripts/smoke-test.py`, чтобы выполнять example inventory validation и syntax checks без касания реальной инфраструктуры, включая coverage для отдельного Windows playbook
- `scripts/check_translations.py`, чтобы аудитить translated README по metadata, parity структуры разделов и минимальному coverage контента относительно канонического английского README
- `scripts/lint.ps1` и `scripts/lint.sh`, чтобы объединять локальный lint и smoke workflow
- `scripts/proxmox_event_webhook.py`, чтобы работать как optional controller-side webhook для VM events Proxmox
- `scripts/proxmox-vm-hook.pl`, чтобы выполнять роль optional VM hook, установленного на узлах Proxmox
- `scripts/run-playbook.ps1`, чтобы предоставлять единый `ansible-playbook` wrapper в средах Windows и PowerShell
- `scripts/vault.ps1` и `scripts/vault.sh`, чтобы помогать создавать, редактировать, просматривать и шифровать vault-файлы, разделенные по доменам
- `tests/`, чтобы хранить verification surface репозитория, начиная с smoke-test documentation
- `CONTRIBUTING.md`, чтобы документировать ожидаемый contribution и validation workflow
- `SECURITY.md`, чтобы документировать порядок сообщения об уязвимостях и обращения с security-sensitive информацией

Если на вашем controller установлен `ansible-lint`:

```bash
ansible-lint
```

Чтобы запускать repository smoke checks напрямую:

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

Для полного local lint pass:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

Чтобы включить fast lint hook перед каждым commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper теперь напрямую поддерживает и типичные operator options:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Дальнейшие расширения

Типичные расширения, которые логично рассмотреть дальше:

- Packer pipeline для IPA-ready Linux templates
- templates jobs и scheduling в AWX или Automation Controller для объединенных rollout
- более сильные модели tenant и pool в Proxmox
- AD trust workflow для Windows RDP или гибридных identity-сред

## Лицензия

Проект распространяется по [0BSD License](../../LICENSE).
