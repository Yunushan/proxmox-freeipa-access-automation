# Proxmox + FreeIPA 액세스 자동화

이 문서는 [README.md](../../README.md)의 전체 구조와 운영 범위를 한국어로 옮긴 완전 번역본입니다. 영어 문서가 정본이지만, 이 한국어 문서도 같은 수준의 운영 문맥을 담아야 합니다.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## 언어

전체 문서의 정본은 영어판입니다. 추가로 20개 언어의 전체 번역 README도 제공됩니다.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

이 repository 는 Identity 와 Access 의 **source of truth 를 FreeIPA** 로 둡니다. Proxmox 는 LDAP realm 을 통해 그 directory 를 사용하고, Linux guest 는 upstream `ipaclient` role 을 통해 FreeIPA 에 가입하며, access 는 synced groups, HBAC, sudo rules 로 중앙에 유지되고 각 VM 의 local account 로 흩어지지 않습니다.

> [!IMPORTANT]
> 이 프로젝트는 **FreeRADIUS 를 identity source 로 사용하지 않으며**, **각 VM 내부에 local user 를 만들지 않고**, **Proxmox permission 의 모든 edge case 를 관리하려고 하지 않습니다**.

## 이 프로젝트가 존재하는 이유

이 저장소는 다음 전제가 이미 갖춰진 환경을 위한 것입니다.

- 정상적으로 동작하는 FreeIPA
- Proxmox VE 클러스터
- 중앙 인증을 사용해야 하는 Linux guest
- Proxmox LDAP bind 전용 서비스 계정
- 관리자와 운영자를 위한 명확한 그룹 모델

핵심 원칙은 Identity와 Access의 source of truth를 FreeIPA 하나로 두는 것입니다. Proxmox는 그 디렉터리를 LDAP realm으로 소비하고, Linux guest는 upstream `ipaclient` role을 통해 FreeIPA에 가입하며, SSH, HBAC, `sudo` 제어는 각 VM의 로컬 계정으로 흩어지지 않고 중앙에 남습니다.

다음과 같은 onboarding / offboarding 흐름을 원할 때 이 repository 가 잘 맞습니다.

1. FreeIPA 에서 user 와 group 을 생성하거나 갱신한다
2. 그 identity 를 Proxmox 로 sync 한다
3. synced group 으로부터 Proxmox role 과 ACL 을 적용한다
4. FreeIPA login, HBAC, `sudo` rule 로 Linux guest access 를 허용한다

## 제공되는 기능

- FreeIPA의 user group, hostgroup, HBAC rule, `sudo` rule 관리
- Linux 관리자용 FreeIPA 기본 login shell 적용
- FreeIPA를 가리키는 Proxmox LDAP realm 설정
- 지정된 한 클러스터 노드에서 수행하는 주기적 Proxmox realm sync
- 동기화된 디렉터리 그룹에 대한 Proxmox RBAC binding
- static inventory, IP 기반 target, Proxmox VM discovery를 통한 Linux guest의 FreeIPA enrollment
- Proxmox QEMU Guest Agent를 활용하는 reboot 없는 SSH bootstrap 선택 기능
- Proxmox가 관리하는 Linux guest에서 Proxmox 측 guest agent communication channel을 켜는 선택 기능
- 이미 도달 가능한 guest, bootstrap 후 도달 가능해진 guest, Linux enrollment 후 다시 시도할 guest를 대상으로 하는 SSH 또는 WinRM 기반 QEMU Guest Agent 선택 설치
- SSH 도달성과 Proxmox QEMU Guest Agent 상태를 확인하는 선택형 Linux readiness report
- Active Directory를 사용하는 Windows 10/11 및 Windows Server용 분리된 선택형 domain membership workflow
- IPA CA trust, hosts file bootstrap, IPA service 도달성 검증에 한정된 FreeIPA-aware Windows helper workflow
- Linux guest에 대한 최초 접속용 SSH 공개키 bootstrap
- FreeIPA access model 변경 뒤 관리 대상 Linux client에서 SSSD cache 자동 refresh
- Proxmox VM hook과 webhook trigger를 이용한 선택형 event-driven Linux onboarding

## 범위

| 포함됨 | 포함되지 않음 |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm 설정 | FreeIPA user lifecycle 전체 생성 |
| 동기화된 그룹 기반 Proxmox RBAC | Proxmox multi-tenant의 모든 edge case 완전 대응 |
| Linux client의 IPA enrollment | FreeIPA에 대한 Windows native login |
| Windows용 AD domain membership workflow | AD object 또는 GPO의 광범위한 자동화 |
| Windows용 제한적 FreeIPA helper workflow | FreeIPA 기반 Windows helper를 AD와 동등하다고 간주하는 것 |

## Windows 워크플로

Windows 지원은 Linux IPA enrollment 흐름에 섞지 않고 별도 workflow로 분리되어 있습니다.

