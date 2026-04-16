# Proxmox + FreeIPA অ্যাক্সেস অটোমেশন

এই পৃষ্ঠাটি [README.md](../../README.md)-এর পূর্ণ, কাঠামোগতভাবে সমতুল্য বাংলা অনুবাদ। ইংরেজি সংস্করণই canonical source, তবে এই বাংলা সংস্করণও একই operational scope কভার করার জন্য লেখা।

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## ভাষাসমূহ

পূর্ণ ডকুমেন্টেশনের canonical source হলো ইংরেজি README। আরও ২০টি অতিরিক্ত ভাষায় পূর্ণ translated README উপলভ্য আছে।

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

এই repository **FreeIPA-কে identity এবং access-এর source of truth** হিসেবে বিবেচনা করে। Proxmox সেই directory-কে LDAP realm-এর মাধ্যমে consume করে, Linux guest upstream `ipaclient` role-এর মাধ্যমে FreeIPA-তে join করে, এবং synced group, HBAC, ও sudo rule-এর মাধ্যমে access centrally managed থাকে, local account sprawl-এর বদলে।

> [!IMPORTANT]
> এই প্রকল্প **FreeRADIUS-কে identity source হিসেবে ব্যবহার করে না**, **প্রতিটি VM-এর ভেতরে local user তৈরি করে না**, এবং **Proxmox permission-এর সব edge case manage করার চেষ্টা করে না**।

## এই প্রকল্প কেন আছে

এই রিপোজিটরি ব্যবহার করুন যদি আপনার কাছে আগে থেকেই থাকে:

- একটি সুস্থ FreeIPA deployment
- একটি Proxmox VE cluster
- এমন Linux guest যাদের centralized authentication দরকার
- Proxmox LDAP bind-এর জন্য একটি dedicated service account
- admin এবং operator-এর জন্য একটি পরিষ্কার group model

মূল নীতি হলো identity এবং access-এর source of truth হিসেবে FreeIPA-কে ব্যবহার করা। Proxmox সেই directory-কে LDAP realm হিসেবে consume করে, Linux guest upstream `ipaclient` role-এর মাধ্যমে FreeIPA-তে join করে, এবং SSH, HBAC, ও `sudo` নিয়ন্ত্রণ প্রতিটি VM-এর local account-এ ছড়িয়ে না গিয়ে centrally managed থাকে।

আপনি যদি onboarding এবং offboarding-কে মূলত নিচের ধাপে চালাতে চান, তাহলে এই repository একটি ভাল fit:

1. FreeIPA-তে user এবং group create বা update করা
2. সেই identity-গুলোকে Proxmox-এ sync করা
3. synced group থেকে Proxmox role এবং ACL apply করা
4. FreeIPA login, HBAC, এবং sudo rule-এর মাধ্যমে Linux guest access দেওয়া

## আপনি কী পাবেন

- FreeIPA user group, hostgroup, HBAC rule, এবং `sudo` rule-এর ব্যবস্থাপনা
- Linux administrator-দের জন্য FreeIPA default login shell ব্যবস্থাপনা
- FreeIPA-র দিকে point করা Proxmox LDAP realm configuration
- নির্দিষ্ট একটি cluster node থেকে periodic Proxmox realm sync
- synced directory group-এর জন্য Proxmox RBAC binding
- static inventory, IP-based target, অথবা Proxmox VM discovery-এর মাধ্যমে Linux guest-এর FreeIPA enrollment
- Proxmox QEMU Guest Agent-এর মাধ্যমে reboot ছাড়া optional SSH bootstrap
- Proxmox-managed Linux guest-এর জন্য Proxmox side-এ guest agent communication channel enable করার optional ক্ষমতা
- এমন guest-এ SSH বা WinRM-এর মাধ্যমে optional QEMU Guest Agent install যেগুলো ইতিমধ্যে reachable, bootstrap-এর পরে reachable, অথবা Linux enrollment-এর পরে আবার retry করা যাবে
- SSH reachability এবং Proxmox QEMU Guest Agent status দেখার জন্য optional Linux readiness report
- Active Directory-নির্ভর Windows 10/11 এবং Windows Server domain membership-এর জন্য আলাদা optional workflow
- IPA CA trust, hosts file bootstrap, এবং IPA service reachability validation-এ সীমিত FreeIPA-aware Windows helper workflow
- Linux guest-এর জন্য first-touch SSH public-key bootstrap
- FreeIPA access model পরিবর্তনের পরে managed Linux client-এ automatic SSSD cache refresh
- Proxmox VM hook এবং webhook trigger-এর মাধ্যমে optional event-driven Linux onboarding

## পরিধি

| অন্তর্ভুক্ত | অন্তর্ভুক্ত নয় |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm configuration | FreeIPA user lifecycle-এর পূর্ণ সৃষ্টি |
| synced group থেকে Proxmox RBAC | Proxmox multi-tenant edge case-এর পূর্ণ কভারেজ |
| Linux client IPA enrollment | FreeIPA-র বিরুদ্ধে Windows native login |
| Windows-এর জন্য AD domain membership workflow | AD object বা GPO-এর বিস্তৃত automation |
| Windows-এর জন্য সীমিত FreeIPA helper workflow | FreeIPA-ভিত্তিক Windows helper-কে AD-এর সমতুল্য ধরা |

## উইন্ডোজ কর্মপ্রবাহ

Windows support-কে Linux IPA enrollment flow-এর সাথে মেশানো হয়নি। এটি আলাদা workflow হিসেবে বাস্তবায়িত।

