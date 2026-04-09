# Proxmox + FreeIPA Erişim Otomasyonu

Bu sayfa [README.md](../../README.md) dosyasının tam yapı çevirisini sunar. İngilizce sürüm nihai kaynaktır, ancak bu Türkçe sürüm aynı ana bölümleri kapsar.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Bu proje neden var

Bu depo şu durumlar için tasarlanmıştır:

- sağlıklı bir FreeIPA ortamı
- bir Proxmox VE kümesi
- merkezi kimlik doğrulaması kullanması gereken Linux sanal makineleri
- Proxmox LDAP bind için ayrılmış bir FreeIPA servis hesabı
- yönetici ve operatör grupları için net bir erişim modeli

Temel yaklaşım FreeIPA'yı kimlik ve erişim için kaynak sistem olarak kullanmaktır. Proxmox bu dizini LDAP realm üzerinden tüketir, Linux istemciler `ipaclient` rolü ile FreeIPA'ya katılır ve SSH, HBAC ve `sudo` kuralları merkezi kalır.

## Neler sağlar

- FreeIPA kullanıcı grubu, hostgroup, HBAC ve `sudo` kural yönetimi
- FreeIPA'ya bağlı Proxmox LDAP realm yapılandırması
- belirlenmiş bir küme düğümünden periyodik realm senkronizasyonu
- senkronize dizin grupları için Proxmox RBAC bağları
- statik inventory, manuel host tanımı veya Proxmox keşfi ile Linux IPA enrollment
- QEMU Guest Agent üzerinden isteğe bağlı no-reboot SSH bootstrap
- SSH veya WinRM ile erişilebilen makinelerde isteğe bağlı guest-agent kurulumu
- ilk erişim için isteğe bağlı SSH public-key bootstrap
- FreeIPA erişim modeli değişikliklerinden sonra otomatik SSSD yenilemesi
- `post-start` ve `post-migrate` olayları için isteğe bağlı event-driven onboarding

## Kapsam

| Dahil | Dahil Degil |
| --- | --- |
| FreeIPA erişim modeli | Windows domain join |
| Proxmox LDAP realm kurulumu | FreeRADIUS kurulumu |
| Senkronize gruplardan Proxmox RBAC | FreeIPA kullanıcı yaşam döngüsü oluşturma |
| Linux IPA client enrollment | Tüm Proxmox multi-tenant kenar durumları |

## Mimari

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

Uzun tasarım açıklaması için [docs/ARCHITECTURE.md](../ARCHITECTURE.md) dosyasına bakın.

## Gereksinimler

### Kontrol düğümü

- Ansible Core 2.14+
- Proxmox ana düğümü, IPA sunucuları ve Linux istemcilerine SSH erişimi
- gerektiğinde `sudo` veya `root`
- QGA SSH bootstrap açıksa guest içinde çalışan QEMU Guest Agent
- Windows guest-agent fallback açıksa `windows_qemu_guest_agent_clients` grubunda erişilebilir Windows hostları
- Linux SSH bootstrap açıksa kontrolcüde SSH anahtar çifti ve ilk parola tabanlı erişim

### Hedefler

- `proxmox_primary` altında Proxmox VE 6.x veya sonrası
- Proxmox ve Linux istemcilerinden erişilebilen FreeIPA
- düzgün DNS ve zaman senkronizasyonu
- `proxmox_primary` için `root` veya `pveversion`, `pvesh`, `pveum` komutlarını `sudo` ile çalıştırabilen kullanıcı
- Proxmox discovery kullanılıyorsa QEMU Guest Agent üzerinden kullanılabilir IP

## Ağ portları

Tam port tablosu İngilizce README'dedir. Bu projede öne çıkan portlar:

- `22/TCP` SSH
- `53/TCP,UDP` IPA DNS
- `88/TCP,UDP` ve `464/TCP,UDP` Kerberos
- `389/TCP` LDAP
- varsayılan `443/TCP` olan `linux_freeipa_enroll_https_port`
- `ldaps` modunda `636/TCP`

## Uyumluluk

- Proxmox VE 6.x ve sonrası hedeflenir
- varsayılan major sürümler: `6`, `7`, `8`, `9`, `10`
- `proxmox_supported_major_versions` ile override edilebilir
- `proxmox_allow_future_major_versions` varsayılanı `true`

## Hızlı başlangıç