- `windows_qemu_guest_agent_clients`는 선택형 QEMU Guest Agent helper task 전용입니다.
- `10-features.yml`에서 `windows_domain_membership_enabled: true`를 설정하면 Windows workflow가 활성화됩니다.
- `windows_management_clients`는 `playbooks/windows-management.yml`과 `playbooks/site.yml`의 선택형 Windows 단계가 사용하는 별도 그룹입니다.
- 실제 Windows login은 Active Directory domain membership으로 처리합니다. FreeIPA 중심 환경에서는 Windows를 FreeIPA에 직접 join시키기보다 FreeIPA-AD trust의 AD 측에 참여시키는 편이 맞습니다.

FreeIPA만으로 Windows를 join하는 것은 이 저장소의 지원 범위가 아닙니다. Active Directory 또는 FreeIPA-AD trust가 없다면, Windows 측 자동화는 도달 가능한 guest 관리와 선택형 QEMU Guest Agent 설치 정도로 제한됩니다.

도메인 join 없이도 FreeIPA-aware한 제한적 Windows path가 필요하다면, `windows_freeipa_helpers_enabled: true`를 활성화하고 `playbooks/windows-freeipa-helpers.yml`과 함께 `windows_freeipa_helper_clients`를 사용하십시오. 이 helper workflow는 IPA CA trust, bootstrap용 IPA CA 자동 수집, 기대 CA thumbprint의 선택적 pinning, hosts file entry의 선택적 관리, IPA DNS 및 주요 TCP port 검증, Windows에서의 HTTPS 도달성 검증, IPA 관련 endpoint에 대한 Windows time source 검증, Windows local group membership 관리, OpenSSH Server의 선택적 설치 또는 노출을 수행할 수 있지만, FreeIPA에 대한 Windows native login은 제공하지 않습니다.

같은 helper group에 대해 변경 없이 readiness check만 수행하고 싶다면 `playbooks/windows-freeipa-validate.yml`을 실행하십시오. 이 workflow는 validation과 summary 흐름은 유지하되, CA import, hosts file 변경, local group 변경, OpenSSH 관리를 해당 run에 한해 non-mutating으로 바꿉니다.

이 workflow는 WinRM 또는 PSRP로 도달 가능한 Windows 10/11 및 Windows Server guest를 대상으로 합니다.

## 아키텍처

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

더 긴 설계 설명은 [docs/ARCHITECTURE.md](../ARCHITECTURE.md)에 있습니다.

## 요구 사항

### 컨트롤러

- Ansible Core 2.14 이상
- Proxmox primary node, IPA server, Linux client로의 SSH 도달성
- Windows workflow를 사용할 경우 Windows guest로의 WinRM 또는 PSRP 도달성
- 필요 시 `sudo` 또는 `root`
- QGA SSH bootstrap을 사용할 경우 guest 내부에서 QEMU Guest Agent가 이미 실행 중이어야 함
- Windows용 guest agent install fallback을 사용할 경우 도달 가능한 Windows host가 `windows_qemu_guest_agent_clients`에 포함되어야 함
- Windows domain membership를 사용할 경우 도달 가능한 Windows host가 `windows_management_clients`에 포함되어야 하며 AD join credential을 제공할 수 있어야 함
- Windows용 FreeIPA helper task를 사용할 경우 도달 가능한 Windows host가 `windows_freeipa_helper_clients`에 포함되어야 함
- Linux SSH bootstrap을 사용할 경우 controller에는 SSH keypair와 Ansible이 사용할 guest account로의 초기 password login 경로가 필요함

### 대상 호스트

- `proxmox_primary` 내부 host는 Proxmox VE 6.x 이상이어야 함
- Proxmox와 Linux client에서 FreeIPA에 도달 가능해야 함
- Windows 10/11 및 Windows Server guest는 WinRM 또는 PSRP로 도달 가능하면 분리된 Windows workflow로 관리 가능함
- DNS와 시간 동기화가 올바라야 함
- `proxmox_primary`에서는 `pveversion`, `pvesh`, `pveum`을 실행할 수 있는 `root` 또는 `sudo` 가능한 SSH user를 사용해야 함
- Windows domain membership를 사용할 경우 대상 Windows guest가 해당 AD domain controller에 도달 가능해야 함
- Windows용 제한적 FreeIPA helper workflow를 사용할 경우 대상 Windows guest가 해당 IPA server에 도달 가능해야 함
- Proxmox discovery를 사용할 경우 guest가 QEMU Guest Agent를 통해 usable IP를 노출해야 함

## 네트워크 포트

이 표는 이 저장소의 controller, Proxmox LDAP automation, Linux IPA enrollment 흐름이 사용하는 네트워크 포트를 보여 줍니다.
여기서는 FreeIPA server-to-server replication 전체가 아니라, 이 프로젝트가 실제로 사용하는 표면만 의도적으로 다룹니다.

