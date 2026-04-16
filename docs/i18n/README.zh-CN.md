# Proxmox + FreeIPA 访问自动化

本页提供 [README.md](../../README.md) 的完整中文结构化翻译。英文版仍然是规范来源，但本页覆盖同样的主要章节，方便中文读者直接阅读完整说明。

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## 语言

英文版是完整文档的规范来源。完整翻译版 README 还提供 20 种附加语言。

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [翻译索引](README.md) | [翻译指南](TRANSLATION_GUIDE.md)

本仓库将 **FreeIPA 视为身份与访问控制的事实来源**。Proxmox 通过 LDAP realm 消费这套目录，Linux 来宾通过上游 `ipaclient` 角色加入 FreeIPA，而访问控制则通过同步组、HBAC 和 sudo 规则集中管理，而不是散落在每台主机的本地账户中。

> [!IMPORTANT]
> 本项目 **不会把 FreeRADIUS 当作身份源**，**不会在每台 VM 内创建本地用户**，也 **不会试图覆盖 Proxmox 所有可能的权限边界场景**。

## 为什么需要这个项目

当你已经具备以下条件时，这个仓库才有意义：

- 一个运行稳定的 FreeIPA 环境
- 一个 Proxmox VE 集群
- 需要使用集中身份认证的 Linux 虚拟机
- 一个专门用于 Proxmox LDAP 绑定的 FreeIPA 服务账号
- 清晰的管理员与运维权限模型

核心思路是把 FreeIPA 作为身份与访问控制的唯一事实来源。Proxmox 通过 LDAP realm 消费目录，Linux 来宾通过上游 `ipaclient` 角色加入 FreeIPA，SSH、HBAC 与 `sudo` 权限保持集中管理，而不是散落在每一台主机上。

当你希望 onboarding 与 offboarding 大致遵循下列顺序时，这套方案尤其合适：

1. 在 FreeIPA 中创建或更新用户与组
2. 将这些身份同步到 Proxmox
3. 依据同步组应用 Proxmox 角色与 ACL
4. 通过 FreeIPA 登录、HBAC 与 sudo 规则授予 Linux 来宾访问权限

## 你将获得什么

- FreeIPA 用户组、主机组、HBAC 规则与 `sudo` 规则管理
- 面向 Linux 管理员用户的自动 FreeIPA 登录 shell 默认值
- 面向 FreeIPA 的 Proxmox LDAP realm 配置
- 从指定集群节点发起的周期性 Proxmox realm 同步
- 基于同步目录组的 Proxmox RBAC 绑定
- 通过静态 inventory、变量中的手工主机定义或 Proxmox 自动发现实现 Linux IPA 加入
- 基于 QEMU Guest Agent 的可选免重启 SSH bootstrap
- 面向 Proxmox 托管 Linux 来宾的可选宿主侧 guest-agent 通道启用
- 对已可达来宾通过 SSH 或 WinRM 安装 QEMU Guest Agent 的可选回退路径
- 面向 SSH 可达性与 Proxmox QEMU Guest Agent 状态的可选 Linux readiness 报告
- 面向 Windows 10/11 与 Windows Server 来宾、基于 Active Directory 的独立可选 Windows 域成员工作流
- 面向 IPA CA 信任、hosts bootstrap 与 IPA reachability 检查的受限可选 FreeIPA-aware Windows helper 工作流
- 首次接触时的可选 SSH 公钥 bootstrap
- 在 FreeIPA 访问模型变更后自动刷新 SSSD 缓存
- 基于 `post-start` 和 `post-migrate` 的可选事件驱动入管

## 范围

| 包含 | 不包含 |
| --- | --- |
| FreeIPA 访问模型 | FreeRADIUS 部署 |
| Proxmox LDAP realm 配置 | FreeIPA 用户生命周期创建 |
| 基于同步组的 Proxmox RBAC | 覆盖所有 Proxmox 多租户权限边界场景 |
| Linux IPA 客户端入管 | 直接针对 FreeIPA 的原生 Windows 登录 |
| 独立的 Windows AD 域成员工作流 | GPO 或更广泛的 AD 对象生命周期自动化 |
| 受限的 FreeIPA-aware Windows helper 工作流 | 把 FreeIPA-only 的 Windows helper 冒充成与 AD 等价 |

## Windows 工作流

Windows 支持并未嵌入 Linux IPA enrollment 流程，而是作为独立工作流实现。

