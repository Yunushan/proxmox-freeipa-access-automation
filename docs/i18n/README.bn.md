# Proxmox + FreeIPA অ্যাক্সেস অটোমেশন

এই পৃষ্ঠাটি [README.md](../../README.md)-এর পূর্ণ কাঠামোগত বাংলা অনুবাদ। ইংরেজি সংস্করণই canonical উৎস, তবে এই ফাইল একই প্রধান অংশগুলো কভার করে।

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## এই প্রকল্প কেন আছে

এই রিপোজিটরি ব্যবহার করুন যদি আপনার কাছে আগে থেকেই থাকে:

- একটি স্থিতিশীল FreeIPA পরিবেশ
- একটি Proxmox VE ক্লাস্টার
- এমন Linux guest যাদের central authentication দরকার
- Proxmox LDAP bind-এর জন্য dedicated service account
- admin এবং operator-এর জন্য পরিষ্কার group model

মূল ধারণা হলো FreeIPA-কে identity ও access-এর source of truth হিসেবে ব্যবহার করা। Proxmox এটিকে LDAP realm হিসেবে ব্যবহার করে, Linux guest `ipaclient` role দিয়ে FreeIPA-তে join করে, এবং SSH, HBAC, `sudo` নীতিগুলো কেন্দ্রীভূত থাকে।

## আপনি কী পাবেন

- FreeIPA user group, hostgroup, HBAC rule এবং `sudo` rule management
- FreeIPA-এর সাথে Proxmox LDAP realm configuration
- নির্দিষ্ট cluster node থেকে periodic realm sync
- synced group-এর জন্য Proxmox RBAC binding
- static inventory, manual host definition বা Proxmox discovery থেকে Linux enrollment
- QEMU Guest Agent-এর মাধ্যমে optional no-reboot SSH bootstrap
- reachable guest-এর জন্য optional SSH/WinRM guest-agent install
- first-touch-এর জন্য optional SSH public-key bootstrap
- FreeIPA access model পরিবর্তনের পর automatic SSSD refresh
- `post-start` ও `post-migrate`-এর জন্য optional event-driven onboarding

## পরিধি

| অন্তর্ভুক্ত | অন্তর্ভুক্ত নয় |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| synced group থেকে Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | সব Proxmox multi-tenant edge case |

## আর্কিটেকচার

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## প্রয়োজনীয়তা

### Controller

- Ansible Core 2.14+
- Proxmox primary node, IPA server এবং Linux client-এ SSH reachability
- প্রয়োজনমতো `sudo` বা `root`
- QGA SSH bootstrap চালু থাকলে guest-এর ভেতরে QEMU Guest Agent আগে থেকেই চালু থাকতে হবে
- Windows fallback চালু থাকলে host-গুলো `windows_qemu_guest_agent_clients`-এ থাকতে হবে
- Linux SSH bootstrap চালু থাকলে controller-এ SSH keypair এবং initial password path দরকার

### Targets

- `proxmox_primary`-এ Proxmox VE 6.x বা নতুন
- Proxmox ও Linux client থেকে reachable FreeIPA
- সঠিক DNS এবং time sync
- `proxmox_primary`-এর জন্য `root` বা `pveversion`, `pvesh`, `pveum` চালাতে পারে এমন sudo-capable user
- Proxmox discovery-এর জন্য QEMU Guest Agent থেকে usable IP

## নেটওয়ার্ক পোর্ট

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` এবং `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, ডিফল্ট `443/TCP`
- `636/TCP` for `ldaps`

## সামঞ্জস্যতা

- Proxmox VE 6.x এবং পরবর্তী সংস্করণের জন্য
- default supported major: `6`, `7`, `8`, `9`, `10`
- `proxmox_supported_major_versions` দিয়ে override করা যায়
- `proxmox_allow_future_major_versions` ডিফল্ট `true`

## দ্রুত শুরু

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

আপনার পরিবেশ অনুযায়ী `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, `vault-proxmox.yml` সম্পাদনা করুন।

## Rollout ক্রম

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

ডিফল্ট rollout ইচ্ছাকৃতভাবে conservative: FreeIPA এবং Proxmox-এর জন্য `serial: 1`, Linux-এর জন্য `serial: 10`, এবং `max_fail_percentage: 0`.

## Tag মডেল

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

আপনি যদি চান Proxmox `post-start` বা `post-migrate`-এর পরে সাথে সাথে Linux discovery ও IPA enrollment trigger করুক, তাহলে [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md)-এ বর্ণিত optional hook/webhook workflow ব্যবহার করুন। এই পথ `playbooks/proxmox-vm-event.yml` ব্যবহার করে, প্রতিটি event-এ LDAP realm বা RBAC পুনরায় চালায় না, এবং নতুন VM-কে প্রথম `post-start`-এ ধরতে পারে।

## Inventory মডেল

মূল গ্রুপগুলো:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only বা Proxmox discovery ব্যবহার করলেও guest-এর final FQDN দরকার, `ipa_hostname` বা `hostname -f` দিয়ে।

### Linux source mode

1. static inventory host
2. `linux_ipa_client_hosts`-এ manual definition
3. `linux_ipa_proxmox_discovery_*` দিয়ে Proxmox discovery

গুরুত্বপূর্ণ নোট: discovery QEMU Guest Agent network data-র উপর নির্ভরশীল, `linux_ipa_proxmox_discovery_vmids` event path-এ উপকারী, short hostname-এর জন্য `linux_ipa_identity_hostname_suffix` ব্যবহার করা যায়, authoritative DNS repair-এর জন্য `linux_freeipa_enroll_manage_authoritative_dns: true` ব্যবহার করা যায়, আর DNS প্রস্তুত না থাকলে `/etc/hosts` bootstrap পাওয়া যায়।

## Configuration surface

মূল ফাইল:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## উদাহরণ group strategy

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## নিরাপত্তা

- secret শুধু vault file-এ রাখুন
- Proxmox-এর জন্য dedicated read-only LDAP bind account ব্যবহার করুন
- certificate verification সহ TLS পছন্দ করুন
- disposable lab ছাড়া SSH host key checking বন্ধ করবেন না

## Idempotency এবং caveat

এই প্রকল্প repeatable run-এর জন্য লেখা, কিন্তু production-এর আগে lab validation প্রয়োজন। পরিচিত সীমাবদ্ধতার মধ্যে আছে Proxmox CLI output পার্থক্য, LDAP filter tuning, discovery-র QGA ও running guest-এর উপর নির্ভরতা, এবং IP-based target-এর জন্য valid final hostname-এর প্রয়োজন।

## যাচাই

- FreeIPA-তে group, hostgroup, HBAC ও `sudo` verify করুন
- Proxmox-এ LDAP realm, sync ও ACL binding verify করুন
- Linux guest-এ allowed login, denied HBAC case, `sudo -l`, এবং home creation পরীক্ষা করুন

## রিপোজিটরি বিন্যাস

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## উন্নয়ন

রিপোজিটরিতে `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflow, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, এবং `scripts/vault.*` আছে।

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## পরবর্তী সম্প্রসারণ

- IPA-ready Linux template-এর জন্য Packer pipeline
- AWX job template ও schedule
- আলাদা Proxmox tenant ও pool model
- RDP-কেন্দ্রিক পরিবেশের জন্য Windows বা AD-trust flow

## লাইসেন্স

এই প্রকল্প [MIT License](../../LICENSE)-এর অধীনে প্রকাশিত।