| Name | Port | Protocol | Source | Destination | Required when | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | 항상 | Ansible 연결 |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | Windows management 활성 시 | Windows guest에 대한 Ansible 연결 |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS server | Linux guest가 IPA DNS를 사용할 때 | IPA record 및 외부 이름 해석 |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment 및 login 시 | Kerberos 인증 |
| LDAP | `389` | `TCP` | Linux guest | IPA server | Linux IPA enrollment 및 login 시 | LDAP 및 FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port`, 기본 `443` | `TCP` | Linux guest | IPA server | Linux IPA enrollment 시 | client 설치 중 IPA web/API 검증 |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment 및 password 작업 시 | Kerberos password 및 keytab 작업 |
| LDAPS | `636` | `TCP` | Primary Proxmox node | IPA 또는 LDAP server | Proxmox LDAP realm이 기본 `ldaps`를 사용할 때 | Proxmox LDAP realm 연결 |

참고:

- `LDAPS 636/TCP`는 `proxmox_ldap_mode`의 기본값이 `ldaps`이므로 이 저장소의 기본입니다. LDAP mode 또는 port를 바꾸는 경우 실제로 쓰는 `proxmox_ldap_port`를 허용해야 합니다.
- `WinRM`은 Windows transport 설정에 따라 보통 HTTPS용 `5986/TCP`, HTTP용 `5985/TCP`를 사용합니다.
- `DNS 53/TCP,UDP`는 Linux guest가 IPA server를 resolver로 쓸 때만 필요합니다.
- `Kerberos 88`과 `Kerberos Password 464`는 둘 다 `TCP`와 `UDP`가 필요합니다.
- Active Directory domain join에는 표준 Windows-to-domain-controller port도 필요하지만, 그 행렬은 환경 의존적이므로 여기서는 자세히 다루지 않습니다.
- Kerberos가 안정적으로 동작하려면 시간 동기화도 필수지만, NTP source는 환경에 따라 달라지며 이 저장소가 관리하지 않습니다.

## 호환성

이 저장소의 Proxmox automation은 Proxmox VE 6.x 이상에서 realm과 RBAC를 위해 사용하는 `pveum` 및 `pvesh` interface를 기준으로 작성되었습니다.

- 기본 지원 major: `6`, `7`, `8`, `9`, `10`
- validation은 `pveversion`을 통해 감지한 Proxmox version을 확인함
- 지원 major 목록은 환경에 맞게 `proxmox_supported_major_versions`로 좁히거나 넓힐 수 있음
- `proxmox_allow_future_major_versions` 기본값은 `true`이므로, 검증된 최고 버전보다 높은 future major도 기본적으로 validation을 통과함
- 다만 future major version은 공개된 Proxmox interface가 이 automation과 실제로 검증되기 전까지는 compatibility candidate로 취급해야 함
- `1`부터 `5` 같은 구버전은 이 공개 저장소가 tested support라고 주장하지 않음. 로컬에서 추가한다면 명시적 compatibility override로 취급하고 먼저 lab에서 전체 workflow를 검증해야 함

legacy lab용 local override 예시:

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

## 빠른 시작

아래 예시는 shell command를 사용합니다. 관련 있을 때는 PowerShell 대응도 함께 적습니다.

### 1. 예시 인벤토리 및 볼트 템플릿 복사

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

### 2. 환경별 파일 편집

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- Windows management를 사용할 경우 `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- Windows management를 사용할 경우 `inventories/production/group_vars/all/vault-windows.yml`

IPA와 Proxmox 설정 외에도 Linux guest source mode를 하나 선택해야 합니다.

- `linux_ipa_clients` 아래의 static inventory entry
- `group_vars/all/30-linux-clients.yml` 안의 `linux_ipa_client_hosts` entry
- `linux_ipa_proxmox_discovery_enabled: true`를 이용한 Proxmox VM discovery

Linux IPA enrollment에서는 domain 값과 server 목록을 구분해야 합니다.

- `ipaclient_domain`은 공유 IPA DNS domain입니다. 예: `example.com`
- `linux_ipa_servers`는 IPA server hostname 목록입니다. 예: `ipa01.example.com`

`root` 대신 `sudo` 가능한 일반 사용자로 Proxmox에 SSH 접속하려면, `hosts.yml`의 `proxmox_primary`에서 이를 설정하고 sudo password는 `vault-proxmox.yml`에 저장하십시오.

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

이 구성에서 `vault_proxmox_become_password`는 Proxmox host에서 평소 `sudo`를 실행할 때 입력하는 password를 의미합니다.

### 3. 볼트 파일 암호화

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

Windows workflow를 활성화할 경우 같은 command에 `inventories/production/group_vars/all/vault-windows.yml`도 추가하십시오.