- `windows_qemu_guest_agent_clients` 仅用于可选的 QEMU Guest Agent 辅助任务。
- 通过 `windows_domain_membership_enabled: true` 启用独立的 Windows 管理流程。
- `windows_management_clients` 会被 `playbooks/windows-management.yml` 以及统一的 `playbooks/site.yml` 中的 Windows 阶段使用。
- Windows 本地登录通过 Active Directory 域成员关系完成；在 FreeIPA 为核心的环境中，真正可行的企业级路径通常是 AD 域加入，或通过 FreeIPA-AD trust 间接接入，而不是尝试把 Windows 主机直接加入 FreeIPA。

本仓库不支持 FreeIPA-only 的 Windows 域加入。没有 Active Directory 或 FreeIPA-AD trust 时，Windows 侧只能使用辅助型自动化能力。

若你只需要这条受限路径，可启用 `windows_freeipa_helpers_enabled: true`，并对 `windows_freeipa_helper_clients` 组运行 `playbooks/windows-freeipa-helpers.yml`。该辅助工作流可以提供 IPA CA 信任、可选的 CA 自动抓取与指纹校验、hosts 文件 bootstrap、IPA DNS 与 TCP 连通性验证、HTTPS 验证、Windows 时间源检查、本地组成员关系管理以及可选的 OpenSSH Server 管理，但它不会让 Windows 通过 FreeIPA 实现本地域登录。

如果你只想做验证而不做变更，请运行 `playbooks/windows-freeipa-validate.yml`。这个流程保留摘要与验证逻辑，但关闭会修改主机状态的 helper 步骤。

这一工作流面向通过 WinRM 或 PSRP 可达的 Windows 10/11 与 Windows Server 来宾。

## 架构

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

更完整的设计说明见 [docs/ARCHITECTURE.md](../ARCHITECTURE.md)。

## 前提要求

### 控制端

- Ansible Core 2.14 或更高版本
- 能通过 SSH 到达 Proxmox 主节点、IPA 服务器和 Linux 客户端
- 当你使用 Windows 工作流时，需要通过 WinRM 或 PSRP 到达 Windows 来宾
- 需要时具备 `sudo` 或 `root`
- 启用 QGA SSH bootstrap 时，来宾内的 QEMU Guest Agent 必须已经运行
- 启用 Windows 客户端回退安装时，可达主机必须放在 `windows_qemu_guest_agent_clients` 组中
- 启用 Windows 域成员管理时，可达的 Windows 主机必须放在 `windows_management_clients` 组中，并提供 AD 域加入凭据
- 启用 Windows FreeIPA helper 任务时，可达的 Windows 主机必须放在 `windows_freeipa_helper_clients` 组中
- 启用 Linux SSH bootstrap 时，控制端需要 SSH 密钥对以及一条基于密码的首次登录路径

### 目标端

- `proxmox_primary` 中的主机运行 Proxmox VE 6.x 或更高版本
- Proxmox 与 Linux 客户端都能访问 FreeIPA
- 当通过 WinRM 或 PSRP 可达时，Windows 10/11 与 Windows Server 来宾可由独立 Windows 工作流管理
- DNS 与时间同步正常
- `proxmox_primary` 应使用 `root`，或使用能对 `pveversion`、`pvesh`、`pveum` 执行 `sudo` 的 SSH 用户
- 如果你使用 Windows 域成员工作流，目标 Windows 来宾必须能够到达相关 AD 域控制器
- 如果你使用受限 Windows FreeIPA helper 工作流，目标 Windows 来宾必须能够到达相关 IPA 服务器
- 启用 Proxmox 自动发现时，被发现的来宾必须能够通过 QEMU Guest Agent 提供可用 IP

## 网络端口

下表列出本仓库在控制端、Proxmox LDAP 自动化以及 Linux IPA enrollment 流程中使用的网络端口。
它不是完整的 FreeIPA 服务器互联复制矩阵，只覆盖这个项目实际会用到的通信面。

