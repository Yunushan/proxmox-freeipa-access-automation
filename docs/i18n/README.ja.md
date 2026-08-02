# Proxmox + FreeIPA アクセス自動化

このページは [README.md](../../README.md) の完全な構造対応翻訳です。英語版が正本ですが、この日本語版でも同じ運用範囲を読めるように保つ必要があります。

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## 言語

完全なドキュメントの正本は英語版です。さらに 20 言語の完全翻訳 README も利用できます。

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

この repository は、Identity と Access の **source of truth を FreeIPA** として扱います。Proxmox は LDAP realm を通してその directory を利用し、Linux guest は upstream の `ipaclient` role を通じて FreeIPA に参加し、access は synced groups、HBAC、sudo rules によって中央管理され、各 VM の local account へ散らばりません。

> [!IMPORTANT]
> このプロジェクトは **FreeRADIUS を identity source として使わず**、**各 VM の中に local user を作らず**、**Proxmox の permission edge case をすべて管理しようとはしません**。

## このプロジェクトが存在する理由

このリポジトリは、次のような前提がすでにある環境向けです。

- 健全に動作している FreeIPA
- Proxmox VE クラスタ
- 集中認証を使う必要がある Linux ゲスト
- Proxmox の LDAP bind 用に分離されたサービスアカウント
- 管理者と運用担当者のための明確なグループモデル

中心となる考え方は、Identity と Access の source of truth を FreeIPA に一本化することです。Proxmox は LDAP realm としてそのディレクトリを利用し、Linux ゲストは upstream の `ipaclient` role で FreeIPA に参加し、SSH、HBAC、`sudo` の制御は各 VM のローカルアカウントへ分散させず中央管理のまま維持します。

次のような onboarding / offboarding を主な流れにしたい場合に、この repository は適しています。

1. FreeIPA で user と group を作成または更新する
2. それらの identity を Proxmox に sync する
3. synced group から Proxmox role と ACL を適用する
4. FreeIPA login、HBAC、`sudo` rule を通じて Linux guest access を許可する

## 得られるもの

- FreeIPA の user group、hostgroup、HBAC rule、`sudo` rule の管理
- Linux 管理者向け FreeIPA default login shell の適用
- FreeIPA に接続する Proxmox LDAP realm の設定
- 指定した 1 台のクラスタノードから行う定期的な Proxmox realm sync
- 同期済みディレクトリグループに対する Proxmox RBAC binding
- static inventory、IP ベース target、Proxmox VM discovery による Linux guest の FreeIPA enrollment
- Proxmox QEMU Guest Agent を使った reboot 不要の SSH bootstrap を任意で利用可能
- Proxmox 管理下の Linux guest に対して、Proxmox 側で guest agent communication channel を有効化する任意機能
- すでに到達可能な guest、bootstrap 後に到達可能になる guest、Linux enrollment 後に再試行できる guest に対して、SSH または WinRM 経由で QEMU Guest Agent を任意インストール
- SSH 到達性と Proxmox QEMU Guest Agent 状態を確認するための任意の Linux readiness report
- Active Directory を使った Windows 10/11 と Windows Server 向けの分離された任意の domain membership workflow
- IPA CA trust、hosts file bootstrap、IPA service 到達性検証に限定した FreeIPA-aware な Windows helper workflow
- Linux guest への初回接続用 SSH 公開鍵 bootstrap
- FreeIPA access model 変更後に管理対象 Linux client で SSSD cache を自動 refresh
- Proxmox VM hook と webhook trigger を使った任意の event-driven Linux onboarding

## スコープ

| 含まれるもの | 含まれないもの |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm 設定 | FreeIPA user lifecycle 全体の作成 |
| 同期済みグループからの Proxmox RBAC | Proxmox multi-tenant のすべての edge case への完全対応 |
| Linux client の IPA enrollment | FreeIPA への Windows native login |
| Windows 向け AD domain membership workflow | AD object や GPO の広範な自動化 |
| Windows 向け限定 FreeIPA helper workflow | FreeIPA ベースの Windows helper を AD と同等と見なすこと |

## Windows ワークフロー