또는 helper wrapper를 사용할 수 있습니다. 이것은 기본적으로 domain별로 분리된 vault ID를 사용하고, 필요하면 example template에서 working vault file을 생성합니다.

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

playbook 실행 시 domain마다 다른 password를 쓰고 싶다면 `--ask-vault-pass` 대신 vault ID를 사용하십시오.

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

선택적 Windows workflow도 별도 vault password를 사용한다면 같은 command에 `windows@prompt`를 추가하십시오.

해당 playbook이 참조하는 모든 vault file이 동일 password를 공유할 때만 `-AskVaultPass`를 사용하십시오.

### 4. 필요한 컬렉션 설치

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

또는 직접 실행합니다.

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

이 저장소가 compatibility patch를 추가하기 전에 `freeipa.ansible_freeipa`를 설치해 두었다면 bootstrap helper를 다시 실행하거나 `python .\scripts\patch_freeipa_collection.py`를 한 번 실행해 user-level collection install도 patch하십시오.

`scripts/run-playbook.ps1`를 사용할 경우 `ansible-playbook` 호출 전에 해당 patch helper가 자동 실행됩니다.

### 5. 먼저 검증 실행

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

변경 없이 Windows FreeIPA helper-only path만 검증하려면:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

runtime guest 중 어떤 것이 SSH로 도달 가능한지, 그리고 Proxmox-discovered guest 중 어떤 것이 QEMU Guest Agent에 응답하는지 read-only로 점검하려면:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

readiness report는 기본적으로 `.ansible/linux-readiness-report.json`에 기록됩니다.
주요 field는 다음처럼 해석하십시오.

- `ssh.ready=true`: 현재 구성된 Ansible SSH path가 controller에서 성공한다는 뜻
- `ssh.promptless=true`: `ansible_password` 없이 SSH probe가 성공했으므로 해당 path는 Ansible에 대해 non-interactive함
- `ssh.auth_mode=password_configured`: host에 `ansible_password`가 있어 probe가 `sshpass`를 사용함
- `ssh.auth_mode=key_or_agent`: `ansible_password` 없이 SSH batch mode에서 probe가 성공함
- `qga.status=available`: 해당 VM을 소유한 Proxmox node에서 `qm guest ping`이 성공함
- `qga.status=disabled`: Proxmox VM 설정에서 QEMU Guest Agent가 활성화되어 있지 않음
- `qga.status=configured_unresponsive`: Proxmox 설정상 guest agent는 켜져 있지만 응답하지 않음
- `qga.status=node_unreachable`: VM을 소유한 Proxmox node에 controller가 도달하지 못해 probe를 수행하지 못함
- `qga.status=not_applicable`: host가 Proxmox discovery로 생성된 것이 아니므로 QGA probe를 시도하지 않음

빠른 확인 예시:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. 선택 사항: 계획된 변경 미리 보기

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> check mode는 완전한 simulation이 아니라 부분적인 preview로 취급해야 합니다. 이 저장소는 일부 Proxmox 설정에 직접 CLI command를 사용하고 Linux enrollment에는 upstream FreeIPA client role을 사용하므로, `--check`는 유용하지만 절대적인 결과는 아닙니다.
>
> FreeIPA HBAC rule의 경우 check mode에서는 rule definition step은 검증하지만 그 뒤의 enable 또는 disable action은 skip합니다. dry run에서는 rule이 실제로 생성되지 않기 때문에 FreeIPA가 "존재하지 않는다"고 응답하면서 false failure가 나는 것을 막기 위함입니다.
>
> Proxmox realm sync timer role도 check mode에서는 마지막 `systemd` enable 또는 start step을 skip합니다. unit file은 diff에 나타나더라도 dry run 동안 실제로 쓰이지 않기 때문입니다.
>
> Linux IPA enrollment 역시 check mode에서는 skip됩니다. 저장소는 discovery, hostname resolution, input validation은 계속 수행하지만 upstream `ipaclient` role 자체는 dry run 동안 실행하지 않습니다.

### 7. 전체 구성 적용

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

선택적 Windows workflow가 활성화되어 있고 `vault-windows.yml`이 별도 password를 쓴다면, `--ask-vault-pass` 대신 `--vault-id windows@prompt` 또는 PowerShell wrapper의 `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt`를 사용해 같은 playbook을 실행하십시오.

## Rollout 순서

첫 deployment에서는 다음 순서대로 stack을 적용하십시오.

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

이 순서는 모든 것을 한 번에 실행하는 것보다 troubleshooting을 훨씬 쉽게 만듭니다.

예를 들어 하나의 Linux guest만 대상으로 하는 제한적 PowerShell rollout 예시는 다음과 같습니다.

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

기본 rollout control은 보수적으로 설정되어 있습니다.

