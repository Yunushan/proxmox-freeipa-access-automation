# Proxmox + FreeIPA 访问自动化

本页提供 [README.md](../../README.md) 的完整中文结构化翻译。英文版仍然是规范来源，但本页覆盖同样的主要章节，方便中文读者直接阅读完整说明。

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## 为什么需要这个项目

当你已经具备以下条件时，可以使用这个仓库：

- 稳定可用的 FreeIPA 环境
- Proxmox VE 集群
- 需要集中认证的 Linux 虚拟机
- 专门用于 Proxmox LDAP 绑定的 FreeIPA 服务账号
- 明确的管理员与运维组模型

核心目标是把 FreeIPA 作为身份与访问控制的唯一事实来源。Proxmox 通过 LDAP realm 消费目录，Linux 来宾通过上游 `ipaclient` 角色加入 FreeIPA，SSH、HBAC 与 `sudo` 权限保持集中管理，而不是在每台主机上散落本地账号。

## 你将获得什么

- FreeIPA 用户组、主机组、HBAC 规则与 `sudo` 规则管理
- 面向 FreeIPA 的 Proxmox LDAP realm 配置
- 从指定集群节点执行的周期性 Proxmox realm 同步
- 基于同步目录组的 Proxmox RBAC 绑定
- 通过静态清单、手工主机定义或 Proxmox 发现实现 Linux 加入 FreeIPA
- 基于 QEMU Guest Agent 的可选无重启 SSH bootstrap
- 对可达来宾通过 SSH 或 WinRM 安装 QEMU Guest Agent 的可选回退路径
- 首次接入时的可选 SSH 公钥 bootstrap
- 在 FreeIPA 访问模型变更后自动刷新 SSSD 缓存
- 基于 `post-start` 和 `post-migrate` 的可选事件驱动入管

## 范围

| 包含 | 不包含 |
| --- | --- |
| FreeIPA 访问模型 | Windows 域加入 |
| Proxmox LDAP realm 配置 | FreeRADIUS 部署 |
| 基于同步组的 Proxmox RBAC | FreeIPA 用户生命周期创建 |
| Linux IPA 客户端入管 | 覆盖所有 Proxmox 多租户边界场景 |

## 架构

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

更完整的设计说明见 [docs/ARCHITECTURE.md](../ARCHITECTURE.md)。

## 前提要求

### 控制端

- Ansible Core 2.14 或更高版本
- 能通过 SSH 到达 Proxmox 主节点、IPA 服务器和 Linux 客户端
- 需要时具备 `sudo` 或 `root`
- 启用 QGA SSH bootstrap 时，来宾内的 QEMU Guest Agent 必须已经运行
- 启用 Windows 客户端回退安装时，可达主机必须加入 `windows_qemu_guest_agent_clients`
- 启用 Linux SSH bootstrap 时，控制端需要 SSH 密钥对以及一条可使用密码的初始登录路径

### 目标端

- `proxmox_primary` 中的主机运行 Proxmox VE 6.x 或更高版本
- Proxmox 与 Linux 客户端都能访问 FreeIPA
- DNS 与时间同步正常
- `proxmox_primary` 应使用 `root`，或使用能对 `pveversion`、`pvesh`、`pveum` 执行 `sudo` 的 SSH 用户
- 启用 Proxmox 自动发现时，被发现的来宾必须通过 QEMU Guest Agent 提供可用 IP

## 网络端口

完整端口表仍以英文 README 为准。本仓库主要使用以下端口：

- `22/TCP`：控制端到 Proxmox、IPA、Linux 来宾的 SSH
- `53/TCP,UDP`：Linux 来宾到 IPA DNS 服务器
- `88/TCP,UDP` 与 `464/TCP,UDP`：Kerberos 认证与口令相关操作
- `389/TCP`：Linux IPA 加入流程中的 LDAP
- `linux_freeipa_enroll_https_port`，默认 `443/TCP`：IPA Web/API 预检
- `636/TCP`：`ldaps` 模式下的 Proxmox LDAP realm

## 兼容性

- 面向 Proxmox VE 6.x 及后续版本
- 默认支持的大版本：`6`, `7`, `8`, `9`, `10`
- 可通过 `proxmox_supported_major_versions` 覆盖
- `proxmox_allow_future_major_versions` 默认值为 `true`

## 快速开始

### 1. 复制示例清单与 vault 模板

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

### 2. 修改环境相关文件

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

同时还要选择 Linux 来宾来源方式：静态清单、`linux_ipa_client_hosts`，或启用 `linux_ipa_proxmox_discovery_enabled: true`。

### 3. 加密 vault 文件

```bash
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
```

### 4. 安装所需 collection

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

### 5. 先运行校验

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

### 6. 可选：预览变更

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

### 7. 应用完整配置

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## 发布顺序