| 名称 | 端口 | 协议 | 来源 | 目标 | 何时需要 | 用途 |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible 控制端 | Proxmox 节点、IPA 服务器、Linux 来宾 | 始终 | Ansible 连接 |
| WinRM | `5985`, `5986` | `TCP` | Ansible 控制端 | Windows 来宾 | 启用 Windows 管理时 | 连接 Windows 来宾 |
| DNS | `53` | `TCP`, `UDP` | Linux 来宾 | IPA DNS 服务器 | Linux 来宾使用 IPA DNS 时 | 解析 IPA 记录与公共域名 |
| Kerberos | `88` | `TCP`, `UDP` | Linux 来宾 | IPA 服务器 | Linux IPA enrollment 与登录 | Kerberos 认证 |
| LDAP | `389` | `TCP` | Linux 来宾 | IPA 服务器 | Linux IPA enrollment 与登录 | LDAP 与 FreeIPA 客户端发现 |
| HTTPS | `linux_freeipa_enroll_https_port`，默认 `443` | `TCP` | Linux 来宾 | IPA 服务器 | Linux IPA enrollment | IPA Web/API 预检 |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux 来宾 | IPA 服务器 | Linux IPA enrollment 与密码相关操作 | Kerberos 密码与 keytab 操作 |
| LDAPS | `636` | `TCP` | Proxmox 主节点 | IPA 或 LDAP 服务器 | 默认 `ldaps` 模式的 Proxmox LDAP realm | Proxmox LDAP realm 连接 |

说明：

- `LDAPS 636/TCP` 是仓库默认值，因为 `proxmox_ldap_mode` 默认是 `ldaps`。如果你修改了 LDAP 模式或端口，就需要开放你实际配置的 `proxmox_ldap_port`。
- `WinRM` 根据环境通常使用 `5986/TCP` 作为 HTTPS，`5985/TCP` 作为 HTTP。
- `DNS 53/TCP,UDP` 仅在 Linux 来宾把 IPA 服务器作为解析器时才需要。
- `Kerberos 88` 与 `Kerberos Password 464` 都需要同时开放 `TCP` 与 `UDP`。
- Active Directory 域加入还需要常见的 Windows 域控端口集合，但这部分高度依赖环境，这里不把它硬编码成完整矩阵。
- Kerberos 的稳定运行仍然依赖时间同步，不过 NTP 来源因环境而异，本仓库不直接管理。

## 兼容性

本仓库中的 Proxmox 自动化围绕 Proxmox VE 6.x 及以后版本可用的 `pveum` 与 `pvesh` realm / RBAC 接口编写。

- 默认支持的大版本为：`6`, `7`, `8`, `9`, `10`
- 校验流程会通过 `pveversion` 检查检测到的 Proxmox 版本
- 可通过 `proxmox_supported_major_versions` 覆盖支持列表，以适配你的环境
- `proxmox_allow_future_major_versions` 默认值为 `true`，因此比当前测试过的最高版本更高的新 major 版本默认也会放行
- 这些更新版本仍应被视为兼容性候选，需要在你的环境中先完成验证
- `1` 到 `5` 这样的旧版 major 不属于本公开仓库声明的测试支持范围；如果你在本地把它们加回支持列表，请把它当作明确的兼容性覆盖，并先在实验环境中验证完整流程

面向旧版实验环境的本地覆盖示例：

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

## 快速开始

以下示例使用 shell 命令；在有必要的地方也给出了 PowerShell 等价写法。

