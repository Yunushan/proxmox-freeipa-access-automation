# Otomasi Akses Proxmox + FreeIPA

Halaman ini menyediakan terjemahan penuh dan setara secara struktural dari [README.md](../../README.md). Versi bahasa Inggris tetap menjadi sumber kanonik, tetapi versi bahasa Indonesia ini harus mencakup cakupan operasional yang sama untuk operator berbahasa Indonesia.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## Bahasa

Versi bahasa Inggris adalah sumber kanonik untuk dokumentasi lengkap. README terjemahan penuh juga tersedia dalam 20 bahasa tambahan.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

[Tiếng Việt](README.vi.md) | [Translation Index](README.md) | [Translation Guide](TRANSLATION_GUIDE.md)

Repositori ini memperlakukan **FreeIPA sebagai source of truth** untuk identitas dan akses. Proxmox mengonsumsi direktori itu melalui LDAP realm, guest Linux bergabung ke FreeIPA melalui role upstream `ipaclient`, dan akses tetap terpusat melalui grup tersinkron, HBAC, dan aturan sudo alih-alih tersebar sebagai akun lokal di setiap VM.

> [!IMPORTANT]
> Proyek ini **tidak** memakai FreeRADIUS sebagai sumber identitas, **tidak** membuat user lokal di dalam setiap VM, dan **tidak** mencoba menangani semua edge case izin Proxmox yang mungkin ada.

## Mengapa proyek ini ada

Gunakan repositori ini jika Anda sudah memiliki:

- deployment FreeIPA yang sehat
- cluster Proxmox VE
- guest Linux yang harus menggunakan autentikasi terpusat
- akun layanan khusus untuk bind LDAP Proxmox
- model grup yang jelas untuk admin dan operator

Prinsip utamanya adalah menjadikan FreeIPA sebagai sumber kebenaran untuk identitas dan akses. Proxmox memakai direktori itu melalui LDAP realm, guest Linux bergabung ke FreeIPA melalui role upstream `ipaclient`, dan kontrol SSH, HBAC, serta `sudo` tetap terpusat, bukan tersebar sebagai akun lokal di setiap VM.

Repositori ini cocok ketika Anda ingin onboarding dan offboarding kira-kira mengikuti urutan berikut:

1. membuat atau memperbarui user dan grup di FreeIPA
2. menyinkronkan identitas tersebut ke Proxmox
3. menerapkan role dan ACL Proxmox dari grup yang tersinkron
4. mengizinkan akses guest Linux melalui login FreeIPA, HBAC, dan aturan sudo

## Yang Anda dapatkan

- manajemen grup pengguna, hostgroup, aturan HBAC, dan aturan `sudo` FreeIPA
- login shell default FreeIPA untuk administrator Linux
- konfigurasi LDAP realm Proxmox yang terhubung ke FreeIPA
- sinkronisasi realm Proxmox yang berulang dari satu node cluster yang ditetapkan
- binding RBAC Proxmox untuk grup direktori yang tersinkron
- enrollment guest Linux ke FreeIPA melalui inventaris statis, target berbasis IP, atau discovery VM Proxmox
- bootstrap SSH tanpa reboot secara opsional melalui QEMU Guest Agent Proxmox
- pengaktifan opsional kanal komunikasi guest agent di sisi Proxmox untuk guest Linux yang dikelola lewat Proxmox
- instalasi opsional QEMU Guest Agent melalui SSH atau WinRM sebagai fallback untuk guest yang sudah dapat dijangkau, menjadi dapat dijangkau setelah bootstrap, atau dicoba lagi setelah enrollment Linux
- laporan readiness Linux opsional untuk jangkauan SSH dan status QEMU Guest Agent Proxmox
- workflow terpisah dan opsional untuk domain membership Windows 10/11 dan Windows Server melalui Active Directory
- workflow Windows terbatas dan sadar FreeIPA untuk trust CA IPA, bootstrap hosts file, dan validasi jangkauan layanan IPA
- bootstrap kunci publik SSH opsional untuk first-touch ke guest Linux
- refresh cache SSSD otomatis pada klien Linux terkelola setelah perubahan model akses FreeIPA
- onboarding Linux berbasis event secara opsional dari hook VM Proxmox dan pemicu webhook

## Cakupan

| Termasuk | Tidak termasuk |
| --- | --- |
| Model akses FreeIPA | Deployment FreeRADIUS |
| Konfigurasi LDAP realm Proxmox | Pembuatan siklus hidup pengguna FreeIPA penuh |
| RBAC Proxmox dari grup tersinkron | Cakupan penuh semua edge case multi-tenant Proxmox |
| Enrollment klien Linux ke IPA | Login native Windows langsung terhadap FreeIPA |
| Workflow domain membership AD untuk Windows | Otomasi objek AD atau GPO secara luas |
| Workflow helper FreeIPA terbatas untuk Windows | Menganggap helper Windows berbasis FreeIPA setara dengan AD |

## Workflow Windows

Dukungan Windows diterapkan sebagai workflow terpisah, bukan dicampur ke dalam alur enrollment Linux ke IPA.