- `windows_qemu_guest_agent_clients` শুধুমাত্র optional QEMU Guest Agent helper task-এর জন্য সংরক্ষিত।
- `10-features.yml`-এ `windows_domain_membership_enabled: true` সেট করলে Windows workflow সক্রিয় হয়।
- `windows_management_clients` একটি আলাদা Windows group, যা `playbooks/windows-management.yml` এবং `playbooks/site.yml`-এর optional Windows পর্যায় ব্যবহার করে।
- বাস্তব Windows login Active Directory domain membership-এর মাধ্যমে পরিচালিত হয়। FreeIPA-কেন্দ্রিক environment-এ Windows host-কে সরাসরি FreeIPA-তে join করানোর বদলে FreeIPA-AD trust-এর AD side-এ join করাই সঠিক পথ।

শুধুমাত্র FreeIPA-ভিত্তিক Windows join এই repository সমর্থন করে না। Active Directory বা FreeIPA-AD trust না থাকলে Windows side-এর scope কেবল helper task-এ সীমাবদ্ধ থাকে, যেমন already reachable guest management এবং optional QEMU Guest Agent installation।

তারপরও যদি domain join ছাড়া একটি সীমিত FreeIPA-aware Windows path দরকার হয়, তাহলে `windows_freeipa_helpers_enabled: true` সক্রিয় করুন এবং `playbooks/windows-freeipa-helpers.yml`-এর সাথে `windows_freeipa_helper_clients` ব্যবহার করুন। এই helper workflow IPA CA trust install করতে পারে, bootstrap-এর জন্য IPA CA স্বয়ংক্রিয়ভাবে fetch করতে পারে, expected CA thumbprint optionally pin করতে পারে, hosts file entries optionally manage করতে পারে, IPA DNS এবং গুরুত্বপূর্ণ TCP port validate করতে পারে, Windows থেকে HTTPS reachability validate করতে পারে, IPA-সংশ্লিষ্ট endpoint-এর বিরুদ্ধে Windows time source validate করতে পারে, Windows local group membership manage করতে পারে, এবং OpenSSH Server optionally install বা expose করতে পারে, কিন্তু এটি FreeIPA-র বিরুদ্ধে Windows native login দেয় না।

যদি আপনি একই helper group-এ কোনো পরিবর্তন না করে শুধু readiness check চালাতে চান, তাহলে `playbooks/windows-freeipa-validate.yml` চালান। এই workflow validation এবং summary path বজায় রাখে, কিন্তু সেই run-এর জন্য CA import, hosts file change, local group change, এবং OpenSSH management-কে non-mutating করে দেয়।

এই workflow WinRM বা PSRP-এর মাধ্যমে reachable Windows 10/11 এবং Windows Server guest-কে target করে।

## আর্কিটেকচার

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

আরও দীর্ঘ design explanation [docs/ARCHITECTURE.md](../ARCHITECTURE.md)-এ আছে।

## প্রয়োজনীয়তা

### নিয়ন্ত্রণ যন্ত্র

- Ansible Core 2.14 বা নতুন
- Proxmox primary node, IPA server, এবং Linux client-এ SSH reachability
- আপনি যদি Windows workflow ব্যবহার করেন, তাহলে Windows guest-এ WinRM বা PSRP reachability
- প্রয়োজনমতো `sudo` বা `root`
- QGA SSH bootstrap enabled থাকলে guest-এর ভেতরে QEMU Guest Agent আগে থেকেই চলমান থাকতে হবে
- Windows-এর জন্য guest-agent installation fallback enabled থাকলে reachable Windows host-গুলো `windows_qemu_guest_agent_clients`-এ থাকতে হবে
- Windows domain membership enabled থাকলে reachable Windows host-গুলো `windows_management_clients`-এ থাকতে হবে এবং AD join credentials দিতে হবে
- Windows-এর জন্য FreeIPA helper task enabled থাকলে reachable Windows host-গুলো `windows_freeipa_helper_clients`-এ থাকতে হবে
- Linux SSH bootstrap enabled থাকলে controller-এর কাছে SSH keypair এবং guest account-এর জন্য initial password-based login path থাকতে হবে

### লক্ষ্যসমূহ

- `proxmox_primary`-এ Proxmox VE 6.x বা তার নতুন সংস্করণ
- Proxmox এবং Linux client থেকে reachable FreeIPA
- Windows 10/11 এবং Windows Server guest আলাদা Windows workflow দিয়ে manage করা যাবে যদি তারা WinRM বা PSRP-এর মাধ্যমে reachable হয়
- সঠিক DNS এবং time synchronization
- `proxmox_primary`-এর জন্য `root` বা এমন SSH user যার `pveversion`, `pvesh`, এবং `pveum` চালানোর মতো `sudo` আছে
- আপনি যদি Windows domain membership ব্যবহার করেন, তাহলে target Windows guest-গুলোকে সংশ্লিষ্ট AD domain controller-এ পৌঁছাতে হবে
- আপনি যদি Windows-এর জন্য সীমিত FreeIPA helper workflow ব্যবহার করেন, তাহলে target Windows guest-গুলোকে সংশ্লিষ্ট IPA server-এ পৌঁছাতে হবে
- আপনি যদি Proxmox discovery ব্যবহার করেন, তাহলে guest-গুলোকে QEMU Guest Agent-এর মাধ্যমে usable IP প্রকাশ করতে হবে

## নেটওয়ার্ক পোর্ট