### 1. 复制示例清单与 vault 模板

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# 如果你计划管理 Windows 来宾，可选复制：
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# 如果你计划管理 Windows 来宾，可选复制：
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. 编辑环境相关文件

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- 如果启用 Windows 管理，则还要编辑 `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- 如果启用 Windows 管理，则还要编辑 `inventories/production/group_vars/all/vault-windows.yml`

除 IPA 与 Proxmox 设置外，你还需要选择一种 Linux 来宾来源模式：

- `linux_ipa_clients` 下的静态 inventory 条目
- `group_vars/all/30-linux-clients.yml` 中的 `linux_ipa_client_hosts`
- 启用 `linux_ipa_proxmox_discovery_enabled: true` 的 Proxmox VM 自动发现

对于 Linux IPA enrollment，要区分域名与服务器列表：

- `ipaclient_domain` 是共享的 IPA DNS 域，例如 `example.com`
- `linux_ipa_servers` 则是 IPA 服务器主机名列表，例如 `ipa01.example.com`

如果你想用普通但可 `sudo` 的用户而不是 `root` 来 SSH 到 Proxmox，请在 `hosts.yml` 中的 `proxmox_primary` 下配置它，并把 sudo 密码放进 `vault-proxmox.yml`：

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

在这个模式下，`vault_proxmox_become_password` 就是你平时在 Proxmox 节点上手工输入给 `sudo` 的密码。

### 3. 加密 vault 文件

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

若你启用了 Windows 工作流，请把 `inventories/production/group_vars/all/vault-windows.yml` 也加入同一个命令。

你也可以使用辅助封装脚本。它们默认使用分离的 vault ID，并在需要时从 example 模板创建工作用 vault 文件：

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

如果你在运行 playbook 时希望为不同域使用不同密码，请优先使用 vault ID，而不是 `--ask-vault-pass`：

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

如果可选的 Windows 工作流也使用单独密码，请在同一命令里再加上 `windows@prompt`。

只有在该 playbook 所使用的所有 vault 文件都共享同一个密码时，才建议使用 `-AskVaultPass`。

### 4. 安装所需集合

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

或者直接安装：

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

如果你在本仓库加入兼容性修补之前就已安装了 `freeipa.ansible_freeipa`，请重新运行任一 bootstrap helper，或者单独执行一次 `python .\scripts\patch_freeipa_collection.py`，以同时修补现有的用户级 collection 安装。

当你使用 `scripts/run-playbook.ps1` 时，它会在调用 `ansible-playbook` 前自动运行这个 patch helper。

### 5. 先运行校验

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

如果你只想验证 helper-only 的 Windows FreeIPA 路径，而不实际修改主机：

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

如果你想要一个只读的 Linux readiness 审计，用来查看哪些 runtime 来宾能通过 SSH 到达，以及哪些通过 Proxmox 发现的来宾能响应 QEMU Guest Agent：

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

readiness report 默认写入 `.ansible/linux-readiness-report.json`。
主要字段可按如下方式理解：

- `ssh.ready=true`：当前配置的 Ansible SSH 路径已从控制端成功工作
- `ssh.promptless=true`：SSH 探测在没有 `ansible_password` 的情况下成功，说明这条路径对 Ansible 来说是非交互式的
- `ssh.auth_mode=password_configured`：探测因主机定义了 `ansible_password` 而使用了 `sshpass`
- `ssh.auth_mode=key_or_agent`：探测在没有 `ansible_password` 的 SSH batch mode 下成功
- `qga.status=available`：所属 Proxmox 节点上的 `qm guest ping` 成功
- `qga.status=disabled`：该 VM 在 Proxmox 配置中没有启用 QEMU Guest Agent
- `qga.status=configured_unresponsive`：Proxmox 配置已启用 guest agent，但来宾未响应
- `qga.status=node_unreachable`：控制端无法到达所属 Proxmox 节点，因此无法执行探测
- `qga.status=not_applicable`：该主机不是由 Proxmox 自动发现创建，因此不会尝试 QGA 探测

快速查看示例：

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. 可选：预览计划中的变更

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> 请把 check mode 当作局部预览，而不是完整模拟。本仓库对部分 Proxmox 配置使用直接 CLI 命令，对 Linux enrollment 使用上游 FreeIPA client 角色，因此 `--check` 很有参考价值，但不是绝对权威。
>
> 对 FreeIPA HBAC 规则来说，check mode 会验证规则定义步骤，但会跳过后续 enable 或 disable 动作。这样可以避免 dry run 时规则并未真正创建，导致 FreeIPA 报“规则不存在”的误判。
>
> Proxmox realm sync timer 角色在 check mode 下也会跳过最后的 `systemd` enable 或 start 步骤，因为 unit 文件虽然会显示 diff，但在 dry run 中并不会真的写入磁盘。
>
> Linux IPA enrollment 也会在 check mode 下被跳过。仓库仍会执行发现、主机名解析与输入校验，但不会真正执行上游 `ipaclient` 角色。

### 7. 应用完整配置

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

如果启用了可选 Windows 工作流，且 `vault-windows.yml` 使用独立密码，请使用 `--vault-id windows@prompt`，或在 PowerShell wrapper 中使用 `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt`，而不是继续用 `--ask-vault-pass`。

## 发布顺序

首次部署建议按下列顺序应用整套栈：

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# 如果你要管理 Windows 来宾，可选：
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# 如果你需要受限的 Windows FreeIPA helper 工作流，可选：
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# 如果你只想验证 helper 工作流，可选：
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

这种顺序比一次性全部运行更容易排障。

有限范围 PowerShell 发布示例，例如仅面向一台 Linux 来宾：

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

默认的 rollout 控制相对保守：

- FreeIPA 访问模型使用 `serial: 1`
- Proxmox 变更使用 `serial: 1`
- Linux 主机名解析、校验与 enrollment 使用 `serial: 10`
- Windows 管理变更使用 `serial: 10`
- 所有 rollout 路径默认 `max_fail_percentage: 0`

这些值可在 `inventories/production/group_vars/all/15-rollout.yml` 中调整。

## Tag 模型

使用 tag 可以针对稳定的发布切片，而不必不断创建更多 playbook。

- 核心域：`freeipa`, `proxmox`, `linux`, `validate`
- Windows 域：`windows`, `windows_domain`
- Windows FreeIPA helper：`windows`, `windows_freeipa`
- FreeIPA 访问模型：`freeipa_access`
- Proxmox 子域：`proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux 准备阶段：`inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment：`linux_enroll`
- 事件驱动 VM 流程：`event`, `linux_refresh`

示例：

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## 事件驱动 VM 入管

如果你希望 Proxmox 在 VM 启动或迁移后立即触发 Linux 发现与 IPA enrollment，请使用 [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) 中说明的可选 hook / webhook 工作流。

该路径使用专用事件 playbook `playbooks/proxmox-vm-event.yml`，因此触发器只会处理 Linux 与 FreeIPA 来宾侧逻辑，而不会在每个 VM 事件上重新运行 Proxmox LDAP realm 或 RBAC 自动化。

当设置了 `proxmox_vm_event_onboarding_enabled: true` 且相关 webhook 变量已完整提供时，仓库也可以通过 `site.yml` 或 `proxmox.yml` 自动部署这套可选 hook / webhook 栈。

Proxmox VM hook 不提供独立的 `create` 阶段。实际效果是：新 VM 往往会在第一次 `post-start` 时被捕获，而迁移 hook 则可能在源节点和目标节点两侧都触发。

## Inventory 模型

本仓库使用六个定义好的 inventory 组，以及一个运行时生成的组：

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

你也可以定义自己的额外 inventory 组，并在 FreeIPA hostgroup 定义中引用它们。如果你想在 FreeIPA hostgroup 侧引用准备好的全部 Linux 来宾集合，请使用 `linux_ipa_clients_runtime`。

> [!IMPORTANT]
> FreeIPA 仍然需要每个来宾有最终主机名。如果你使用纯 IP 目标或 Proxmox 自动发现，请显式提供 `ipa_hostname`，或确保来宾内的 `hostname -f` 能返回最终 FQDN。现在 playbook 会在构建 FreeIPA hostgroup 成员关系之前先解析这个主机名。

> [!TIP]
> 不要把可复用的 golden template 直接 enroll 到 FreeIPA。应当先克隆 VM、赋予最终主机名，再对克隆出来的来宾执行 enrollment。

### Linux 来宾来源模式

你可以用三种方式向 `linux_ipa_clients` 提供 Linux 来宾。

#### 1. 静态 inventory 主机

如果你已经知道来宾名称，可以直接使用普通 Ansible inventory 条目：

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. 在变量中手工定义主机

如果你想把来宾保留在 `hosts.yml` 之外，或者手里只有 IP，可以使用 `linux_ipa_client_hosts`：

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

说明：

- 如果 `name` 本身就是可解析的主机名或 FQDN，则 `ansible_host` 可选
- 如果你只知道 IP，`name` 可以填任意稳定别名
- 若省略 `ipa_hostname`，playbook 会回退到来宾内的 `hostname -f`

#### 3. Proxmox VM 自动发现

如果你希望 playbook 从一个或多个 Proxmox 节点自动拉取 Linux 来宾，请使用 discovery：

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# 可选：只允许经过批准的来宾进入 discovery 驱动的自动化。
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# 可选：即使启用了广泛的节点 discovery，也始终排除基础设施或敏感来宾。
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# 可选的首次接触 SSH 设置：当 guest agent 尚未运行，而仓库需要先通过 SSH
# 连入来宾才能安装它时使用。
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

说明：

- discovery 会把 VM 加入与其他 playbook 共用的同一个 `linux_ipa_clients_runtime` 组
- IP 发现依赖 QEMU guest agent 能报告网络接口
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` 只信任本身已经是 FQDN 的 VM 名称
- 如果你也希望把诸如 `Teleport-Server-1` 这样的安全短 VM 名自动提升为 `teleport-server-1.example.com` 之类的主机名提示，请设置 `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true`，并结合 `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` 是可选的，主要用于事件驱动的 hook / webhook 工作流，将 discovery 限定到一个或多个特定 VMID
- 来宾仍然需要最终主机名，该主机名要么已经在 VM 内配置好，要么通过手工定义中的 `ipa_hostname` 提供
- 来宾真实的系统主机名也必须适用于 enrollment；诸如 `localhost.localdomain` 这样的占位值必须在运行 `linux-clients` 或 `site` 之前先修正
- 如果来宾使用 `app-server-01` 这样的短主机名，你可以设置 `linux_ipa_identity_hostname_suffix`，并可选启用 `linux_freeipa_enroll_manage_hostname: true`，让项目在 enrollment 之前先解析并应用完整主机名，例如 `app-server-01.example.net`
- 如果 FreeIPA DNS 对你的来宾主机名拥有权威性，可设置 `linux_freeipa_enroll_manage_authoritative_dns: true`，这样项目会在 enrollment 前修复对应来宾的 A 与 PTR 记录，并移除链路本地 `fe80::/10` AAAA 记录
- 如果 DNS 还没准备好，可设置 `linux_ipa_manage_etc_hosts: true` 并提供 `linux_ipa_etc_hosts_entries`，这样角色会在 enrollment 检查前添加一个受管的 `/etc/hosts` bootstrap 块，用于 IPA 服务器和来宾 FQDN
- `guest_qemu_agent_install_enabled` 会在已可通过 SSH 或 WinRM 访问的来宾上安装 QEMU Guest Agent；对在同一次流程中后来才变得可达的 Linux 来宾也会重试；在 Linux enrollment 后还会再次重试，以便后续依赖 Proxmox agent 的工作流能够使用它
- 当你希望 discovery 保持开启，但只允许严格批准的来宾子集进入 Linux runtime inventory 时，请设置 `linux_ipa_proxmox_discovery_allowlist_enabled: true`；allowlist 可按精确 VMID、IP 与名称匹配
- 当启用了 discovery 的节点同时还承载防火墙、DNS 服务器等基础设施 VM，且这些 VM 绝不能接受 Linux IPA 自动化时，请设置 `linux_ipa_proxmox_discovery_blacklist_vmids`、`linux_ipa_proxmox_discovery_blacklist_ips` 或 `linux_ipa_proxmox_discovery_blacklist_names`；blacklist 的匹配优先级始终高于广泛 discovery 或 allowlist 带来的准入
- 对于尚未具备可用 guest agent 的 Proxmox-discovered Linux 来宾，请设置 `linux_ipa_proxmox_discovery_ansible_user`，以及 `linux_ipa_proxmox_discovery_ansible_password` 或 `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file`，以确保仓库有一条可用的首次接触 SSH 路径来安装 QEMU Guest Agent
- 如果这些被发现的来宾使用的是非 root SSH 用户，还需要设置 `linux_ipa_proxmox_discovery_ansible_become`、`linux_ipa_proxmox_discovery_ansible_become_method` 与 `linux_ipa_proxmox_discovery_ansible_become_password`，除非该账户已经具备无密码 sudo
- `guest_qemu_agent_install_manage_proxmox_vm_agent` 也会在来宾内安装路径运行前，为 Proxmox-backed Linux 来宾启用 Proxmox 侧的 guest-agent 通道（`qm set <vmid> --agent 1`）
- 如果这个 Proxmox VM 选项在运行中的 VM 上发生变化，仓库默认只发出警告，因为 Proxmox 可能需要一次新的 VM 启动才能让宿主开始使用 guest-agent 通道；若你希望仓库自动重启这些运行中的 VM，请设置 `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true`
- `linux_ipa_ssh_host_key_policy` 对 Linux 来宾连接默认使用 `accept_new`，这样新发现的 VM 可在不完全关闭 host key 校验的情况下建立连接；已改变的 host key 仍会失败，并要求操作者人工确认
- `linux_ipa_qga_ssh_bootstrap_enabled` 是 Proxmox-backed 来宾的首选免重启 bootstrap 路径，因为它可以在 SSH 尚不可用时，通过 QEMU Guest Agent 创建一个专用的仅密钥 automation 用户
- `linux_ipa_qga_ssh_bootstrap_qm_path` 默认是 `qm`，在真正失败前，bootstrap 流程也会探测 Proxmox 节点上的常见备用路径
- 对于允许 `guest-ping` 但拒绝 `guest-exec` 的来宾，QGA bootstrap 默认会跳过；请为它们保留另一条 SSH 路径，或设置 `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` 以便快速失败
- `linux_ipa_ssh_bootstrap_enabled` 可在主机名解析与 enrollment 前，把控制端 SSH 公钥安装到 Linux 来宾；即使关闭 key bootstrap，`linux_ipa_ssh_bootstrap_password` 仍会被用作 runtime Linux 来宾的共享首次接触密码回退
- Linux IPA enrollment 会重试因 FreeIPA JSON-RPC timeout 失败的上游 client join，并通过 `linux_ipaclient_kinit_attempts` 暴露对较慢或较忙 IPA 环境的调节能力
- Linux IPA enrollment 默认还会把 `ipa_servers` inventory 主机名合并进 join server 列表，这样客户端就能使用完整的 IPA 服务器集合，而不只是单一配置端点
- 当存在多个 IPA 服务器时，每一轮重试都会在 Linux client enrollment 过程中逐个尝试这些 IPA 服务器候选
- 统一的 `site` 工作流会先创建 FreeIPA hostgroup，再在 Linux enrollment 完成后把已注册的 runtime 主机加入其中，因此不会因为主机尚未 enrollment 而在 hostgroup 成员步骤上提前失败