- FreeIPA access 변경은 `serial: 1`
- Proxmox 변경은 `serial: 1`
- hostname resolution, validation, Linux enrollment는 `serial: 10`
- Windows management 변경은 `serial: 10`
- 모든 rollout path는 기본 `max_fail_percentage: 0` 사용

이 값들은 `inventories/production/group_vars/all/15-rollout.yml`에서 조정하십시오.

## Tag 모델

계속해서 playbook을 더 만들기보다, 안정적인 rollout slice를 target하기 위해 tag를 사용하십시오.

- core domain: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helper: `windows`, `windows_freeipa`
- FreeIPA access model: `freeipa_access`
- Proxmox subset: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- event-driven VM handling: `event`, `linux_refresh`

예시:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## 이벤트 기반 VM 온보딩

VM이 start된 직후 또는 migration 이후에 Proxmox가 Linux discovery와 IPA enrollment를 즉시 trigger하도록 하려면, [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md)에 설명된 선택형 hook / webhook path를 사용하십시오.

이 path는 event 전용 playbook `playbooks/proxmox-vm-event.yml`을 사용하므로 Linux guest 측과 FreeIPA 측만 다룹니다. 각 VM event마다 Proxmox LDAP realm automation이나 RBAC를 다시 실행하지 않습니다.

이 저장소는 현재 `proxmox_vm_event_onboarding_enabled: true`가 설정되고 필요한 webhook variable이 준비되어 있다면 `site.yml` 또는 `proxmox.yml`을 통해 해당 hook / webhook stack 자체도 설치할 수 있습니다.

Proxmox VM hook에는 별도의 `create` phase가 없습니다. 실제로는 새 VM이 보통 첫 `post-start` event에서 포착되고, migration hook은 source node와 destination node 양쪽에서 trigger될 수 있습니다.

## Inventory 모델

이 저장소는 명시적으로 정의된 여섯 개 inventory group과 runtime에 생성되는 한 개 group을 사용합니다.

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

필요하다면 별도의 inventory group을 추가 정의하고 FreeIPA hostgroup definition에서 그것을 참조할 수도 있습니다. 준비된 Linux guest 전체를 FreeIPA hostgroup 쪽에서 활용하고 싶다면 `linux_ipa_clients_runtime` group을 참조하십시오.

> [!IMPORTANT]
> FreeIPA는 각 guest에 대해 최종 hostname을 필요로 합니다. IP-only target 또는 Proxmox discovery를 사용하는 경우 `ipa_hostname`을 명시하거나 guest 내부의 `hostname -f`가 최종 FQDN을 반환하도록 해야 합니다. playbook은 FreeIPA hostgroup membership을 구성하기 전에 그 hostname을 먼저 해결합니다.

> [!TIP]
> 재사용할 golden template를 FreeIPA에 직접 enroll하지 마십시오. 먼저 VM을 clone하고 최종 hostname을 부여한 뒤 결과 guest를 enroll하십시오.

### Linux 게스트 소스 모드

`linux_ipa_clients`를 채우는 방법은 세 가지입니다.

#### 1. static inventory hosts

guest 이름을 이미 알고 있다면 일반적인 Ansible inventory entry를 사용합니다.

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. variable에서 manual host definition 사용

guest를 `hosts.yml` 밖에 두고 싶거나 IP만 알고 있는 경우 `linux_ipa_client_hosts`를 사용하십시오.

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

참고:

- `name`이 이미 resolve 가능한 hostname 또는 FQDN이면 `ansible_host`는 선택 사항입니다
- IP만 알고 있다면 `name`에는 안정적인 아무 alias나 사용해도 됩니다
- `ipa_hostname`을 생략하면 playbook은 guest 내부의 `hostname -f`로 fallback합니다

#### 3. Proxmox VM auto-discovery

하나 이상의 Proxmox node에서 Linux guest를 끌어오고 싶다면 discovery를 사용하십시오.

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

참고:

- discovery는 다른 playbook과 동일한 `linux_ipa_clients_runtime` group에 VM을 추가합니다
- IP discovery는 network interface를 보고할 수 있는 QEMU guest agent에 의존합니다
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint`는 이미 FQDN인 VM 이름만 신뢰합니다
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true`를 설정하면 `Teleport-Server-1` 같은 안전한 short VM name도 `linux_ipa_identity_hostname_suffix`를 통해 `teleport-server-1.example.com` 같은 hostname hint로 자동 승격할 수 있습니다
- `linux_ipa_proxmox_discovery_vmids`는 선택 사항이며 주로 event-driven hook 또는 webhook workflow에서 discovery를 특정 VMID 몇 개로 제한할 때 사용합니다
- guest는 여전히 최종 hostname이 필요하며, 이는 VM 내부에 이미 설정되어 있거나 manual definition에서 `ipa_hostname`으로 제공되어야 합니다
- guest의 실제 system hostname도 enrollment에 유효해야 합니다. `localhost.localdomain` 같은 placeholder는 `linux-clients` 또는 `site`를 실행하기 전에 VM 내부에서 바꿔야 합니다
- guest가 `app-server-01` 같은 short hostname을 사용할 경우 `linux_ipa_identity_hostname_suffix`와 필요 시 `linux_freeipa_enroll_manage_hostname: true`를 설정하여 `app-server-01.example.net` 같은 full hostname으로 해결·적용한 뒤 enrollment할 수 있습니다
- FreeIPA DNS가 guest hostname에 대해 authoritative하다면 `linux_freeipa_enroll_manage_authoritative_dns: true`를 설정해 관련 A / PTR record를 고치고 enrollment 전에 link-local `fe80::/10` AAAA record를 제거할 수 있습니다
- DNS가 아직 준비되지 않았다면 `linux_ipa_manage_etc_hosts: true`와 `linux_ipa_etc_hosts_entries`를 설정하여 IPA server와 guest FQDN용 관리형 `/etc/hosts` bootstrap block을 enrollment check보다 먼저 추가할 수 있습니다
- `guest_qemu_agent_install_enabled`는 SSH 또는 WinRM으로 이미 도달 가능한 guest에 QEMU Guest Agent를 설치하고, 같은 workflow 내에서 나중에 도달 가능해진 Linux guest에 다시 시도하고, Linux enrollment 이후에도 다시 시도하여 agent 의존 Proxmox workflow가 이를 활용할 수 있게 합니다
- `linux_ipa_proxmox_discovery_allowlist_enabled: true`를 설정하면 discovery 자체는 켠 채로, 명시적으로 승인된 Proxmox guest만 Linux runtime inventory에 admission할 수 있습니다. allowlist는 VMID, IP, 이름으로 정확히 match할 수 있습니다
- `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, `linux_ipa_proxmox_discovery_blacklist_names`를 설정하면 discovery 대상 node에 함께 있는 firewall, DNS server 같은 infrastructure VM에 Linux IPA automation이 적용되는 것을 막을 수 있습니다. blacklist match는 광역 discovery와 allowlist admission보다 항상 우선합니다
- Proxmox discovery된 Linux guest에 아직 guest agent가 동작하지 않는다면 `linux_ipa_proxmox_discovery_ansible_user`와 함께 `linux_ipa_proxmox_discovery_ansible_password` 또는 `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file`을 설정해 repository가 QEMU Guest Agent 설치용 first-touch SSH path를 가지도록 해야 합니다
- 그 discovery guest가 non-root SSH user를 사용한다면 `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, `linux_ipa_proxmox_discovery_ansible_become_password`도 설정하십시오. 해당 account가 이미 passwordless `sudo`를 가진 경우에는 생략할 수 있습니다
- `guest_qemu_agent_install_manage_proxmox_vm_agent`는 guest 내부 설치 경로를 시작하기 전에 Proxmox 쪽 guest agent communication (`qm set <vmid> --agent 1`)도 활성화합니다
- 이 Proxmox VM option을 실행 중인 VM에 대해 바꾸면 repository는 기본적으로 warning만 출력합니다. Proxmox가 guest agent channel을 사용하기 전에 VM 재시작을 요구할 수 있기 때문입니다. 실행 중인 VM을 자동 reboot하고 싶다면 `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true`를 설정하십시오
- `linux_ipa_ssh_host_key_policy`는 Linux guest 연결에 기본적으로 `accept_new`를 사용하므로 newly discovered VM에도 host key checking을 완전히 끄지 않고 연결할 수 있습니다. 변경된 host key는 여전히 fail하며 operator 검토가 필요합니다
- `linux_ipa_qga_ssh_bootstrap_enabled`는 Proxmox 기반 guest에 권장되는 no-reboot bootstrap path입니다. 일반 SSH login 이전에 QEMU Guest Agent를 사용해 key-only 전용 automation user를 만들 수 있습니다
- `linux_ipa_qga_ssh_bootstrap_qm_path` 기본값은 `qm`이며, bootstrap flow는 fail하기 전에 Proxmox node의 일반적인 fallback path도 함께 확인합니다
- `guest-ping`은 허용하지만 `guest-exec`는 거부하는 guest는 QGA bootstrap 중 기본적으로 skip됩니다. 이런 guest에는 다른 SSH path를 제공하거나 `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true`를 설정해 즉시 fail시키십시오
- `linux_ipa_ssh_bootstrap_enabled`는 hostname resolution과 enrollment 전에 controller의 public key를 Linux guest에 선택적으로 설치합니다. `linux_ipa_ssh_bootstrap_password`는 key-based bootstrap을 끄더라도 Linux runtime guest에 대한 shared first-touch password fallback으로도 사용됩니다
- Linux IPA enrollment는 FreeIPA JSON-RPC timeout 때문에 실패한 upstream client join을 retry하며, 더 느리거나 더 바쁜 IPA 환경을 위해 `linux_ipaclient_kinit_attempts`를 노출합니다
- Linux IPA enrollment는 기본적으로 inventory의 `ipa_servers` hostname도 join server list에 포함하므로 client가 한 개 endpoint가 아니라 전체 IPA server set을 활용할 수 있습니다
- IPA server가 둘 이상일 경우 각 retry round는 Linux client enrollment 과정에서 그 candidate IPA server들을 순차적으로 시도합니다
- combined workflow `site`는 먼저 FreeIPA hostgroup을 만들고 그 다음 enrolled runtime host를 추가하므로, pre-enrollment run이 guest가 아직 enrolled되지 않았다는 이유만으로 hostgroup membership step에서 실패하지 않습니다