### 1. Örnek inventory ve vault dosyalarını kopyalayın

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
```

### 2. Ortama özel dosyaları düzenleyin

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

Linux kaynak modu olarak statik hostlar, `linux_ipa_client_hosts` veya Proxmox discovery seçilebilir.

### 3. Vault dosyalarını şifreleyin

```bash
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
```

### 4. Gerekli collection'ı kurun

```bash
./scripts/bootstrap.sh
```

### 5. Önce doğrulama çalıştırın

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

### 6. İsteğe bağlı önizleme

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

### 7. Tam yapılandırmayı uygulayın

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## Yayılım sırası

İlk kurulum için:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Varsayılan rollout değerleri tutucudur: FreeIPA ve Proxmox için `serial: 1`, Linux için `serial: 10`, tüm akışlarda `max_fail_percentage: 0`.

## Etiket modeli

- temel alanlar: `freeipa`, `proxmox`, `linux`, `validate`
- FreeIPA erişim modeli: `freeipa_access`
- Proxmox alt kümeleri: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux hazırlık: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- olay akışı: `event`, `linux_refresh`

## Olay güdümlü VM onboarding

Proxmox, VM açılışından veya taşınmasından hemen sonra Linux discovery ve IPA enrollment tetiklesin istiyorsanız [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) dosyasındaki hook/webhook akışını kullanın. Bu yol `playbooks/proxmox-vm-event.yml` kullanır, her olayda LDAP realm veya RBAC yeniden çalıştırılmaz ve yeni VM'ler pratikte ilk `post-start` sırasında yakalanır.

## Inventory modeli

Ana gruplar:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

IP-only veya Proxmox discovery kullanıyorsanız guest'in nihai FQDN'i `ipa_hostname` veya `hostname -f` üzerinden yine gereklidir.

### Linux kaynak modları

1. statik inventory hostları
2. `linux_ipa_client_hosts` içindeki manuel tanımlar
3. `linux_ipa_proxmox_discovery_*` ile Proxmox discovery

Önemli notlar:

- discovery, QEMU Guest Agent ağ verilerine bağlıdır
- `linux_ipa_proxmox_discovery_vmids` özellikle event-driven akış için yararlıdır
- kısa host adları için `linux_ipa_identity_hostname_suffix` ve `linux_freeipa_enroll_manage_hostname: true` kullanılabilir
- authoritative DNS onarımı için `linux_freeipa_enroll_manage_authoritative_dns: true` kullanılabilir
- DNS hazır değilse `linux_ipa_manage_etc_hosts: true` ve `linux_ipa_etc_hosts_entries` kullanılabilir

## Yapılandırma yüzeyi

Başlıca değerler:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

Dosya bazlı açıklama için [docs/VARIABLES.md](../VARIABLES.md) dosyasına bakın.

## Örnek grup stratejisi

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## Güvenlik

- tüm sırları vault dosyalarında saklayın
- Proxmox için mümkünse read-only LDAP bind hesabı kullanın
- certificate verification ile TLS tercih edin
- disposable lab dışı ortamlarda SSH host key denetimini kapatmayın

## İdempotensi ve notlar

Bu proje büyük ölçüde tekrar çalıştırılabilir olacak şekilde yazılmıştır, ancak üretimden önce laboratuvarda doğrulanmalıdır. Bilinen sınırlamalar arasında Proxmox CLI çıktı farklılıkları, LDAP filter ayarı gereksinimi, discovery'nin çalışan guest'lere ve QGA verisine bağlı olması ve IP-only tanımların yine geçerli host adı gerektirmesi bulunur.

## Doğrulama

- FreeIPA'da grup, hostgroup, HBAC ve `sudo` kurallarını doğrulayın
- Proxmox'ta LDAP realm, sync ve ACL bağlarını doğrulayın
- Linux guest üzerinde izin verilen giriş, reddedilen kullanıcı, `sudo -l` ve `mkhomedir` davranışını test edin

## Depo düzeni

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

Tam ağaç görünümü İngilizce README içinde kalır.

## Geliştirme

Yardımcı dosyalar arasında `.editorconfig`, `.ansible-lint`, `.yamllint`, CI iş akışları, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1`, `scripts/vault.*` bulunur.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## Sonraki genişletmeler

- IPA-ready Linux template'leri için Packer hattı
- AWX job template ve schedule'ları
- ayrı Proxmox tenant ve pool modelleri
- RDP odaklı ortamlar için Windows veya AD-trust akışı

## Lisans

[MIT License](../../LICENSE) altında yayımlanır.