## 配置面

大多数变量位于以下文件中：

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

关于逐文件布局，请参见 [docs/VARIABLES.md](../VARIABLES.md)。

关键变量族如下：

| 区域 | 变量 |
| --- | --- |
| FreeIPA 访问模型 | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Rollout 控制 | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Linux readiness 报告 | `linux_readiness_report_*` |
| Windows 管理 | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helper | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Ansible 连接机密 | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## 示例组策略

一个简单且可扩展的模式如下：

- FreeIPA 用户组 `proxmox-admins`
- FreeIPA 用户组 `linux-ssh-admins`
- FreeIPA 主机组 `linux-all`
- HBAC 规则 `allow-linux-ssh-admins`
- Sudo 规则 `allow-linux-ssh-admins-sudo`
- 面向同步组 `proxmox-admins-ipa` 的 Proxmox ACL 绑定

当你希望统一的 `site.yml` 运行自动把某些 IPA 用户授予 Linux SSH 与 `sudo` 访问权限时，请在 [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) 中填充 `freeipa_linux_admin_users`。

请记住，Proxmox LDAP sync 会按如下后缀生成同步组：

```text
<group-name>-<realm>
```

如果你的 FreeIPA 组名是 `proxmox-admins`，而 Proxmox realm 是 `ipa`，则同步后的 PVE 组名会变成：