এই টেবিলটি সেই network port-গুলো তালিকাভুক্ত করে যেগুলো এই repository-এর controller, Proxmox LDAP automation, এবং Linux IPA enrollment flow ব্যবহার করে।
এটি ইচ্ছাকৃতভাবে শুধু সেই surface-এ সীমিত যেটি এই প্রকল্প বাস্তবে ব্যবহার করে; এটি FreeIPA server-to-server replication matrix-এর পূর্ণ তালিকা নয়।

| নাম | পোর্ট | প্রোটোকল | উৎস | গন্তব্য | কখন প্রয়োজন | উদ্দেশ্য |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | সবসময় | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | Windows management enabled থাকলে | Windows guest-এ Ansible connectivity |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS server | Linux guest IPA DNS ব্যবহার করলে | IPA record এবং external name resolve করা |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment এবং login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA server | Linux IPA enrollment এবং login | LDAP এবং FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port`, default `443` | `TCP` | Linux guest | IPA server | Linux IPA enrollment | client installation-এর সময় IPA web/API verification |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment এবং password operations | Kerberos password ও keytab operations |
| LDAPS | `636` | `TCP` | Primary Proxmox node | IPA বা LDAP server | Proxmox LDAP realm default `ldaps` mode ব্যবহার করলে | Proxmox LDAP realm connection |

নোট:

- `LDAPS 636/TCP` repository default কারণ `proxmox_ldap_mode`-এর default হলো `ldaps`। আপনি যদি LDAP mode বা port বদলান, তাহলে আপনি বাস্তবে যে `proxmox_ldap_port` ব্যবহার করেন সেটিই allow করুন।
- `WinRM` সাধারণত HTTPS-এর জন্য `5986/TCP` বা HTTP-এর জন্য `5985/TCP` ব্যবহার করে; এটি Windows transport configuration-এর উপর নির্ভর করে।
- `DNS 53/TCP,UDP` কেবল তখনই দরকার যখন Linux guest-গুলো IPA server-কে resolver হিসেবে ব্যবহার করে।
- `Kerberos 88` এবং `Kerberos Password 464`—দুটোরই `TCP` এবং `UDP` উভয়ই লাগে।
- Active Directory domain join-এর জন্য standard Windows-to-domain-controller port-ও লাগে, কিন্তু সেগুলো environment-specific হওয়ায় এখানে বিস্তারিত তালিকাভুক্ত করা হয়নি।
- Kerberos নির্ভরযোগ্যভাবে কাজ করতে time synchronization-ও জরুরি, কিন্তু NTP source environment-specific এবং এই repository তা manage করে না।

## সামঞ্জস্যতা

এই repository-এর Proxmox automation `pveum` এবং `pvesh` interface-এর চারপাশে লেখা, যেগুলো Proxmox VE 6.x এবং পরবর্তী version-গুলো realm ও RBAC-এর জন্য ব্যবহার করে।

- default supported majors: `6`, `7`, `8`, `9`, `10`
- validation `pveversion`-এর মাধ্যমে detected Proxmox version যাচাই করে
- supported version list `proxmox_supported_major_versions` দিয়ে আপনার environment অনুযায়ী সংকুচিত বা প্রসারিত করা যায়
- `proxmox_allow_future_major_versions`-এর default `true`, তাই highest tested version-এর ওপরে থাকা future major version-গুলোও default অবস্থায় validation পার হয়ে যায়
- future major version-গুলোকে compatibility candidate হিসেবেই দেখা উচিত যতক্ষণ না তাদের published Proxmox interface এই automation-এর সাথে বাস্তবে যাচাই করা হয়
- `1` থেকে `5`-এর মতো পুরনো version-গুলোকে এই public repository tested support হিসেবে দাবি করে না; আপনি যদি এগুলো locally যোগ করেন, তাহলে একে explicit compatibility override হিসেবে ধরুন এবং আগে lab-এ full workflow validate করুন

legacy lab-এর জন্য local override উদাহরণ:

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

## দ্রুত শুরু

নিচের উদাহরণগুলো shell command ব্যবহার করে। যেখানে প্রযোজ্য সেখানে PowerShell equivalent-ও দেওয়া আছে।

### 1. উদাহরণ ইনভেন্টরি এবং ভল্ট টেমপ্লেট কপি করুন

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

### 2. পরিবেশ-নির্দিষ্ট ফাইল সম্পাদনা করুন

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- আপনি যদি Windows management ব্যবহার করেন, তাহলে `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- আপনি যদি Windows management ব্যবহার করেন, তাহলে `inventories/production/group_vars/all/vault-windows.yml`

IPA এবং Proxmox settings-এর পাশাপাশি Linux guest-এর জন্য একটি source mode বেছে নিন:

- `linux_ipa_clients`-এর অধীনে static inventory entry
- `group_vars/all/30-linux-clients.yml`-এ `linux_ipa_client_hosts` entry
- `linux_ipa_proxmox_discovery_enabled: true` সহ Proxmox VM discovery

Linux IPA enrollment-এর ক্ষেত্রে domain value এবং server list আলাদা করে বুঝুন:

- `ipaclient_domain` হলো shared IPA DNS domain, যেমন `example.com`
- `linux_ipa_servers` হলো IPA server hostname-এর তালিকা, যেমন `ipa01.example.com`

আপনি যদি `root`-এর পরিবর্তে এমন সাধারণ user দিয়ে Proxmox-এ SSH করতে চান যার `sudo` আছে, তাহলে সেটি `hosts.yml`-এর `proxmox_primary`-এ configure করুন এবং sudo password-টি `vault-proxmox.yml`-এ রাখুন:

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

