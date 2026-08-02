# Proxmox + FreeIPA ਐਕਸੈੱਸ ਆਟੋਮੇਸ਼ਨ

ਇਹ ਸਫ਼ਾ [README.md](../../README.md) ਦੀ ਪੂਰੀ ਸੰਰਚਨਾਤਮਕ ਪੰਜਾਬੀ ਰੂਪਾਂਤਰਨ ਵਰਜਨ ਦਿੰਦਾ ਹੈ। ਅੰਗਰੇਜ਼ੀ ਸੰਸਕਰਣ canonical source ਰਹਿੰਦਾ ਹੈ, ਪਰ ਇਹ ਫਾਇਲ ਉਹੀ ਮੁੱਖ ਭਾਗ ਕਵਰ ਕਰਦੀ ਹੈ।

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## ਭਾਸ਼ਾਵਾਂ

ਅੰਗਰੇਜ਼ੀ README ਇਸ ਦਸਤਾਵੇਜ਼ ਦਾ canonical source ਹੈ। ਹੋਰ ਪੂਰੀਆਂ ਅਨੁਵਾਦਿਤ README ਫਾਇਲਾਂ translation index ਵਿੱਚ ਉਪਲਬਧ ਹਨ।

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

## ਇਹ ਪ੍ਰੋਜੈਕਟ ਕਿਉਂ ਹੈ

ਇਸ repository ਨੂੰ ਤਦੋਂ ਵਰਤੋਂ ਜਦੋਂ ਤੁਹਾਡੇ ਕੋਲ ਪਹਿਲਾਂ ਹੀ ਹੋਵੇ:

- ਇੱਕ ਸਿਹਤਮੰਦ FreeIPA deployment
- ਇੱਕ Proxmox VE cluster
- ਅਜੇਹੇ Linux guest ਜਿਨ੍ਹਾਂ ਨੂੰ central authentication ਚਾਹੀਦੀ ਹੈ
- Proxmox LDAP bind ਲਈ dedicated service account
- admins ਅਤੇ operators ਲਈ ਸਾਫ group model

ਇਹ ਪ੍ਰੋਜੈਕਟ ਉਸ ਵੇਲੇ ਖਾਸ ਤੌਰ ਤੇ ਠੀਕ ਬੈਠਦਾ ਹੈ ਜਦੋਂ ਤੁਸੀਂ onboarding ਅਤੇ offboarding ਨੂੰ ਮੁੱਖ ਤੌਰ ਤੇ ਇਸ ਕ੍ਰਮ ਵਿੱਚ ਚਲਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ:

1. FreeIPA ਵਿੱਚ users ਅਤੇ groups ਬਣਾਉਣਾ ਜਾਂ ਅਪਡੇਟ ਕਰਨਾ
2. ਉਹ identities Proxmox ਵਿੱਚ sync ਕਰਨਾ
3. synced groups ਤੋਂ Proxmox roles ਅਤੇ ACLs ਲਾਗੂ ਕਰਨਾ
4. FreeIPA login, HBAC, ਅਤੇ sudo rules ਰਾਹੀਂ Linux guest access ਦੇਣਾ

## ਤੁਹਾਨੂੰ ਕੀ ਮਿਲਦਾ ਹੈ

- FreeIPA user groups, hostgroups, HBAC rules ਅਤੇ `sudo` rules ਦਾ ਪ੍ਰਬੰਧਨ
- Linux admin users ਲਈ automatic FreeIPA login-shell defaults
- FreeIPA ਦੇ ਖਿਲਾਫ Proxmox LDAP realm configuration
- ਨਿਰਧਾਰਤ cluster node ਤੋਂ periodic realm sync
- synced groups ਲਈ Proxmox RBAC bindings
- static inventory, manual host definitions ਜਾਂ Proxmox discovery ਤੋਂ Linux enrollment
- QEMU Guest Agent ਰਾਹੀਂ optional no-reboot SSH bootstrap
- Proxmox-backed Linux guest ਲਈ optional Proxmox-side guest-agent communication enablement
- ਉਹ guest ਜਿਹੜੇ ਪਹਿਲਾਂ ਹੀ reachable ਹਨ, bootstrap ਤੋਂ ਬਾਅਦ reachable ਹੋ ਜਾਂਦੇ ਹਨ, ਜਾਂ Linux enrollment ਤੋਂ ਬਾਅਦ ਦੁਬਾਰਾ retry ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਉਹਨਾਂ ਲਈ optional SSH ਜਾਂ WinRM fallback QEMU Guest Agent installation
- SSH reachability ਅਤੇ Proxmox QEMU Guest Agent status ਲਈ optional Linux readiness reporting
- Active Directory ਰਾਹੀਂ Windows 10/11 ਅਤੇ Windows Server guest ਲਈ ਵੱਖਰਾ Windows domain-membership workflow
- IPA CA trust, hosts bootstrap, ਅਤੇ IPA reachability checks ਲਈ limited FreeIPA-aware Windows helper workflow
- first-touch ਲਈ optional SSH public-key bootstrap
- FreeIPA access changes ਤੋਂ ਬਾਅਦ automatic SSSD refresh
- `post-start` ਅਤੇ `post-migrate` ਲਈ optional event-driven onboarding

## ਦਾਇਰਾ

| ਸ਼ਾਮਲ | ਸ਼ਾਮਲ ਨਹੀਂ |
| --- | --- |
| FreeIPA access model | FreeRADIUS deployment |
| Proxmox LDAP realm setup | FreeIPA user lifecycle creation |
| synced groups ਤੋਂ Proxmox RBAC | ਪੂਰੀ Proxmox multi-tenant policy coverage |
| Linux IPA client enrollment | FreeIPA ਖ਼ਿਲਾਫ ਸਿੱਧਾ native Windows logon |
| ਵੱਖਰਾ Windows AD domain-membership workflow | GPO ਜਾਂ broader AD object lifecycle automation |
| limited FreeIPA-aware Windows helper workflow | FreeIPA-only Windows helpers ਨੂੰ AD ਦੇ ਬਰਾਬਰ ਸਮਝਣਾ |

## ਵਿੰਡੋਜ਼ ਵਰਕਫਲੋ

Windows support ਨੂੰ Linux IPA enrollment ਵਿੱਚ ਮਿਲਾਇਆ ਨਹੀਂ ਗਿਆ; ਇਸਨੂੰ ਵੱਖਰੇ workflow ਵਜੋਂ ਰੱਖਿਆ ਗਿਆ ਹੈ।

- `windows_qemu_guest_agent_clients` ਸਿਰਫ optional QEMU Guest Agent helper tasks ਲਈ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ।
- workflow ਨੂੰ enable ਕਰਨ ਲਈ `10-features.yml` ਵਿੱਚ `windows_domain_membership_enabled: true` ਸੈੱਟ ਕਰੋ।
- `windows_management_clients` ਉਹ ਵੱਖਰਾ Windows management group ਹੈ ਜੋ `playbooks/windows-management.yml` ਅਤੇ `playbooks/site.yml` ਦੇ optional Windows stage ਵੱਲੋਂ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ।
- actual Windows logon Active Directory domain membership ਰਾਹੀਂ ਸੰਭਾਲਿਆ ਜਾਂਦਾ ਹੈ; FreeIPA-centered environments ਵਿੱਚ Windows hosts ਨੂੰ FreeIPA ਨਾਲ ਸਿੱਧਾ join ਕਰਨ ਦੀ ਥਾਂ FreeIPA-AD trust ਦੇ AD ਪਾਸੇ join ਕਰੋ।

FreeIPA-only Windows domain join ਇਸ repository ਵੱਲੋਂ supported ਨਹੀਂ ਹੈ। Active Directory ਜਾਂ FreeIPA-AD trust ਤੋਂ ਬਿਨਾਂ, Windows workflow ਸਿਰਫ helper tasks ਜਿਵੇਂ reachable guest management ਅਤੇ optional QEMU Guest Agent installation ਤੱਕ ਸੀਮਿਤ ਰਹਿੰਦਾ ਹੈ।

