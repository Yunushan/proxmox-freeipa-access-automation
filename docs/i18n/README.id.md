# Otomasi Akses Proxmox + FreeIPA

Halaman ini menyediakan terjemahan penuh atas struktur [README.md](../../README.md). Versi bahasa Inggris tetap menjadi sumber kanonik, tetapi terjemahan ini mencakup bagian utama yang sama.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Mengapa proyek ini ada

Gunakan repositori ini jika Anda sudah memiliki:

- deployment FreeIPA yang sehat
- cluster Proxmox VE
- guest Linux yang harus menggunakan autentikasi terpusat
- akun layanan khusus untuk bind LDAP Proxmox
- model grup yang jelas untuk admin dan operator

Prinsip utamanya adalah menjadikan FreeIPA sebagai sumber kebenaran untuk identitas dan akses. Proxmox memakai direktori itu melalui LDAP realm, guest Linux bergabung ke FreeIPA melalui role `ipaclient`, dan kontrol SSH, HBAC, serta `sudo` tetap terpusat.

## Yang Anda dapatkan

- manajemen grup pengguna, hostgroup, aturan HBAC, dan aturan `sudo` FreeIPA
- konfigurasi LDAP realm Proxmox yang terhubung ke FreeIPA
- sinkronisasi realm berkala dari satu node cluster yang ditetapkan
- binding RBAC Proxmox untuk grup yang tersinkron
- enrollment Linux dari inventory statis, definisi host manual, atau discovery Proxmox
- bootstrap SSH tanpa reboot secara opsional melalui QEMU Guest Agent
- instalasi QEMU Guest Agent opsional melalui SSH atau WinRM untuk guest yang sudah dapat dijangkau
- bootstrap kunci publik SSH opsional untuk first-touch
- refresh cache SSSD otomatis setelah perubahan model akses FreeIPA
- onboarding berbasis event opsional untuk `post-start` dan `post-migrate`

## Cakupan

| Termasuk | Tidak termasuk |
| --- | --- |
| Model akses FreeIPA | Windows domain join |
| Konfigurasi LDAP realm Proxmox | Deployment FreeRADIUS |
| RBAC Proxmox dari grup tersinkron | Pembuatan siklus hidup pengguna FreeIPA penuh |
| Enrollment Linux IPA client | Semua edge case multi-tenant Proxmox |

## Arsitektur

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## Persyaratan

### Controller

- Ansible Core 2.14+
- keterjangkauan SSH ke node Proxmox utama, server IPA, dan klien Linux
- `sudo` atau `root` bila diperlukan
- jika QGA SSH bootstrap aktif, QEMU Guest Agent harus sudah aktif di guest
- jika fallback Windows aktif, host yang dapat dijangkau harus berada di `windows_qemu_guest_agent_clients`
- jika bootstrap SSH Linux aktif, controller membutuhkan keypair SSH dan jalur login awal berbasis kata sandi

### Target

- Proxmox VE 6.x atau lebih baru pada host di `proxmox_primary`
- FreeIPA dapat dijangkau dari Proxmox dan klien Linux
- DNS dan sinkronisasi waktu yang benar
- untuk `proxmox_primary`, gunakan `root` atau user SSH dengan `sudo` untuk `pveversion`, `pvesh`, dan `pveum`
- jika memakai Proxmox discovery, guest harus menampilkan IP yang dapat dipakai melalui QEMU Guest Agent

## Port jaringan

Port utama:

- `22/TCP` untuk SSH
- `53/TCP,UDP` untuk DNS IPA
- `88/TCP,UDP` dan `464/TCP,UDP` untuk Kerberos
- `389/TCP` untuk LDAP
- `linux_freeipa_enroll_https_port`, default `443/TCP`
- `636/TCP` untuk `ldaps`

## Kompatibilitas

- ditujukan untuk Proxmox VE 6.x dan yang lebih baru
- major yang didukung secara default: `6`, `7`, `8`, `9`, `10`
- bisa dioverride dengan `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions` default `true`

## Mulai cepat

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

Sunting `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml`, dan `vault-proxmox.yml` sesuai lingkungan Anda.

## Urutan rollout

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Default rollout bersifat konservatif: `serial: 1` untuk FreeIPA dan Proxmox, `serial: 10` untuk Linux, dan `max_fail_percentage: 0`.

## Model tag

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Onboarding VM berbasis event

Jika Anda ingin Proxmox memicu discovery Linux dan enrollment IPA segera setelah `post-start` atau `post-migrate`, gunakan alur hook/webhook opsional di [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md). Alur ini memakai `playbooks/proxmox-vm-event.yml`, tidak menjalankan ulang LDAP realm atau RBAC setiap event, dan menangani VM baru saat `post-start` pertama.

## Model inventory

Grup utama:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

Bahkan pada target IP-only atau discovery Proxmox, guest tetap memerlukan FQDN akhir lewat `ipa_hostname` atau `hostname -f`.

### Mode sumber Linux

1. host statis di inventory
2. definisi manual di `linux_ipa_client_hosts`
3. discovery Proxmox melalui `linux_ipa_proxmox_discovery_*`

Catatan penting: discovery bergantung pada data jaringan QEMU Guest Agent, `linux_ipa_proxmox_discovery_vmids` berguna untuk alur event-driven, nama pendek dapat dilengkapi dengan `linux_ipa_identity_hostname_suffix`, authoritative DNS dapat diperbaiki dengan `linux_freeipa_enroll_manage_authoritative_dns`, dan `/etc/hosts` bootstrap tersedia lewat `linux_ipa_manage_etc_hosts`.

## Permukaan konfigurasi

File utama:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Contoh strategi grup

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## Keamanan

- simpan rahasia hanya di file vault
- gunakan akun bind LDAP read-only khusus untuk Proxmox jika memungkinkan
- utamakan TLS dengan verifikasi sertifikat
- jangan matikan pemeriksaan host key SSH di luar lab sementara

## Idempotensi dan catatan

Repositori ini dirancang agar dapat dijalankan ulang, tetapi tetap harus divalidasi di lab sebelum produksi. Batasan yang diketahui mencakup variasi output CLI Proxmox, penyesuaian filter LDAP, ketergantungan discovery pada guest yang sedang hidup dan data QGA, serta kebutuhan hostname final yang valid untuk target berbasis IP.

## Verifikasi

- di FreeIPA, cek grup, hostgroup, HBAC, dan `sudo`
- di Proxmox, cek LDAP realm, sync awal, dan binding ACL
- di guest Linux, cek login yang diizinkan, penolakan HBAC, `sudo -l`, dan pembuatan home

## Tata letak repositori

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## Pengembangan

Repositori ini mencakup `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, workflow CI, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, dan `scripts/vault.*`.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## Ekstensi berikutnya

- pipeline Packer untuk template Linux siap IPA
- template dan jadwal job AWX
- model tenant dan pool Proxmox terpisah
- alur Windows atau AD-trust untuk lingkungan berbasis RDP

## Lisensi

Dirilis di bawah [MIT License](../../LICENSE).