- `windows_qemu_guest_agent_clients` tetap dikhususkan untuk tugas helper QEMU Guest Agent yang opsional.
- aktifkan workflow dengan `windows_domain_membership_enabled: true` di `10-features.yml`
- `windows_management_clients` adalah grup Windows terpisah yang dipakai oleh `playbooks/windows-management.yml` dan tahap Windows opsional di `playbooks/site.yml`
- login Windows yang sesungguhnya dikelola melalui domain membership Active Directory; pada lingkungan yang berpusat pada FreeIPA, gabungkan host Windows ke sisi AD dari trust FreeIPA-AD daripada mencoba menggabungkan Windows langsung ke FreeIPA

Windows join berbasis FreeIPA saja tidak didukung oleh repositori ini. Tanpa Active Directory atau trust FreeIPA-AD, sisi Windows hanya terbatas pada tugas helper seperti pengelolaan guest yang sudah dapat dijangkau dan instalasi opsional QEMU Guest Agent.

Jika Anda tetap menginginkan jalur Windows yang terbatas dan sadar FreeIPA tanpa domain join, aktifkan `windows_freeipa_helpers_enabled: true` dan gunakan `windows_freeipa_helper_clients` dengan `playbooks/windows-freeipa-helpers.yml`. Workflow helper ini dapat menanamkan trust ke CA IPA, mengambil CA IPA secara otomatis untuk bootstrap, mem-pin thumbprint CA yang diharapkan secara opsional, mengelola entri hosts file secara opsional, memvalidasi DNS IPA dan port TCP penting, memvalidasi jangkauan HTTPS dari Windows, memvalidasi sumber waktu Windows terhadap endpoint terkait IPA, mengelola keanggotaan grup lokal Windows, serta memasang atau mengekspos OpenSSH Server secara opsional, tetapi tidak menyediakan login native Windows terhadap FreeIPA.

Jika Anda ingin pemeriksaan readiness tanpa melakukan perubahan untuk grup helper yang sama, jalankan `playbooks/windows-freeipa-validate.yml`. Workflow ini mempertahankan jalur validasi dan ringkasan, tetapi memaksa impor CA, perubahan hosts file, perubahan grup lokal, dan manajemen OpenSSH menjadi non-mutating untuk run tersebut.

Workflow ini menargetkan guest Windows 10/11 dan Windows Server yang dapat dijangkau lewat WinRM atau PSRP.

## Arsitektur

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