ਜੇ ਤੁਸੀਂ Windows ਲਈ domain join ਤੋਂ ਬਿਨਾਂ ਇੱਕ limited FreeIPA-aware path ਚਾਹੁੰਦੇ ਹੋ, ਤਾਂ `windows_freeipa_helpers_enabled: true` enable ਕਰੋ ਅਤੇ `windows_freeipa_helper_clients` ਨੂੰ `playbooks/windows-freeipa-helpers.yml` ਨਾਲ ਵਰਤੋ। ਇਹ helper workflow IPA CA ਨੂੰ trust ਕਰ ਸਕਦਾ ਹੈ, bootstrap ਲਈ IPA CA auto-fetch ਕਰ ਸਕਦਾ ਹੈ, expected IPA CA thumbprint pin ਕਰ ਸਕਦਾ ਹੈ, optional hosts-file bootstrap entries manage ਕਰ ਸਕਦਾ ਹੈ, IPA DNS ਅਤੇ ਮੁੱਖ TCP ports validate ਕਰ ਸਕਦਾ ਹੈ, Windows ਤੋਂ HTTPS reachability validate ਕਰ ਸਕਦਾ ਹੈ, IPA-related endpoint ਦੇ ਖਿਲਾਫ Windows time source validate ਕਰ ਸਕਦਾ ਹੈ, local Windows group memberships manage ਕਰ ਸਕਦਾ ਹੈ, ਅਤੇ optional ਤੌਰ ਤੇ OpenSSH Server install ਜਾਂ expose ਕਰ ਸਕਦਾ ਹੈ। ਪਰ ਇਹ FreeIPA ਖਿਲਾਫ native Windows logon ਨਹੀਂ ਦਿੰਦਾ।

ਉਸੇ helper group ਲਈ non-mutating readiness check ਚਾਹੀਦਾ ਹੋਵੇ ਤਾਂ `playbooks/windows-freeipa-validate.yml` ਚਲਾਓ। ਇਹ validation ਅਤੇ summary path ਨੂੰ ਜਿਵੇਂ ਦਾ ਤਿਵੇਂ ਰੱਖਦਾ ਹੈ ਪਰ ਉਸ run ਲਈ CA import, hosts-file changes, local-group changes, ਅਤੇ OpenSSH management ਨੂੰ force off ਕਰ ਦਿੰਦਾ ਹੈ।

ਇਹ workflow WinRM ਜਾਂ PSRP ਰਾਹੀਂ reachable Windows 10/11 ਅਤੇ Windows Server guest ਨੂੰ target ਕਰਦਾ ਹੈ।

## ਆਰਕੀਟੈਕਚਰ

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

ਵੱਡੀ architecture explanation ਲਈ [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) ਵੇਖੋ।

## ਲੋੜਾਂ

### ਕੰਟਰੋਲਰ

- Ansible Core 2.14+
- Proxmox primary node, IPA servers ਅਤੇ Linux clients ਤੱਕ SSH ਪਹੁੰਚ
- Windows workflow ਵਰਤਣ ਸਮੇਂ Windows guests ਤੱਕ WinRM ਜਾਂ PSRP ਪਹੁੰਚ
- ਲੋੜ ਅਨੁਸਾਰ `sudo` ਜਾਂ `root`
- QGA SSH bootstrap ਲਈ guest ਵਿੱਚ QEMU Guest Agent ਪਹਿਲਾਂ ਤੋਂ ਚਾਲੂ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ
- Windows fallback ਲਈ host `windows_qemu_guest_agent_clients` ਵਿੱਚ ਹੋਣ
- ਜੇ Windows domain membership enable ਹੈ ਤਾਂ reachable Windows hosts `windows_management_clients` ਵਿੱਚ ਹੋਣ ਅਤੇ ਤੁਹਾਨੂੰ AD join credentials ਦੇਣੇ ਪੈਣਗੇ
- ਜੇ Windows FreeIPA helper tasks enable ਹਨ ਤਾਂ reachable Windows hosts `windows_freeipa_helper_clients` ਵਿੱਚ ਹੋਣ
- Linux SSH bootstrap ਲਈ SSH keypair ਅਤੇ initial password path

### ਟਾਰਗੇਟ

- `proxmox_primary` host ਉੱਤੇ Proxmox VE 6.x ਜਾਂ ਇਸ ਤੋਂ ਨਵਾਂ
- Proxmox ਅਤੇ Linux clients ਤੋਂ reachable FreeIPA
- ਜੇ WinRM ਜਾਂ PSRP ਰਾਹੀਂ reachable ਹੋਣ ਤਾਂ Windows 10/11 ਅਤੇ Windows Server guests ਨੂੰ ਵੱਖਰੇ Windows workflow ਨਾਲ manage ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ
- ਸਹੀ DNS ਅਤੇ time synchronization
- `proxmox_primary` ਲਈ `root` ਜਾਂ ਉਹ user ਵਰਤੋ ਜੋ `pveversion`, `pvesh` ਅਤੇ `pveum` ਨੂੰ `sudo` ਨਾਲ ਚਲਾ ਸਕੇ
- ਜੇ ਤੁਸੀਂ Windows domain membership ਵਰਤਦੇ ਹੋ ਤਾਂ target Windows guests ਸੰਬੰਧਿਤ AD domain controllers ਤੱਕ ਪਹੁੰਚ ਸਕਣ
- ਜੇ ਤੁਸੀਂ limited Windows FreeIPA helper workflow ਵਰਤਦੇ ਹੋ ਤਾਂ target Windows guests ਸੰਬੰਧਿਤ IPA servers ਤੱਕ ਪਹੁੰਚ ਸਕਣ
- Proxmox discovery ਮੋਡ ਵਿੱਚ guest ਨੂੰ QEMU Guest Agent ਰਾਹੀਂ usable IP report ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ

## ਨੈੱਟਵਰਕ ਪੋਰਟ

ਇਹ ਸਾਰਣੀ ਇਸ repository ਦੇ controller, Proxmox LDAP automation, ਅਤੇ Linux IPA enrollment flow ਵੱਲੋਂ ਵਰਤੇ ਜਾਂਦੇ network ports ਦਿਖਾਉਂਦੀ ਹੈ। ਇਸ ਨੂੰ ਇਸ ਪ੍ਰੋਜੈਕਟ ਦੀ ਹੱਦ ਵਿੱਚ ਹੀ ਰੱਖਿਆ ਗਿਆ ਹੈ; ਇਹ FreeIPA server-to-server replication ਦੀ ਪੂਰੀ matrix ਨਹੀਂ ਹੈ।