এই configuration-এ `vault_proxmox_become_password` বলতে সেই password-কে বোঝায় যেটি আপনি সাধারণত Proxmox host-এ `sudo` চালানোর সময় টাইপ করেন।

### 3. ভল্ট ফাইল এনক্রিপ্ট করুন

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

আপনি যদি Windows workflow enable করেন, তাহলে একই command-এ `inventories/production/group_vars/all/vault-windows.yml`-ও যোগ করুন।

অথবা helper wrapper ব্যবহার করুন, যা default অবস্থায় domain-separated vault ID ব্যবহার করে এবং প্রয়োজন হলে example template থেকে working vault file তৈরি করে:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

আপনি যদি playbook run-এর জন্য আলাদা domain-specific password চান, তাহলে `--ask-vault-pass`-এর বদলে vault ID ব্যবহার করুন:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

যদি optional Windows workflow-ও আলাদা vault password ব্যবহার করে, তাহলে একই command-এ `windows@prompt` যোগ করুন।

`-AskVaultPass` কেবল তখনই ব্যবহার করুন যখন সংশ্লিষ্ট playbook-এর সব vault file একই password share করে।

### 4. প্রয়োজনীয় কালেকশন ইনস্টল করুন

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

অথবা সরাসরি:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

এই repository compatibility patch যোগ করার আগে যদি আপনি `freeipa.ansible_freeipa` install করে থাকেন, তাহলে bootstrap helper আবার চালান বা `python .\scripts\patch_freeipa_collection.py` একবার চালিয়ে user-level collection installation-ও patch করুন।

যখন আপনি `scripts/run-playbook.ps1` ব্যবহার করেন, এটি `ansible-playbook` চালানোর আগে ওই patch helper স্বয়ংক্রিয়ভাবে চালায়।

### 5. প্রথমে যাচাই চালান

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

আপনি যদি কোনো পরিবর্তন না করে শুধু Windows FreeIPA helper-only path validate করতে চান:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

যদি আপনি read-only Linux readiness audit চান যা বলে কোন runtime guest SSH-এ reachable এবং কোন Proxmox-discovered guest QEMU Guest Agent-এর মাধ্যমে respond করছে:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

readiness report defaultভাবে `.ansible/linux-readiness-report.json`-এ লেখা হয়।
মূল field-গুলোর ব্যাখ্যা:

- `ssh.ready=true`: বর্তমান Ansible SSH path controller থেকে সফল
- `ssh.promptless=true`: `ansible_password` ছাড়া SSH probe সফল হয়েছে, তাই path-টি Ansible-এর জন্য non-interactive
- `ssh.auth_mode=password_configured`: probe `sshpass` ব্যবহার করেছে কারণ host-এ `ansible_password` configured আছে
- `ssh.auth_mode=key_or_agent`: probe `ansible_password` ছাড়া SSH batch mode-এ সফল হয়েছে
- `qga.status=available`: VM-এর owner Proxmox node-এ `qm guest ping` সফল হয়েছে
- `qga.status=disabled`: Proxmox VM configuration-এ QEMU Guest Agent enabled নয়
- `qga.status=configured_unresponsive`: guest agent Proxmox configuration-এ enabled আছে কিন্তু respond করছে না
- `qga.status=node_unreachable`: controller সংশ্লিষ্ট Proxmox node-এ পৌঁছাতে পারেনি, তাই probe করা যায়নি
- `qga.status=not_applicable`: host Proxmox discovery থেকে তৈরি নয়, তাই QGA probe চেষ্টা করা হয়নি

দ্রুত inspection উদাহরণ:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. ঐচ্ছিক: পরিকল্পিত পরিবর্তনের পূর্বরূপ দেখুন

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> check mode-কে পূর্ণ simulation নয়, বরং partial preview হিসেবে দেখুন। এই repository কিছু Proxmox configuration-এর জন্য direct CLI command ব্যবহার করে এবং Linux enrollment-এর জন্য upstream FreeIPA client role ব্যবহার করে, তাই `--check` উপকারী হলেও এটি চূড়ান্ত সত্য নয়।
>
> FreeIPA HBAC rule-এর ক্ষেত্রে check mode rule definition step validate করে, কিন্তু পরে enable বা disable action skip করে। এর ফলে dry run-এ বাস্তবে তৈরি না হওয়া rule-কে FreeIPA missing বলে false failure তৈরি করতে পারে না।
>
> Proxmox realm sync timer role-ও check mode-এ শেষের `systemd` enable বা start step skip করে, কারণ unit file diff-এ দেখা গেলেও dry run-এর সময় আসলে লেখা হয় না।
>
> Linux IPA enrollment-ও check mode-এ skip হয়। repository discovery, hostname resolution, এবং input validation চালিয়ে যায়, কিন্তু upstream `ipaclient` role dry run-এর সময় execute হয় না।

### 7. পূর্ণ কনফিগারেশন প্রয়োগ করুন

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

যদি optional Windows workflow enabled থাকে এবং `vault-windows.yml` আলাদা password ব্যবহার করে, তাহলে একই playbook `--ask-vault-pass`-এর বদলে `--vault-id windows@prompt` বা PowerShell wrapper-এর `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` দিয়ে চালান।

## রোলআউটের ক্রম

প্রথম deployment-এর জন্য stack এই ক্রমে apply করুন:

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

এই ক্রম troubleshooting-কে অনেক সহজ করে, সবকিছু একসাথে চালানোর তুলনায়।

উদাহরণ হিসেবে, শুধুমাত্র একটি Linux guest-এর জন্য সীমিত PowerShell rollout:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