Windows サポートは、Linux IPA enrollment と混在させず、別ワークフローとして実装されています。

- `windows_qemu_guest_agent_clients` は、任意の QEMU Guest Agent helper task 専用です。
- `10-features.yml` で `windows_domain_membership_enabled: true` を設定すると Windows workflow が有効になります。
- `windows_management_clients` は `playbooks/windows-management.yml` と `playbooks/site.yml` 内の任意 Windows ステージが使う独立グループです。
- 実際の Windows login は Active Directory domain membership で扱います。FreeIPA を中心にする環境では、Windows を FreeIPA に直接 join させるのではなく、FreeIPA-AD trust の AD 側に参加させてください。

FreeIPA のみを使った Windows join はこのリポジトリではサポートしていません。Active Directory または FreeIPA-AD trust がない場合、Windows 側は到達済み guest の helper task と任意の QEMU Guest Agent install に限られます。

それでも domain join を伴わない、FreeIPA-aware な限定 Windows path が必要な場合は、`windows_freeipa_helpers_enabled: true` を有効にし、`playbooks/windows-freeipa-helpers.yml` とともに `windows_freeipa_helper_clients` を使ってください。この helper workflow では、IPA CA の trust、bootstrap 用の IPA CA 自動取得、期待する CA thumbprint の任意 pin、hosts file entry の任意管理、IPA DNS と重要 TCP port の検証、Windows からの HTTPS 到達性検証、IPA 関連 endpoint に対する Windows time source 検証、Windows local group membership 管理、OpenSSH Server の任意 install または公開はできますが、FreeIPA に対する Windows native login は提供しません。

同じ helper group に対して変更を加えず readiness check だけを行いたい場合は、`playbooks/windows-freeipa-validate.yml` を実行してください。この workflow は validation と summary の流れは保持しつつ、CA import、hosts file 変更、local group 変更、OpenSSH 管理をその run に限って non-mutating にします。

この workflow は WinRM または PSRP で到達可能な Windows 10/11 および Windows Server guest を対象にしています。

## アーキテクチャ

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

より長い設計説明は [docs/ARCHITECTURE.md](../ARCHITECTURE.md) にあります。

## 要件

### コントローラ

- Ansible Core 2.14 以上
- Proxmox primary node、IPA server、Linux client への SSH 到達性
- Windows workflow を使う場合は Windows guest への WinRM または PSRP 到達性
- 必要に応じた `sudo` または `root`
- QGA SSH bootstrap を使う場合、guest 内で QEMU Guest Agent がすでに稼働していること
- Windows 向け guest agent install fallback を使う場合、到達可能な Windows host が `windows_qemu_guest_agent_clients` に入っていること
- Windows domain membership を使う場合、到達可能な Windows host が `windows_management_clients` に入っており、AD join credential を提供できること
- Windows 向け FreeIPA helper task を使う場合、到達可能な Windows host が `windows_freeipa_helper_clients` に入っていること
- Linux SSH bootstrap を使う場合、controller には SSH keypair と、Ansible が使う guest account に対する初回 password login path が必要

### 対象ホスト

- `proxmox_primary` 内の host では Proxmox VE 6.x 以上
- Proxmox と Linux client から FreeIPA に到達できること
- Windows 10/11 と Windows Server guest は、WinRM または PSRP で到達できるなら分離された Windows workflow で管理可能
- DNS と時刻同期が正しいこと
- `proxmox_primary` では、`pveversion`、`pvesh`、`pveum` を実行できる `root`、または `sudo` 付き SSH user を使うこと
- Windows domain membership を使う場合、対象 Windows guest から対応する AD domain controller に到達できること
- Windows 向け限定 FreeIPA helper workflow を使う場合、対象 Windows guest から対応する IPA server に到達できること
- Proxmox discovery を使う場合、guest が QEMU Guest Agent 経由で利用可能な IP を公開できること

## ネットワークポート

この表は、このリポジトリの controller、Proxmox LDAP automation、Linux IPA enrollment flow が使う network port を示します。
ここでは、FreeIPA server-to-server replication 全体ではなく、このプロジェクトが実際に使う面に絞って記載しています。