```text
proxmox-admins-ipa
```

## 安全

- 所有机密信息都应存放在 `vault-freeipa.yml` 与 `vault-proxmox.yml` 中，而不是明文 inventory 变量文件里
- 对 Proxmox 来说，优先使用专用的只读 LDAP bind 账号
- 优先使用启用证书校验的 TLS
- 除一次性实验环境外，应保持 SSH host key 校验开启
- 当 Proxmox 来宾已经有可用的 QEMU Guest Agent 时，优先使用 `linux_ipa_qga_ssh_bootstrap_enabled`，而不是共享临时密码
- 只有在仓库已经具备一条有效的来宾管理路径时，才启用 `guest_qemu_agent_install_enabled`；对于 Proxmox discovery，这意味着要么 QGA 已在运行，要么已配置 `linux_ipa_proxmox_discovery_ansible_user` 加密码或密钥访问
- 如果启用了 Linux SSH bootstrap，请把共享 bootstrap 密码保存在加密变量中，并在密钥访问建立后尽快轮换或移除
- 不要把 IPA 管理员账号复用成 Proxmox LDAP bind 账号
- 在生产 rollout 前，检查 `proxmox_ldap_filter` 与 `proxmox_ldap_group_filter`，避免导入过多对象

如果你在一次性实验环境中明确要绕过 SSH host verification，请按 shell session 粒度关闭，而不是修改仓库默认值：

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## 幂等性与注意事项