## 구성 표면

대부분의 값은 다음 위치에 있습니다.

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

파일별 정리는 [docs/VARIABLES.md](../VARIABLES.md)를 참고하십시오.

주요 variable family:

| Area | Variables |
| --- | --- |
| FreeIPA access model | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Rollout control | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Linux readiness reporting | `linux_readiness_report_*` |
| Windows management | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helper | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Ansible 연결 secret | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## 예시 그룹 전략

단순하지만 잘 확장되는 기본 패턴은 다음과 같습니다.

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa`에 대한 Proxmox ACL binding

특정 IPA user에게 Linux SSH 및 sudo 권한을 자동 부여하고 싶다면 [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml)의 `freeipa_linux_admin_users`를 채우십시오. 그러면 `site.yml` combined run이 관리형 group `linux-ssh-admins`를 통해 권한을 부여합니다.

Proxmox LDAP sync는 suffix가 붙은 synced group을 만든다는 점을 기억해야 합니다.

```text
<group-name>-<realm>
```

예를 들어 FreeIPA group이 `proxmox-admins`이고 Proxmox realm이 `ipa`라면 생성되는 synced PVE group은 다음과 같습니다.

```text
proxmox-admins-ipa
```

## 보안

- 모든 secret은 plaintext inventory variable file이 아니라 `vault-freeipa.yml`, `vault-proxmox.yml`에 저장
- Proxmox에는 read-only 전용 LDAP bind account를 우선 사용
- certificate verification이 활성화된 TLS 선호
- 임시 lab이 아니면 SSH host key checking을 켠 상태 유지
- Proxmox guest에 이미 QEMU Guest Agent가 동작 중이라면 shared temporary password보다 `linux_ipa_qga_ssh_bootstrap_enabled`를 우선 사용
- `guest_qemu_agent_install_enabled`는 repository가 guest 내부로 들어갈 유효한 management path를 이미 가지고 있을 때만 사용. Proxmox discovery에서는 QGA가 이미 실행 중이거나 `linux_ipa_proxmox_discovery_ansible_user`와 password 또는 key access가 설정되어 있어야 함을 의미함
- Linux SSH bootstrap을 활성화할 경우 shared bootstrap password는 암호화된 variable에 저장하고 key-based access가 확립된 뒤에는 rotate하거나 제거
- IPA admin account를 Proxmox LDAP bind account로 재사용하지 않기
- production rollout 전에 `proxmox_ldap_filter`, `proxmox_ldap_group_filter`를 검토해 너무 많은 object가 import되지 않도록 하기

임시 lab에서 의도적으로 SSH host key verification을 우회하고 싶다면 repository 기본값을 바꾸지 말고 shell session 단위로 opt-out하십시오.

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## 멱등성과 주의점

이 저장소는 재실행 가능하도록 작성되었고 대부분은 idempotent하지만, production rollout 전에는 반드시 lab에서 검증해야 합니다.

알려진 주의점:

- Proxmox CLI output은 release마다 조금씩 다를 수 있음
- FreeIPA directory layout은 유연하므로 LDAP filter가 환경에 맞게 조정되어야 할 수 있음
- 기존에 수동 관리되던 PVE ACL과 role은 automation이 덮기 전에 비교 검토해야 함
- Proxmox VM auto-discovery는 실행 중인 guest와 QEMU guest agent의 network data에 의존함
- IP 기반 guest definition도 guest 내부의 유효한 최종 hostname 또는 명시적 `ipa_hostname`이 필요함
- Proxmox play는 privilege escalation과 함께 실행되므로 non-root SSH user는 동작하는 `sudo`가 필요하고, 그 user가 passwordless `sudo`가 아니라면 `-K`로 become password를 제공해야 함
- `ansible_become_password`를 `vault-proxmox.yml`에 저장해 두면 Ansible이 암호화된 variable에서 sudo password를 읽으므로 `-K`를 생략할 수 있음

## 검증

rollout이 성공한 뒤에는 모든 access path가 맞다고 가정하지 말고 최종 상태를 확인하십시오.

### FreeIPA에서 확인할 것

- 기대한 user group이 존재하는지 확인
- 기대한 hostgroup이 존재하는지 확인
- 기대한 HBAC rule이 존재하고 활성 상태인지 확인
- 기대한 `sudo` rule이 존재하고 활성 상태인지 확인

### Proxmox에서 확인할 것

- LDAP realm이 존재하는지 확인
- initial sync가 기대한 user / group을 import했는지 확인
- 대상 synced group에 기대한 ACL binding이 있는지 확인

### Linux guest에서 확인할 것

- 허용된 IPA user가 login 가능한지 확인
- 허용되지 않은 user가 HBAC에 의해 차단되는지 확인
- 허용된 IPA admin이 `sudo -l`을 실행할 수 있는지 확인
- `linux_ipaclient_mkhomedir`가 활성화되어 있다면 첫 login 시 home directory가 생성되는지 확인

## 저장소 레이아웃

<details>
<summary>저장소 레이아웃 보기</summary>

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

## 개발

이 저장소에 포함된 주요 helper file은 다음과 같습니다.

- `.editorconfig`: editor 사이에서 공백, encoding, 줄 끝 기본값을 일관되게 유지
- `.gitattributes`: 일반 text file에 `LF` 줄 끝 강제
- `.gitignore`: 생성된 inventory, vault data, local collection, editor 잡파일이 Git에 들어가지 않도록 방지
- `.ansible-lint`: vendor collection path를 제외하고 YAML line-length rule만 억제
- `.yamllint`: playbook, inventory, workflow 전반에서 일관된 YAML validation 유지
- `.github/CODEOWNERS`: 저장소 주요 영역에 대한 review ownership 지정
- `.github/workflows/ci.yml`: push 및 pull request에서 lint와 smoke validation 실행
- `.pre-commit-config.yaml`: `pre-commit`이 설치된 경우 commit 전에 빠른 lint hook 실행
- `CHANGELOG.md`: 중요한 repository change를 한 곳에서 추적
- `docs/VARIABLES.md`: 분리된 inventory variable 구조 설명
- `docs/i18n/`: 번역 README 저장 위치이며, 이 file들은 영어 `README.md`의 전체 section 구조를 반영해야 함
- `docs/i18n/TRANSLATION_GUIDE.md`: 번역 README를 동기화하는 방법 설명
- `scripts/bootstrap.ps1`, `scripts/bootstrap.sh`: 필요한 collection을 local `collections/` path에 설치하고 ansible-core 2.24+용 compatibility patch 적용
- `scripts/patch_freeipa_collection.py`: pinned FreeIPA collection 내부의 deprecated import를 다시 써서 향후 ansible-core와의 호환성 유지
- `scripts/lint.py`: local, CI, pre-commit에서 사용하는 cross-platform lint entry point 제공
- `scripts/smoke-test.py`: 실제 인프라를 건드리지 않고 example inventory validation과 syntax check를 수행하며, 분리된 Windows playbook coverage도 포함
- `scripts/check_translations.py`: 번역 README의 metadata, section structure parity, 영어 canonical README 대비 최소 content coverage를 점검
- `scripts/lint.ps1`, `scripts/lint.sh`: local lint와 smoke workflow 묶음
- `scripts/proxmox_event_webhook.py`: controller 측 선택형 Proxmox VM event webhook 역할 수행
- `scripts/proxmox-vm-hook.pl`: node에 설치하는 선택형 Proxmox VM hook 역할 수행
- `scripts/run-playbook.ps1`: Windows / PowerShell 환경용 일관된 `ansible-playbook` wrapper 제공
- `scripts/vault.ps1`, `scripts/vault.sh`: domain별로 분리된 vault file의 생성, 편집, 조회, 암호화를 보조
- `tests/`: smoke-test documentation 부터 시작하는 repository verification surface 를 담고 있음
- `CONTRIBUTING.md`: 기대되는 contribution 과 validation workflow 를 문서화함
- `SECURITY.md`: vulnerability 보고와 security-sensitive 정보 처리 방식을 문서화함

controller 에 `ansible-lint` 가 설치되어 있다면:

```bash
ansible-lint
```

repository smoke check 를 직접 실행하려면:

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

전체 local lint pass 를 실행하려면:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

각 commit 전에 fast lint hook 를 켜려면:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper 는 일반적인 operator option 도 직접 지원합니다:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## 다음 확장

다음 단계로 자연스러운 확장:

- IPA-ready Linux template용 Packer pipeline
- combined rollout용 AWX 또는 Automation Controller job template 및 scheduling
- 더 강한 Proxmox tenant / pool model
- Windows RDP 또는 hybrid identity 환경을 위한 AD trust workflow

## 라이선스

[0BSD License](../../LICENSE) 하에 배포됩니다.