Penjelasan desain yang lebih panjang tersedia di [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Persyaratan

### Controller

- Ansible Core 2.14 atau lebih baru
- jangkauan SSH ke node Proxmox utama, server IPA, dan klien Linux
- jangkauan WinRM atau PSRP ke guest Windows bila Anda menggunakan workflow Windows
- `sudo` atau `root` bila diperlukan
- jika QGA SSH bootstrap aktif, QEMU Guest Agent harus sudah berjalan di dalam guest
- jika fallback instalasi guest agent untuk Windows aktif, host Windows yang dapat dijangkau harus berada di `windows_qemu_guest_agent_clients`
- jika domain membership Windows aktif, host Windows yang dapat dijangkau harus berada di `windows_management_clients` dan Anda harus menyediakan kredensial join AD
- jika tugas helper FreeIPA untuk Windows aktif, host Windows yang dapat dijangkau harus berada di `windows_freeipa_helper_clients`
- jika bootstrap SSH Linux aktif, controller membutuhkan pasangan kunci SSH dan jalur login awal berbasis kata sandi untuk akun guest yang digunakan Ansible

### Target

- Proxmox VE 6.x atau lebih baru pada host di `proxmox_primary`
- FreeIPA dapat dijangkau dari Proxmox dan klien Linux
- guest Windows 10/11 dan Windows Server dapat dikelola lewat workflow Windows terpisah bila dapat dijangkau via WinRM atau PSRP
- DNS dan sinkronisasi waktu harus benar
- untuk `proxmox_primary`, gunakan `root` atau user SSH dengan `sudo` untuk `pveversion`, `pvesh`, dan `pveum`
- jika Anda memakai domain membership Windows, guest Windows target harus dapat menjangkau domain controller AD yang sesuai
- jika Anda memakai workflow helper FreeIPA terbatas untuk Windows, guest Windows target harus dapat menjangkau server IPA yang sesuai
- jika memakai Proxmox discovery, guest harus menampilkan IP yang dapat dipakai melalui QEMU Guest Agent

## Port jaringan

Tabel ini mencantumkan port jaringan yang dipakai oleh controller repositori ini, otomasi LDAP Proxmox, dan alur enrollment Linux ke IPA.
Tabel ini sengaja dibatasi pada permukaan yang benar-benar dipakai proyek ini, bukan matriks replikasi server-ke-server FreeIPA secara penuh.

| Nama | Port | Protokol | Sumber | Tujuan | Diperlukan saat | Tujuan |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Controller Ansible | Node Proxmox, server IPA, guest Linux | Selalu | Konektivitas Ansible |
| WinRM | `5985`, `5986` | `TCP` | Controller Ansible | Guest Windows | Saat manajemen Windows aktif | Konektivitas Ansible ke guest Windows |
| DNS | `53` | `TCP`, `UDP` | Guest Linux | Server DNS IPA | Saat guest Linux memakai DNS IPA | Resolusi record IPA dan nama eksternal via IPA DNS |
| Kerberos | `88` | `TCP`, `UDP` | Guest Linux | Server IPA | Enrollment dan login Linux IPA | Autentikasi Kerberos |
| LDAP | `389` | `TCP` | Guest Linux | Server IPA | Enrollment dan login Linux IPA | LDAP dan discovery klien FreeIPA |
| HTTPS | `linux_freeipa_enroll_https_port`, default `443` | `TCP` | Guest Linux | Server IPA | Enrollment Linux IPA | Verifikasi web/API IPA selama instalasi klien |
| Kerberos Password | `464` | `TCP`, `UDP` | Guest Linux | Server IPA | Enrollment Linux IPA dan operasi kata sandi | Operasi kata sandi dan keytab Kerberos |
| LDAPS | `636` | `TCP` | Node utama Proxmox | Server IPA atau LDAP | Saat LDAP realm Proxmox memakai mode default `ldaps` | Koneksi LDAP realm Proxmox |

Catatan:

- `LDAPS 636/TCP` adalah default repositori karena `proxmox_ldap_mode` menggunakan `ldaps` secara default. Jika Anda mengubah mode atau port LDAP, izinkan `proxmox_ldap_port` yang benar-benar Anda gunakan.
- `WinRM` biasanya memakai `5986/TCP` untuk HTTPS atau `5985/TCP` untuk HTTP, tergantung konfigurasi transport Windows Anda.
- `DNS 53/TCP,UDP` hanya diperlukan bila guest Linux memakai server IPA sebagai resolver.
- `Kerberos 88` dan `Kerberos Password 464` sama-sama memerlukan `TCP` dan `UDP`.
- Domain join Active Directory juga memerlukan port Windows-to-domain-controller standar, tetapi matriks itu bergantung pada lingkungan dan tidak dirinci di sini.
- Sinkronisasi waktu tetap diperlukan agar Kerberos bekerja andal, tetapi sumber NTP bergantung pada lingkungan dan tidak dikelola oleh repositori ini.

## Kompatibilitas

Otomasi Proxmox di repositori ini ditulis di sekitar antarmuka `pveum` dan `pvesh` untuk realm dan RBAC yang dipakai oleh Proxmox VE 6.x dan yang lebih baru.

- major yang didukung secara default: `6`, `7`, `8`, `9`, `10`
- validasi memeriksa versi Proxmox yang terdeteksi melalui `pveversion`
- daftar versi yang didukung dapat disesuaikan dengan `proxmox_supported_major_versions` bila Anda perlu mempersempit atau memperluasnya di lingkungan Anda
- `proxmox_allow_future_major_versions` bernilai `true` secara default, sehingga major versi di atas versi tertinggi yang sudah diuji juga lolos validasi secara default
- major versi masa depan tetap harus diperlakukan sebagai kandidat kompatibilitas sampai antarmuka Proxmox yang dipublikasikan benar-benar diverifikasi terhadap otomasi ini
- versi lama seperti `1` sampai `5` tidak diklaim sebagai dukungan yang sudah teruji oleh repositori publik ini; jika Anda menambahkannya secara lokal, perlakukan itu sebagai override kompatibilitas yang eksplisit dan validasi workflow penuh terlebih dahulu di lab

Contoh override lokal untuk lab legacy:

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

## Mulai cepat

Contoh di bawah memakai perintah shell. Padanan PowerShell disertakan saat relevan.

### 1. Salin inventaris contoh dan template vault

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Opsional jika Anda berencana mengelola guest Windows:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Opsional jika Anda berencana mengelola guest Windows:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Sunting file yang spesifik untuk lingkungan

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` bila Anda memakai manajemen Windows
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` bila Anda memakai manajemen Windows

Selain pengaturan IPA dan Proxmox, pilih satu mode sumber untuk guest Linux:

- entri inventaris statis di bawah `linux_ipa_clients`
- entri `linux_ipa_client_hosts` di `group_vars/all/30-linux-clients.yml`
- discovery VM Proxmox dengan `linux_ipa_proxmox_discovery_enabled: true`

Untuk enrollment Linux ke IPA, bedakan nilai domain dan daftar server:

- `ipaclient_domain` adalah domain DNS IPA bersama, misalnya `example.com`
- `linux_ipa_servers` berisi hostname server IPA, misalnya `ipa01.example.com`

Jika Anda ingin SSH ke Proxmox memakai user biasa yang memiliki `sudo`, bukan `root`, atur itu di bawah `proxmox_primary` dalam `hosts.yml` dan simpan kata sandi sudo di `vault-proxmox.yml`:

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

Dalam konfigurasi tersebut, `vault_proxmox_become_password` adalah kata sandi yang biasanya Anda ketik untuk `sudo` di host Proxmox.

### 3. Enkripsi file vault

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

Tambahkan `inventories/production/group_vars/all/vault-windows.yml` ke perintah yang sama saat Anda mengaktifkan workflow Windows.

Atau gunakan wrapper helper, yang secara default memakai vault ID terpisah dan membuat file vault kerja dari template contoh jika diperlukan:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Jika Anda ingin kata sandi terpisah per domain saat menjalankan playbook, gunakan vault ID alih-alih `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Jika workflow Windows opsional juga memakai kata sandi vault sendiri, tambahkan `windows@prompt` ke perintah yang sama.

Gunakan `-AskVaultPass` hanya bila semua file vault yang dipakai playbook itu berbagi kata sandi yang sama.

### 4. Instal koleksi yang diperlukan

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Atau langsung:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

Jika Anda menginstal `freeipa.ansible_freeipa` sebelum repositori ini menambahkan patch kompatibilitas, jalankan ulang salah satu helper bootstrap atau jalankan `python .\scripts\patch_freeipa_collection.py` sekali untuk mem-patch instalasi collection di level user juga.

Saat Anda menggunakan `scripts/run-playbook.ps1`, ia menjalankan helper patch itu secara otomatis sebelum `ansible-playbook`.

### 5. Validasi terlebih dahulu

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Jika Anda ingin memvalidasi hanya jalur Windows FreeIPA helper-only tanpa melakukan perubahan pada host:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Jika Anda menginginkan audit readiness Linux yang read-only untuk melaporkan guest runtime mana yang dapat dijangkau via SSH dan guest hasil discovery Proxmox mana yang merespons melalui QEMU Guest Agent:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Laporan readiness secara default ditulis ke `.ansible/linux-readiness-report.json`.
Interpretasikan field utamanya seperti ini:

- `ssh.ready=true`: jalur SSH Ansible yang saat ini dikonfigurasi berhasil dari controller
- `ssh.promptless=true`: probe SSH berhasil tanpa `ansible_password`, jadi jalur itu non-interaktif untuk Ansible
- `ssh.auth_mode=password_configured`: probe menggunakan `sshpass` karena host memiliki `ansible_password`
- `ssh.auth_mode=key_or_agent`: probe berhasil dalam SSH batch mode tanpa `ansible_password`
- `qga.status=available`: `qm guest ping` berhasil pada node Proxmox pemilik VM
- `qga.status=disabled`: konfigurasi VM Proxmox tidak mengaktifkan QEMU Guest Agent
- `qga.status=configured_unresponsive`: guest agent diaktifkan dalam konfigurasi Proxmox tetapi tidak merespons
- `qga.status=node_unreachable`: controller tidak dapat menjangkau node Proxmox pemilik VM untuk probe
- `qga.status=not_applicable`: host tidak dibuat oleh Proxmox discovery, jadi tidak ada probe QGA yang dicoba

Contoh inspeksi cepat:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. Opsional: pratinjau perubahan yang direncanakan

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Perlakukan check mode sebagai pratinjau parsial, bukan simulasi penuh. Repositori ini memakai perintah CLI langsung untuk sebagian konfigurasi Proxmox dan role upstream FreeIPA client untuk enrollment Linux, jadi `--check` berguna tetapi tidak sepenuhnya otoritatif.
>
> Untuk aturan HBAC FreeIPA, check mode memvalidasi langkah definisi aturan tetapi melewati aksi enable atau disable sesudahnya. Ini mencegah false failure ketika FreeIPA melaporkan aturan tidak ada karena memang tidak benar-benar dibuat selama dry run.
>
> Role timer sinkronisasi realm Proxmox juga melewati langkah akhir `systemd` enable atau start pada check mode, karena unit file hanya muncul di diff tetapi tidak benar-benar ditulis selama dry run.
>
> Enrollment Linux ke IPA juga dilewati dalam check mode. Repositori tetap melakukan discovery, resolusi hostname, dan validasi input, tetapi role upstream `ipaclient` tidak dieksekusi selama dry run.

### 7. Terapkan konfigurasi penuh

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

Jika workflow Windows opsional aktif dan `vault-windows.yml` memakai kata sandi terpisah, jalankan playbook yang sama dengan `--vault-id windows@prompt` atau wrapper PowerShell `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` alih-alih `--ask-vault-pass`.

## Urutan rollout

Untuk deployment pertama, terapkan stack dalam urutan ini:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Opsional jika Anda mengelola guest Windows:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Opsional jika Anda ingin workflow helper Windows FreeIPA yang terbatas:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Opsional jika Anda hanya ingin cakupan validasi untuk workflow helper:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

Urutan ini membuat troubleshooting jauh lebih mudah daripada menjalankan semuanya sekaligus.

Contoh rollout PowerShell terbatas, misalnya untuk satu guest Linux:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Kontrol rollout default bersifat konservatif:

- perubahan akses FreeIPA berjalan dengan `serial: 1`
- perubahan Proxmox berjalan dengan `serial: 1`
- resolusi hostname, validasi, dan enrollment Linux berjalan dengan `serial: 10`
- perubahan manajemen Windows berjalan dengan `serial: 10`
- semua jalur rollout menggunakan `max_fail_percentage: 0` secara default

Sesuaikan nilai-nilai itu di `inventories/production/group_vars/all/15-rollout.yml`.

## Model tag

Gunakan tag untuk menargetkan irisan rollout yang stabil daripada terus membuat playbook tambahan.

- domain inti: `freeipa`, `proxmox`, `linux`, `validate`
- domain Windows: `windows`, `windows_domain`
- helper Windows FreeIPA: `windows`, `windows_freeipa`
- model FreeIPA: `freeipa_access`
- subset Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- persiapan Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- enrollment Linux: `linux_enroll`
- penanganan VM berbasis event: `event`, `linux_refresh`

Contoh:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Onboarding VM berbasis event

Jika Anda ingin Proxmox memicu discovery Linux dan enrollment IPA segera setelah VM start atau setelah migrasi, gunakan alur hook dan webhook opsional yang dijelaskan di [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

Jalur ini memakai playbook event khusus `playbooks/proxmox-vm-event.yml`, sehingga pemicu hanya menangani sisi guest Linux dan FreeIPA. Ia tidak menjalankan ulang otomasi LDAP realm atau RBAC Proxmox pada setiap event VM.

Repositori ini sekarang juga dapat memasang stack hook dan webhook opsional tersebut melalui `site.yml` atau `proxmox.yml` ketika `proxmox_vm_event_onboarding_enabled: true` telah disetel dan variabel webhook yang diperlukan sudah tersedia.

Hook VM Proxmox tidak menyediakan fase `create` yang terpisah. Dalam praktiknya, VM baru biasanya tertangkap pada event `post-start` pertama, sementara hook migrasi dapat dipicu pada node sumber maupun node tujuan.

## Model inventaris

Repositori ini menggunakan enam grup inventaris yang didefinisikan dan satu grup yang dihasilkan saat runtime:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Anda juga dapat mendefinisikan grup inventaris tambahan sendiri dan mereferensikannya di definisi hostgroup FreeIPA. Jika Anda ingin menggunakan keseluruhan himpunan guest Linux yang sudah dipersiapkan dari sisi hostgroup FreeIPA, referensikan grup `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> FreeIPA tetap membutuhkan hostname akhir untuk setiap guest. Jika Anda memakai target IP-only atau discovery Proxmox, berikan `ipa_hostname` secara eksplisit atau pastikan `hostname -f` di dalam guest mengembalikan FQDN akhir. Playbook sekarang menyelesaikan hostname itu sebelum menyusun keanggotaan hostgroup FreeIPA.

> [!TIP]
> Jangan melakukan enrollment template golden yang dapat dipakai ulang langsung ke FreeIPA. Kloning dulu VM-nya, beri hostname akhir, lalu enroll guest hasilnya.

### Mode sumber untuk guest Linux

Anda dapat mengisi `linux_ipa_clients` dengan tiga cara berbeda.

#### 1. Host statis di inventaris

Jika Anda sudah mengetahui nama guest, gunakan entri inventaris Ansible biasa:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. Definisi host manual di variabel

Gunakan `linux_ipa_client_hosts` bila Anda ingin menjaga guest tetap di luar `hosts.yml` atau ketika yang Anda miliki hanyalah IP:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Catatan:

- jika `name` sudah berupa hostname yang dapat di-resolve atau FQDN, `ansible_host` bersifat opsional
- jika Anda hanya mengetahui IP, gunakan alias stabil apa pun untuk `name`
- ketika `ipa_hostname` dihilangkan, playbook akan fallback ke `hostname -f` di dalam guest

#### 3. Auto-discovery VM Proxmox

Gunakan discovery jika Anda ingin playbook menarik guest Linux dari satu atau lebih node Proxmox:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Opsional: batasi otomasi berbasis discovery hanya ke guest yang disetujui.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Opsional: selalu kecualikan guest infrastruktur atau sensitif walau
# discovery node yang luas diaktifkan.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# Pengaturan SSH first-touch opsional untuk guest yang discovered saat guest
# agent belum berjalan dan repositori perlu masuk via SSH untuk memasangnya.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

Catatan:

- discovery menambahkan VM ke grup `linux_ipa_clients_runtime` yang sama seperti dipakai oleh playbook lain
- discovery IP bergantung pada QEMU guest agent yang dapat melaporkan antarmuka jaringan
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` hanya mempercayai nama VM yang sudah berupa FQDN
- set `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` bila Anda juga ingin nama VM Proxmox pendek yang aman seperti `Teleport-Server-1` dipromosikan otomatis menjadi hint hostname seperti `teleport-server-1.example.com` melalui `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` bersifat opsional dan terutama dipakai oleh workflow hook atau webhook berbasis event untuk membatasi discovery ke satu atau beberapa VMID tertentu
- guest tetap membutuhkan hostname akhir, baik yang sudah dikonfigurasi di dalam VM atau diberikan melalui `ipa_hostname` pada definisi manual
- hostname sistem guest yang sebenarnya juga harus valid untuk enrollment; nilai placeholder seperti `localhost.localdomain` harus diganti di VM sebelum menjalankan `linux-clients` atau `site`
- ketika guest memakai hostname pendek seperti `app-server-01`, Anda dapat mengatur `linux_ipa_identity_hostname_suffix` dan opsional `linux_freeipa_enroll_manage_hostname: true` agar proyek menyelesaikan dan menerapkan hostname penuh seperti `app-server-01.example.net` sebelum enrollment
- ketika DNS FreeIPA bersifat otoritatif untuk hostname guest Anda, Anda dapat mengatur `linux_freeipa_enroll_manage_authoritative_dns: true` agar proyek memperbaiki record A dan PTR guest yang relevan serta menghapus record AAAA link-local `fe80::/10` sebelum enrollment
- ketika DNS belum siap, Anda dapat mengatur `linux_ipa_manage_etc_hosts: true` dan menyediakan `linux_ipa_etc_hosts_entries` agar role menambahkan blok bootstrap `/etc/hosts` terkelola untuk server IPA dan FQDN guest sebelum pemeriksaan enrollment
- `guest_qemu_agent_install_enabled` memasang QEMU Guest Agent pada guest yang sudah dapat dijangkau via SSH atau WinRM, mencoba ulang pada guest Linux yang menjadi dapat dijangkau kemudian dalam workflow yang sama, dan mencoba lagi setelah enrollment Linux sehingga workflow Proxmox yang bergantung pada agent dapat memakainya
- set `linux_ipa_proxmox_discovery_allowlist_enabled: true` bila Anda ingin discovery tetap aktif tetapi hanya subset guest Proxmox yang benar-benar disetujui yang masuk ke inventaris runtime Linux; allowlist dapat mencocokkan VMID, IP, dan nama secara tepat
- set `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips`, atau `linux_ipa_proxmox_discovery_blacklist_names` bila node dengan discovery juga menampung VM infrastruktur seperti firewall atau server DNS yang tidak boleh menerima otomasi Linux IPA; kecocokan blacklist selalu menang atas admission dari discovery luas maupun allowlist
- untuk guest Linux hasil discovery Proxmox yang belum memiliki guest agent fungsional, set `linux_ipa_proxmox_discovery_ansible_user` dan juga `linux_ipa_proxmox_discovery_ansible_password` atau `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` agar repositori punya jalur SSH first-touch yang dapat dipakai untuk memasang QEMU Guest Agent
- ketika guest hasil discovery itu memakai user SSH non-root, set juga `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method`, dan `linux_ipa_proxmox_discovery_ansible_become_password`, kecuali akun itu sudah memiliki `sudo` tanpa kata sandi
- `guest_qemu_agent_install_manage_proxmox_vm_agent` juga mengaktifkan komunikasi guest agent di sisi Proxmox (`qm set <vmid> --agent 1`) untuk guest Linux berbasis Proxmox sebelum jalur instalasi di dalam guest berjalan
- ketika opsi VM Proxmox itu berubah pada VM yang sedang berjalan, repositori secara default hanya memberi peringatan karena Proxmox mungkin memerlukan start VM baru sebelum host bisa memakai kanal guest agent; set `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` bila Anda ingin repositori me-reboot VM yang sedang berjalan itu secara otomatis
- `linux_ipa_ssh_host_key_policy` secara default memakai `accept_new` untuk koneksi ke guest Linux sehingga VM baru hasil discovery dapat dihubungi tanpa mematikan pemeriksaan host key sepenuhnya; host key yang berubah tetap akan gagal dan memerlukan peninjauan operator
- `linux_ipa_qga_ssh_bootstrap_enabled` adalah jalur bootstrap tanpa reboot yang disukai untuk guest berbasis Proxmox karena ia dapat membuat user otomatisasi khusus yang hanya memakai kunci melalui QEMU Guest Agent sebelum ada login SSH apa pun
- `linux_ipa_qga_ssh_bootstrap_qm_path` default-nya `qm`, dan alur bootstrap juga memeriksa jalur fallback umum pada node Proxmox sebelum gagal
- guest yang mengizinkan `guest-ping` tetapi menolak `guest-exec` akan dilewati secara default selama bootstrap QGA; sediakan jalur SSH lain untuk mereka atau set `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` untuk gagal cepat
- `linux_ipa_ssh_bootstrap_enabled` secara opsional memasang kunci publik SSH controller ke guest Linux sebelum resolusi hostname dan enrollment; `linux_ipa_ssh_bootstrap_password` juga dipakai sebagai fallback kata sandi first-touch bersama untuk guest Linux runtime bahkan saat bootstrap berbasis kunci dinonaktifkan
- enrollment Linux ke IPA mencoba ulang join klien upstream yang gagal karena timeout JSON-RPC FreeIPA dan mengekspos `linux_ipaclient_kinit_attempts` untuk lingkungan IPA yang lebih lambat atau lebih sibuk
- enrollment Linux ke IPA juga secara default menggabungkan hostname inventaris `ipa_servers` ke daftar server join, sehingga klien dapat memakai keseluruhan himpunan server IPA, bukan satu endpoint yang dikonfigurasi
- ketika lebih dari satu server IPA tersedia, setiap putaran retry mencoba kandidat server IPA itu satu per satu selama enrollment klien Linux
- workflow gabungan `site` membuat hostgroup FreeIPA terlebih dahulu lalu menambahkan host runtime yang sudah enrolled setelahnya, sehingga run pra-enrollment tidak gagal pada langkah keanggotaan hostgroup hanya karena guest belum enrolled

## Permukaan konfigurasi

Sebagian besar nilai berada di:

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

Untuk tata letak per file, lihat [docs/VARIABLES.md](../VARIABLES.md).

Keluarga variabel utama:

| Area | Variabel |
| --- | --- |
| Model akses FreeIPA | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Kontrol rollout | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| LDAP realm Proxmox | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| RBAC Proxmox | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Enrollment Linux ke IPA | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Pelaporan readiness Linux | `linux_readiness_report_*` |
| Manajemen Windows | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Helper Windows FreeIPA | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Rahasia koneksi Ansible | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Contoh strategi grup

Pola sederhana yang dapat diskalakan dengan baik:

- grup pengguna FreeIPA `proxmox-admins`
- grup pengguna FreeIPA `linux-ssh-admins`
- hostgroup FreeIPA `linux-all`
- aturan HBAC `allow-linux-ssh-admins`
- aturan sudo `allow-linux-ssh-admins-sudo`
- binding ACL Proxmox untuk grup tersinkron `proxmox-admins-ipa`

Isi `freeipa_linux_admin_users` di [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) bila Anda ingin run gabungan `site.yml` secara otomatis memberikan akses SSH dan sudo Linux kepada user IPA tertentu melalui grup terkelola `linux-ssh-admins`.

Ingat bahwa sinkronisasi LDAP Proxmox membuat grup tersinkron dengan suffix:

```text
<group-name>-<realm>
```

Jika grup FreeIPA Anda adalah `proxmox-admins` dan realm Proxmox Anda adalah `ipa`, maka grup PVE tersinkron yang dihasilkan menjadi:

```text
proxmox-admins-ipa
```

## Keamanan

- simpan semua rahasia di `vault-freeipa.yml` dan `vault-proxmox.yml`, bukan di file variabel inventaris plaintext
- utamakan akun LDAP bind khusus yang read-only untuk Proxmox
- utamakan TLS dengan verifikasi sertifikat yang aktif
- pertahankan pemeriksaan SSH host key tetap aktif di luar lab sementara
- utamakan `linux_ipa_qga_ssh_bootstrap_enabled` dibanding kata sandi sementara bersama ketika guest Proxmox Anda sudah memiliki QEMU Guest Agent yang berfungsi
- gunakan `guest_qemu_agent_install_enabled` hanya ketika repositori sudah mempunyai jalur manajemen yang valid ke dalam guest; untuk discovery Proxmox ini berarti QGA sudah berjalan atau `linux_ipa_proxmox_discovery_ansible_user` beserta akses kata sandi atau kunci sudah dikonfigurasi
- jika Anda mengaktifkan bootstrap SSH Linux, simpan kata sandi bootstrap bersama di variabel yang terenkripsi dan rotasi atau hapus setelah akses berbasis kunci terbentuk
- jangan gunakan ulang akun admin IPA sebagai akun LDAP bind Proxmox
- tinjau `proxmox_ldap_filter` dan `proxmox_ldap_group_filter` sebelum rollout produksi untuk menghindari impor objek yang terlalu banyak

Untuk lab sementara yang memang ingin melewati verifikasi host key SSH, lakukan opt-out per sesi shell alih-alih mengubah default repositori:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Idempotensi dan catatan

Repositori ini ditulis agar dapat dipakai ulang dan sebagian besar idempoten, tetapi tetap harus diuji di lab sebelum rollout produksi.

Catatan yang sudah diketahui:

- output CLI Proxmox dapat sedikit berbeda antar rilis
- layout direktori FreeIPA fleksibel, jadi filter LDAP mungkin perlu disetel untuk tree Anda
- ACL dan role PVE yang dikelola manual sebelumnya harus dibandingkan sebelum otomasi diterapkan di atasnya
- auto-discovery VM Proxmox bergantung pada guest yang sedang berjalan dan data jaringan QEMU guest agent
- definisi guest berbasis IP tetap memerlukan hostname akhir yang valid di dalam guest, atau `ipa_hostname` yang eksplisit
- play Proxmox berjalan dengan privilege escalation, jadi user SSH non-root harus memiliki `sudo` yang berfungsi dan Anda harus memberikan kata sandi become dengan `-K` kecuali user itu sudah memiliki `sudo` tanpa kata sandi
- jika Anda menyimpan `ansible_become_password` di `vault-proxmox.yml`, Anda dapat melewati `-K` karena Ansible akan membaca kata sandi sudo dari variabel terenkripsi

## Verifikasi

Setelah rollout berhasil, verifikasi keadaan akhirnya alih-alih mengasumsikan bahwa semua jalur akses sudah benar.

### Di FreeIPA

- pastikan grup pengguna yang diharapkan ada
- pastikan hostgroup yang diharapkan ada
- pastikan aturan HBAC yang diharapkan ada dan aktif
- pastikan aturan `sudo` yang diharapkan ada dan aktif

### Di Proxmox

- pastikan LDAP realm ada
- pastikan sinkronisasi awal mengimpor pengguna atau grup yang diharapkan
- pastikan grup tersinkron yang dituju memiliki binding ACL yang diharapkan

### Di guest Linux

- pastikan user IPA yang diizinkan bisa login
- pastikan user yang tidak diizinkan diblokir oleh HBAC
- pastikan admin IPA yang diizinkan dapat menjalankan `sudo -l`
- pastikan direktori home dibuat saat login pertama bila `linux_ipaclient_mkhomedir` diaktifkan

## Tata letak repositori

<details>
<summary>Tampilkan tata letak repositori</summary>

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

## Pengembangan

File helper utama yang disertakan dalam repositori ini adalah:

- `.editorconfig`, untuk menjaga default spasi, encoding, dan akhir baris tetap konsisten antar editor
- `.gitattributes`, untuk memaksa file teks umum memakai akhir baris `LF`
- `.gitignore`, untuk mencegah inventaris hasil generate, data vault, collection lokal, dan file sampah editor masuk ke Git
- `.ansible-lint`, untuk mengecualikan path collection vendor dan hanya menekan aturan panjang baris YAML
- `.yamllint`, untuk menjaga validasi YAML tetap konsisten pada playbook, inventaris, dan workflow
- `.github/CODEOWNERS`, untuk mengarahkan kepemilikan review pada area utama repositori
- `.github/workflows/ci.yml`, untuk menjalankan validasi lint dan smoke pada event push dan pull request
- `.pre-commit-config.yaml`, untuk menjalankan hook lint cepat sebelum commit ketika `pre-commit` dipasang
- `CHANGELOG.md`, untuk melacak perubahan penting repositori di satu tempat
- `docs/VARIABLES.md`, untuk menjelaskan struktur variabel inventaris yang dipisah
- `docs/i18n/`, untuk menampung README terjemahan; file-file ini harus mencerminkan struktur bagian penuh dari `README.md` bahasa Inggris
- `docs/i18n/TRANSLATION_GUIDE.md`, untuk menjelaskan cara menjaga README terjemahan tetap sinkron
- `scripts/bootstrap.ps1` dan `scripts/bootstrap.sh`, untuk menginstal collection yang diperlukan ke path lokal `collections/` dan menerapkan patch kompatibilitas untuk ansible-core 2.24+
- `scripts/patch_freeipa_collection.py`, untuk menulis ulang import yang deprecated di dalam collection FreeIPA yang dipin agar tetap kompatibel dengan versi ansible-core mendatang
- `scripts/lint.py`, untuk menyediakan entry point lint lintas platform yang dipakai secara lokal, di CI, dan pada pre-commit
- `scripts/smoke-test.py`, untuk menjalankan validasi inventaris contoh dan pemeriksaan sintaks tanpa menyentuh infrastruktur nyata, termasuk cakupan untuk playbook Windows terpisah
- `scripts/check_translations.py`, untuk mengaudit README terjemahan terhadap metadata, paritas struktur bagian, dan cakupan konten minimum dibanding README kanonik bahasa Inggris
- `scripts/lint.ps1` dan `scripts/lint.sh`, untuk menggabungkan workflow lint dan smoke lokal
- `scripts/proxmox_event_webhook.py`, untuk berfungsi sebagai webhook opsional di sisi controller untuk event VM Proxmox
- `scripts/proxmox-vm-hook.pl`, untuk bertindak sebagai hook VM opsional yang dipasang di node Proxmox
- `scripts/run-playbook.ps1`, untuk menyediakan wrapper `ansible-playbook` yang konsisten pada lingkungan Windows dan PowerShell
- `scripts/vault.ps1` dan `scripts/vault.sh`, untuk membantu membuat, mengedit, melihat, dan mengenkripsi file vault yang dipisah per domain
- `tests/`, menampung permukaan verifikasi repositori, dimulai dari dokumentasi smoke-test
- `CONTRIBUTING.md`, mendokumentasikan alur kontribusi dan validasi yang diharapkan
- `SECURITY.md`, mendokumentasikan cara melaporkan kerentanan dan menangani informasi yang sensitif terhadap keamanan

Jika `ansible-lint` terpasang di controller Anda:

```bash
ansible-lint
```

Untuk menjalankan smoke check repositori secara langsung:

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

Untuk lint pass lokal penuh:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

Untuk mengaktifkan hook lint cepat sebelum setiap commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Wrapper playbook PowerShell sekarang juga mendukung opsi operator umum secara langsung:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Ekstensi berikutnya

Ekstensi yang umum masuk akal berikutnya:

- pipeline Packer untuk template Linux yang sudah siap IPA
- template job dan penjadwalan AWX atau Automation Controller untuk rollout terpadu
- model tenant dan pool Proxmox yang lebih kuat
- workflow trust AD untuk Windows RDP atau lingkungan identitas hibrida

## Lisensi

Dirilis di bawah [0BSD License](../../LICENSE).