本项目的设计目标是可复用且尽量保持幂等，但在生产 rollout 前仍应先在实验环境中验证。

已知注意点包括：

- Proxmox CLI 输出在不同版本之间可能有轻微差异
- FreeIPA 目录布局非常灵活，因此 LDAP 过滤器可能需要按你的目录树进行微调
- 如果已有手工管理的 PVE ACL 与角色，应先比对再让自动化覆盖其上
- Proxmox VM 自动发现依赖运行中的来宾与 QEMU guest-agent 提供的网络数据
- 纯 IP 的来宾定义仍然需要来宾内存在有效的最终主机名，或显式提供 `ipa_hostname`
- Proxmox playbook 通过提权运行，因此非 root SSH 用户必须具备可用的 `sudo`；若不是无密码 sudo，则你需要通过 `-K` 提供 become 密码
- 如果你把 `ansible_become_password` 存在 `vault-proxmox.yml` 中，就可以不使用 `-K`，因为 Ansible 会从加密变量中读取 sudo 密码

## 验证

在一次看似成功的 rollout 之后，不要假设所有访问路径都已经正确，应显式检查结果状态。

### 在 FreeIPA 中

- 确认预期的用户组已创建
- 确认预期的主机组已创建
- 确认预期的 HBAC 规则存在且处于启用状态
- 确认预期的 `sudo` 规则存在且处于启用状态