| ਨਾਮ | ਪੋਰਟ | ਪ੍ਰੋਟੋਕੋਲ | ਸਰੋਤ | ਮੰਜ਼ਿਲ | ਕਦੋਂ ਲੋੜੀਂਦਾ | ਮਕਸਦ |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | ਹਮੇਸ਼ਾਂ | Ansible connectivity |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | ਜਦੋਂ Windows management enable ਹੋਵੇ | Windows guests ਲਈ Ansible connectivity |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS servers | ਜਦੋਂ Linux guests IPA DNS ਵਰਤਦੇ ਹੋਣ | IPA records ਅਤੇ external names resolve ਕਰਨਾ |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment ਅਤੇ login | Kerberos authentication |
| LDAP | `389` | `TCP` | Linux guest | IPA servers | Linux IPA enrollment ਅਤੇ login | LDAP ਅਤੇ FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port` (default `443`) | `TCP` | Linux guest | IPA servers | Linux IPA enrollment | client install ਦੌਰਾਨ IPA web/API verification |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA servers | Linux IPA enrollment ਅਤੇ password operations | Kerberos password ਅਤੇ keytab operations |
| LDAPS | `636` | `TCP` | Proxmox primary node | IPA/LDAP servers | default `ldaps` mode ਵਿੱਚ Proxmox LDAP realm | Proxmox LDAP realm connection |

ਨੋਟ:

- `LDAPS 636/TCP` repository default ਹੈ ਕਿਉਂਕਿ `proxmox_ldap_mode` default ਤੌਰ ਤੇ `ldaps` ਹੈ। ਜੇ ਤੁਸੀਂ LDAP mode ਜਾਂ port ਬਦਲਦੇ ਹੋ, ਤਾਂ configured `proxmox_ldap_port` ਨੂੰ allow ਕਰੋ।
- Windows transport setup ਦੇ ਅਨੁਸਾਰ `WinRM` ਆਮ ਤੌਰ ਤੇ HTTPS ਲਈ `5986/TCP` ਜਾਂ HTTP ਲਈ `5985/TCP` ਵਰਤਦਾ ਹੈ।
- `DNS 53/TCP,UDP` ਸਿਰਫ਼ ਉਸ ਵੇਲੇ ਲੋੜੀਂਦਾ ਹੈ ਜਦੋਂ Linux guests IPA servers ਨੂੰ DNS resolvers ਵਜੋਂ ਵਰਤਦੇ ਹਨ।
- `Kerberos 88` ਅਤੇ `Kerberos Password 464` ਦੋਵਾਂ ਲਈ `TCP` ਅਤੇ `UDP` ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ।
- Active Directory domain join ਲਈ ਆਮ Windows-to-domain-controller port set ਵੀ ਲੋੜੀਂਦਾ ਹੈ, ਪਰ ਉਹ environment-specific ਹੈ ਅਤੇ ਇੱਥੇ ਜਾਣ-ਬੁੱਝ ਕੇ ਪੂਰੀ ਤਰ੍ਹਾਂ ਦਰਜ ਨਹੀਂ ਕੀਤਾ ਗਿਆ।
- Kerberos ਦੇ ਭਰੋਸੇਯੋਗ ਤਰੀਕੇ ਨਾਲ ਕੰਮ ਕਰਨ ਲਈ time synchronization ਵੀ ਲੋੜੀਂਦੀ ਹੈ, ਪਰ NTP source environment-specific ਹੈ ਅਤੇ ਇਸ repository ਵੱਲੋਂ manage ਨਹੀਂ ਕੀਤੀ ਜਾਂਦੀ।

## ਅਨੁਕੂਲਤਾ

- ਇਸ repository ਦੀ Proxmox automation, Proxmox VE 6.x ਅਤੇ ਇਸ ਤੋਂ ਬਾਅਦ ਦੀਆਂ releases ਵਿੱਚ ਵਰਤੇ ਜਾਣ ਵਾਲੇ `pveum` ਅਤੇ `pvesh` realm ਅਤੇ RBAC interfaces ਦੇ ਆਲੇ ਦੁਆਲੇ ਬਣਾਈ ਗਈ ਹੈ।
- ਇਹ repository Proxmox VE 6.x ਅਤੇ ਉਸ ਤੋਂ ਨਵੀਆਂ major releases ਨੂੰ ਧਿਆਨ ਵਿੱਚ ਰੱਖ ਕੇ ਬਣਾਈ ਗਈ ਹੈ
- default supported major versions: `6`, `7`, `8`, `9`, `10`
- validation `pveversion` ਨਾਲ detected Proxmox version check ਕਰਦੀ ਹੈ
- `proxmox_supported_major_versions` ਨਾਲ ਤੁਸੀਂ list ਨੂੰ narrow ਜਾਂ extend ਕਰ ਸਕਦੇ ਹੋ
- `proxmox_allow_future_major_versions` ਦਾ default `true` ਹੈ, ਇਸ ਲਈ listed tested versions ਤੋਂ ਉੱਪਰ ਵਾਲੇ future majors ਵੀ by default pass ਕਰ ਸਕਦੇ ਹਨ
- future major versions ਨੂੰ ਫਿਰ ਵੀ compatibility candidates ਵਜੋਂ ਹੀ ਸਮਝਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ ਜਦ ਤੱਕ released Proxmox interface ਨੂੰ ਇਸ automation ਦੇ ਨਾਲ verify ਨਾ ਕਰ ਲਿਆ ਜਾਵੇ
- `1` ਤੋਂ `5` ਵਰਗੇ ਪੁਰਾਣੇ legacy majors ਇਸ public repository ਵਿੱਚ tested support ਵਜੋਂ claim ਨਹੀਂ ਕੀਤੇ ਜਾਂਦੇ; ਜੇ ਤੁਸੀਂ ਉਹਨਾਂ ਨੂੰ locally ਜੋੜਦੇ ਹੋ ਤਾਂ ਇਸਨੂੰ explicit compatibility override ਸਮਝੋ ਅਤੇ ਪੂਰੇ workflow ਨੂੰ lab ਵਿੱਚ validate ਕਰੋ

ਪੁਰਾਣੇ lab environment ਲਈ local override example:

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

## ਤੇਜ਼ ਸ਼ੁਰੂਆਤ

ਹੇਠਾਂ ਦਿੱਤੀਆਂ examples shell commands ਵਰਤਦੀਆਂ ਹਨ। ਜਿੱਥੇ ਲੋੜ ਹੋਵੇ ਉੱਥੇ PowerShell equivalents ਵੀ ਦਿੱਤੇ ਗਏ ਹਨ।

### 1. ਉਦਾਹਰਨ ਇਨਵੈਂਟਰੀ ਅਤੇ ਵਾਲਟ ਟੈਂਪਲੇਟ ਕਾਪੀ ਕਰੋ

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Optional when you plan to manage Windows guests:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Optional when you plan to manage Windows guests:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. ਵਾਤਾਵਰਣ-ਖ਼ਾਸ ਫਾਈਲਾਂ ਸੋਧੋ

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` when you use Windows management
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` when you use Windows management

Linux guest source mode ਵਿੱਚੋਂ ਇੱਕ ਚੁਣੋ:

- static inventory entries under `linux_ipa_clients`
- `linux_ipa_client_hosts` entries in `group_vars/all/30-linux-clients.yml`
- Proxmox VM discovery with `linux_ipa_proxmox_discovery_enabled: true`

Linux IPA enrollment ਲਈ:

- `ipaclient_domain` shared IPA DNS domain ਹੈ, ਜਿਵੇਂ `example.com`
- `linux_ipa_servers` ਵਿੱਚ IPA servers ਦੇ hostnames ਹੁੰਦੇ ਹਨ, ਜਿਵੇਂ `ipa01.example.com`

ਜੇ ਤੁਸੀਂ Proxmox ਨਾਲ `root` ਦੀ ਥਾਂ ਕਿਸੇ regular sudo-capable user ਨਾਲ SSH ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ, ਤਾਂ `hosts.yml` ਵਿੱਚ `proxmox_primary` ਹੇਠ ਇਹ ਸੈੱਟ ਕਰੋ ਅਤੇ sudo password ਨੂੰ `vault-proxmox.yml` ਵਿੱਚ ਰੱਖੋ:

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

ਇਸ setup ਵਿੱਚ `vault_proxmox_become_password` ਉਹੀ password ਹੈ ਜੋ ਤੁਸੀਂ Proxmox host ਉੱਤੇ `sudo` ਲਈ ਟਾਈਪ ਕਰਦੇ ਹੋ।

### 3. ਵਾਲਟ ਫਾਈਲਾਂ ਇਨਕ੍ਰਿਪਟ ਕਰੋ

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

ਜੇ Windows workflow enable ਕਰਨਾ ਹੈ ਤਾਂ `inventories/production/group_vars/all/vault-windows.yml` ਨੂੰ ਵੀ include ਕਰੋ।

ਜਾਂ helper wrappers ਵਰਤੋ:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

ਜੇ ਤੁਸੀਂ playbooks ਨੂੰ ਵੱਖ-ਵੱਖ domain passwords ਨਾਲ ਚਲਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ, ਤਾਂ vault IDs ਨੂੰ `--ask-vault-pass` ਤੋਂ ਤਰਜੀਹ ਦਿਓ:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

ਜੇ optional Windows workflow ਵੀ ਆਪਣਾ ਵੱਖਰਾ vault password ਵਰਤਦਾ ਹੈ, ਤਾਂ ਇਸੇ command ਵਿੱਚ `windows@prompt` ਵੀ ਸ਼ਾਮਲ ਕਰੋ।

`-AskVaultPass` ਸਿਰਫ਼ ਉਹਨਾਂ ਹਾਲਤਾਂ ਵਿੱਚ ਵਰਤੋ ਜਿੱਥੇ ਉਸ playbook ਵੱਲੋਂ ਵਰਤੀਆਂ ਜਾਣ ਵਾਲੀਆਂ ਸਭ vault files ਇੱਕੋ password ਸਾਂਝਾ ਕਰਦੀਆਂ ਹੋਣ।

### 4. ਲੋੜੀਂਦੀ ਕਲੈਕਸ਼ਨ ਇੰਸਟਾਲ ਕਰੋ

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

ਜਾਂ direct:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

### 5. ਪਹਿਲਾਂ ਵੈਲੀਡੇਸ਼ਨ ਚਲਾਓ

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Helper-only Windows FreeIPA path ਲਈ:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Linux readiness audit ਲਈ:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Readiness report by default `.ansible/linux-readiness-report.json` ਲਿਖਦਾ ਹੈ।

- `ssh.ready=true`: configured SSH path ਕੰਮ ਕਰ ਗਿਆ
- `ssh.promptless=true`: SSH probe ਬਿਨਾਂ `ansible_password` ਸਫਲ ਹੋਇਆ
- `ssh.auth_mode=password_configured`: `sshpass` ਵਰਤਿਆ ਗਿਆ
- `ssh.auth_mode=key_or_agent`: SSH batch mode ਬਿਨਾਂ password ਕੰਮ ਕਰ ਗਿਆ
- `qga.status=available`: `qm guest ping` owning Proxmox node ਉੱਤੇ ਸਫਲ ਹੋਇਆ
- `qga.status=disabled`: QEMU Guest Agent Proxmox config ਵਿੱਚ enabled ਨਹੀਂ
- `qga.status=configured_unresponsive`: config ਵਿੱਚ enabled ਹੈ ਪਰ ਜਵਾਬ ਨਹੀਂ ਦੇ ਰਿਹਾ
- `qga.status=node_unreachable`: controller owning Proxmox node ਤੱਕ ਨਹੀਂ ਪਹੁੰਚਿਆ
- `qga.status=not_applicable`: host Proxmox discovery ਤੋਂ ਨਹੀਂ ਆਇਆ

Quick inspection example:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. ਚੋਣਵਾਂ: ਯੋਜਿਤ ਤਬਦੀਲੀਆਂ ਦੀ ਝਲਕ ਵੇਖੋ

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Check mode ਨੂੰ partial preview ਸਮਝੋ, full simulation ਨਹੀਂ। Repository ਦਾ ਕੁਝ Proxmox configuration direct CLI commands ਰਾਹੀਂ ਹੁੰਦਾ ਹੈ ਅਤੇ Linux enrollment ਲਈ upstream FreeIPA client role ਵਰਤੀ ਜਾਂਦੀ ਹੈ।

### 7. ਪੂਰੀ ਸੰਰਚਨਾ ਲਾਗੂ ਕਰੋ

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

## ਰੋਲਆਉਟ ਕ੍ਰਮ

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Optional when you manage Windows guests:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Optional when you want the limited Windows FreeIPA helper workflow:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Optional when you want validation-only coverage for the helper workflow:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

ਇਹ sequence troubleshooting ਨੂੰ ਕਾਫ਼ੀ ਆਸਾਨ ਬਣਾਉਂਦਾ ਹੈ।

PowerShell limited rollout example:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Defaults conservative ਹਨ:

- FreeIPA access changes ਲਈ `serial: 1`
- Proxmox changes ਲਈ `serial: 1`
- Linux hostname resolution, validation, and enrollment ਲਈ `serial: 10`
- Windows management changes ਲਈ `serial: 10`
- ਸਾਰੇ rollout paths ਲਈ `max_fail_percentage: 0`

ਇਹ values `inventories/production/group_vars/all/15-rollout.yml` ਵਿੱਚ tune ਕਰੋ।

## ਟੈਗ ਮਾਡਲ

- `freeipa`, `proxmox`, `linux`, `validate`
- `windows`, `windows_domain`
- `windows`, `windows_freeipa`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

Examples:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## ਇਵੈਂਟ-ਚਲਿਤ VM ਆਨਬੋਰਡਿੰਗ

ਜੇ ਤੁਸੀਂ ਚਾਹੁੰਦੇ ਹੋ ਕਿ Proxmox `post-start` ਜਾਂ `post-migrate` ਤੋਂ ਬਾਅਦ ਤੁਰੰਤ Linux discovery ਅਤੇ IPA enrollment ਚਲਾਏ, ਤਾਂ [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../../docs/EVENT_DRIVEN_VM_ONBOARDING.md) ਵਿੱਚ ਦਿੱਤਾ optional hook/webhook workflow ਵਰਤੋ।

ਇਹ workflow `playbooks/proxmox-vm-event.yml` ਨਾਮ ਦੇ dedicated event playbook ਨੂੰ ਵਰਤਦਾ ਹੈ, ਇਸ ਲਈ trigger path ਸਿਰਫ਼ Linux ਅਤੇ FreeIPA guest side ਨੂੰ ਹੀ handle ਕਰਦਾ ਹੈ। ਹਰ VM event ਤੇ Proxmox LDAP realm ਜਾਂ RBAC automation ਮੁੜ ਨਹੀਂ ਚਲਦੀ।

`proxmox_vm_event_onboarding_enabled: true` ਅਤੇ required webhook variables ਦੇ ਨਾਲ repository ਇਸ optional hook/webhook stack ਨੂੰ `site.yml` ਜਾਂ `proxmox.yml` ਤੋਂ deploy ਵੀ ਕਰ ਸਕਦੀ ਹੈ।

Proxmox VM hooks standalone `create` phase expose ਨਹੀਂ ਕਰਦੀਆਂ। ਅਮਲ ਵਿੱਚ ਨਵੇਂ VM ਆਪਣੀ ਪਹਿਲੀ `post-start` event ਤੇ pick ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ migration hooks source ਅਤੇ target nodes ਦੋਵਾਂ ਤੇ trigger ਹੋ ਸਕਦੇ ਹਨ।

## ਇਨਵੈਂਟਰੀ ਮਾਡਲ

ਇਹ repository ਛੇ declared groups ਅਤੇ ਇੱਕ generated runtime group ਵਰਤਦੀ ਹੈ:

- `ipa_servers`: ਇੱਕ ਜਾਂ ਵੱਧ FreeIPA servers
- `proxmox_primary`: ਇੱਕ Proxmox node ਜਿਸ ਕੋਲ realm configuration ਅਤੇ recurring sync timer ਦੀ ownership ਹੈ
- `linux_ipa_clients`: Linux guests ਲਈ declarative source inventory group
- `linux_ipa_clients_runtime`: static inventory, manual host definitions, ਅਤੇ optional Proxmox discovery ਤੋਂ ਬਣਿਆ generated runtime group
- `windows_qemu_guest_agent_clients`: ਸਿਰਫ਼ QEMU Guest Agent installation ਲਈ optional Windows guest group
- `windows_management_clients`: separate Windows domain-membership workflow ਵੱਲੋਂ ਵਰਤਿਆ ਜਾਣ ਵਾਲਾ optional Windows guest group
- `windows_freeipa_helper_clients`: limited FreeIPA-aware helper workflow ਵਾਸਤੇ optional Windows guest group

ਤੁਸੀਂ ਆਪਣੇ inventory groups ਵੀ ਜੋੜ ਸਕਦੇ ਹੋ ਅਤੇ ਉਹਨਾਂ ਨੂੰ FreeIPA hostgroup definitions ਤੋਂ reference ਕਰ ਸਕਦੇ ਹੋ। ਜੇ ਤੁਹਾਨੂੰ FreeIPA hostgroups ਵਿੱਚ ਪੂਰਾ prepared Linux guest set ਚਾਹੀਦਾ ਹੈ, ਤਾਂ `linux_ipa_clients_runtime` ਨੂੰ reference ਕਰੋ।

> [!IMPORTANT]
> FreeIPA ਨੂੰ ਹਰ guest ਦਾ final hostname ਚਾਹੀਦਾ ਹੈ। IP-only targets ਜਾਂ discovery mode ਵਿੱਚ `ipa_hostname` explicitly ਦਿਓ ਜਾਂ ਯਕੀਨੀ ਬਣਾਓ ਕਿ guest ਉੱਤੇ `hostname -f` final FQDN ਵਾਪਸ ਕਰਦਾ ਹੈ।

> [!TIP]
> reusable golden template ਨੂੰ FreeIPA ਵਿੱਚ enroll ਨਾ ਕਰੋ। ਪਹਿਲਾਂ VM clone ਕਰੋ, final hostname ਦਿਓ, ਅਤੇ ਬਣੇ guest ਨੂੰ enroll ਕਰੋ।

### ਲਿਨਕਸ ਗੈਸਟ ਸਰੋਤ ਮੋਡ

ਤੁਸੀਂ `linux_ipa_clients` ਨੂੰ ਤਿੰਨ ਵੱਖ-ਵੱਖ ਤਰੀਕਿਆਂ ਨਾਲ ਭਰ ਸਕਦੇ ਹੋ।

#### 1. Static inventory hosts

ਜੇ ਤੁਹਾਨੂੰ guest names ਪਹਿਲਾਂ ਹੀ ਪਤਾ ਹਨ, ਤਾਂ ਆਮ Ansible inventory entries ਵਰਤੋ:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. Manual host definitions in variables

ਜੇ ਤੁਸੀਂ guests ਨੂੰ `hosts.yml` ਤੋਂ ਬਾਹਰ ਰੱਖਣਾ ਚਾਹੁੰਦੇ ਹੋ ਜਾਂ ਤੁਹਾਡੇ ਕੋਲ ਸਿਰਫ਼ IP ਹੈ, ਤਾਂ `linux_ipa_client_hosts` ਵਰਤੋ:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

ਨੋਟ:

- ਜੇ `name` ਇੱਕ resolvable hostname ਜਾਂ FQDN ਹੋਵੇ, ਤਾਂ `ansible_host` optional ਹੈ
- ਜੇ ਤੁਹਾਨੂੰ ਸਿਰਫ਼ IP ਪਤਾ ਹੈ, ਤਾਂ `name` ਲਈ ਕੋਈ stable alias ਵਰਤੋ
- ਜਦੋਂ `ipa_hostname` ਨਾ ਦਿੱਤਾ ਜਾਵੇ, ਤਾਂ playbook guest ਉੱਤੇ `hostname -f` ਨੂੰ fallback ਵਜੋਂ ਵਰਤਦੀ ਹੈ

#### 3. Proxmox VM auto-discovery

ਜਦੋਂ ਤੁਸੀਂ ਚਾਹੁੰਦੇ ਹੋ ਕਿ playbook ਇੱਕ ਜਾਂ ਵੱਧ Proxmox nodes ਤੋਂ Linux guests ਖਿੱਚ ਲਿਆਵੇ, ਤਾਂ discovery ਵਰਤੋ:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Optional: gate discovery-driven automation to approved guests only.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Optional: always exclude infrastructure or sensitive guests even when broad
# node discovery is enabled.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# Optional first-touch SSH settings for discovered guests when the guest agent
# is not running yet and the repository must connect over SSH to install it.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

Notes:

- discovery ਉਸੇ `linux_ipa_clients_runtime` group ਵਿੱਚ VM ਜੋੜਦੀ ਹੈ ਜੋ ਬਾਕੀ playbooks ਵਰਤਦੀਆਂ ਹਨ
- IP discovery, QEMU Guest Agent ਵੱਲੋਂ network interfaces report ਕਰਨ ਉੱਤੇ depend ਕਰਦੀ ਹੈ
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` ਸਿਰਫ਼ ਉਹ VM names trust ਕਰਦੀ ਹੈ ਜੋ ਪਹਿਲਾਂ ਹੀ FQDN ਹਨ
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` ਸੈੱਟ ਕਰਨ ਨਾਲ `Teleport-Server-1` ਵਰਗੇ safe short Proxmox VM names ਨੂੰ `linux_ipa_identity_hostname_suffix` ਰਾਹੀਂ `teleport-server-1.example.com` ਵਰਗੇ hostname hints ਵਿੱਚ promote ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ
- `linux_ipa_proxmox_discovery_vmids` optional ਹੈ ਅਤੇ event-driven hook/webhook workflow ਵਿੱਚ discovery ਨੂੰ ਇੱਕ ਜਾਂ ਵੱਧ specific VMIDs ਤੱਕ scope ਕਰਨ ਲਈ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ
- guest ਨੂੰ ਫਿਰ ਵੀ final hostname ਚਾਹੀਦਾ ਹੈ, ਜੋ ਜਾਂ ਤਾਂ VM ਅੰਦਰ ਪਹਿਲਾਂ ਹੀ configured ਹੋਵੇ ਜਾਂ manual definition ਵਿੱਚ `ipa_hostname` ਰਾਹੀਂ ਦਿੱਤਾ ਗਿਆ ਹੋਵੇ
- guest ਦਾ ਅਸਲ system hostname enrollment ਲਈ ਵੀ valid ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ; `localhost.localdomain` ਵਰਗੀਆਂ placeholder values ਨੂੰ `linux-clients` ਜਾਂ `site` ਚਲਾਉਣ ਤੋਂ ਪਹਿਲਾਂ VM ਉੱਤੇ ਬਦਲੋ
- ਜੇ guests `app-server-01` ਵਰਗੇ short hostnames ਵਰਤਦੇ ਹਨ, ਤਾਂ ਤੁਸੀਂ `linux_ipa_identity_hostname_suffix` ਅਤੇ optional `linux_freeipa_enroll_manage_hostname: true` ਸੈੱਟ ਕਰਕੇ enrollment ਤੋਂ ਪਹਿਲਾਂ ਪੂਰਾ hostname ਜਿਵੇਂ `app-server-01.example.net` resolve ਅਤੇ apply ਕਰ ਸਕਦੇ ਹੋ
- ਜੇ ਤੁਹਾਡੇ guest hostnames ਲਈ FreeIPA DNS authoritative ਹੈ, ਤਾਂ `linux_freeipa_enroll_manage_authoritative_dns: true` ਸੈੱਟ ਕਰਕੇ ਖਾਸ guest A ਅਤੇ PTR records repair ਕਰ ਸਕਦੇ ਹੋ ਅਤੇ enrollment ਤੋਂ ਪਹਿਲਾਂ link-local `fe80::/10` AAAA records ਹਟਾ ਸਕਦੇ ਹੋ
- ਜੇ DNS ਹਾਲੇ ready ਨਾ ਹੋਵੇ, ਤਾਂ `linux_ipa_manage_etc_hosts: true` ਅਤੇ `linux_ipa_etc_hosts_entries` ਦੇ ਕੇ IPA servers ਅਤੇ guest FQDNs ਲਈ managed `/etc/hosts` bootstrap block enrollment checks ਤੋਂ ਪਹਿਲਾਂ ਜੋੜਿਆ ਜਾ ਸਕਦਾ ਹੈ
- `guest_qemu_agent_install_enabled` ਉਹਨਾਂ guests ਉੱਤੇ QEMU Guest Agent install ਕਰਦੀ ਹੈ ਜੋ SSH ਜਾਂ WinRM ਰਾਹੀਂ ਪਹਿਲਾਂ ਹੀ reachable ਹਨ, ਫਿਰ ਉਸੇ workflow ਵਿੱਚ ਬਾਅਦ ਵਿੱਚ reachable ਹੋਣ ਵਾਲੇ Linux guests ਉੱਤੇ retry ਕਰਦੀ ਹੈ, ਅਤੇ Linux enrollment ਤੋਂ ਬਾਅਦ ਫਿਰ ਇੱਕ ਵਾਰ retry ਕਰਦੀ ਹੈ
- `linux_ipa_proxmox_discovery_allowlist_enabled: true` ਵਰਤੋ ਜੇ ਤੁਸੀਂ ਚਾਹੁੰਦੇ ਹੋ ਕਿ discovery ਚਾਲੂ ਰਹੇ ਪਰ ਸਿਰਫ਼ tightly approved Proxmox guests ਹੀ Linux runtime inventory ਵਿੱਚ ਆਉਣ; allowlist exact VMIDs, IPs, ਅਤੇ names ਨਾਲ match ਕਰ ਸਕਦੀ ਹੈ
- `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, ਜਾਂ `linux_ipa_proxmox_discovery_blacklist_names` ਵਰਤੋ ਜਦੋਂ discovery-enabled nodes ਉੱਤੇ firewalls ਜਾਂ DNS servers ਵਰਗੇ infrastructure VMs ਵੀ ਹੋਣ ਜਿਨ੍ਹਾਂ ਨੂੰ Linux IPA automation ਕਦੇ ਨਹੀਂ ਮਿਲਣੀ ਚਾਹੀਦੀ; blacklist broad discovery ਜਾਂ allowlist ਰਾਹੀਂ admission ਉੱਤੇ ਵੀ ਹਮੇਸ਼ਾਂ ਹਾਵੀ ਰਹਿੰਦੀ ਹੈ
- ਉਹਨਾਂ Proxmox-discovered Linux guests ਲਈ ਜਿਨ੍ਹਾਂ ਕੋਲ ਪਹਿਲਾਂ ਤੋਂ working guest agent ਨਹੀਂ ਹੈ, `linux_ipa_proxmox_discovery_ansible_user` ਅਤੇ `linux_ipa_proxmox_discovery_ansible_password` ਜਾਂ `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` ਸੈੱਟ ਕਰੋ ਤਾਂ ਜੋ repository ਕੋਲ QEMU Guest Agent install ਕਰਨ ਲਈ usable first-touch SSH path ਹੋਵੇ
- ਜੇ ਉਹ discovered guests non-root SSH user ਵਰਤਦੇ ਹਨ, ਤਾਂ `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, ਅਤੇ `linux_ipa_proxmox_discovery_ansible_become_password` ਵੀ ਸੈੱਟ ਕਰੋ ਜਦ ਤੱਕ ਉਸ account ਕੋਲ passwordless sudo ਪਹਿਲਾਂ ਹੀ ਨਾ ਹੋਵੇ
- `guest_qemu_agent_install_manage_proxmox_vm_agent` Proxmox-backed Linux guests ਲਈ Proxmox-side guest-agent communication (`qm set <vmid> --agent 1`) ਨੂੰ ਵੀ guest-side install path ਤੋਂ ਪਹਿਲਾਂ enable ਕਰਦੀ ਹੈ
- ਜੇ ਉਹ Proxmox VM option ਚੱਲਦੇ VM ਉੱਤੇ ਬਦਲੇ, ਤਾਂ repository default ਵਜੋਂ ਸਿਰਫ਼ warning ਦਿੰਦੀ ਹੈ ਕਿਉਂਕਿ Proxmox ਨੂੰ host side ਤੋਂ guest-agent channel ਵਰਤਣ ਲਈ ਨਵੀਂ VM start ਦੀ ਲੋੜ ਹੋ ਸਕਦੀ ਹੈ; ਜੇ ਤੁਸੀਂ ਉਹਨਾਂ running VMs ਨੂੰ ਆਪੇ reboot ਕਰਵਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ ਤਾਂ `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` ਸੈੱਟ ਕਰੋ
- `linux_ipa_ssh_host_key_policy` default ਤੌਰ ਤੇ `accept_new` ਹੈ, ਤਾਂ ਜੋ ਨਵੇਂ discover ਹੋਏ VMs ਨਾਲ host key checking ਪੂਰੀ ਤਰ੍ਹਾਂ disable ਕੀਤੇ ਬਿਨਾਂ ਸੰਪਰਕ ਕੀਤਾ ਜਾ ਸਕੇ; ਪਰ ਬਦਲੇ ਹੋਏ host keys ਫਿਰ ਵੀ fail ਹੁੰਦੇ ਹਨ ਅਤੇ operator review ਮੰਗਦੇ ਹਨ
- `linux_ipa_qga_ssh_bootstrap_enabled` Proxmox-backed guests ਲਈ preferred no-reboot bootstrap path ਹੈ ਕਿਉਂਕਿ ਇਹ ਕਿਸੇ SSH login ਤੋਂ ਪਹਿਲਾਂ ਹੀ QEMU Guest Agent ਰਾਹੀਂ dedicated key-only automation user ਬਣਾ ਸਕਦੀ ਹੈ
- `linux_ipa_qga_ssh_bootstrap_qm_path` default ਤੌਰ ਤੇ `qm` ਹੈ, ਅਤੇ bootstrap flow fail ਹੋਣ ਤੋਂ ਪਹਿਲਾਂ Proxmox node ਉੱਤੇ common fallback paths ਵੀ probe ਕਰਦੀ ਹੈ
- ਜਿਹੜੇ guests `guest-ping` allow ਕਰਦੇ ਹਨ ਪਰ `guest-exec` reject ਕਰਦੇ ਹਨ, ਉਹ default ਤੌਰ ਤੇ QGA bootstrap ਦੌਰਾਨ skip ਹੋ ਜਾਂਦੇ ਹਨ; ਉਹਨਾਂ ਲਈ ਹੋਰ SSH path ready ਰੱਖੋ ਜਾਂ ਤੁਰੰਤ fail ਕਰਵਾਉਣ ਲਈ `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` ਸੈੱਟ ਕਰੋ
- `linux_ipa_ssh_bootstrap_enabled` hostname resolution ਅਤੇ enrollment ਤੋਂ ਪਹਿਲਾਂ controller SSH public key ਨੂੰ Linux guests ਉੱਤੇ install ਕਰਨ ਦਾ optional ਤਰੀਕਾ ਦਿੰਦੀ ਹੈ; `linux_ipa_ssh_bootstrap_password` runtime Linux guests ਲਈ shared first-touch password fallback ਵਜੋਂ ਵੀ ਵਰਤੀ ਜਾਂਦੀ ਹੈ, ਭਾਵੇਂ key bootstrap disable ਹੋਵੇ
- Linux IPA enrollment ਉਹ upstream client joins retry ਕਰਦੀ ਹੈ ਜੋ FreeIPA JSON-RPC timeout ਨਾਲ fail ਹੋਣ, ਅਤੇ ਹੌਲੀ ਜਾਂ busy IPA environments ਲਈ `linux_ipaclient_kinit_attempts` expose ਕਰਦੀ ਹੈ
- Linux IPA enrollment default ਤੌਰ ਤੇ `ipa_servers` inventory hostnames ਨੂੰ join server list ਵਿੱਚ merge ਕਰਦੀ ਹੈ, ਤਾਂ ਜੋ clients ਇੱਕੇ configured endpoint ਦੀ ਥਾਂ ਪੂਰਾ IPA server set ਵਰਤ ਸਕਣ
- ਜਦੋਂ ਇੱਕ ਤੋਂ ਵੱਧ IPA servers available ਹੋਣ, ਹਰ retry pass ਉਹਨਾਂ server candidates ਨੂੰ ਇੱਕ-ਇੱਕ ਕਰਕੇ try ਕਰਦੀ ਹੈ
- combined `site` workflow ਪਹਿਲਾਂ FreeIPA hostgroups ਬਣਾਉਂਦੀ ਹੈ, ਫਿਰ Linux enrollment ਤੋਂ ਬਾਅਦ enrolled runtime hosts ਜੋੜਦੀ ਹੈ, ਤਾਂ ਜੋ not-yet-enrolled guests ਕਾਰਨ pre-enrollment hostgroup membership fail ਨਾ ਹੋਵੇ

## ਸੰਰਚਨਾ ਪਰਿਧੀ

Most values ਇਨ੍ਹਾਂ ਫਾਇਲਾਂ ਵਿੱਚ ਰਹਿੰਦੀਆਂ ਹਨ:

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

Variable layout ਲਈ [docs/VARIABLES.md](../../docs/VARIABLES.md) ਵੇਖੋ।

Key variable families:

| Area | Variables |
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

## ਗਰੁੱਪ ਰਣਨੀਤੀ ਦੀ ਉਦਾਹਰਨ

- ਇੱਕ ਸਰਲ pattern ਜੋ ਵਧੀਆ ਤਰੀਕੇ ਨਾਲ scale ਕਰਦੀ ਹੈ:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- Sudo rule `allow-linux-ssh-admins-sudo`
- synced group `proxmox-admins-ipa` ਲਈ Proxmox ACL binding

`freeipa_linux_admin_users` ਨੂੰ [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) ਵਿੱਚ populate ਕਰੋ ਜੇ ਤੁਸੀਂ managed `linux-ssh-admins` group ਰਾਹੀਂ ਖ਼ਾਸ IPA users ਨੂੰ Linux SSH ਅਤੇ sudo ਦੇਣਾ ਚਾਹੁੰਦੇ ਹੋ।

ਯਾਦ ਰੱਖੋ ਕਿ Proxmox LDAP sync suffix ਨਾਲ synced groups ਬਣਾਉਂਦੀ ਹੈ:

```text
<group-name>-<realm>
```

ਜੇ ਤੁਹਾਡਾ FreeIPA group `proxmox-admins` ਹੈ ਅਤੇ Proxmox realm `ipa` ਹੈ, ਤਾਂ synced PVE group ਇਹ ਬਣਦੀ ਹੈ:

```text
proxmox-admins-ipa
```

## ਸੁਰੱਖਿਆ

- plaintext inventory variable files ਦੀ ਥਾਂ ਸਾਰੇ secrets ਨੂੰ `vault-freeipa.yml` ਅਤੇ `vault-proxmox.yml` ਵਿੱਚ ਰੱਖੋ
- Proxmox ਲਈ dedicated read-only LDAP bind account ਵਰਤੋ
- certificate verification ਦੇ ਨਾਲ TLS ਨੂੰ ਤਰਜੀਹ ਦਿਓ
- disposable lab ਤੋਂ ਬਾਹਰ SSH host key checking ਬੰਦ ਨਾ ਕਰੋ
- QGA available ਹੋਵੇ ਤਾਂ shared temporary passwords ਦੀ ਥਾਂ `linux_ipa_qga_ssh_bootstrap_enabled` ਨੂੰ ਤਰਜੀਹ ਦਿਓ
- Linux SSH bootstrap enable ਹੋਵੇ ਤਾਂ shared bootstrap passwords ਨੂੰ vaulted variables ਵਿੱਚ ਰੱਖੋ ਅਤੇ ਬਾਅਦ ਵਿੱਚ rotate/remove ਕਰੋ
- Proxmox LDAP bind account ਵਾਸਤੇ IPA admin account reuse ਨਾ ਕਰੋ
- `guest_qemu_agent_install_enabled` ਸਿਰਫ਼ ਉਸ ਵੇਲੇ ਵਰਤੋ ਜਦੋਂ repository ਕੋਲ guest ਅੰਦਰ ਜਾਣ ਲਈ valid management path ਪਹਿਲਾਂ ਹੀ ਹੋਵੇ; Proxmox discovery ਲਈ ਇਸਦਾ ਮਤਲਬ ਹੈ ਕਿ QGA ਪਹਿਲਾਂ ਤੋਂ ਚੱਲ ਰਹੀ ਹੋਵੇ ਜਾਂ `linux_ipa_proxmox_discovery_ansible_user` ਦੇ ਨਾਲ password ਜਾਂ key access configured ਹੋਵੇ
- production rollout ਤੋਂ ਪਹਿਲਾਂ `proxmox_ldap_filter` ਅਤੇ `proxmox_ldap_group_filter` ਨੂੰ review ਕਰੋ ਤਾਂ ਜੋ ਬਹੁਤ ਜ਼ਿਆਦਾ import ਨਾ ਹੋਵੇ

ਜੇ ਤੁਸੀਂ disposable lab ਵਿੱਚ ਜਾਣ-ਬੁੱਝ ਕੇ SSH host verification bypass ਕਰਨੀ ਹੈ, ਤਾਂ repository defaults ਬਦਲਣ ਦੀ ਥਾਂ ਹਰ shell session ਲਈ opt out ਕਰੋ:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## ਆਈਡੈਂਪੋਟੈਂਸੀ ਅਤੇ ਸਾਵਧਾਨੀਆਂ

ਇਹ project largely idempotent ਰੂਪ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਹੈ, ਪਰ production ਤੋਂ ਪਹਿਲਾਂ lab ਵਿੱਚ test ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

- Proxmox CLI output releases ਅਨੁਸਾਰ ਥੋੜ੍ਹਾ ਬਦਲ ਸਕਦਾ ਹੈ
- FreeIPA LDAP filters ਨੂੰ ਤੁਹਾਡੇ tree ਲਈ tuning ਦੀ ਲੋੜ ਹੋ ਸਕਦੀ ਹੈ
- existing hand-managed PVE ACLs ਅਤੇ roles ਨੂੰ automation ਤੋਂ ਪਹਿਲਾਂ compare ਕਰੋ
- Proxmox VM auto-discovery running guests ਅਤੇ QEMU guest-agent data ਉੱਤੇ depend ਕਰਦੀ ਹੈ
- IP-only guest definitions ਨੂੰ valid final hostname ਜਾਂ explicit `ipa_hostname` ਚਾਹੀਦਾ ਹੈ
- non-root Proxmox SSH user ਲਈ working `sudo` ਲਾਜ਼ਮੀ ਹੈ; passwordless sudo ਨਾ ਹੋਵੇ ਤਾਂ `-K` ਨਾਲ become password ਦਿਓ
- ਜੇ `ansible_become_password` ਨੂੰ `vault-proxmox.yml` ਵਿੱਚ store ਕੀਤਾ ਹੋਵੇ, ਤਾਂ Ansible ਉਹ password encrypted variable ਤੋਂ ਪੜ੍ਹ ਸਕਦੀ ਹੈ

## ਤਸਦੀਕ

Rollout ਤੋਂ ਬਾਅਦ ਹਰ access path ਠੀਕ ਹੈ ਇਹ ਮੰਨਣ ਦੀ ਥਾਂ resulting state verify ਕਰੋ।

### FreeIPA ਵਿੱਚ

- expected user groups ਮੌਜੂਦ ਹਨ ਇਹ verify ਕਰੋ
- expected hostgroups ਮੌਜੂਦ ਹਨ ਇਹ verify ਕਰੋ
- expected HBAC rules ਮੌਜੂਦ ਅਤੇ enabled ਹਨ ਇਹ verify ਕਰੋ
- expected sudo rules ਮੌਜੂਦ ਅਤੇ enabled ਹਨ ਇਹ verify ਕਰੋ

### Proxmox ਵਿੱਚ

- LDAP realm ਮੌਜੂਦ ਹੈ ਇਹ verify ਕਰੋ
- initial sync ਨੇ expected users ਜਾਂ groups import ਕੀਤੇ ਹਨ ਇਹ verify ਕਰੋ
- intended synced group ਲਈ expected ACL binding verify ਕਰੋ

### ਲਿਨਕਸ ਗੈਸਟ ਉੱਤੇ

- allowed IPA user login ਕਰ ਸਕਦਾ ਹੈ ਇਹ verify ਕਰੋ
- disallowed user ਨੂੰ HBAC block ਕਰਦੀ ਹੈ ਇਹ verify ਕਰੋ
- allowed IPA admin `sudo -l` ਚਲਾ ਸਕਦਾ ਹੈ ਇਹ verify ਕਰੋ
- `linux_ipaclient_mkhomedir` enable ਹੋਵੇ ਤਾਂ first login ਤੇ home directory ਬਣਦੀ ਹੈ ਇਹ verify ਕਰੋ

## ਰਿਪੋਜ਼ਿਟਰੀ ਬਣਤਰ

<details>
<summary>Repository layout ਦਿਖਾਓ</summary>

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
    └── bootstrap.sh
```

