# Автоматизация доступа Proxmox + FreeIPA

Эта страница содержит полную структурную русскую версию [README.md](../../README.md). Английский текст остается каноническим источником, но здесь сохранены те же основные разделы.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Зачем нужен этот проект

Используйте репозиторий, если у вас уже есть:

- рабочее развертывание FreeIPA
- кластер Proxmox VE
- Linux-гости, которым нужна централизованная аутентификация
- отдельная сервисная учетная запись для LDAP bind Proxmox
- понятная модель групп для администраторов и операторов

Проект делает FreeIPA источником истины для идентификации и доступа. Proxmox использует этот каталог через LDAP realm, Linux-клиенты вступают в FreeIPA через роль `ipaclient`, а SSH, HBAC и `sudo` остаются централизованными.

## Что вы получаете

- управление группами пользователей, hostgroup, правилами HBAC и правилами `sudo` в FreeIPA
- настройку LDAP realm Proxmox на FreeIPA
- периодическую синхронизацию realm с одного выбранного узла кластера
- RBAC-привязки Proxmox для синхронизированных групп
- подключение Linux через статический inventory, ручные описания или Proxmox discovery
- необязательный SSH bootstrap без перезагрузки через QEMU Guest Agent
- необязательную установку QEMU Guest Agent через SSH или WinRM
- необязательный bootstrap публичного SSH-ключа для первого доступа
- автоматическое обновление кэша SSSD после изменений модели доступа
- необязательное event-driven onboarding для `post-start` и `post-migrate`

## Область охвата

| Включено | Не включено |
| --- | --- |
| Модель доступа FreeIPA | Ввод Windows в домен |
| Настройка LDAP realm Proxmox | Развертывание FreeRADIUS |
| RBAC Proxmox из синхронизированных групп | Полный жизненный цикл пользователей FreeIPA |
| Подключение Linux IPA clients | Все крайние случаи multi-tenant Proxmox |

## Архитектура

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## Требования

### Контроллер

- Ansible Core 2.14+
- SSH-доступ к основному узлу Proxmox, IPA-серверам и Linux-клиентам
- `sudo` или `root`, где это требуется
- при включенном QGA SSH bootstrap агент QEMU должен уже работать в госте
- для Windows fallback доступные хосты должны быть в `windows_qemu_guest_agent_clients`
- для Linux SSH bootstrap нужен SSH-ключ и начальный парольный доступ

### Цели

- Proxmox VE 6.x и новее на хосте `proxmox_primary`
- доступный FreeIPA для Proxmox и Linux-клиентов
- корректные DNS и синхронизация времени
- на `proxmox_primary` нужен `root` или SSH-пользователь с `sudo` для `pveversion`, `pvesh` и `pveum`
- при Proxmox discovery гость должен отдавать usable IP через QEMU Guest Agent

## Сетевые порты

Основные порты:

- `22/TCP` для SSH
- `53/TCP,UDP` для IPA DNS
- `88/TCP,UDP` и `464/TCP,UDP` для Kerberos
- `389/TCP` для LDAP
- `linux_freeipa_enroll_https_port`, по умолчанию `443/TCP`
- `636/TCP` для `ldaps`

## Совместимость

- рассчитано на Proxmox VE 6.x и новее
- major-версии по умолчанию: `6`, `7`, `8`, `9`, `10`
- список меняется через `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions` по умолчанию `true`

## Быстрый старт

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

Перед запуском отредактируйте `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml` и `vault-proxmox.yml`.

## Порядок rollout

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

По умолчанию используются консервативные значения: `serial: 1` для FreeIPA и Proxmox, `serial: 10` для Linux и `max_fail_percentage: 0`.

## Модель тегов

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven onboarding ВМ

Для автоматического запуска Linux discovery и IPA enrollment после `post-start` или `post-migrate` используйте workflow из [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md). Он использует `playbooks/proxmox-vm-event.yml`, не повторяет LDAP realm и RBAC на каждый VM event и подхватывает новые VM на первом `post-start`.

## Модель inventory

Основные группы:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

Даже при IP-only и Proxmox discovery гостю нужен финальный FQDN через `ipa_hostname` или `hostname -f`.

### Источники Linux-гостей

1. статические inventory hosts
2. ручные записи в `linux_ipa_client_hosts`
3. Proxmox discovery через `linux_ipa_proxmox_discovery_*`

Ключевые замечания: discovery зависит от QEMU Guest Agent, `linux_ipa_proxmox_discovery_vmids` полезен для event path, короткие имена можно расширять через `linux_ipa_identity_hostname_suffix`, authoritative DNS можно чинить через `linux_freeipa_enroll_manage_authoritative_dns`, а при неготовом DNS можно использовать `linux_ipa_manage_etc_hosts`.

## Поверхность конфигурации

Основные файлы:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Пример групповой стратегии

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## Безопасность

- храните секреты только в vault
- для Proxmox лучше использовать отдельный read-only LDAP bind account
- предпочитайте TLS с проверкой сертификатов
- не отключайте SSH host key checking вне временных лабораторий

## Идемпотентность и ограничения

Проект рассчитан на повторные запуски, но должен быть проверен в лаборатории до продакшена. Известные ограничения: различия вывода CLI Proxmox, необходимость настройки LDAP filter, зависимость discovery от работающих VM и QGA, а также обязательность корректного финального hostname для IP-only целей.

## Проверка

- в FreeIPA проверьте группы, hostgroup, HBAC и `sudo`
- в Proxmox проверьте LDAP realm, sync и ACL bindings
- на Linux-госте проверьте вход разрешенного пользователя, блокировку запрещенного, `sudo -l` и создание home

## Структура репозитория

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## Разработка

Репозиторий включает `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflow, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1` и `scripts/vault.*`.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## Дальнейшие расширения

- Packer pipeline для IPA-ready Linux templates
- AWX job templates и schedules
- отдельные модели tenant и pool в Proxmox
- Windows или AD-trust путь для RDP-ориентированных сред

## Лицензия

Проект распространяется по [MIT License](../../LICENSE).