### 在 Proxmox 中

- 确认 LDAP realm 已存在
- 确认首次同步导入了预期的用户或组
- 确认目标同步组拥有预期的 ACL 绑定

### 在 Linux 来宾上

- 确认被允许的 IPA 用户可以登录
- 确认被拒绝的用户会被 HBAC 阻止
- 确认被允许的 IPA 管理员可以执行 `sudo -l`
- 若启用了 `linux_ipaclient_mkhomedir`，确认首次登录时会创建家目录

## 仓库布局

<details>
<summary>显示仓库布局</summary>

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

## 开发

仓库中主要的辅助文件包括：

- `.editorconfig`，用于在不同编辑器之间保持缩进、编码与换行约定一致
- `.gitattributes`，用于把常见文本文件固定为 `LF` 换行
- `.gitignore`，用于防止生成的 inventory、vault 数据、本地 collection 与编辑器垃圾文件进入 Git
- `.ansible-lint`，用于排除 vendor collection 路径，并仅抑制 YAML 行长规则
- `.yamllint`，用于在 playbook、inventory 与 workflow 文件上保持一致的 YAML 校验策略
- `.github/CODEOWNERS`，用于为主要仓库区域分配评审归属
- `.github/workflows/ci.yml`，在 push 与 pull request 事件上运行 lint 与 smoke 校验
- `.pre-commit-config.yaml`，如果安装了 `pre-commit`，会在提交前运行快速 lint hook
- `CHANGELOG.md`，集中记录仓库中的重要变更
- `docs/VARIABLES.md`，解释拆分后的 inventory 变量结构
- `docs/i18n/`，保存各语言 README；这些翻译文件应与英文 `README.md` 保持完整章节结构同步
- `docs/i18n/TRANSLATION_GUIDE.md`，说明如何让翻译 README 与英文源保持同步
- `scripts/bootstrap.ps1` 与 `scripts/bootstrap.sh`，将所需 collection 安装到仓库本地 `collections/` 路径，并应用 ansible-core 2.24+ 兼容修补
- `scripts/patch_freeipa_collection.py`，改写固定版本 FreeIPA collection 中的已弃用导入，以保持对未来 ansible-core 版本的兼容性
- `scripts/lint.py`，提供跨平台的 lint 入口，供本地使用、CI 与 pre-commit 复用
- `scripts/smoke-test.py`，在不触碰真实基础设施的前提下执行 example inventory 校验与 syntax 检查，也覆盖独立的 Windows playbook
- `scripts/check_translations.py`，对翻译版 README 进行元数据、章节结构与相对英文 README 的最小内容覆盖校验
- `scripts/lint.ps1` 与 `scripts/lint.sh`，将本地 lint 与 smoke 工作流打包执行
- `scripts/proxmox_event_webhook.py`，实现 Proxmox VM 事件的可选控制端 webhook 服务
- `scripts/proxmox-vm-hook.pl`，实现安装在 Proxmox 节点上的可选 VM hook 脚本
- `scripts/run-playbook.ps1`，为 Windows / PowerShell 环境提供统一的 `ansible-playbook` 封装
- `scripts/vault.ps1` 与 `scripts/vault.sh`，帮助创建、编辑、查看与加密分域 vault 文件
- `tests/`，承载仓库的验证面，当前从 smoke-test 文档开始
- `CONTRIBUTING.md`，说明预期的贡献与验证流程
- `SECURITY.md`，说明如何报告漏洞以及如何处理安全敏感信息

如果你的控制端已经安装了 `ansible-lint`：

```bash
ansible-lint
```

常用开发命令：

```bash
python scripts/smoke-test.py
python scripts/check_translations.py
python scripts/check_translations.py --strict
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
python .\scripts\check_translations.py
python .\scripts\check_translations.py --strict
.\scripts\lint.ps1
```

若要在每次提交前启用快速 lint hook：

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper 现在也直接支持常见运维参数：

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## 后续扩展

后续常见可扩展方向包括：

- 面向已准备好 IPA 的 Linux 模板构建 Packer 流水线
- 为统一 rollout 添加 AWX / Automation Controller 作业模板与调度
- 更强的 Proxmox tenant 与 pool 模型
- 面向 Windows RDP 或混合身份环境的 AD trust 工作流

## 许可证

本项目基于 [MIT License](../../LICENSE) 发布。
