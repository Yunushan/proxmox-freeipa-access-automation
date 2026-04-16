# Tu dong hoa truy cap Proxmox + FreeIPA

Trang nay cung cap ban dich day du va tuong duong ve cau truc cua [README.md](../../README.md). Ban tieng Anh van la nguon chuan, nhung ban tieng Viet nay phai bao phu cung mot pham vi van hanh cho operator dung tieng Viet.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## Ngon ngu

Ban tieng Anh la nguon chuan cho tai lieu day du. Cung co cac README ban dich day du cho 20 ngon ngu bo sung.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

Repository nay coi **FreeIPA la source of truth** cho identity va access. Proxmox tieu thu directory do thong qua LDAP realm, guest Linux join vao FreeIPA bang role upstream `ipaclient`, va access duoc giu tap trung thong qua synced groups, HBAC, va sudo rules thay vi bi phan tan thanh local account tren tung VM.

> [!IMPORTANT]
> Du an nay **khong dung FreeRADIUS lam identity source**, **khong tao local user ben trong moi VM**, va **khong co muc tieu quan ly moi permission edge case co the xay ra trong Proxmox**.

## Tai sao du an nay ton tai

Hay dung kho nay neu ban da co:

- mot he thong FreeIPA on dinh
- mot cum Proxmox VE
- cac guest Linux can dung xac thuc tap trung
- mot tai khoan dich vu rieng cho LDAP bind cua Proxmox
- mo hinh nhom ro rang cho admin va operator

Nguyen tac chinh la coi FreeIPA la nguon su that cho danh tinh va quyen truy cap. Proxmox su dung thu muc do thong qua LDAP realm, guest Linux join vao FreeIPA bang role upstream `ipaclient`, va kiem soat SSH, HBAC, va `sudo` duoc giu tap trung thay vi bi phan tan thanh tai khoan local tren tung VM.

Repository nay phu hop khi ban muon onboarding va offboarding chu yeu dien ra theo trinh tu sau:

1. tao hoac cap nhat user va group trong FreeIPA
2. dong bo nhung identity do vao Proxmox
3. ap dung Proxmox role va ACL tu synced groups
4. cap quyen guest Linux thong qua FreeIPA login, HBAC, va `sudo` rules

## Ban nhan duoc gi

- quan ly nhom nguoi dung, hostgroup, rule HBAC, va rule `sudo` trong FreeIPA
- login shell mac dinh cua FreeIPA cho cac admin Linux
- cau hinh LDAP realm cua Proxmox tro den FreeIPA
- dong bo realm Proxmox dinh ky tu mot cluster node duoc chi dinh
- Proxmox RBAC binding cho cac nhom thu muc da dong bo
- Linux guest enrollment vao FreeIPA qua inventory tinh, target theo IP, hoac Proxmox VM discovery
- SSH bootstrap tuy chon khong can reboot thong qua Proxmox QEMU Guest Agent
- kich hoat tuy chon kenh guest agent o phia Proxmox cho guest Linux duoc quan ly tu Proxmox
- cai dat tuy chon QEMU Guest Agent qua SSH hoac WinRM nhu mot fallback cho guest da truy cap duoc, se truy cap duoc sau bootstrap, hoac duoc thu lai sau Linux enrollment
- Linux readiness report tuy chon cho kha nang truy cap SSH va trang thai QEMU Guest Agent tren Proxmox
- workflow rieng va tuy chon cho domain membership cua Windows 10/11 va Windows Server thong qua Active Directory
- workflow Windows gioi han va co nhan thuc ve FreeIPA de trust IPA CA, bootstrap hosts file, va validate kha nang truy cap cac dich vu IPA
- SSH public key bootstrap tuy chon cho lan truy cap Linux guest dau tien
- tu dong refresh SSSD cache tren Linux client duoc quan ly sau khi mo hinh truy cap FreeIPA thay doi
- onboarding Linux tuy chon theo su kien tu Proxmox VM hook va webhook trigger

## Pham vi

| Bao gom | Khong bao gom |
| --- | --- |
| Mo hinh truy cap FreeIPA | Trien khai FreeRADIUS |
| Cau hinh LDAP realm cho Proxmox | Tao toan bo vong doi user FreeIPA |
| Proxmox RBAC tu cac nhom da dong bo | Bao phu day du moi edge case multi-tenant cua Proxmox |
| Linux client enrollment vao IPA | Dang nhap Windows native truc tiep vao FreeIPA |
| Workflow AD domain membership cho Windows | Tu dong hoa rong cho AD object hoac GPO |
| Workflow helper FreeIPA gioi han cho Windows | Xem helper Windows dua tren FreeIPA la tuong duong voi AD |