| Name | Port | Protocol | Source | Destination | Required when | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node、IPA server、Linux guest | 常時 | Ansible 接続 |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | Windows management 有効時 | Windows guest への Ansible 接続 |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS server | Linux guest が IPA DNS を使う場合 | IPA record と外部名の解決 |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment と login 時 | Kerberos 認証 |
| LDAP | `389` | `TCP` | Linux guest | IPA server | Linux IPA enrollment と login 時 | LDAP と FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port`、既定 `443` | `TCP` | Linux guest | IPA server | Linux IPA enrollment 時 | client install 中の IPA web/API 検証 |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment と password 操作時 | Kerberos password と keytab 操作 |
| LDAPS | `636` | `TCP` | Primary Proxmox node | IPA または LDAP server | Proxmox LDAP realm が既定 `ldaps` を使う場合 | Proxmox LDAP realm 接続 |

補足:

- `LDAPS 636/TCP` は `proxmox_ldap_mode` の既定が `ldaps` であるため、このリポジトリの既定です。LDAP mode や port を変える場合は、実際に使う `proxmox_ldap_port` を許可してください。
- `WinRM` は Windows transport の設定に応じて通常 `5986/TCP` を HTTPS、`5985/TCP` を HTTP に使います。
- `DNS 53/TCP,UDP` は Linux guest が IPA server を resolver として使う場合だけ必要です。
- `Kerberos 88` と `Kerberos Password 464` はどちらも `TCP` と `UDP` の両方が必要です。
- Active Directory domain join には標準的な Windows-to-domain-controller port も必要ですが、それらは環境依存のためここでは詳細に列挙していません。
- Kerberos を安定して動かすには時刻同期も必須ですが、NTP source は環境依存であり、このリポジトリでは管理しません。

## 互換性

このリポジトリの Proxmox automation は、Proxmox VE 6.x 以降が使う realm と RBAC の `pveum` および `pvesh` interface を前提に書かれています。

- 既定でサポートする major: `6`, `7`, `8`, `9`, `10`
- validation は `pveversion` で検出した Proxmox version を確認します
- サポート対象 major の一覧は `proxmox_supported_major_versions` で環境に合わせて狭めたり広げたりできます
- `proxmox_allow_future_major_versions` は既定で `true` なので、最高 tested version を超える future major も既定では validation を通します
- ただし future major version は、この automation と公開された Proxmox interface が実際に確認されるまでは、あくまで compatibility candidate と見なしてください
- `1` から `5` のような旧 version は、この公開リポジトリでは tested support として主張していません。ローカルで追加する場合は、明示的な compatibility override として扱い、まず lab で full workflow を検証してください

legacy lab 向け local override 例:

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

## クイックスタート

以下の例は shell command を使います。必要な箇所では PowerShell 相当も併記します。

### 1. サンプル インベントリ と vault テンプレートをコピーする

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

### 2. 環境固有のファイルを編集する

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- Windows management を使う場合は `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- Windows management を使う場合は `inventories/production/group_vars/all/vault-windows.yml`

IPA と Proxmox の設定に加えて、Linux guest の source mode を 1 つ選びます。

- `linux_ipa_clients` 配下の static inventory entry
- `group_vars/all/30-linux-clients.yml` 内の `linux_ipa_client_hosts` entry
- `linux_ipa_proxmox_discovery_enabled: true` による Proxmox VM discovery

Linux IPA enrollment では、domain 値と server 一覧を区別してください。

- `ipaclient_domain` は共有される IPA DNS domain です。例: `example.com`
- `linux_ipa_servers` は IPA server の hostname 一覧です。例: `ipa01.example.com`

`root` ではなく `sudo` 可能な通常ユーザーで Proxmox に SSH 接続したい場合は、`hosts.yml` の `proxmox_primary` でそれを設定し、sudo password を `vault-proxmox.yml` に保存します。

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

この構成では、`vault_proxmox_become_password` は Proxmox host 上で通常 `sudo` 実行時に入力する password を意味します。

### 3. vault ファイルを暗号化する

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