default rollout controls ইচ্ছাকৃতভাবে conservative:

- FreeIPA access changes `serial: 1` দিয়ে চলে
- Proxmox changes `serial: 1` দিয়ে চলে
- hostname resolution, validation, এবং Linux enrollment `serial: 10` দিয়ে চলে
- Windows management changes `serial: 10` দিয়ে চলে
- সব rollout path defaultভাবে `max_fail_percentage: 0` ব্যবহার করে

এই value-গুলো `inventories/production/group_vars/all/15-rollout.yml`-এ adjust করুন।

## ট্যাগ মডেল

অযথা নতুন playbook বাড়ানোর বদলে stable rollout slice target করতে tag ব্যবহার করুন।

- core domain: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helper: `windows`, `windows_freeipa`
- FreeIPA access model: `freeipa_access`
- Proxmox subset: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- event-driven VM handling: `event`, `linux_refresh`

উদাহরণ:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## ইভেন্ট-চালিত VM অনবোর্ডিং

আপনি যদি চান Proxmox কোনো VM start হওয়ার সাথে সাথে বা migration-এর পরে Linux discovery এবং IPA enrollment trigger করুক, তাহলে [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md)-এ বর্ণিত optional hook এবং webhook path ব্যবহার করুন।

এই path event-specific playbook `playbooks/proxmox-vm-event.yml` ব্যবহার করে, তাই trigger শুধুমাত্র Linux guest side এবং FreeIPA side handle করে। এটি প্রতিটি VM event-এ Proxmox LDAP realm automation বা RBAC আবার চালায় না।

এখন এই repository optional hook এবং webhook stack-টিও `site.yml` বা `proxmox.yml`-এর মাধ্যমে install করতে পারে, যদি `proxmox_vm_event_onboarding_enabled: true` সেট করা থাকে এবং প্রয়োজনীয় webhook variable-গুলো উপলব্ধ থাকে।

Proxmox VM hook কোনো আলাদা `create` phase দেয় না। বাস্তবে, নতুন VM সাধারণত প্রথম `post-start` event-এ ধরা পড়ে, আর migration hook source node এবং destination node—দুই জায়গাতেই trigger হতে পারে।

## ইনভেন্টরি মডেল

এই repository ছয়টি defined inventory group এবং একটি runtime-generated group ব্যবহার করে:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

আপনি চাইলে নিজের অতিরিক্ত inventory group-ও define করতে পারেন এবং FreeIPA hostgroup definition-এ reference করতে পারেন। যদি FreeIPA hostgroup side থেকে পুরো prepared Linux guest set ব্যবহার করতে চান, তাহলে `linux_ipa_clients_runtime` group reference করুন।

> [!IMPORTANT]
> FreeIPA প্রতিটি guest-এর জন্য final hostname চায়। আপনি যদি IP-only target বা Proxmox discovery ব্যবহার করেন, তাহলে `ipa_hostname` explicitভাবে দিন অথবা নিশ্চিত করুন যে guest-এর ভেতরের `hostname -f` final FQDN return করে। playbook FreeIPA hostgroup membership assemble করার আগেই hostname resolve করে।

> [!TIP]
> reusable golden template-কে সরাসরি FreeIPA-তে enroll করবেন না। আগে VM clone করুন, final hostname দিন, তারপর resulting guest enroll করুন।

### লিনাক্স গেস্ট উৎস মোড

আপনি `linux_ipa_clients` তিনটি আলাদা পদ্ধতিতে populate করতে পারেন।

#### 1. static inventory hosts

যদি আপনি আগেই guest names জানেন, তাহলে সাধারণ Ansible inventory entry ব্যবহার করুন:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. variable-এ manual host definition

যদি guest-গুলোকে `hosts.yml`-এর বাইরে রাখতে চান, অথবা আপনার কাছে শুধু IP থাকে, তাহলে `linux_ipa_client_hosts` ব্যবহার করুন:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

নোট:

- যদি `name` ইতিমধ্যেই resolvable hostname বা FQDN হয়, তাহলে `ansible_host` optional
- যদি আপনি শুধু IP জানেন, তাহলে `name`-এর জন্য যেকোনো স্থিতিশীল alias ব্যবহার করুন
- `ipa_hostname` না দিলে playbook guest-এর ভেতরের `hostname -f`-এ fallback করবে

#### 3. Proxmox VM auto-discovery

যদি আপনি এক বা একাধিক Proxmox node থেকে Linux guest pull করতে চান, তাহলে discovery ব্যবহার করুন:

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

নোট:

- discovery VMs-কে একই `linux_ipa_clients_runtime` group-এ যোগ করে, যেটি অন্য playbook-ও ব্যবহার করে
- IP discovery এমন QEMU guest agent-এর উপর নির্ভরশীল যেটি network interface report করতে পারে
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` কেবল সেই VM name-এ বিশ্বাস করে যেগুলো আগেই FQDN
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` সেট করলে `Teleport-Server-1`-এর মতো নিরাপদ short VM name-কে `linux_ipa_identity_hostname_suffix` ব্যবহার করে `teleport-server-1.example.com`-এর মতো hostname hint-এ promote করা যায়
- `linux_ipa_proxmox_discovery_vmids` optional, এবং মূলত event-driven hook বা webhook workflow-এ discovery-কে নির্দিষ্ট VMID-এ সীমাবদ্ধ করতে উপকারী
- guest-গুলোর এখনও final hostname দরকার, যা হয় VM-এর ভেতরে configured থাকবে অথবা manual definition-এ `ipa_hostname` হিসেবে দেওয়া হবে
- guest-এর বাস্তব system hostname-ও enrollment-এর জন্য valid হতে হবে; `localhost.localdomain`-এর মতো placeholder value-গুলো `linux-clients` বা `site` চালানোর আগে VM-এর ভেতরে বদলাতে হবে
- guest যদি `app-server-01`-এর মতো short hostname ব্যবহার করে, তাহলে `linux_ipa_identity_hostname_suffix` এবং প্রয়োজনে `linux_freeipa_enroll_manage_hostname: true` সেট করে project-কে enrollment-এর আগে `app-server-01.example.net`-এর মতো full hostname resolve ও apply করতে দিতে পারেন
- যদি FreeIPA DNS আপনার guest hostname-এর জন্য authoritative হয়, তাহলে `linux_freeipa_enroll_manage_authoritative_dns: true` সেট করে project-কে সম্পর্কিত A এবং PTR record repair করতে এবং enrollment-এর আগে link-local `fe80::/10` AAAA record মুছে ফেলতে দিতে পারেন
- DNS যদি এখনও ready না হয়, তাহলে `linux_ipa_manage_etc_hosts: true` এবং `linux_ipa_etc_hosts_entries` সেট করে role-কে IPA server এবং guest FQDN-এর জন্য managed `/etc/hosts` bootstrap block যোগ করতে দিতে পারেন
- `guest_qemu_agent_install_enabled` SSH বা WinRM-এ আগে থেকেই reachable guest-এ QEMU Guest Agent install করে, একই workflow-এ পরে reachable হওয়া Linux guest-এ retry করে, এবং Linux enrollment-এর পরে আবার retry করে যাতে agent-dependent Proxmox workflow সেগুলো ব্যবহার করতে পারে
- `linux_ipa_proxmox_discovery_allowlist_enabled: true` সেট করলে discovery চালু থাকলেও কেবল explicitly approved Proxmox guest-ই Linux runtime inventory-তে admit হবে; allowlist VMID, IP, এবং name-এ exact matching করতে পারে
- `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, বা `linux_ipa_proxmox_discovery_blacklist_names` সেট করুন যদি discovery-enabled node-এ firewall, DNS server, বা অন্য infrastructure VM থাকে যেগুলোকে Linux IPA automation থেকে সবসময় বাদ রাখতে হবে; blacklist matching broad discovery এবং allowlist admission—দুটোর উপর precedence নেয়
- যে Proxmox-discovered Linux guest-এ এখনও functional guest agent নেই, তাদের জন্য `linux_ipa_proxmox_discovery_ansible_user` এবং সাথে `linux_ipa_proxmox_discovery_ansible_password` বা `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` সেট করুন, যাতে repository QEMU Guest Agent install করার usable first-touch SSH path পায়
- যদি সেই discovered guest non-root SSH user ব্যবহার করে, তাহলে `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, এবং `linux_ipa_proxmox_discovery_ansible_become_password`-ও সেট করুন, যদি না ওই account-এর কাছে আগেই passwordless `sudo` থাকে
- `guest_qemu_agent_install_manage_proxmox_vm_agent` guest-এর ভেতরের installation path শুরু হওয়ার আগে Proxmox side-এ guest agent communication (`qm set <vmid> --agent 1`) enable করে
- যখন একই Proxmox VM option running VM-এ পরিবর্তন করা হয়, repository defaultভাবে শুধু warning দেয়, কারণ guest agent channel usable হওয়ার আগে Proxmox VM restart চাইতে পারে; যদি আপনি চান repository এই running VM-গুলো automatically reboot করুক, তাহলে `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` সেট করুন
- `linux_ipa_ssh_host_key_policy` defaultভাবে Linux guest connection-এর জন্য `accept_new` ব্যবহার করে, যাতে newly discovered VM-এ host key checking পুরোপুরি disable না করেও পৌঁছানো যায়; পরিবর্তিত host key তবুও fail করবে এবং operator review লাগবে
- `linux_ipa_qga_ssh_bootstrap_enabled` হলো Proxmox-based guest-এর জন্য preferred no-reboot bootstrap path, কারণ এটি সাধারণ SSH login-এর আগে QEMU Guest Agent ব্যবহার করে dedicated key-only automation user তৈরি করতে পারে
- `linux_ipa_qga_ssh_bootstrap_qm_path`-এর default `qm`, এবং bootstrap flow fail হওয়ার আগে Proxmox node-এর common fallback path-ও পরীক্ষা করে
- যে guest `guest-ping` allow করে কিন্তু `guest-exec` block করে, সেগুলো defaultভাবে QGA bootstrap চলাকালে skip হয়; এদের জন্য অন্য SSH path দিন অথবা `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` সেট করে run-টিকে সঙ্গে সঙ্গে fail করতে দিন
- `linux_ipa_ssh_bootstrap_enabled` hostname resolution এবং enrollment-এর আগে controller-এর public key Linux guest-এ optionally install করে; `linux_ipa_ssh_bootstrap_password` shared first-touch password fallback হিসেবেও ব্যবহার হয়, এমনকি key-based bootstrap disabled থাকলেও
- Linux IPA enrollment FreeIPA JSON-RPC timeout-এর কারণে fail হওয়া upstream client join-গুলো retry করে, এবং ধীর বা ব্যস্ত IPA environment-এর জন্য `linux_ipaclient_kinit_attempts` expose করে
- Linux IPA enrollment defaultভাবে inventory `ipa_servers` hostnames-ও join server list-এ merge করে, যাতে client-রা single endpoint নয়, বরং পুরো IPA server set ব্যবহার করতে পারে
- যখন একাধিক IPA server থাকে, প্রতিটি retry round enrollment-এর সময় সেই candidate IPA server-গুলো ক্রমানুসারে চেষ্টা করে
- combined `site` workflow আগে FreeIPA hostgroup তৈরি করে, তারপর enrolled runtime host যোগ করে, যাতে pre-enrollment run কেবল guest এখনও enrolled নয় বলে hostgroup membership step-এ fail না হয়

