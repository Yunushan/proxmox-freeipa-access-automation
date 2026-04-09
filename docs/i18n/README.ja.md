# Proxmox + FreeIPA アクセス自動化

このページは [README.md](../../README.md) の完全な構造翻訳です。英語版が最終的な canonical source ですが、この日本語版でも同じ主要セクションを読めます。

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## このプロジェクトが存在する理由

次の前提がある環境で使うことを想定しています。

- 健全な FreeIPA 環境
- Proxmox VE クラスタ
- 集中認証を使う Linux ゲスト
- Proxmox LDAP bind 用の専用サービスアカウント
- 管理者と運用者の明確なグループモデル

基本方針は、FreeIPA を identity と access の source of truth にすることです。Proxmox は LDAP realm としてこのディレクトリを利用し、Linux ゲストは `ipaclient` role で FreeIPA に参加し、SSH・HBAC・`sudo` の制御は集中管理のまま維持されます。

## 得られるもの

- FreeIPA の user group、hostgroup、HBAC rule、`sudo` rule 管理
- FreeIPA 向け Proxmox LDAP realm 設定
- 指定クラスタノードからの定期 realm sync
- 同期されたグループに対する Proxmox RBAC binding
- static inventory、manual host definitions、Proxmox discovery による Linux enrollment
- QEMU Guest Agent を使った optional な no-reboot SSH bootstrap
- 到達可能な guest に対する SSH/WinRM 経由の optional guest-agent install
- first-touch 用の optional SSH public-key bootstrap
- FreeIPA access model 変更後の自動 SSSD refresh
- `post-start` と `post-migrate` に対する optional event-driven onboarding

## スコープ

| 含まれるもの | 含まれないもの |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm 設定 | FreeRADIUS deployment |
| synced group からの Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | すべての Proxmox multi-tenant edge case |

## アーキテクチャ

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## 要件

### Controller

- Ansible Core 2.14+
- Proxmox primary node、IPA server、Linux client への SSH 到達性
- 必要に応じた `sudo` または `root`
- QGA SSH bootstrap を使う場合、guest 内で QEMU Guest Agent が起動済みであること
- Windows fallback を使う場合、到達可能な host が `windows_qemu_guest_agent_clients` に入っていること
- Linux SSH bootstrap を使う場合、SSH keypair と初回 password login path が必要

### Targets

- `proxmox_primary` の host は Proxmox VE 6.x 以降
- Proxmox と Linux client から FreeIPA に到達できること
- 正しい DNS と時刻同期
- `proxmox_primary` では `root` か、`pveversion`、`pvesh`、`pveum` を `sudo` で実行できる SSH user
- Proxmox discovery では QEMU Guest Agent から usable IP が取得できること

## ネットワークポート

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` と `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`、既定 `443/TCP`
- `636/TCP` for `ldaps`

## 互換性

- Proxmox VE 6.x 以降を対象
- default supported majors: `6`, `7`, `8`, `9`, `10`
- `proxmox_supported_major_versions` で上書き可能
- `proxmox_allow_future_major_versions` は既定で `true`

## クイックスタート

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

環境に合わせて `hosts.yml`、`10-features.yml`、`15-rollout.yml`、`20-freeipa.yml`、`30-linux-clients.yml`、`40-proxmox-ldap.yml`、`50-proxmox-sync.yml`、`60-proxmox-rbac.yml`、`vault-freeipa.yml`、`vault-proxmox.yml` を編集してください。

## Rollout 順序

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

既定値は保守的です。FreeIPA と Proxmox は `serial: 1`、Linux は `serial: 10`、`max_fail_percentage: 0` が使われます。

## Tag モデル

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

`post-start` や `post-migrate` の直後に Linux discovery と IPA enrollment を自動実行したい場合は、[docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) の optional hook/webhook workflow を使います。この経路は `playbooks/proxmox-vm-event.yml` を使用し、各 event ごとに LDAP realm や RBAC を再実行せず、新しい VM は最初の `post-start` で取り込みます。

## Inventory モデル

主要グループ:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only や Proxmox discovery を使う場合でも、guest には `ipa_hostname` または `hostname -f` による最終 FQDN が必要です。

### Linux source mode

1. static inventory hosts
2. `linux_ipa_client_hosts` の manual definitions
3. `linux_ipa_proxmox_discovery_*` による Proxmox discovery

重要な注意点: discovery は QEMU Guest Agent の network data に依存し、`linux_ipa_proxmox_discovery_vmids` は event path で有用です。短いホスト名には `linux_ipa_identity_hostname_suffix` が使え、authoritative DNS repair には `linux_freeipa_enroll_manage_authoritative_dns`、DNS 未整備時には `/etc/hosts` bootstrap が使えます。

## Configuration surface

主要ファイル:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## グループ戦略の例

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## セキュリティ

- secrets は vault files のみに保存する
- Proxmox には read-only の dedicated LDAP bind account を使う
- certificate verification 付き TLS を優先する
- disposable lab 以外では SSH host key checking を無効にしない

## Idempotency と注意点

この repository は繰り返し実行できるよう設計されていますが、production 前に lab で検証すべきです。既知の制約には Proxmox CLI output の差異、LDAP filter tuning、discovery の QGA と稼働中 guest への依存、IP ベース target に対する最終 hostname の必要性があります。

## 検証

- FreeIPA で groups、hostgroups、HBAC、`sudo` を確認する
- Proxmox で LDAP realm、sync、ACL bindings を確認する
- Linux guest で許可された login、拒否される HBAC case、`sudo -l`、home 作成を確認する

## リポジトリ構成

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## 開発

この repository には `.editorconfig`、`.gitattributes`、`.gitignore`、`.ansible-lint`、`.yamllint`、CI workflow、`scripts/bootstrap.*`、`scripts/lint.*`、`scripts/smoke-test.py`、`scripts/proxmox_event_webhook.py`、`scripts/proxmox-vm-hook.pl`、`scripts/run-playbook.ps1`、`scripts/vault.*` が含まれます。

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## 次の拡張

- IPA-ready Linux template 向け Packer pipeline
- AWX job template と schedule
- 分離された Proxmox tenant / pool model
- RDP 指向環境向け Windows または AD-trust flow

## ライセンス

このプロジェクトは [MIT License](../../LICENSE) の下で公開されています。