Windows workflow を有効にする場合は、同じ command に `inventories/production/group_vars/all/vault-windows.yml` も追加してください。

または helper wrapper を使えます。これは既定で domain ごとに分離した vault ID を使い、必要なら example template から working vault file を作成します。

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

playbook 実行時に domain ごとに別 password を使いたい場合は、`--ask-vault-pass` ではなく vault ID を使ってください。

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

任意の Windows workflow でも別の vault password を使うなら、同じ command に `windows@prompt` を追加してください。

その playbook が参照するすべての vault file が同じ password を共有している場合にだけ `-AskVaultPass` を使ってください。

### 4. 必要なコレクションをインストールする

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

または直接実行します。

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

このリポジトリが compatibility patch を追加する前に `freeipa.ansible_freeipa` をインストールしていた場合は、bootstrap helper を再実行するか、`python .\scripts\patch_freeipa_collection.py` を 1 回実行して user-level collection install も patch してください。

`scripts/run-playbook.ps1` を使う場合は、`ansible-playbook` の前にその patch helper が自動実行されます。

### 5. まず検証を実行する

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

変更を加えずに Windows FreeIPA helper-only path だけを検証したい場合:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

runtime guest のうちどれが SSH で到達可能か、そして Proxmox-discovered guest のうちどれが QEMU Guest Agent に応答するかを read-only で監査したい場合:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

readiness report は既定で `.ansible/linux-readiness-report.json` に書き込まれます。
主要 field は次のように解釈してください。

- `ssh.ready=true`: 現在構成されている Ansible の SSH path が controller から成功している
- `ssh.promptless=true`: `ansible_password` なしで SSH probe が成功しているため、その path は Ansible にとって非対話的
- `ssh.auth_mode=password_configured`: host に `ansible_password` があるため probe が `sshpass` を使った
- `ssh.auth_mode=key_or_agent`: `ansible_password` なしの SSH batch mode で probe が成功した
- `qga.status=available`: その VM を所有する Proxmox node 上で `qm guest ping` が成功した
- `qga.status=disabled`: Proxmox VM 設定で QEMU Guest Agent が有効化されていない
- `qga.status=configured_unresponsive`: Proxmox 設定では guest agent が有効だが応答しない
- `qga.status=node_unreachable`: VM を所有する Proxmox node に controller から到達できず probe できなかった
- `qga.status=not_applicable`: host が Proxmox discovery 由来ではないため QGA probe を試していない

簡単な確認例:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. 任意: 予定されている変更を事前確認する

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> check mode は完全な simulation ではなく、部分的な preview として扱ってください。このリポジトリでは一部の Proxmox 設定に直接 CLI command を使い、Linux enrollment には upstream FreeIPA client role を使っているため、`--check` は有用ですが絶対的ではありません。
>
> FreeIPA HBAC rule については、check mode では rule definition step は検証しますが、その後段の enable または disable action は skip します。これは、dry run では実際には rule が作成されないため FreeIPA が「存在しない」と返して false failure になるのを避けるためです。
>
> Proxmox realm sync timer role も、check mode では最後の `systemd` enable または start step を skip します。unit file は diff に現れますが、dry run 中には実際には書き込まれないためです。
>
> Linux IPA enrollment も check mode では skip されます。repository は discovery、hostname resolution、input validation は行いますが、upstream の `ipaclient` role 自体は dry run 中に実行しません。

### 7. フル構成を適用する

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

任意の Windows workflow が有効で、`vault-windows.yml` が別 password を使う場合は、`--ask-vault-pass` ではなく `--vault-id windows@prompt` または PowerShell wrapper の `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` を使って同じ playbook を実行してください。

## Rollout 順序

初回 deployment では、stack を次の順序で適用してください。

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

この順序は、すべてを一度に流すよりも troubleshooting をかなり容易にします。

例えば、1 台の Linux guest だけに限定して rollout する PowerShell 例:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

既定の rollout control は保守的です。

- FreeIPA access の変更は `serial: 1`
- Proxmox の変更は `serial: 1`
- hostname resolution、validation、Linux enrollment は `serial: 10`
- Windows management の変更は `serial: 10`
- すべての rollout path で既定 `max_fail_percentage: 0`

