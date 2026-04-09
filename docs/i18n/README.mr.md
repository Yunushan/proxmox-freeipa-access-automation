# Proxmox + FreeIPA प्रवेश स्वयंचलन

हे पृष्ठ [README.md](../../README.md) चे संपूर्ण रचना-आधारित मराठी रूप देते. इंग्रजी आवृत्ती canonical source राहते, पण ही फाइल तेच मुख्य विभाग कव्हर करते.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## हा प्रकल्प का आहे

ही repository तेव्हा वापरा जेव्हा तुमच्याकडे आधीपासून:

- एक स्थिर FreeIPA वातावरण
- एक Proxmox VE cluster
- केंद्रीय authentication वापरणारे Linux guest
- Proxmox LDAP bind साठी dedicated service account
- admins आणि operators साठी स्पष्ट group model

मुख्य कल्पना अशी आहे की FreeIPA ला identity आणि access साठी source of truth म्हणून वापरायचे. Proxmox ते LDAP realm म्हणून वापरतो, Linux guest `ipaclient` role ने FreeIPA मध्ये enroll होतात, आणि SSH, HBAC, `sudo` नियंत्रण केंद्रीकृत राहते.

## तुम्हाला काय मिळते

- FreeIPA user groups, hostgroups, HBAC rules आणि `sudo` rules चे व्यवस्थापन
- FreeIPA विरुद्ध Proxmox LDAP realm configuration
- ठरवलेल्या cluster node वरून periodic realm sync
- synced groups साठी Proxmox RBAC bindings
- static inventory, manual host definitions किंवा Proxmox discovery मधून Linux enrollment
- QEMU Guest Agent मार्गे optional no-reboot SSH bootstrap
- reachable guest साठी optional SSH/WinRM guest-agent install
- first-touch साठी optional SSH public-key bootstrap
- FreeIPA access बदलांनंतर automatic SSSD refresh
- `post-start` आणि `post-migrate` साठी optional event-driven onboarding

## व्याप्ती

| समाविष्ट | समाविष्ट नाही |
| --- | --- |
| FreeIPA access model | Windows domain join |
| Proxmox LDAP realm setup | FreeRADIUS deployment |
| synced groups मधून Proxmox RBAC | FreeIPA user lifecycle creation |
| Linux IPA enrollment | सर्व Proxmox multi-tenant edge cases |

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

## आवश्यकता

- Ansible Core 2.14+
- Proxmox primary node, IPA servers आणि Linux clients पर्यंत SSH
- गरजेनुसार `sudo` किंवा `root`
- QGA SSH bootstrap साठी guest मध्ये QEMU Guest Agent आधीपासून चालू असणे
- Windows fallback साठी host `windows_qemu_guest_agent_clients` मध्ये असणे
- Linux SSH bootstrap साठी SSH keypair आणि initial password path

## नेटवर्क पोर्ट

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` आणि `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- `linux_freeipa_enroll_https_port`, default `443/TCP`
- `636/TCP` for `ldaps`

## जलद सुरुवात

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

तुमच्या environment नुसार `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, `vault-proxmox.yml` बदला.

## Rollout क्रम

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Defaults conservative आहेत: FreeIPA आणि Proxmox साठी `serial: 1`, Linux साठी `serial: 10`, आणि `max_fail_percentage: 0`.

## Tag मॉडेल

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Event-driven VM onboarding

जर Proxmox ने `post-start` किंवा `post-migrate` नंतर लगेच Linux discovery आणि IPA enrollment चालवावे असे वाटत असेल, तर [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) मधील optional hook/webhook workflow वापरा. हा मार्ग `playbooks/proxmox-vm-event.yml` वापरतो, प्रत्येक event वर LDAP realm किंवा RBAC पुन्हा चालवत नाही, आणि नवीन VM पहिल्या `post-start` ला पकडतो.

## Inventory मॉडेल

मुख्य समूह:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only किंवा Proxmox discovery वापरले तरी guest ला final FQDN लागतो, `ipa_hostname` किंवा `hostname -f` मार्फत.

## Configuration surface

मुख्य files:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Group strategy उदाहरण

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## सुरक्षा

- secrets फक्त vault files मध्ये ठेवा
- Proxmox साठी dedicated read-only LDAP bind account वापरा
- certificate verification सह TLS प्राधान्य द्या
- disposable lab बाहेर SSH host key checking बंद करू नका

## पडताळणी

- FreeIPA मध्ये groups, hostgroups, HBAC, `sudo` तपासा
- Proxmox मध्ये LDAP realm, sync, ACL bindings तपासा
- Linux guest वर allowed login, denied HBAC case, `sudo -l` आणि home creation तपासा

## Repository layout

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

या repository मध्ये `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflows, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, आणि `scripts/vault.*` आहेत.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## पुढील विस्तार

- IPA-ready Linux templates साठी Packer pipeline
- AWX job templates आणि schedules
- स्वतंत्र Proxmox tenant/pool models
- RDP-oriented वातावरणासाठी Windows किंवा AD-trust flow

## परवाना

हा प्रकल्प [MIT License](../../LICENSE) अंतर्गत प्रकाशित आहे.