## Quy trinh Windows

Ho tro Windows duoc trien khai thanh workflow rieng, khong tron vao luong Linux IPA enrollment.

- `windows_qemu_guest_agent_clients` van duoc danh rieng cho cac tac vu helper QEMU Guest Agent tuy chon.
- bat workflow bang `windows_domain_membership_enabled: true` trong `10-features.yml`
- `windows_management_clients` la nhom Windows rieng duoc dung boi `playbooks/windows-management.yml` va giai doan Windows tuy chon trong `playbooks/site.yml`
- dang nhap Windows thuc su duoc xu ly thong qua Active Directory domain membership; trong moi truong lay FreeIPA lam trung tam, hay join host Windows vao phia AD cua FreeIPA-AD trust thay vi co gang join Windows truc tiep vao FreeIPA

Windows join chi dua tren FreeIPA khong duoc kho nay ho tro. Neu khong co Active Directory hoac FreeIPA-AD trust, phia Windows chi gioi han o cac tac vu helper nhu quan ly guest da truy cap duoc va cai dat QEMU Guest Agent tuy chon.

Neu ban van muon mot duong Windows gioi han, co nhan thuc ve FreeIPA nhung khong domain join, hay bat `windows_freeipa_helpers_enabled: true` va dung `windows_freeipa_helper_clients` voi `playbooks/windows-freeipa-helpers.yml`. Workflow helper nay co the cai trust cho IPA CA, tu dong lay IPA CA de bootstrap, tuy chon pin thumbprint CA mong doi, tuy chon quan ly hosts file entry, validate IPA DNS va cac cong TCP quan trong, validate kha nang truy cap HTTPS tu Windows, validate time source cua Windows toi cac endpoint lien quan toi IPA, quan ly local group membership tren Windows, va tuy chon cai dat hoac expose OpenSSH Server, nhung khong cung cap dang nhap Windows native vao FreeIPA.

Neu ban muon readiness check ma khong thay doi gi tren cung nhom helper do, hay chay `playbooks/windows-freeipa-validate.yml`. Workflow nay giu logic validate va summary, nhung ep import CA, thay doi hosts file, thay doi local group, va quan ly OpenSSH thanh non-mutating cho run do.

Workflow nay huong toi guest Windows 10/11 va Windows Server co the truy cap duoc qua WinRM hoac PSRP.

## Kien truc

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