これらの値は `inventories/production/group_vars/all/15-rollout.yml` で調整してください。

## Tag モデル

細かい playbook を増やし続けるのではなく、安定した rollout slice を target するために tag を使ってください。

- core domain: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helper: `windows`, `windows_freeipa`
- FreeIPA access model: `freeipa_access`
- Proxmox subset: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- event-driven VM handling: `event`, `linux_refresh`

例:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## イベント駆動型 VM オンボーディング

VM start 直後や migration 後に Proxmox から Linux discovery と IPA enrollment を即座に trigger したい場合は、[docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) にある任意の hook / webhook path を使ってください。

この path は event 専用 playbook `playbooks/proxmox-vm-event.yml` を使うため、処理対象は Linux guest 側と FreeIPA 側に限定されます。各 VM event のたびに Proxmox LDAP realm automation や RBAC を再実行することはありません。

このリポジトリは現在、`proxmox_vm_event_onboarding_enabled: true` が設定され、必要な webhook variable が揃っている場合、`site.yml` または `proxmox.yml` からその任意 hook / webhook stack 自体も導入できます。

Proxmox VM hook には独立した `create` phase はありません。実運用では、新しい VM は通常、最初の `post-start` event で捕捉され、migration hook は source node と destination node の両方で trigger される可能性があります。

## Inventory モデル

このリポジトリでは、明示定義された 6 つの inventory group と、runtime に生成される 1 つの group を使います。

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

必要であれば独自の inventory group を追加定義し、それを FreeIPA hostgroup definition から参照することもできます。hostgroup 側から「準備済みの Linux guest 全体」を使いたい場合は、`linux_ipa_clients_runtime` group を参照してください。

> [!IMPORTANT]
> FreeIPA は各 guest に対して最終 hostname を必要とします。IP-only target や Proxmox discovery を使う場合は、`ipa_hostname` を明示するか、guest 内の `hostname -f` が最終 FQDN を返すことを確認してください。playbook は FreeIPA hostgroup membership を組み立てる前にその hostname を解決します。

> [!TIP]
> 再利用する golden template をそのまま FreeIPA に enroll しないでください。先に VM を clone し、最終 hostname を設定してから resulting guest を enroll してください。

### Linux ゲストのソースモード

`linux_ipa_clients` を埋める方法は 3 つあります。

#### 1. static inventory hosts

guest 名がすでに分かっているなら、通常の Ansible inventory entry を使います。

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. variable で manual host definition を行う

guest を `hosts.yml` の外に置きたい場合や、手元に IP しかない場合は `linux_ipa_client_hosts` を使ってください。

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

補足:

- `name` がすでに解決可能な hostname または FQDN であれば、`ansible_host` は任意です
- IP しか分からない場合は、`name` には安定した任意の alias を使ってください
- `ipa_hostname` を省略した場合、playbook は guest 内の `hostname -f` に fallback します

#### 3. Proxmox VM auto-discovery

1 台以上の Proxmox node から Linux guest を引いてきたい場合は discovery を使います。

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

補足:

- discovery は他の playbook と同じ `linux_ipa_clients_runtime` group に VM を追加します
- IP discovery は network interface を報告できる QEMU guest agent に依存します
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` は、すでに FQDN である VM 名だけを信用します
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` を設定すると、`Teleport-Server-1` のような安全な short VM name も `linux_ipa_identity_hostname_suffix` を通じて `teleport-server-1.example.com` のような hostname hint に自動昇格できます
- `linux_ipa_proxmox_discovery_vmids` は任意で、主に event-driven hook または webhook workflow で discovery 対象を特定の VMID に絞るために使います
- guest には依然として final hostname が必要であり、それは VM 内ですでに設定されているか、manual definition で `ipa_hostname` として与える必要があります
- 実際の guest system hostname も enrollment に有効でなければなりません。`localhost.localdomain` のような placeholder は、`linux-clients` または `site` を実行する前に VM 内で置き換えてください
- guest が `app-server-01` のような short hostname を使う場合、`linux_ipa_identity_hostname_suffix` と必要に応じて `linux_freeipa_enroll_manage_hostname: true` を設定することで、`app-server-01.example.net` のような完全 hostname に解決・適用してから enrollment できます
- FreeIPA DNS が guest hostname に対して authoritative なら、`linux_freeipa_enroll_manage_authoritative_dns: true` を設定することで、関連する A / PTR record を修復し、enrollment 前に link-local `fe80::/10` の AAAA record を削除できます
- DNS がまだ整っていない場合は、`linux_ipa_manage_etc_hosts: true` と `linux_ipa_etc_hosts_entries` を設定して、IPA server と guest FQDN 用の管理済み `/etc/hosts` bootstrap block を enrollment check より前に追加できます
- `guest_qemu_agent_install_enabled` は、SSH または WinRM で到達可能な guest に QEMU Guest Agent をインストールし、同じ workflow の中で後から到達可能になった Linux guest に再試行し、さらに Linux enrollment 後にも再試行するため、agent に依存する Proxmox workflow が利用可能になります
- `linux_ipa_proxmox_discovery_allowlist_enabled: true` を設定すると、discovery 自体は有効のままでも、明示的に許可した一部の Proxmox guest だけを Linux runtime inventory に admission できます。allowlist は VMID、IP、name で正確に match します
- `linux_ipa_proxmox_discovery_blacklist_vmids`、`linux_ipa_proxmox_discovery_blacklist_ips`、`linux_ipa_proxmox_discovery_blacklist_names` を設定すると、discovery 対象 node 上にある firewall や DNS server のような infrastructure VM に Linux IPA automation が誤適用されるのを防げます。blacklist match は広域 discovery と allowlist admission のどちらよりも優先されます
- Proxmox discovery された Linux guest でまだ guest agent が機能していない場合は、`linux_ipa_proxmox_discovery_ansible_user` とあわせて `linux_ipa_proxmox_discovery_ansible_password` または `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` を設定し、repository が QEMU Guest Agent install 用の first-touch SSH path を持てるようにしてください
- その discovery guest が non-root SSH user を使うなら、`linux_ipa_proxmox_discovery_ansible_become`、`linux_ipa_proxmox_discovery_ansible_become_method`、`linux_ipa_proxmox_discovery_ansible_become_password` も設定してください。その account がすでに passwordless `sudo` を持つ場合は不要です
- `guest_qemu_agent_install_manage_proxmox_vm_agent` は、guest 内の install path を始める前に、Proxmox 側の guest agent communication (`qm set <vmid> --agent 1`) も有効化します
- その Proxmox VM option を稼働中 VM に対して変更した場合、既定では repository は warning のみ出します。Proxmox 側で guest agent channel を使うには再起動が必要な場合があるからです。稼働中 VM を自動 reboot したいなら `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` を設定してください
- `linux_ipa_ssh_host_key_policy` は Linux guest への接続に既定で `accept_new` を使うため、newly discovered VM に対して host key checking を完全無効化せずに接続できます。変更された host key は依然として fail し、operator review が必要です
- `linux_ipa_qga_ssh_bootstrap_enabled` は Proxmox-based guest に推奨される no-reboot bootstrap path です。通常の SSH login より前に、QEMU Guest Agent を使って key-only の専用 automation user を作成できます
- `linux_ipa_qga_ssh_bootstrap_qm_path` の既定は `qm` であり、bootstrap flow は fail する前に Proxmox node 上の一般的な fallback path も確認します
- `guest-ping` は許可しつつ `guest-exec` を拒否する guest は、QGA bootstrap 中に既定で skip されます。その場合は別の SSH path を用意するか、`linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` を設定して即 fail させてください
- `linux_ipa_ssh_bootstrap_enabled` は Linux guest に controller の public key を hostname resolution と enrollment より前に任意でインストールします。`linux_ipa_ssh_bootstrap_password` は key-based bootstrap を無効にしていても Linux runtime guest に対する shared first-touch password fallback としても使われます
- Linux IPA enrollment は FreeIPA JSON-RPC timeout で失敗した upstream client join を retry し、より遅いまたは混雑した IPA 環境向けに `linux_ipaclient_kinit_attempts` を公開します
- Linux IPA enrollment は既定で inventory 上の `ipa_servers` hostname も join server list に統合するため、client は 1 つの configured endpoint だけでなく server set 全体を使えます
- IPA server が複数ある場合、各 retry round は Linux client enrollment 中にそれらの candidate IPA server を順番に試します
- 合成 workflow `site` はまず FreeIPA hostgroup を作成し、その後に enrolled 済み runtime host を追加するため、pre-enrollment run が「guest がまだ enrolled されていない」という理由だけで hostgroup membership step で失敗しません