</details>

## ਵਿਕਾਸ

ਇਸ repository ਵਿੱਚ ਹੇਠਲੇ helper files ਸ਼ਾਮਲ ਹਨ:

- `.editorconfig` ਵੱਖ-ਵੱਖ editors ਵਿੱਚ whitespace, encoding, ਅਤੇ line-ending defaults ਨੂੰ ਇਕਸਾਰ ਰੱਖਦਾ ਹੈ
- `.gitattributes` ਆਮ text files ਨੂੰ LF line endings ਉੱਤੇ ਰੱਖਦਾ ਹੈ
- `.gitignore` generated inventory, vault data, local collections, ਅਤੇ editor files ਨੂੰ Git ਤੋਂ ਬਾਹਰ ਰੱਖਦਾ ਹੈ
- `.ansible-lint` vendored collections ਨੂੰ exclude ਕਰਦਾ ਹੈ ਅਤੇ ਸਿਰਫ YAML line-length rule ਨੂੰ suppress ਕਰਦਾ ਹੈ
- `.yamllint` playbooks, inventories, ਅਤੇ workflow files ਵਿੱਚ YAML formatting checks ਨੂੰ ਇਕਸਾਰ ਰੱਖਦਾ ਹੈ
- `.github/CODEOWNERS` repository ਦੇ ਮੁੱਖ ਹਿੱਸਿਆਂ ਲਈ review ownership route ਕਰਦਾ ਹੈ
- `.github/workflows/ci.yml` pushes ਅਤੇ pull requests ਉੱਤੇ repository lint checks ਅਤੇ smoke validation ਚਲਾਂਦਾ ਹੈ
- `.pre-commit-config.yaml` `pre-commit` install ਹੋਣ ਤੇ commits ਤੋਂ ਪਹਿਲਾਂ fast lint hook ਚਲਾਂਦਾ ਹੈ
- `CHANGELOG.md` repository ਦੇ ਮਹੱਤਵਪੂਰਨ ਬਦਲਾਅ ਇੱਕੋ ਜਗ੍ਹਾ track ਕਰਦਾ ਹੈ
- `docs/VARIABLES.md` split inventory variable layout ਦੀ ਵਿਆਖਿਆ ਕਰਦਾ ਹੈ
- `docs/i18n/` translated README files ਰੱਖਦਾ ਹੈ; `README.md` canonical source ਰਹਿੰਦਾ ਹੈ ਅਤੇ ਇਹਨਾਂ ਫਾਇਲਾਂ ਨੂੰ ਉਸਦੀ ਪੂਰੀ English section structure mirror ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ
- `docs/i18n/TRANSLATION_GUIDE.md` ਦੱਸਦਾ ਹੈ ਕਿ translated README files ਨੂੰ sync ਵਿੱਚ ਕਿਵੇਂ ਰੱਖਣਾ ਹੈ
- `scripts/bootstrap.ps1` ਅਤੇ `scripts/bootstrap.sh` ਲੋੜੀਂਦੀ collection ਨੂੰ repo-local `collections/` path ਵਿੱਚ install ਕਰਦੇ ਹਨ ਅਤੇ ansible-core 2.24+ compatibility ਲਈ patch ਕਰਦੇ ਹਨ
- `scripts/patch_freeipa_collection.py` pinned FreeIPA collection ਵਿੱਚ deprecated imports rewrite ਕਰਦਾ ਹੈ ਤਾਂ ਜੋ ਇਹ future ansible-core releases ਨਾਲ compatible ਰਹੇ
- `scripts/lint.py` local use, CI, ਅਤੇ pre-commit ਲਈ cross-platform lint entrypoint ਦਿੰਦਾ ਹੈ
- `scripts/smoke-test.py` example inventory validate ਕਰਦਾ ਹੈ ਅਤੇ real infrastructure ਨੂੰ ਛੂਹਣ ਤੋਂ ਬਿਨਾਂ syntax checks ਚਲਾਂਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਵੱਖਰਾ Windows playbook ਵੀ ਸ਼ਾਮਲ ਹੈ
- `scripts/check_translations.py` canonical English README ਦੇ ਮੁਕਾਬਲੇ translated README files ਲਈ metadata, section-structure parity, ਅਤੇ minimum content coverage audit ਕਰਦਾ ਹੈ
- `scripts/lint.ps1` ਅਤੇ `scripts/lint.sh` combined local lint ਅਤੇ smoke workflow ਚਲਾਂਦੇ ਹਨ
- `scripts/proxmox_event_webhook.py` Proxmox VM events ਲਈ optional controller-side webhook ਚਲਾਂਦਾ ਹੈ
- `scripts/proxmox-vm-hook.pl` optional Proxmox VM hookscript ਹੈ ਜੋ `post-start` ਅਤੇ `post-migrate` ਤੇ controller webhook ਨੂੰ notify ਕਰਦਾ ਹੈ
- `scripts/run-playbook.ps1` PowerShell users ਲਈ common `ansible-playbook` commands wrap ਕਰਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਵੱਖਰਾ Windows workflow ਵੀ ਸ਼ਾਮਲ ਹੈ
- `scripts/vault.ps1` ਅਤੇ `scripts/vault.sh` FreeIPA, Proxmox, ਅਤੇ optional Windows secrets ਲਈ common split-vault operations wrap ਕਰਦੇ ਹਨ
- `tests/` repository verification surface ਰੱਖਦਾ ਹੈ, ਜੋ smoke-test documentation ਨਾਲ ਸ਼ੁਰੂ ਹੁੰਦਾ ਹੈ
- `CONTRIBUTING.md` expected contribution ਅਤੇ validation workflow document ਕਰਦਾ ਹੈ
- `SECURITY.md` vulnerabilities report ਕਰਨ ਅਤੇ security-sensitive ਜਾਣਕਾਰੀ handle ਕਰਨ ਦੀ ਪ੍ਰਕਿਰਿਆ document ਕਰਦਾ ਹੈ

ਜੇ `ansible-lint` ਤੁਹਾਡੇ controller ਉੱਤੇ install ਹੈ:

```bash
ansible-lint
```

Repository smoke checks ਨੂੰ direct ਚਲਾਉਣ ਲਈ:

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

ਪੂਰੇ local lint pass ਲਈ:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

ਹਰ commit ਤੋਂ ਪਹਿਲਾਂ fast lint hook enable ਕਰਨ ਲਈ:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell wrapper examples:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## ਅਗਲੇ ਵਿਸਥਾਰ

- IPA-ready Linux templates ਲਈ Packer pipeline
- AWX job templates ਅਤੇ schedules
- ਅਲੱਗ Proxmox tenant/pool models
- broader Windows local policy ਜਾਂ GPO integration

## ਲਾਇਸੈਂਸ

ਇਹ ਪ੍ਰੋਜੈਕਟ [0BSD License](../../LICENSE) ਦੇ ਅਧੀਨ ਜਾਰੀ ਕੀਤਾ ਗਿਆ ਹੈ।
