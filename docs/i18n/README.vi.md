# Tu dong hoa truy cap Proxmox + FreeIPA

Trang nay cung cap ban dich day du theo cau truc cua [README.md](../../README.md). Ban tieng Anh van la nguon chuan, nhung ban dich nay bao phu cung cac phan chinh.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Vi sao du an nay ton tai

Hay dung kho nay khi ban da co:

- mot moi truong FreeIPA on dinh
- mot cum Proxmox VE
- cac may Linux can xac thuc tap trung
- mot tai khoan dich vu rieng cho LDAP bind cua Proxmox
- mo hinh nhom ro rang cho quan tri vien va van hanh

Muc tieu la xem FreeIPA nhu nguon su that cho dinh danh va quyen truy cap. Proxmox tieu thu thu muc nay thong qua LDAP realm, guest Linux gia nhap FreeIPA bang role `ipaclient`, va SSH, HBAC, `sudo` duoc giu tap trung.

## Nhung gi ban nhan duoc

- quan ly nhom nguoi dung, hostgroup, quy tac HBAC va quy tac `sudo` cua FreeIPA
- cau hinh Proxmox LDAP realm tro den FreeIPA
- dong bo realm dinh ky tu mot node cum duoc chi dinh
- RBAC binding cua Proxmox cho cac nhom da dong bo
- gia nhap Linux tu inventory tinh, dinh nghia host thu cong hoac Proxmox discovery
- SSH bootstrap tuy chon khong can reboot qua QEMU Guest Agent
- cai QEMU Guest Agent tuy chon qua SSH hoac WinRM cho guest da truy cap duoc
- bootstrap khoa cong khai SSH tuy chon cho lan truy cap dau
- lam moi SSSD cache tu dong sau thay doi mo hinh truy cap
- onboarding tuy chon theo su kien `post-start` va `post-migrate`

## Pham vi

| Bao gom | Khong bao gom |
| --- | --- |
| Mo hinh truy cap FreeIPA | Windows domain join |
| Cau hinh LDAP realm cho Proxmox | Trien khai FreeRADIUS |
| RBAC Proxmox tu nhom dong bo | Tao toan bo vong doi nguoi dung FreeIPA |
| Linux IPA enrollment | Tat ca truong hop multi-tenant cua Proxmox |

## Kien truc

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## Yeu cau

### Controller

- Ansible Core 2.14+
- SSH toi node Proxmox chinh, IPA server va Linux client
- `sudo` hoac `root` khi can
- neu bat QGA SSH bootstrap thi QEMU Guest Agent phai dang chay san trong guest
- neu bat Windows fallback thi host truy cap duoc phai nam trong `windows_qemu_guest_agent_clients`
- neu bat Linux SSH bootstrap thi controller can keypair SSH va mot duong dang nhap ban dau bang mat khau

### Dich den

- Proxmox VE 6.x tro len tren host trong `proxmox_primary`
- FreeIPA co the truy cap tu Proxmox va Linux
- DNS va dong bo thoi gian dung
- voi `proxmox_primary`, dung `root` hoac user SSH co `sudo` cho `pveversion`, `pvesh`, `pveum`
- neu dung Proxmox discovery thi guest phai cung cap IP dung duoc qua QEMU Guest Agent

## Cong mang

- `22/TCP` cho SSH
- `53/TCP,UDP` cho IPA DNS
- `88/TCP,UDP` va `464/TCP,UDP` cho Kerberos
- `389/TCP` cho LDAP
- `linux_freeipa_enroll_https_port`, mac dinh `443/TCP`
- `636/TCP` cho `ldaps`

## Tuong thich

- huong toi Proxmox VE 6.x va moi hon
- major support mac dinh: `6`, `7`, `8`, `9`, `10`
- co the dieu chinh bang `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions` mac dinh `true`

## Bat dau nhanh

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

Hay chinh `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, va `vault-proxmox.yml` cho moi truong cua ban.

## Thu tu rollout

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Mac dinh la than trong: `serial: 1` cho FreeIPA va Proxmox, `serial: 10` cho Linux, `max_fail_percentage: 0`.

## Mo hinh tag

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Onboarding VM theo su kien

Neu ban muon Proxmox kich hoat Linux discovery va IPA enrollment ngay sau `post-start` hoac `post-migrate`, hay dung luong hook/webhook tuy chon trong [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md). Luong nay dung `playbooks/proxmox-vm-event.yml`, khong chay lai LDAP realm hoac RBAC moi lan co event va xu ly VM moi o lan `post-start` dau tien.

## Mo hinh inventory

Nhom chinh:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

Ngay ca voi IP-only hoac Proxmox discovery, guest van can FQDN cuoi cung qua `ipa_hostname` hoac `hostname -f`.

### Nguon Linux guest

1. host tinh trong inventory
2. dinh nghia thu cong trong `linux_ipa_client_hosts`
3. Proxmox discovery bang `linux_ipa_proxmox_discovery_*`

Ghi chu quan trong: discovery phu thuoc vao du lieu mang tu QEMU Guest Agent, `linux_ipa_proxmox_discovery_vmids` huu ich cho event path, ten ngan co the mo rong bang `linux_ipa_identity_hostname_suffix`, DNS authoritative co the sua bang `linux_freeipa_enroll_manage_authoritative_dns`, va `/etc/hosts` bootstrap co the dung khi DNS chua san sang.

## Be mat cau hinh

File chinh:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Vi du chien luoc nhom

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## Bao mat

- chi luu bi mat trong vault
- uu tien tai khoan bind LDAP read-only rieng cho Proxmox
- uu tien TLS co xac minh chung chi
- khong tat SSH host key checking ngoai lab tam thoi

## Tinh idempotent va luu y

Kho duoc thiet ke de co the chay lai, nhung van phai kiem thu trong lab truoc khi dua vao san xuat. Gioi han da biet gom khac biet CLI cua Proxmox, canh chinh LDAP filter, su phu thuoc cua discovery vao guest dang chay va du lieu QGA, cung nhu yeu cau hostname cuoi cung hop le cho cac dinh nghia theo IP.

## Xac minh

- trong FreeIPA, kiem tra nhom, hostgroup, HBAC va `sudo`
- trong Proxmox, kiem tra LDAP realm, sync ban dau va ACL binding
- tren guest Linux, kiem tra dang nhap duoc phep, HBAC chan dung, `sudo -l` va tao home

## Bo cuc repo

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## Phat trien

Repo bao gom `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, CI workflow, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, va `scripts/vault.*`.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## Mo rong tiep theo

- pipeline Packer cho IPA-ready Linux template
- AWX job template va schedule
- mo hinh tenant va pool Proxmox tach rieng
- luong Windows hoac AD-trust cho moi truong huong RDP

## Giay phep

Phat hanh theo [MIT License](../../LICENSE).