## 設定サーフェス

ほとんどの値は次の場所にあります。

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

ファイルごとの整理は [docs/VARIABLES.md](../VARIABLES.md) を参照してください。

主要な variable family:

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
| Ansible 接続 secret | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## グループ戦略の例

単純ですがスケールしやすい基本パターン:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa` に対する Proxmox ACL binding

特定の IPA user に Linux SSH と sudo 権を自動的に付与したい場合は、[`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) の `freeipa_linux_admin_users` を埋めてください。これにより `site.yml` の combined run が管理対象 group `linux-ssh-admins` 経由で権限を付与します。

Proxmox LDAP sync は suffix 付きの synced group を作ることに注意してください。

```text
<group-name>-<realm>
```

例えば FreeIPA group が `proxmox-admins` で Proxmox realm が `ipa` なら、生成される synced PVE group は次のようになります。

```text
proxmox-admins-ipa
```

## セキュリティ

- すべての secret は plaintext の inventory variable file ではなく `vault-freeipa.yml` と `vault-proxmox.yml` に保存する
- Proxmox には read-only の専用 LDAP bind account を優先して使う
- certificate verification を有効にした TLS を優先する
- 一時 lab 以外では SSH host key checking を有効のまま維持する
- Proxmox guest ですでに QEMU Guest Agent が動作している場合は、shared temporary password よりも `linux_ipa_qga_ssh_bootstrap_enabled` を優先する
- `guest_qemu_agent_install_enabled` を使うのは、repository がすでに guest 内に入るための有効な management path を持っている場合に限る。Proxmox discovery では、QGA がすでに動作しているか、`linux_ipa_proxmox_discovery_ansible_user` と password か key access が設定されていることを意味する
- Linux SSH bootstrap を有効にする場合は、shared bootstrap password を暗号化された variable に保存し、key-based access が確立したら rotate または削除する
- IPA admin account を Proxmox LDAP bind account として再利用しない
- production rollout 前に `proxmox_ldap_filter` と `proxmox_ldap_group_filter` を見直し、過剰な object import を避ける

一時 lab で意図的に SSH host key verification を外したい場合は、repository default を変えるのではなく shell session 単位で opt-out してください。

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## 冪等性と注意点

この repository は再実行可能で、ほとんどの部分は idempotent になるように設計されていますが、production rollout 前には必ず lab で検証すべきです。

既知の注意点:

- Proxmox CLI の output は release ごとにわずかに異なる場合がある
- FreeIPA の directory layout には柔軟性があるため、LDAP filter は環境に合わせて tuning が必要な場合がある
- 以前から手動管理されている PVE ACL や role は、その上に automation を適用する前に比較確認するべき
- Proxmox VM auto-discovery は、稼働中 guest と QEMU guest agent の network data に依存する
- IP ベースの guest definition でも、guest 内の有効な final hostname、または明示的な `ipa_hostname` が必要
- Proxmox play は privilege escalation 付きで動くため、non-root SSH user は機能する `sudo` を持つ必要があり、その user に passwordless `sudo` がないなら `-K` で become password を渡す必要がある
- `ansible_become_password` を `vault-proxmox.yml` に保存していれば、Ansible が暗号化 variable から sudo password を読むため `-K` は省略できる

## 検証

rollout が成功した後は、すべての access path が正しくなったと仮定せず final state を確認してください。

### FreeIPA 上で確認すること

