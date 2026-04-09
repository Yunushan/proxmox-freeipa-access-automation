# Proxmox + FreeIPA 액세스 자동화

이 문서는 [README.md](../../README.md)의 전체 구조를 한국어로 옮긴 버전입니다. 영어 문서가 최종 canonical source 이지만, 이 파일도 같은 핵심 섹션을 모두 다룹니다.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## 이 프로젝트가 존재하는 이유

다음 조건이 이미 갖춰진 환경에서 사용합니다.

- 정상적인 FreeIPA 환경
- Proxmox VE 클러스터
- 중앙 인증을 써야 하는 Linux guest
- Proxmox LDAP bind 용 전용 서비스 계정
- 관리자와 운영자용의 명확한 그룹 모델

핵심 원칙은 FreeIPA를 identity와 access의 source of truth로 두는 것입니다. Proxmox는 이를 LDAP realm으로 소비하고, Linux guest는 `ipaclient` role로 FreeIPA에 가입하며, SSH, HBAC, `sudo` 제어는 중앙에 남겨 둡니다.

## 제공되는 기능

- FreeIPA user group, hostgroup, HBAC rule, `sudo` rule 관리
- FreeIPA 기반 Proxmox LDAP realm 설정
- 지정된 클러스터 노드에서 수행되는 주기적 realm sync
- 동기화된 그룹에 대한 Proxmox RBAC binding
- static inventory, manual host definition, Proxmox discovery 기반 Linux enrollment
- QEMU Guest Agent를 통한 optional no-reboot SSH bootstrap
- reachable guest에 대한 optional SSH/WinRM guest-agent install
- first-touch를 위한 optional SSH public-key bootstrap
- FreeIPA access 변경 후 automatic SSSD refresh
- `post-start`, `post-migrate`를 위한 optional event-driven onboarding

## 범위

| 포함 | 포함되지 않음 |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm 설정 | FreeRADIUS deployment |
| synced group 기반 Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | 모든 Proxmox multi-tenant edge case |

## 아키텍처

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## 요구 사항

### Controller

- Ansible Core 2.14+
- Proxmox primary node, IPA server, Linux client로의 SSH 연결
- 필요 시 `sudo` 또는 `root`
- QGA SSH bootstrap 사용 시 guest 안에서 QEMU Guest Agent가 이미 실행 중이어야 함
- Windows fallback 사용 시 reachable host가 `windows_qemu_guest_agent_clients`에 있어야 함
- Linux SSH bootstrap 사용 시 SSH keypair와 초기 password login 경로가 필요함

### Targets

- `proxmox_primary`에 있는 Proxmox VE 6.x 이상
- Proxmox와 Linux client에서 접근 가능한 FreeIPA
- 올바른 DNS와 시간 동기화
- `proxmox_primary`에서는 `root` 또는 `pveversion`, `pvesh`, `pveum`을 `sudo`로 실행 가능한 사용자
- Proxmox discovery 사용 시 QEMU Guest Agent를 통해 usable IP를 제공하는 guest

## 네트워크 포트

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP`, `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, 기본값 `443/TCP`
- `636/TCP` for `ldaps`

## 호환성

- Proxmox VE 6.x 이상을 대상으로 함
- default supported majors: `6`, `7`, `8`, `9`, `10`
- `proxmox_supported_major_versions`로 override 가능
- `proxmox_allow_future_major_versions` 기본값은 `true`

## 빠른 시작

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

환경에 맞게 `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, `vault-proxmox.yml`를 수정합니다.

## Rollout 순서

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

기본값은 보수적입니다. FreeIPA와 Proxmox는 `serial: 1`, Linux는 `serial: 10`, 그리고 `max_fail_percentage: 0`을 사용합니다.

## Tag 모델

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

`post-start` 또는 `post-migrate` 직후에 Linux discovery와 IPA enrollment를 자동 실행하려면 [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md)의 optional hook/webhook workflow를 사용합니다. 이 경로는 `playbooks/proxmox-vm-event.yml`을 사용하고, 각 event마다 LDAP realm이나 RBAC를 다시 실행하지 않으며, 새 VM은 첫 `post-start`에서 처리합니다.

## Inventory 모델

주요 그룹:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only 대상이나 Proxmox discovery를 쓰더라도 guest에는 `ipa_hostname` 또는 `hostname -f`를 통한 최종 FQDN이 필요합니다.

### Linux source mode

1. static inventory hosts
2. `linux_ipa_client_hosts`의 manual definitions
3. `linux_ipa_proxmox_discovery_*`를 통한 Proxmox discovery

중요한 메모: discovery는 QEMU Guest Agent의 network data에 의존하고, `linux_ipa_proxmox_discovery_vmids`는 event path에서 유용하며, 짧은 hostname은 `linux_ipa_identity_hostname_suffix`로 보완할 수 있고, authoritative DNS 수리는 `linux_freeipa_enroll_manage_authoritative_dns`, DNS 미준비 상태는 `/etc/hosts` bootstrap으로 보완할 수 있습니다.

## Configuration surface

주요 파일:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## 예시 그룹 전략

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## 보안

- secrets는 vault 파일에만 저장
- Proxmox에는 read-only 전용 LDAP bind account 사용 권장
- certificate verification이 있는 TLS 선호
- disposable lab이 아니면 SSH host key checking을 끄지 않기

## Idempotency와 주의사항

이 repository는 반복 실행을 염두에 두고 작성되었지만, production 전에 lab에서 검증해야 합니다. 알려진 제약에는 Proxmox CLI output 차이, LDAP filter tuning 필요성, discovery의 QGA 및 running guest 의존성, IP 기반 target에 대한 최종 hostname 요구가 있습니다.

## 검증

- FreeIPA에서 groups, hostgroups, HBAC, `sudo` 확인
- Proxmox에서 LDAP realm, sync, ACL bindings 확인
- Linux guest에서 allowed login, denied HBAC case, `sudo -l`, home 생성 확인

## 저장소 레이아웃

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## 개발

이 저장소에는 `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflows, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, `scripts/vault.*`가 포함됩니다.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## 다음 확장

- IPA-ready Linux template용 Packer pipeline
- AWX job template 및 schedule
- 분리된 Proxmox tenant / pool model
- RDP 지향 환경을 위한 Windows 또는 AD-trust flow

## 라이선스

이 프로젝트는 [MIT License](../../LICENSE)로 배포됩니다.