## কনফিগারেশন পরিধি

বেশিরভাগ value নিম্নোক্ত স্থানে থাকে:

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

প্রতিটি file অনুযায়ী layout দেখতে [docs/VARIABLES.md](../VARIABLES.md) দেখুন।

মূল variable family:

| ক্ষেত্র | Variables |
| --- | --- |
| FreeIPA access model | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Rollout controls | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Linux readiness reporting | `linux_readiness_report_*` |
| Windows management | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helpers | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Ansible connection secrets | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## গ্রুপ কৌশলের উদাহরণ

একটি সহজ কিন্তু ভালোভাবে scale হওয়া pattern:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa`-এর জন্য Proxmox ACL binding

যদি আপনি চান combined `site.yml` run কিছু IPA user-কে automatically Linux SSH এবং sudo access দিক, তাহলে [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml)-এ `freeipa_linux_admin_users` পূরণ করুন, যাতে managed `linux-ssh-admins` group-এর মাধ্যমে access দেওয়া যায়।

মনে রাখবেন Proxmox LDAP sync suffix-সহ group তৈরি করে:

```text
<group-name>-<realm>
```

যদি আপনার FreeIPA group `proxmox-admins` হয় এবং Proxmox realm `ipa` হয়, তাহলে resulting synced PVE group হবে:

```text
proxmox-admins-ipa
```

## নিরাপত্তা

- সব secret plaintext inventory variable file-এর বদলে `vault-freeipa.yml` এবং `vault-proxmox.yml`-এ রাখুন
- Proxmox-এর জন্য dedicated read-only LDAP bind account-কে অগ্রাধিকার দিন
- certificate verification enabled রেখে TLS ব্যবহারকে অগ্রাধিকার দিন
- temporary lab ছাড়া SSH host key checking চালু রাখুন
- যদি আপনার Proxmox guest-এ QEMU Guest Agent আগেই functional থাকে, তাহলে shared temporary password-এর তুলনায় `linux_ipa_qga_ssh_bootstrap_enabled`-কে অগ্রাধিকার দিন
- `guest_qemu_agent_install_enabled` কেবল তখন ব্যবহার করুন যখন repository-এর কাছে guest-এর ভিতরে ঢোকার জন্য valid management path থাকে; Proxmox discovery-এর ক্ষেত্রে এর মানে QGA আগে থেকেই চলবে বা `linux_ipa_proxmox_discovery_ansible_user` এবং password বা key access configured থাকতে হবে
- যদি আপনি Linux SSH bootstrap enable করেন, তাহলে shared bootstrap password-কে encrypted variable-এ রাখুন এবং key-based access প্রতিষ্ঠিত হওয়ার পরে এটি rotate বা remove করুন
- IPA admin account-কে Proxmox LDAP bind account হিসেবে reuse করবেন না
- production rollout-এর আগে `proxmox_ldap_filter` এবং `proxmox_ldap_group_filter` review করুন যাতে অত্যধিক object import না হয়

যদি আপনি disposable lab-এ ইচ্ছাকৃতভাবে SSH host key verification disable করতে চান, তাহলে repository default পরিবর্তন না করে shell session level-এ opt-out করুন:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## আইডেমপোটেন্সি এবং সতর্কতা

এই repository পুনরায় চালানোর উপযোগীভাবে লেখা এবং অধিকাংশ ক্ষেত্রে idempotent, কিন্তু production rollout-এর আগে lab-এ validate করা উচিত।

পরিচিত caveat:

- Proxmox CLI output release অনুযায়ী সামান্য ভিন্ন হতে পারে
- FreeIPA directory layout flexible হওয়ায় LDAP filter-কে আপনার tree অনুযায়ী tune করতে হতে পারে
- আগে থেকে manually managed PVE ACL এবং role-গুলো automation প্রয়োগের আগে compare করে নেওয়া উচিত
- Proxmox VM auto-discovery running guest এবং QEMU guest agent network data-র উপর নির্ভরশীল
- IP-based guest definition-এও guest-এর ভিতরে valid final hostname বা explicit `ipa_hostname` দরকার
- Proxmox play privilege escalation-এর সাথে চলে, তাই non-root SSH user-এর working `sudo` থাকতে হবে, এবং যদি account-এর passwordless `sudo` না থাকে তাহলে `-K` দিয়ে become password দিতে হবে
- আপনি যদি `ansible_become_password`-কে `vault-proxmox.yml`-এ রাখেন, তাহলে `-K` বাদ দেওয়া যায় কারণ Ansible encrypted variable থেকেই sudo password পড়বে

## যাচাই

rollout সফল হওয়ার পর final state verify করুন; ধরে নেবেন না যে সব access path নিজে থেকেই ঠিক হয়েছে।

### FreeIPA-তে

- নিশ্চিত করুন expected user group-গুলো আছে
- নিশ্চিত করুন expected hostgroup-গুলো আছে
- নিশ্চিত করুন expected HBAC rule-গুলো আছে এবং enabled
- নিশ্চিত করুন expected `sudo` rule-গুলো আছে এবং enabled

### Proxmox-এ

- নিশ্চিত করুন LDAP realm আছে
- নিশ্চিত করুন initial sync expected user বা group import করেছে
- নিশ্চিত করুন target synced group-এ expected ACL binding আছে

### লিনাক্স গেস্ট-এ

- নিশ্চিত করুন allowed IPA user login করতে পারে
- নিশ্চিত করুন disallowed user-কে HBAC block করে
- নিশ্চিত করুন allowed IPA admin `sudo -l` চালাতে পারে
- যদি `linux_ipaclient_mkhomedir` enabled থাকে, তাহলে প্রথম login-এ home directory তৈরি হয়

## রেপোজিটরি বিন্যাস

<details>
<summary>রিপোজিটরি বিন্যাস দেখান</summary>

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

## উন্নয়ন

এই repository-তে অন্তর্ভুক্ত প্রধান helper file:

- `.editorconfig`, যাতে editor-গুলোর মধ্যে space, encoding, এবং line ending-এর defaults consistent থাকে
- `.gitattributes`, যাতে common text file-এ `LF` line ending enforce করা যায়
- `.gitignore`, যাতে generated inventory, vault data, local collection, এবং editor junk Git-এ ঢুকে না পড়ে
- `.ansible-lint`, যাতে vendor collection path exclude করা যায় এবং শুধু YAML line-length rule suppress করা যায়
- `.yamllint`, যাতে playbook, inventory, এবং workflow জুড়ে YAML validation consistent থাকে
- `.github/CODEOWNERS`, যাতে repository-এর মূল অংশগুলোতে review ownership পরিষ্কার থাকে
- `.github/workflows/ci.yml`, যাতে push এবং pull request event-এ lint ও smoke validation চালানো যায়
- `.pre-commit-config.yaml`, যাতে `pre-commit` install থাকলে commit-এর আগে fast lint hook চালানো যায়
- `CHANGELOG.md`, যাতে গুরুত্বপূর্ণ repository change এক জায়গায় track করা যায়
- `docs/VARIABLES.md`, যাতে split inventory variable structure ব্যাখ্যা করা যায়
- `docs/i18n/`, যেখানে translated README রাখা হয়; এসব file-এ ইংরেজি `README.md`-এর পূর্ণ section structure reflect করা উচিত
- `docs/i18n/TRANSLATION_GUIDE.md`, যাতে translated README sync-এ রাখার পদ্ধতি ব্যাখ্যা করা যায়
- `scripts/bootstrap.ps1` এবং `scripts/bootstrap.sh`, যাতে প্রয়োজনীয় collection local `collections/` path-এ install করা যায় এবং ansible-core 2.24+ compatibility patch apply করা যায়
- `scripts/patch_freeipa_collection.py`, যাতে pinned FreeIPA collection-এর ভিতরের deprecated import rewrite করে ভবিষ্যৎ ansible-core version-এর সঙ্গে compatibility বজায় রাখা যায়
- `scripts/lint.py`, যাতে local, CI, এবং pre-commit-এর জন্য cross-platform lint entry point দেওয়া যায়
- `scripts/smoke-test.py`, যাতে বাস্তব infrastructure ছুঁয়ে না গিয়ে example inventory validation ও syntax check চালানো যায়, যার মধ্যে আলাদা Windows playbook-এর coverage-ও আছে
- `scripts/check_translations.py`, যাতে translated README-এর metadata, section structure parity, এবং canonical English README-এর তুলনায় minimum content coverage যাচাই করা যায়
- `scripts/lint.ps1` এবং `scripts/lint.sh`, যাতে local lint এবং smoke workflow একসাথে চালানো যায়
- `scripts/proxmox_event_webhook.py`, যাতে controller side optional webhook হিসেবে কাজ করা যায় যা Proxmox VM event handle করে
- `scripts/proxmox-vm-hook.pl`, যাতে Proxmox node-এ optional VM hook হিসেবে কাজ করা যায়
- `scripts/run-playbook.ps1`, যাতে Windows ও PowerShell environment-এর জন্য consistent `ansible-playbook` wrapper দেওয়া যায়
- `scripts/vault.ps1` এবং `scripts/vault.sh`, যাতে domain-separated vault file create, edit, view, এবং encrypt করা সহজ হয়
- `tests/` repository-এর verification surface ধরে রাখে, যা smoke-test documentation দিয়ে শুরু হয়
- `CONTRIBUTING.md`, যাতে expected contribution ও validation workflow document করা যায়
- `SECURITY.md`, যাতে vulnerability report করা এবং security-sensitive তথ্য handle করার পদ্ধতি document করা যায়

যদি আপনার controller-এ `ansible-lint` install করা থাকে:

```bash
ansible-lint
```

repository smoke check সরাসরি চালাতে:

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

পূর্ণ local lint pass-এর জন্য:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

প্রতিটি commit-এর আগে fast lint hook enable করতে:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper এখন সাধারণ operator option-ও সরাসরি সমর্থন করে:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## পরবর্তী সম্প্রসারণ

সাধারণত পরবর্তী উপকারী extension:

- IPA-ready Linux template-এর জন্য Packer pipeline
- combined rollout-এর জন্য AWX বা Automation Controller job template এবং scheduling
- আরও শক্তিশালী Proxmox tenant ও pool model
- Windows RDP বা hybrid identity environment-এর জন্য AD trust workflow

## লাইসেন্স

এই repository [MIT License](../../LICENSE)-এর অধীনে প্রকাশিত।