Giai thich thiet ke day du hon nam trong [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Yeu cau

### May dieu khien

- Ansible Core 2.14 hoac moi hon
- co kha nang SSH toi node Proxmox chinh, IPA server, va Linux client
- co kha nang WinRM hoac PSRP toi guest Windows neu ban su dung workflow Windows
- `sudo` hoac `root` khi can
- neu QGA SSH bootstrap duoc bat, QEMU Guest Agent phai da chay san trong guest
- neu fallback cai dat guest agent cho Windows duoc bat, cac host Windows truy cap duoc phai nam trong `windows_qemu_guest_agent_clients`
- neu Windows domain membership duoc bat, cac host Windows truy cap duoc phai nam trong `windows_management_clients` va ban phai cung cap thong tin xac thuc de join AD
- neu FreeIPA helper task cho Windows duoc bat, cac host Windows truy cap duoc phai nam trong `windows_freeipa_helper_clients`
- neu Linux SSH bootstrap duoc bat, controller can co SSH keypair va mot duong dang nhap ban dau bang mat khau cho tai khoan guest ma Ansible se dung

### Doi tuong dich

- Proxmox VE 6.x tro len tren cac host trong `proxmox_primary`
- FreeIPA phai truy cap duoc tu Proxmox va Linux client
- guest Windows 10/11 va Windows Server co the duoc quan ly thong qua workflow Windows rieng neu truy cap duoc qua WinRM hoac PSRP
- DNS va dong bo thoi gian phai dung
- voi `proxmox_primary`, dung `root` hoac user SSH co `sudo` cho `pveversion`, `pvesh`, va `pveum`
- neu ban dung Windows domain membership, guest Windows dich phai truy cap duoc domain controller AD phu hop
- neu ban dung workflow FreeIPA helper gioi han cho Windows, guest Windows dich phai truy cap duoc IPA server phu hop
- neu dung Proxmox discovery, guest phai xuat ra IP co the su dung thong qua QEMU Guest Agent

## Cong mang

Bang nay liet ke cac cong mang duoc su dung boi controller cua kho nay, Proxmox LDAP automation, va luong Linux IPA enrollment.
Bang nay co y gioi han o be mat that su duoc du an nay su dung, khong co gang liet ke toan bo ma tran FreeIPA server-to-server replication.

| Ten | Cong | Giao thuc | Nguon | Dich | Can khi | Muc dich |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible controller | Proxmox node, IPA server, Linux guest | Always | Ket noi Ansible |
| WinRM | `5985`, `5986` | `TCP` | Ansible controller | Windows guest | Khi bat quan ly Windows | Ket noi Ansible toi guest Windows |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS server | Khi Linux guest dung IPA DNS | Phan giai IPA record va ten ben ngoai qua IPA DNS |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment va login | Xac thuc Kerberos |
| LDAP | `389` | `TCP` | Linux guest | IPA server | Linux IPA enrollment va login | LDAP va FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port`, mac dinh `443` | `TCP` | Linux guest | IPA server | Linux IPA enrollment | Xac minh web/API IPA trong luc cai dat client |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA server | Linux IPA enrollment va thao tac mat khau | Mat khau Kerberos va keytab operation |
| LDAPS | `636` | `TCP` | Primary Proxmox node | IPA hoac LDAP server | Khi Proxmox LDAP realm dung mac dinh `ldaps` | Ket noi LDAP realm cua Proxmox |

Luu y:

- `LDAPS 636/TCP` la mac dinh cua kho nay vi `proxmox_ldap_mode` mac dinh la `ldaps`. Neu ban doi LDAP mode hoac port, hay mo dung `proxmox_ldap_port` ma ban thuc su dung.
- `WinRM` thuong dung `5986/TCP` cho HTTPS hoac `5985/TCP` cho HTTP, tuy thuoc vao cau hinh Windows transport cua ban.
- `DNS 53/TCP,UDP` chi can khi Linux guest dung IPA server nhu resolver.
- `Kerberos 88` va `Kerberos Password 464` deu can ca `TCP` lan `UDP`.
- Active Directory domain join cung can cac cong Windows-to-domain-controller tieu chuan, nhung ma tran do phu thuoc moi truong va khong duoc liet ke chi tiet o day.
- Dong bo thoi gian van can thiet de Kerberos hoat dong on dinh, nhung NTP source phu thuoc moi truong va khong duoc kho nay quan ly.

## Tuong thich

Proxmox automation trong kho nay duoc viet xoay quanh giao dien `pveum` va `pvesh` cho realm va RBAC ma Proxmox VE 6.x tro len su dung.

- major duoc ho tro mac dinh: `6`, `7`, `8`, `9`, `10`
- validate se kiem tra Proxmox version phat hien qua `pveversion`
- danh sach major version ho tro co the duoc dieu chinh bang `proxmox_supported_major_versions` neu ban can thu hep hoac mo rong trong moi truong cua minh
- `proxmox_allow_future_major_versions` mac dinh la `true`, nen cac major version lon hon muc da duoc kiem thu cao nhat van duoc validate cho qua theo mac dinh
- future major version van nen duoc coi la ung vien tuong thich cho den khi giao dien Proxmox cong khai duoc xac minh thuc te voi bo automation nay
- cac ban cu hon nhu `1` den `5` khong duoc repo cong khai nay xem la da ho tro chinh thuc; neu ban them chung o local, hay xem do la mot compatibility override ro rang va validate toan bo workflow trong lab truoc

Vi du local override cho legacy lab:

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

## Bat dau nhanh

Vi du duoi day dung shell command. PowerShell tuong duong duoc liet ke khi phu hop.

### 1. Sao chep tep inventory va vault mau

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

### 2. Chinh sua cac tep dac thu moi truong

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` neu ban dung Windows management
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` neu ban dung Windows management

Ngoai cac cai dat IPA va Proxmox, hay chon mot source mode cho Linux guest:

- static inventory entry duoi `linux_ipa_clients`
- `linux_ipa_client_hosts` entry trong `group_vars/all/30-linux-clients.yml`
- Proxmox VM discovery voi `linux_ipa_proxmox_discovery_enabled: true`

Cho Linux IPA enrollment, hay phan biet gia tri domain va danh sach server:

- `ipaclient_domain` la IPA DNS domain chung, vi du `example.com`
- `linux_ipa_servers` chua hostname cua IPA server, vi du `ipa01.example.com`

Neu ban muon SSH vao Proxmox bang mot user thuong co `sudo` thay vi `root`, hay dat dieu do duoi `proxmox_primary` trong `hosts.yml` va luu sudo password trong `vault-proxmox.yml`:

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

Trong cau hinh do, `vault_proxmox_become_password` la mat khau ma ban thuong go khi dung `sudo` tren host Proxmox.

### 3. Ma hoa cac tep vault

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

Them `inventories/production/group_vars/all/vault-windows.yml` vao cung lenh neu ban bat workflow Windows.

Hoac dung wrapper helper, no mac dinh su dung vault ID tach rieng va tao working vault file tu example template khi can:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Neu ban muon tach rieng mat khau theo tung domain khi chay playbook, hay dung vault ID thay vi `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Neu workflow Windows tuy chon cung dung mat khau vault rieng, hay them `windows@prompt` vao cung cau lenh.

Chi dung `-AskVaultPass` khi tat ca cac vault file ma playbook do can cung chia se mot mat khau.

### 4. Cai dat cac bo suu tap can thiet

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Hoac chay truc tiep:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

Neu ban da cai `freeipa.ansible_freeipa` truoc khi kho nay them compatibility patch, hay chay lai mot trong cac bootstrap helper hoac chay `python .\scripts\patch_freeipa_collection.py` mot lan de patch ca user-level collection install.

Khi ban dung `scripts/run-playbook.ps1`, no tu dong chay helper patch do truoc khi goi `ansible-playbook`.

### 5. Chay kiem tra truoc

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Neu ban chi muon validate duong Windows FreeIPA helper-only ma khong thay doi gi tren host:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Neu ban muon mot Linux readiness audit read-only de bao cao guest runtime nao truy cap duoc qua SSH va guest nao duoc Proxmox discovery va tra loi thong qua QEMU Guest Agent:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Readiness report mac dinh duoc ghi vao `.ansible/linux-readiness-report.json`.
Hay doc cac field chinh nhu sau:

- `ssh.ready=true`: duong SSH Ansible hien tai da cau hinh thanh cong tu controller
- `ssh.promptless=true`: SSH probe thanh cong ma khong can `ansible_password`, nen duong do non-interactive cho Ansible
- `ssh.auth_mode=password_configured`: probe dung `sshpass` vi host co `ansible_password`
- `ssh.auth_mode=key_or_agent`: probe thanh cong trong SSH batch mode ma khong can `ansible_password`
- `qga.status=available`: `qm guest ping` thanh cong tren Proxmox node dang so huu VM
- `qga.status=disabled`: cau hinh Proxmox cua VM chua bat QEMU Guest Agent
- `qga.status=configured_unresponsive`: guest agent da bat trong cau hinh Proxmox nhung khong tra loi
- `qga.status=node_unreachable`: controller khong the ket noi den Proxmox node so huu VM de probe
- `qga.status=not_applicable`: host khong duoc tao tu Proxmox discovery, nen khong co QGA probe nao duoc thu

Vi du kiem tra nhanh:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. Tuy chon: xem truoc cac thay doi

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Hãy xem check mode la mot ban xem truoc tung phan, khong phai mot mo phong hoan hao. Kho nay dung CLI command truc tiep cho mot so cau hinh Proxmox va dung upstream FreeIPA client role cho Linux enrollment, nen `--check` huu ich nhung khong hoan toan la nguon chan ly.
>
> Voi FreeIPA HBAC rule, check mode validate cac buoc dinh nghia rule nhung bo qua action enable hoac disable phia sau. Dieu nay tranh false failure khi FreeIPA bao rule chua ton tai vi no thuc te khong duoc tao trong luc dry run.
>
> Proxmox realm sync timer role cung bo qua buoc `systemd` enable hoac start cuoi cung trong check mode, vi unit file chi xuat hien trong diff nhung khong duoc ghi that trong dry run.
>
> Linux IPA enrollment cung bi bo qua trong check mode. Repo van thuc hien discovery, hostname resolution, va validate input, nhung upstream `ipaclient` role se khong chay trong dry run.

### 7. Ap dung cau hinh day du

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

Neu workflow Windows tuy chon duoc bat va `vault-windows.yml` dung mat khau rieng, hay chay cung playbook do voi `--vault-id windows@prompt` hoac dung PowerShell wrapper `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` thay vi `--ask-vault-pass`.

## Thu tu rollout

Cho deployment lan dau, hay ap dung stack theo dung thu tu nay:

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

Thu tu nay giup viec troubleshooting de hon rat nhieu so voi chay tat ca cung luc.

Vi du rollout PowerShell co gioi han, chi cho mot Linux guest:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Control rollout mac dinh duoc giu bao thu:

- thay doi truy cap FreeIPA chay voi `serial: 1`
- thay doi Proxmox chay voi `serial: 1`
- hostname resolution, validation, va Linux enrollment chay voi `serial: 10`
- thay doi Windows management chay voi `serial: 10`
- moi rollout path deu dung `max_fail_percentage: 0` theo mac dinh

Hay dieu chinh cac gia tri do trong `inventories/production/group_vars/all/15-rollout.yml`.

## Mo hinh tag

Dung tag de target cac phan rollout on dinh thay vi lien tuc tao them playbook moi.

- core domain: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helper: `windows`, `windows_freeipa`
- FreeIPA access model: `freeipa_access`
- Proxmox subset: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux preparation: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- event-driven VM handling: `event`, `linux_refresh`

Vi du:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Dua VM vao su dung theo su kien

Neu ban muon Proxmox trigger Linux discovery va IPA enrollment ngay sau khi VM start hoac sau migration, hay dung hook va webhook path tuy chon duoc mo ta trong [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

Duong nay dung event-specific playbook `playbooks/proxmox-vm-event.yml`, nen trigger chi xu ly phia Linux guest va FreeIPA. No khong chay lai Proxmox LDAP realm automation hay RBAC cho moi VM event.

Kho nay hien cung co the cai dat hook va webhook stack tuy chon do thong qua `site.yml` hoac `proxmox.yml` khi `proxmox_vm_event_onboarding_enabled: true` da duoc set va cac bien webhook can thiet da san sang.

Proxmox VM hook khong co mot phase `create` rieng biet. Trong thuc te, VM moi thuong duoc nhan ra o su kien `post-start` dau tien, trong khi migration hook co the duoc trigger tren ca source node va destination node.

## Mo hinh inventory

Kho nay dung sau inventory group duoc dinh nghia ro rang va mot group duoc tao o runtime:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Ban cung co the dinh nghia them inventory group rieng cua minh va tham chieu chung trong FreeIPA hostgroup definition. Neu ban muon su dung toan bo tap Linux guest da duoc chuan bi trong FreeIPA hostgroup side, hay tham chieu den group `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> FreeIPA van can final hostname cho tung guest. Neu ban dung IP-only target hoac Proxmox discovery, hay cung cap `ipa_hostname` ro rang hoac dam bao `hostname -f` trong guest tra ve final FQDN. Playbook hien giai quyet hostname do truoc khi tao FreeIPA hostgroup membership.

> [!TIP]
> Khong nen enrollment cac golden template co the tai su dung truc tiep vao FreeIPA. Hay clone VM truoc, dat final hostname, roi moi enroll guest duoc tao ra.

### Cac che do nguon cua may khach Linux

Ban co the nap `linux_ipa_clients` bang ba cach khac nhau.

#### 1. Host inventory tinh

Neu ban da biet ten guest, hay dung inventory entry Ansible thong thuong:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. Khai bao host thu cong trong variables

Dung `linux_ipa_client_hosts` neu ban muon de guest nam ngoai `hosts.yml` hoac khi thu duy nhat ban co la IP:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Luu y:

- neu `name` da la mot hostname co the resolve hoac la FQDN, `ansible_host` la tuy chon
- neu ban chi biet IP, hay dung bat ky alias on dinh nao cho `name`
- khi bo `ipa_hostname`, playbook se fallback ve `hostname -f` trong guest

#### 3. Tu dong kham pha Proxmox VM

Dung discovery neu ban muon playbook tu dong lay Linux guest tu mot hoac nhieu Proxmox node:

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

Luu y:

- discovery them cac VM vao cung group `linux_ipa_clients_runtime` ma cac playbook khac su dung
- discovery theo IP phu thuoc vao QEMU guest agent co kha nang bao cao network interface
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` chi tin ten VM khi no da la FQDN
- set `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` neu ban muon nhung ten Proxmox VM ngan va an toan nhu `Teleport-Server-1` duoc nang cap tu dong thanh hostname hint nhu `teleport-server-1.example.com` thong qua `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` la tuy chon va chu yeu dung cho event-driven hook hoac webhook workflow khi ban muon gioi han discovery vao mot hoac mot vai VMID cu the
- guest van can final hostname, duoc cau hinh san trong VM hoac duoc cung cap qua `ipa_hostname` trong manual definition
- hostname he thong that su cua guest cung phai hop le cho enrollment; cac gia tri tam nhu `localhost.localdomain` phai duoc thay trong VM truoc khi chay `linux-clients` hoac `site`
- khi guest dung short hostname nhu `app-server-01`, ban co the set `linux_ipa_identity_hostname_suffix` va tuy chon `linux_freeipa_enroll_manage_hostname: true` de du an tu giai va ap dung full hostname nhu `app-server-01.example.net` truoc khi enrollment
- khi FreeIPA DNS la noi co tham quyen cho guest hostname cua ban, ban co the set `linux_freeipa_enroll_manage_authoritative_dns: true` de du an sua lai cac record A va PTR lien quan, dong thoi xoa cac record AAAA link-local `fe80::/10` truoc khi enrollment
- khi DNS chua san sang, ban co the set `linux_ipa_manage_etc_hosts: true` va cung cap `linux_ipa_etc_hosts_entries` de role them mot khoi `/etc/hosts` bootstrap duoc quan ly cho IPA server va guest FQDN truoc khi cac enrollment check chay
- `guest_qemu_agent_install_enabled` se cai QEMU Guest Agent tren cac guest da truy cap duoc qua SSH hoac WinRM, thu lai tren Linux guest tro nen truy cap duoc muon hon trong cung workflow, va thu lai sau Linux enrollment de cac workflow Proxmox phu thuoc vao agent co the su dung no
- set `linux_ipa_proxmox_discovery_allowlist_enabled: true` neu ban muon discovery van bat nhung chi co mot tap con guest Proxmox duoc phe duyet ro rang moi duoc dua vao Linux runtime inventory; allowlist co the khop chinh xac theo VMID, IP, va ten
- set `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, hoac `linux_ipa_proxmox_discovery_blacklist_names` neu cac node duoc discovery cung chua cac VM ha tang nhu firewall hoac DNS server ma khong bao gio duoc nhan Linux IPA automation; blacklist match luon thang admission tu ca discovery rong lan allowlist
- voi cac guest Linux duoc Proxmox discovery nhung chua co guest agent hoat dong, hay set `linux_ipa_proxmox_discovery_ansible_user` va cung voi do `linux_ipa_proxmox_discovery_ansible_password` hoac `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` de repo co mot duong SSH first-touch co the dung de cai QEMU Guest Agent
- khi guest duoc discovery dung non-root SSH user, hay set them `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, va `linux_ipa_proxmox_discovery_ansible_become_password`, tru khi tai khoan do da co passwordless `sudo`
- `guest_qemu_agent_install_manage_proxmox_vm_agent` cung bat giao tiep guest agent o phia Proxmox (`qm set <vmid> --agent 1`) cho cac Linux guest duoc discovery boi Proxmox truoc khi duong cai dat trong guest bat dau
- khi Proxmox VM option do thay doi tren VM dang chay, repo mac dinh chi canh bao vi Proxmox co the can start lai VM truoc khi host su dung duoc kenh guest agent; set `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` neu ban muon repo tu reboot cac VM dang chay do
- `linux_ipa_ssh_host_key_policy` mac dinh dung `accept_new` cho cac ket noi toi Linux guest de VM moi duoc discovery co the duoc lien he ma khong phai tat hoan toan host key checking; host key bi thay doi van se fail va can operator xem xet
- `linux_ipa_qga_ssh_bootstrap_enabled` la duong bootstrap khong can reboot duoc uu tien cho guest dua tren Proxmox vi no co the tao mot automation user chuyen dung, chi dung key, thong qua QEMU Guest Agent truoc khi co bat ky SSH login nao
- `linux_ipa_qga_ssh_bootstrap_qm_path` mac dinh la `qm`, va bootstrap flow cung kiem tra cac fallback path pho bien tren Proxmox node truoc khi fail
- guest cho phep `guest-ping` nhung tu choi `guest-exec` se bi skip theo mac dinh trong QGA bootstrap; hay cung cap duong SSH khac cho chung hoac set `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` de fail nhanh
- `linux_ipa_ssh_bootstrap_enabled` tuy chon cai public key cua controller vao Linux guest truoc hostname resolution va enrollment; `linux_ipa_ssh_bootstrap_password` cung duoc dung nhu shared first-touch password fallback cho Linux runtime guest ngay ca khi key-based bootstrap tat
- Linux IPA enrollment se retry cac upstream client join fail do FreeIPA JSON-RPC timeout va expose `linux_ipaclient_kinit_attempts` cho moi truong IPA cham hon hoac ban ron hon
- Linux IPA enrollment cung tu dong them hostname tu inventory `ipa_servers` vao danh sach join server, de client co the dung toan bo tap IPA server thay vi chi mot endpoint cau hinh san
- khi co hon mot IPA server, moi lan retry se lan luot thu cac ung vien IPA server do trong qua trinh Linux client enrollment
- workflow tong hop `site` tao FreeIPA hostgroup truoc roi moi them cac runtime host da enrolled vao sau, de pre-enrollment run khong fail o hostgroup membership chi vi guest chua enrolled

## Be mat cau hinh

Phan lon gia tri nam trong:

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

Cho bo tri theo tung file, xem [docs/VARIABLES.md](../VARIABLES.md).

Nhung ho bien chinh:

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

## Vi du ve chien luoc nhom

Mot mo hinh don gian nhung mo rong tot:

- FreeIPA user group `proxmox-admins`
- FreeIPA user group `linux-ssh-admins`
- FreeIPA hostgroup `linux-all`
- HBAC rule `allow-linux-ssh-admins`
- sudo rule `allow-linux-ssh-admins-sudo`
- Proxmox ACL binding cho synced group `proxmox-admins-ipa`

Hay dien `freeipa_linux_admin_users` trong [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) neu ban muon run tong hop `site.yml` tu dong cap SSH va `sudo` cho mot tap IPA user thong qua group duoc quan ly `linux-ssh-admins`.

Can nho rang Proxmox LDAP sync tao synced group co hau to:

```text
<group-name>-<realm>
```

Neu FreeIPA group cua ban la `proxmox-admins` va Proxmox realm la `ipa`, synced PVE group thu duoc se la:

```text
proxmox-admins-ipa
```

## Bao mat

- luu tat ca secret trong `vault-freeipa.yml` va `vault-proxmox.yml`, khong luu trong inventory variable file dang plaintext
- uu tien mot LDAP bind account chuyen dung, chi read-only cho Proxmox
- uu tien TLS voi certificate verification duoc bat
- giu SSH host key checking duoc bat o moi noi ngoai lab tam thoi
- uu tien `linux_ipa_qga_ssh_bootstrap_enabled` hon shared temporary password khi guest Proxmox cua ban da co QEMU Guest Agent hoat dong
- chi dung `guest_qemu_agent_install_enabled` khi repo da co mot management path hop le vao guest; doi voi Proxmox discovery, dieu nay co nghia la QGA da chay hoac `linux_ipa_proxmox_discovery_ansible_user` cung quyen truy cap bang password hoac key da duoc cau hinh
- neu ban bat Linux SSH bootstrap, hay luu shared bootstrap password trong bien duoc ma hoa va rotate hoac bo no di sau khi key-based access da duoc thiet lap
- khong dung lai IPA admin account lam Proxmox LDAP bind account
- xem xet `proxmox_ldap_filter` va `proxmox_ldap_group_filter` truoc rollout production de tranh import qua nhieu object

Cho lab tam thoi, noi ban co chu y muon bo qua SSH host key verification, hay opt-out theo tung shell session thay vi doi default cua repo:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Tinh idempotent va cac luu y

Kho nay duoc viet de co the chay lai va phan lon la idempotent, nhung van phai duoc thu nghiem trong lab truoc rollout production.

Nhung luu y da biet:

- output CLI cua Proxmox co the khac nhe giua cac release
- bo tri thu muc FreeIPA co tinh linh hoat, nen LDAP filter co the can chinh cho phu hop voi cay cua ban
- cac PVE ACL va role da duoc quan ly thu cong truoc do can duoc doi chieu truoc khi de automation ghi de len
- Proxmox VM auto-discovery phu thuoc guest dang chay va du lieu mang tu QEMU guest agent
- IP-based guest definition van can mot final hostname hop le trong guest, hoac can `ipa_hostname` ro rang
- Proxmox play chay voi privilege escalation, nen non-root SSH user phai co `sudo` hoat dong, va ban phai cung cap become password bang `-K` tru khi user do da co passwordless `sudo`
- neu ban luu `ansible_become_password` trong `vault-proxmox.yml`, ban co the bo qua `-K` vi Ansible se doc sudo password tu bien da ma hoa

## Xac minh

Sau khi rollout thanh cong, hay xac minh final state thay vi gia dinh rang moi duong truy cap deu da dung.

### Trong FreeIPA

- dam bao nhung user group mong doi da ton tai
- dam bao nhung hostgroup mong doi da ton tai
- dam bao nhung HBAC rule mong doi da ton tai va dang bat
- dam bao nhung `sudo` rule mong doi da ton tai va dang bat

### Trong Proxmox

- dam bao LDAP realm da ton tai
- dam bao initial sync da import dung user va group mong doi
- dam bao synced group muc tieu co dung ACL binding mong doi

### Tren mot may khach Linux

- dam bao IPA user duoc phep co the dang nhap
- dam bao user khong duoc phep bi chan boi HBAC
- dam bao IPA admin duoc phep co the chay `sudo -l`
- dam bao home directory duoc tao khi dang nhap lan dau neu `linux_ipaclient_mkhomedir` duoc bat

## Cau truc kho ma nguon

<details>
<summary>Hien cau truc repository</summary>

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

## Phat trien

Nhung helper file chinh duoc dua kem trong repo nay la:

- `.editorconfig`, de giu mac dinh ve khoang trang, encoding, va ket thuc dong dong nhat giua cac editor
- `.gitattributes`, de ep cac text file pho bien dung ket thuc dong `LF`
- `.gitignore`, de ngan inventory sinh ra, du lieu vault, local collection, va rac editor bi dua vao Git
- `.ansible-lint`, de loai tru cac duong dan vendor collection va chi suppress YAML line-length rule
- `.yamllint`, de giu YAML validation dong nhat tren playbook, inventory, va workflow
- `.github/CODEOWNERS`, de dieu huong review ownership vao nhung khu vuc chinh cua repo
- `.github/workflows/ci.yml`, de chay lint va smoke validation tren push va pull request event
- `.pre-commit-config.yaml`, de chay nhanh lint hook truoc commit khi `pre-commit` duoc cai
- `CHANGELOG.md`, de theo doi nhung thay doi quan trong cua repo o mot noi
- `docs/VARIABLES.md`, de mo ta cau truc inventory variable da tach file
- `docs/i18n/`, de chua cac README ban dich; cac file nay phai phan anh day du cau truc section cua `README.md` tieng Anh
- `docs/i18n/TRANSLATION_GUIDE.md`, de giai thich cach giu cac README ban dich dong bo
- `scripts/bootstrap.ps1` va `scripts/bootstrap.sh`, de cai nhung collection can thiet vao duong dan local `collections/` va ap dung compatibility patch cho ansible-core 2.24+
- `scripts/patch_freeipa_collection.py`, de viet lai deprecated import trong FreeIPA collection da pin de no van tuong thich voi cac ansible-core version moi hon
- `scripts/lint.py`, de cung cap mot cross-platform lint entry point duoc dung o local, trong CI, va trong pre-commit
- `scripts/smoke-test.py`, de chay example inventory validation va syntax check ma khong dong vao ha tang that, bao gom ca coverage cho cac playbook Windows rieng
- `scripts/check_translations.py`, de kiem toan README ban dich theo metadata, section structure parity, va muc do bao phu noi dung toi thieu so voi README tieng Anh chuan
- `scripts/lint.ps1` va `scripts/lint.sh`, de gom lint va smoke workflow tai local
- `scripts/proxmox_event_webhook.py`, de dong vai tro webhook tuy chon o phia controller cho Proxmox VM event
- `scripts/proxmox-vm-hook.pl`, de dong vai tro Proxmox VM hook tuy chon duoc cai len node
- `scripts/run-playbook.ps1`, de cung cap mot wrapper `ansible-playbook` thong nhat tren moi truong Windows va PowerShell
- `scripts/vault.ps1` va `scripts/vault.sh`, de ho tro tao, sua, xem, va ma hoa cac vault file tach rieng theo domain
- `tests/`, de giu verification surface cua repository, bat dau tu tai lieu smoke-test
- `CONTRIBUTING.md`, de tai lieu hoa contribution va validation workflow duoc ky vong
- `SECURITY.md`, de tai lieu hoa cach bao cao lo hong va xu ly thong tin nhay cam ve bao mat

Neu controller cua ban da cai `ansible-lint`:

```bash
ansible-lint
```

De chay repository smoke checks truc tiep:

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

De chay full local lint pass:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

De bat fast lint hook truoc moi commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper hien cung ho tro truc tiep cac operator option pho bien:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Cac huong mo rong tiep theo

Nhung phan mo rong hop ly tiep theo thuong la:

- Packer pipeline cho Linux template da san sang cho IPA
- AWX hoac Automation Controller job template va scheduling cho rollout tong hop
- mo hinh tenant va pool manh hon cho Proxmox
- AD trust workflow cho Windows RDP hoac moi truong identity lai

## Giay phep

Phat hanh theo [MIT License](../../LICENSE).