- 期待した user group が存在すること
- 期待した hostgroup が存在すること
- 期待した HBAC rule が存在し有効であること
- 期待した `sudo` rule が存在し有効であること

### Proxmox 上で確認すること

- LDAP realm が存在すること
- initial sync が期待どおりの user / group を import していること
- target となる synced group に期待した ACL binding があること

### Linux ゲスト上で確認すること

- 許可された IPA user が login できること
- 許可されていない user が HBAC によって拒否されること
- 許可された IPA admin が `sudo -l` を実行できること
- `linux_ipaclient_mkhomedir` が有効なら、初回 login 時に home directory が作成されること

## リポジトリ構成

<details>
<summary>リポジトリ構成を表示する</summary>

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

## 開発

このリポジトリに含まれる主要 helper file:

- `.editorconfig`: editor 間で空白、encoding、改行の既定値を揃える
- `.gitattributes`: 一般的な text file に `LF` 改行を強制する
- `.gitignore`: 生成 inventory、vault data、local collection、editor のゴミが Git に入るのを防ぐ
- `.ansible-lint`: vendor collection path を除外し、YAML line-length rule のみを抑制する
- `.yamllint`: playbook、inventory、workflow 全体で一貫した YAML validation を保つ
- `.github/CODEOWNERS`: repo の主要領域ごとの review ownership を示す
- `.github/workflows/ci.yml`: push と pull request で lint と smoke validation を実行する
- `.pre-commit-config.yaml`: `pre-commit` が入っている場合に commit 前の軽量 lint hook を実行する
- `CHANGELOG.md`: 重要な repository change を 1 か所で追跡する
- `docs/VARIABLES.md`: 分割された inventory variable 構造を説明する
- `docs/i18n/`: 翻訳 README を格納する。これらの file は英語版 `README.md` の full section structure を反映しなければならない
- `docs/i18n/TRANSLATION_GUIDE.md`: 翻訳 README を同期させる方法を説明する
- `scripts/bootstrap.ps1` と `scripts/bootstrap.sh`: 必要な collection を local `collections/` path にインストールし、ansible-core 2.24+ 向けの compatibility patch を適用する
- `scripts/patch_freeipa_collection.py`: pinned FreeIPA collection 内の deprecated import を書き換え、将来の ansible-core と互換を保つ
- `scripts/lint.py`: local、CI、pre-commit で使う cross-platform lint entry point を提供する
- `scripts/smoke-test.py`: 実インフラに触れずに example inventory validation と syntax check を行い、分離された Windows playbook の coverage も含む
- `scripts/check_translations.py`: 翻訳 README の metadata、section structure parity、英語版 canonical README に対する最小 content coverage を監査する
- `scripts/lint.ps1` と `scripts/lint.sh`: local の lint と smoke workflow を束ねる
- `scripts/proxmox_event_webhook.py`: controller 側の任意 Proxmox VM event webhook として動作する
- `scripts/proxmox-vm-hook.pl`: node に配置する任意 Proxmox VM hook として動作する
- `scripts/run-playbook.ps1`: Windows / PowerShell 環境向けの統一 `ansible-playbook` wrapper を提供する
- `scripts/vault.ps1` と `scripts/vault.sh`: domain ごとに分割した vault file の作成、編集、閲覧、暗号化を補助する
- `tests/`: smoke-test documentation から始まる repository の verification surface を保持する
- `CONTRIBUTING.md`: 想定される contribution と validation workflow を文書化する
- `SECURITY.md`: 脆弱性報告と security-sensitive な情報の扱い方を文書化する

controller に `ansible-lint` が入っている場合:

```bash
ansible-lint
```

repository smoke check を直接実行するには:

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

完全な local lint pass には:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

各 commit の前に fast lint hook を有効化するには:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper は一般的な operator option も直接サポートします:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## 次の拡張

次に考えやすい拡張:

- IPA-ready な Linux template 向け Packer pipeline
- combined rollout 用の AWX または Automation Controller job template と scheduling
- より強い Proxmox tenant / pool model
- Windows RDP や hybrid identity 環境向けの AD trust workflow

## ライセンス

[0BSD License](../../LICENSE) の下で公開されています。
