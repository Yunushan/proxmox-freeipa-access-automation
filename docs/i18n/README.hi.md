# Proxmox + FreeIPA अभिगम स्वचालन

यह पृष्ठ [README.md](../../README.md) की पूर्ण संरचित हिन्दी अनुवाद प्रति देता है। अंग्रेजी संस्करण अंतिम canonical स्रोत बना रहता है, लेकिन यह फ़ाइल वही मुख्य अनुभाग कवर करती है।

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## यह प्रोजेक्ट क्यों है

इस रिपॉजिटरी का उपयोग तब करें जब आपके पास पहले से:

- स्वस्थ FreeIPA deployment
- Proxmox VE cluster
- ऐसे Linux guest जो central authentication इस्तेमाल करें
- Proxmox LDAP bind के लिए dedicated service account
- admins और operators के लिए साफ group model

मुख्य विचार FreeIPA को identity और access का source of truth बनाना है। Proxmox इसे LDAP realm के रूप में consume करता है, Linux guest `ipaclient` role से FreeIPA में enroll होते हैं, और SSH, HBAC, `sudo` नियंत्रण centralized रहते हैं।

## क्या मिलता है

- FreeIPA user groups, hostgroups, HBAC rules और `sudo` rules का प्रबंधन
- FreeIPA के खिलाफ Proxmox LDAP realm configuration
- चुने गए cluster node से periodic realm sync
- synced directory groups के लिए Proxmox RBAC bindings
- static inventory, manual host definitions या Proxmox discovery से Linux enrollment
- QEMU Guest Agent के माध्यम से optional no-reboot SSH bootstrap
- reachable guests के लिए SSH/WinRM आधारित optional guest-agent install
- first-touch के लिए optional SSH public-key bootstrap
- FreeIPA access changes के बाद automatic SSSD refresh
- `post-start` और `post-migrate` के लिए optional event-driven onboarding

## दायरा

| शामिल | शामिल नहीं |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| synced groups से Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | सभी Proxmox multi-tenant edge cases |

## आर्किटेक्चर

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## आवश्यकताएँ

### Controller

- Ansible Core 2.14+
- Proxmox primary node, IPA servers और Linux clients तक SSH पहुंच
- जरूरत पड़ने पर `sudo` या `root`
- QGA SSH bootstrap के लिए guest में QEMU Guest Agent पहले से चालू होना चाहिए
- Windows fallback के लिए reachable hosts `windows_qemu_guest_agent_clients` में होने चाहिए
- Linux SSH bootstrap के लिए SSH keypair और initial password path चाहिए

### Targets

- `proxmox_primary` में Proxmox VE 6.x या नया
- Proxmox और Linux clients से reachable FreeIPA
- सही DNS और time synchronization
- `proxmox_primary` के लिए `root` या `pveversion`, `pvesh`, `pveum` चलाने वाला sudo-capable SSH user
- discovery के लिए QEMU Guest Agent से usable IP

## नेटवर्क पोर्ट

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` और `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, default `443/TCP`
- `636/TCP` for `ldaps`

## अनुकूलता

- Proxmox VE 6.x और आगे के लिए
- default supported majors: `6`, `7`, `8`, `9`, `10`
- `proxmox_supported_major_versions` से बदला जा सकता है
- `proxmox_allow_future_major_versions` default `true`

## त्वरित प्रारंभ

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

अपनी environment के लिए `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, और `vault-proxmox.yml` संपादित करें।

## Rollout क्रम

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Defaults जानबूझकर conservative हैं: FreeIPA और Proxmox के लिए `serial: 1`, Linux के लिए `serial: 10`, और `max_fail_percentage: 0`.

## Tag मॉडल

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

यदि आप चाहते हैं कि Proxmox `post-start` या `post-migrate` के बाद तुरंत Linux discovery और IPA enrollment trigger करे, तो [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) में दिए गए optional hook/webhook workflow का उपयोग करें। यह path `playbooks/proxmox-vm-event.yml` का उपयोग करता है, हर event पर LDAP realm या RBAC दुबारा नहीं चलाता, और नए VM को पहले `post-start` पर पकड़ता है।

## Inventory मॉडल

मुख्य समूह:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only या Proxmox discovery के साथ भी guest को final FQDN चाहिए, `ipa_hostname` या `hostname -f` के माध्यम से।

### Linux source modes

1. static inventory hosts
2. `linux_ipa_client_hosts` में manual definitions
3. `linux_ipa_proxmox_discovery_*` के जरिए Proxmox discovery

महत्वपूर्ण बिंदु: discovery QEMU Guest Agent network data पर निर्भर है, `linux_ipa_proxmox_discovery_vmids` event path में उपयोगी है, short names के लिए `linux_ipa_identity_hostname_suffix` मदद करता है, authoritative DNS सुधारने के लिए `linux_freeipa_enroll_manage_authoritative_dns: true` उपयोगी है, और DNS तैयार न होने पर `/etc/hosts` bootstrap उपलब्ध है।

## Configuration surface

मुख्य फाइलें:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## उदाहरण group strategy

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## सुरक्षा

- secrets केवल vault files में रखें
- Proxmox के लिए dedicated read-only LDAP bind account पसंद करें
- certificate verification के साथ TLS उपयोग करें
- disposable lab के बाहर SSH host key checking बंद न करें

## Idempotency और caveats

यह repository repeatable runs के लिए लिखी गई है, लेकिन production से पहले lab validation ज़रूरी है। ज्ञात सीमाएँ हैं: Proxmox CLI output differences, LDAP filter tuning की जरूरत, discovery की QGA और running guests पर dependency, और IP-based targets के लिए valid final hostname की आवश्यकता।

## सत्यापन

- FreeIPA में groups, hostgroups, HBAC और `sudo` verify करें
- Proxmox में LDAP realm, sync और ACL bindings verify करें
- Linux guest पर allowed login, denied HBAC case, `sudo -l`, और home creation जांचें

## रिपॉजिटरी लेआउट

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## विकास

रिपॉजिटरी में `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflows, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, और `scripts/vault.*` शामिल हैं।

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## आगे के विस्तार

- IPA-ready Linux templates के लिए Packer pipeline
- AWX job templates और schedules
- अलग Proxmox tenant और pool models
- RDP-oriented environments के लिए Windows या AD-trust flow

## लाइसेंस

यह प्रोजेक्ट [MIT License](../../LICENSE) के अंतर्गत जारी किया गया है।