首次部署建议按以下顺序执行：

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

默认策略较为保守：

- FreeIPA 访问模型使用 `serial: 1`
- Proxmox 变更使用 `serial: 1`
- Linux 发现、主机名解析与加入流程使用 `serial: 10`
- 所有路径默认 `max_fail_percentage: 0`

## Tag 模型

- 核心域：`freeipa`, `proxmox`, `linux`, `validate`
- FreeIPA 访问模型：`freeipa_access`
- Proxmox 子集：`proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux 准备：`inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux 加入：`linux_enroll`
- 事件路径：`event`, `linux_refresh`

## 事件驱动 VM 入管

如果希望 Proxmox 在 VM 启动或迁移后立刻触发 Linux 发现与 IPA 加入，请使用 [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) 中说明的可选 hook/webhook 工作流。

- 该流程使用 `playbooks/proxmox-vm-event.yml`
- 不会在每个 VM 事件上重新运行 Proxmox LDAP realm 或 RBAC
- Proxmox hook 没有独立的 `create` 阶段；新 VM 通常在第一次 `post-start` 时被处理
- 当 `proxmox_vm_event_onboarding_enabled: true` 且变量完整时，仓库也可以从 `site.yml` 或 `proxmox.yml` 自动部署该堆栈

## 清单模型

本仓库使用以下核心组：

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

如果你使用仅 IP 的目标或 Proxmox 发现，仍然必须保证来宾最终主机名正确，可通过 `ipa_hostname` 显式指定，或确保 `hostname -f` 返回最终 FQDN。

### Linux 来宾来源模式

1. 静态 inventory 主机
2. 在 `linux_ipa_client_hosts` 中手工定义
3. 通过 `linux_ipa_proxmox_discovery_*` 从 Proxmox 自动发现

关键说明：

- 自动发现依赖 QEMU Guest Agent 提供网络接口信息
- `linux_ipa_proxmox_discovery_vmids` 主要用于事件驱动路径
- 可配合 `linux_ipa_identity_hostname_suffix` 与 `linux_freeipa_enroll_manage_hostname: true`
- 当 FreeIPA DNS 为权威 DNS 时，可用 `linux_freeipa_enroll_manage_authoritative_dns: true`
- 若 DNS 尚未就绪，可用 `linux_ipa_manage_etc_hosts: true` 与 `linux_ipa_etc_hosts_entries`
- `linux_ipa_qga_ssh_bootstrap_enabled` 是首选的无重启 bootstrap 路径

## 配置面

大多数变量位于：

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

逐文件说明见 [docs/VARIABLES.md](../VARIABLES.md)。

## 组策略示例

- FreeIPA 用户组 `proxmox-admins`
- FreeIPA 用户组 `linux-ssh-admins`
- FreeIPA 主机组 `linux-all`
- HBAC 规则 `allow-linux-ssh-admins`
- `sudo` 规则 `allow-linux-ssh-admins-sudo`
- Proxmox 针对同步组 `proxmox-admins-ipa` 的 ACL 绑定

## 安全

- 所有敏感信息只放在 vault 文件中
- 尽量为 Proxmox 使用专用只读 LDAP 绑定账号
- 优先使用启用证书校验的 TLS
- 在非一次性实验环境中保持 SSH 主机密钥校验开启
- 如果 QGA 已可用，优先使用 `linux_ipa_qga_ssh_bootstrap_enabled`，而不是共享临时密码

## 幂等性与注意事项

本项目尽量保持可复用与幂等，但仍应先在实验环境中验证。已知限制包括：

- 不同 Proxmox 版本的 CLI 输出可能略有差异
- LDAP 过滤器可能需要按目录树进行调整
- Proxmox 自动发现依赖运行中的来宾以及 QGA 网络数据
- 仅 IP 的定义仍然需要最终有效主机名

## 验证

部署完成后请显式验证结果：

- 在 FreeIPA 中确认用户组、主机组、HBAC 规则、`sudo` 规则及其启用状态
- 在 Proxmox 中确认 LDAP realm、初次同步结果与 ACL 绑定
- 在 Linux 来宾中确认允许用户可登录、禁止用户被 HBAC 拒绝、`sudo -l` 正常、启用 `mkhomedir` 时首次登录创建家目录

## 仓库结构

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

完整目录树仍以英文 README 为准。

## 开发

仓库内包含的辅助文件与脚本包括：

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

常用命令：

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
.\scripts\lint.ps1
```

## 后续可扩展方向

- 面向 IPA 就绪 Linux 模板的 Packer 流水线
- AWX 作业模板与调度
- 独立的 Proxmox tenant 与 pool 模型
- 面向 RDP 场景的 Windows 或 AD trust 流程

## 许可证

本项目基于 [MIT License](../../LICENSE) 发布。
