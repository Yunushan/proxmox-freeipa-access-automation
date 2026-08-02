# Proxmox + FreeIPA Erişim Otomasyonu

Bu sayfa [README.md](../../README.md) dosyasının tam yapı çevirisini sunar. İngilizce sürüm nihai kaynaktır, ancak bu Türkçe sürüm aynı ana bölümleri kapsar.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-16

## Diller

İngilizce README bu belgenin canonical kaynağıdır. Diğer tam çevrilmiş README dosyaları çeviri dizininde bulunur.

[English](../../README.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [简体中文](README.zh-CN.md) | [Français](README.fr.md)

[Deutsch](README.de.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[मराठी](README.mr.md) | [فارسی](README.fa.md) | [Português](README.pt.md) | [ਪੰਜਾਬੀ](README.pa.md) | [Русский](README.ru.md)

[Español](README.es.md) | [தமிழ்](README.ta.md) | [తెలుగు](README.te.md) | [Türkçe](README.tr.md) | [اردو](README.ur.md)

## Bu proje neden var

Bu depo şu durumlar için tasarlanmıştır:

- sağlıklı bir FreeIPA ortamı
- bir Proxmox VE kümesi
- merkezi kimlik doğrulaması kullanması gereken Linux sanal makineleri
- Proxmox LDAP bind için ayrılmış bir FreeIPA servis hesabı
- yönetici ve operatör grupları için net bir erişim modeli

Temel yaklaşım FreeIPA'yı kimlik ve erişim için kaynak sistem olarak kullanmaktır. Proxmox bu dizini LDAP realm üzerinden tüketir, Linux istemciler `ipaclient` rolü ile FreeIPA'ya katılır ve SSH, HBAC ve `sudo` kuralları merkezi kalır.

Şu onboarding ve offboarding sırasını hedefliyorsanız bu depo özellikle uygundur:

1. FreeIPA içinde kullanıcı ve grupları oluşturmak veya güncellemek
2. Bu kimlikleri Proxmox içine senkronize etmek
3. Senkronize gruplardan Proxmox rol ve ACL bağlarını uygulamak
4. FreeIPA login, HBAC ve `sudo` kuralları ile Linux guest erişimini yönetmek

## Neler sağlar

- FreeIPA kullanıcı grubu, hostgroup, HBAC ve `sudo` kural yönetimi
- Linux yönetici kullanıcıları için otomatik FreeIPA login-shell varsayılanları
- FreeIPA'ya bağlı Proxmox LDAP realm yapılandırması
- belirlenmiş bir küme düğümünden periyodik realm senkronizasyonu
- senkronize dizin grupları için Proxmox RBAC bağları
- statik inventory, manuel host tanımı veya Proxmox keşfi ile Linux IPA enrollment
- QEMU Guest Agent üzerinden isteğe bağlı no-reboot SSH bootstrap
- Proxmox-backed Linux guest'ler için isteğe bağlı Proxmox tarafı guest-agent iletişim etkinleştirmesi
- SSH veya WinRM ile erişilebilen makinelerde isteğe bağlı guest-agent kurulumu
- SSH erişilebilirliği ve Proxmox QEMU Guest Agent durumu için isteğe bağlı Linux readiness raporu
- Active Directory üzerinden Windows 10/11 ve Windows Server guest'ler için ayrı Windows domain-membership akışı
- IPA CA güveni, hosts bootstrap ve IPA erişilebilirlik denetimleri için sınırlı FreeIPA-aware Windows helper akışı
- ilk erişim için isteğe bağlı SSH public-key bootstrap
- FreeIPA erişim modeli değişikliklerinden sonra otomatik SSSD yenilemesi
- `post-start` ve `post-migrate` olayları için isteğe bağlı event-driven onboarding

## Kapsam

| Dahil | Dahil Değil |
| --- | --- |
| FreeIPA erişim modeli | FreeRADIUS kurulumu |
| Proxmox LDAP realm kurulumu | FreeIPA kullanıcı yaşam döngüsü oluşturma |
| Senkronize gruplardan Proxmox RBAC | Tüm Proxmox multi-tenant kenar durumları |
| Linux IPA client enrollment | FreeIPA'ya karşı doğrudan native Windows logon |
| Ayrı Windows AD domain-membership akışı | GPO veya daha geniş AD nesne yaşam döngüsü otomasyonu |
| Sınırlı FreeIPA-aware Windows helper akışı | FreeIPA-only Windows helper'larını AD eşdeğeri saymak |

## Windows İş Akışı

Windows desteği Linux IPA enrollment akışına gömülü değildir; ayrı bir iş akışı olarak uygulanır.

- `windows_qemu_guest_agent_clients` yalnızca isteğe bağlı QEMU Guest Agent yardımcı işleri için kullanılır.
- `windows_domain_membership_enabled: true` ile ayrı Windows yönetim akışı etkinleştirilir.
- `windows_management_clients`, `playbooks/windows-management.yml` ve birleşik `playbooks/site.yml` içindeki Windows aşaması için kullanılır.
- yerel Windows oturumu Active Directory domain membership ile sağlanır; FreeIPA merkezli ortamlarda Windows hostlarını doğrudan FreeIPA'ya katmaya çalışmak yerine FreeIPA-AD trust tarafına bağlamak gerekir.

FreeIPA-only Windows domain join bu depo tarafından desteklenmez. Active Directory veya FreeIPA-AD trust olmadan Windows tarafı yalnızca yardımcı görevlerle sınırlıdır.

Bu sınırlı yol için `windows_freeipa_helpers_enabled: true` kullanın ve `windows_freeipa_helper_clients` grubunu `playbooks/windows-freeipa-helpers.yml` ile çalıştırın. Bu yardımcı akış IPA CA güveni, isteğe bağlı CA auto-fetch ve thumbprint pinleme, hosts-file bootstrap, IPA DNS ve TCP erişilebilirlik doğrulaması, HTTPS doğrulaması, Windows zaman kaynağı denetimi, yerel grup üyeliği yönetimi ve isteğe bağlı OpenSSH Server yönetimi sağlayabilir; ancak FreeIPA üzerinden yerel Windows logon sağlamaz.

Salt doğrulama istiyorsanız `playbooks/windows-freeipa-validate.yml` kullanın. Bu akış özet ve doğrulama yolunu korur, ancak değişiklik yapan helper adımlarını kapatır.

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

Bu tablo, bu deponun kontrol düğümü, Proxmox LDAP otomasyonu ve Linux IPA enrollment akışında kullanılan ağ portlarını listeler.
Tam FreeIPA sunucu-sunucu replikasyon matrisi değildir; yalnızca bu projenin kullandığı yüzeyi kapsar.

| Ad | Port | Protokol | Kaynak | Hedef | Ne zaman gerekir | Amaç |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible kontrol düğümü | Proxmox node, IPA sunucusu, Linux guest | Her zaman | Ansible bağlantısı |
| WinRM | `5985`, `5986` | `TCP` | Ansible kontrol düğümü | Windows guest | Windows yönetimi açıksa | Windows guest'lere Ansible bağlantısı |
| DNS | `53` | `TCP`, `UDP` | Linux guest | IPA DNS sunucuları | Linux guest'ler IPA DNS kullanıyorsa | IPA kayıtlarını ve dış isimleri çözmek |
| Kerberos | `88` | `TCP`, `UDP` | Linux guest | IPA sunucuları | Linux IPA enrollment ve login | Kerberos kimlik doğrulaması |
| LDAP | `389` | `TCP` | Linux guest | IPA sunucuları | Linux IPA enrollment ve login | LDAP ve FreeIPA client discovery |
| HTTPS | `linux_freeipa_enroll_https_port` varsayılanı `443` | `TCP` | Linux guest | IPA sunucuları | Linux IPA enrollment | Client kurulumunda IPA web/API doğrulaması |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux guest | IPA sunucuları | Linux IPA enrollment ve parola işlemleri | Kerberos parola ve keytab işlemleri |
| LDAPS | `636` | `TCP` | Proxmox primary node | IPA veya LDAP sunucuları | Varsayılan `ldaps` modlu Proxmox LDAP realm | Proxmox LDAP realm bağlantısı |

Notlar:

- `LDAPS 636/TCP` depo varsayılanıdır çünkü `proxmox_ldap_mode` varsayılan olarak `ldaps` gelir. LDAP modu veya port değişirse, bunun yerine yapılandırdığınız `proxmox_ldap_port` açılmalıdır.
- `WinRM`, ortamınıza göre çoğunlukla HTTPS için `5986/TCP`, HTTP için `5985/TCP` kullanır.
- `DNS 53/TCP,UDP` yalnızca Linux guest'ler IPA sunucularını resolver olarak kullanıyorsa gereklidir.
- `Kerberos 88` ve `Kerberos Password 464` için hem `TCP` hem `UDP` gerekir.
- Active Directory domain join ayrıca normal Windows-domain-controller port setini de gerektirir, ancak bu matris ortam bağımlıdır ve burada özellikle tam liste olarak verilmemiştir.
- Kerberos'un güvenilir çalışması için zaman senkronizasyonu yine gereklidir, ancak NTP kaynağı ortam bağımlıdır ve bu depo tarafından yönetilmez.

## Uyumluluk

Bu depodaki Proxmox otomasyonu, Proxmox VE 6.x ve sonrası sürümlerde kullanılan `pveum` ve `pvesh` realm ile RBAC arayüzleri etrafında yazılmıştır.

- varsayılan desteklenen major sürümler: `6`, `7`, `8`, `9`, `10`
- doğrulama, tespit edilen Proxmox sürümünü `pveversion` ile kontrol eder
- desteklenen major sürüm listesi, ortamınıza göre daraltmak veya genişletmek için `proxmox_supported_major_versions` ile override edilebilir
- `proxmox_allow_future_major_versions` varsayılanı `true` olduğu için, listelenen en yüksek testli sürümden daha yeni major sürümler de varsayılan olarak doğrulamadan geçer
- daha yeni major sürümler yine de, otomasyon bu yeni Proxmox arayüzü ile doğrulanana kadar uyumluluk adayı olarak değerlendirilmelidir
- `1` ile `5` arası eski legacy major sürümler bu halka açık depo tarafından test edilmiş destek olarak iddia edilmez; bunları yerel olarak eklerseniz bunu açık bir compatibility override olarak düşünün ve tam akışı önce lab ortamında doğrulayın

Legacy bir lab ortamı için yerel override örneği:

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

## Hızlı başlangıç

Aşağıdaki örnekler shell komutları kullanır. Gerekli olduğu yerlerde PowerShell karşılıkları da eklenmiştir.

### 1. Örnek envanter ve vault dosyalarını kopyalayın

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# İsteğe bağlı, Windows guest yönetecekseniz:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# İsteğe bağlı, Windows guest yönetecekseniz:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Ortama özel dosyaları düzenleyin

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- Windows yönetimi kullanıyorsanız `inventories/production/group_vars/all/35-windows-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- Windows yönetimi kullanıyorsanız `inventories/production/group_vars/all/vault-windows.yml`

IPA ve Proxmox ayarlarının yanında bir Linux guest kaynak modu seçin:

- `linux_ipa_clients` altında statik inventory girdileri
- `group_vars/all/30-linux-clients.yml` içindeki `linux_ipa_client_hosts` girdileri
- `linux_ipa_proxmox_discovery_enabled: true` ile Proxmox VM discovery

Linux IPA enrollment için domain ve server değerlerini ayrı düşünün:

- `ipaclient_domain`, ortak IPA DNS domain değeridir; örneğin `example.com`
- `linux_ipa_servers`, IPA sunucu host adlarını içerir; örneğin `ipa01.example.com`

Proxmox'a `root` yerine `sudo` yetkili normal bir kullanıcıyla SSH bağlanmak istiyorsanız, bunu `hosts.yml` içinde `proxmox_primary` altında tanımlayın ve sudo parolasını `vault-proxmox.yml` içinde tutun:

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

Bu kurulumda `vault_proxmox_become_password`, Proxmox host üzerinde normalde `sudo` için elle gireceğiniz paroladır.

### 3. Vault dosyalarını şifreleyin

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

Windows iş akışını etkinleştiriyorsanız `inventories/production/group_vars/all/vault-windows.yml` dosyasını da aynı komuta ekleyin.

İsterseniz helper wrapper script'leri de kullanabilirsiniz. Bunlar varsayılan olarak ayrı vault ID'leri kullanır ve gerekirse çalışma vault dosyalarını example template'lerden oluşturur:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Playbook çalıştırırken domain başına ayrı parola istiyorsanız `--ask-vault-pass` yerine vault ID kullanımını tercih edin:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

İsteğe bağlı Windows iş akışı da ayrı vault parolası kullanıyorsa aynı komuta `windows@prompt` ekleyin.

Kullandığınız tüm vault dosyaları aynı parolayı paylaşıyorsa `-AskVaultPass` yeterlidir.

### 4. Gerekli koleksiyonu kurun

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Doğrudan kurmak isterseniz:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

`freeipa.ansible_freeipa` koleksiyonunu bu depo uyumluluk yaması eklenmeden önce yüklediyseniz bootstrap helper'larından birini yeniden çalıştırın veya mevcut kullanıcı düzeyi koleksiyon kurulumunu da yamamak için `python .\scripts\patch_freeipa_collection.py` komutunu bir kez çalıştırın.

`scripts/run-playbook.ps1` kullanıldığında, bu patch helper `ansible-playbook` öncesinde otomatik çalışır.

### 5. Önce doğrulama çalıştırın

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Sadece helper-only Windows FreeIPA yolunu host üzerinde değişiklik yapmadan doğrulamak istiyorsanız:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Runtime Linux guest'lerden hangilerinin SSH ile erişilebilir olduğunu ve Proxmox-discovered guest'lerden hangilerinin QEMU Guest Agent üzerinden cevap verdiğini görmek için read-only bir Linux readiness denetimi çalıştırmak istiyorsanız:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Readiness report varsayılan olarak `.ansible/linux-readiness-report.json` dosyasını yazar.
Başlıca alanları şu şekilde yorumlayın:

- `ssh.ready=true`: şu anda yapılandırılmış Ansible SSH yolu kontrol düğümünden başarıyla çalıştı
- `ssh.promptless=true`: SSH probe, `ansible_password` olmadan başarılı oldu; yani yol Ansible için interaktif değildir
- `ssh.auth_mode=password_configured`: host üzerinde `ansible_password` bulunduğu için probe `sshpass` kullandı
- `ssh.auth_mode=key_or_agent`: probe, `ansible_password` olmadan SSH batch mode ile başarılı oldu
- `qga.status=available`: ilgili Proxmox node üzerinde `qm guest ping` başarılı oldu
- `qga.status=disabled`: Proxmox VM config içinde QEMU Guest Agent etkin değil
- `qga.status=configured_unresponsive`: guest agent Proxmox config içinde açık, ancak cevap vermedi
- `qga.status=node_unreachable`: kontrol düğümü, ilgili Proxmox node'a probe için ulaşamadı
- `qga.status=not_applicable`: host, Proxmox discovery ile oluşturulmadığı için QGA probe denenmedi

Hızlı inceleme örneği:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. İsteğe bağlı önizleme

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Check mode'u tam simülasyon değil, kısmi önizleme olarak değerlendirin. Bu depo Proxmox yapılandırmasının bir kısmında doğrudan CLI komutları ve Linux enrollment için upstream FreeIPA client rolü kullandığı için `--check` yararlıdır ancak mutlak otorite değildir.
>
> FreeIPA HBAC kuralları için check mode, kural tanım adımını doğrular ancak devamındaki enable veya disable adımını atlar. Bunun nedeni dry-run sırasında kural gerçekten oluşturulmadığı için FreeIPA'nın kural yokmuş gibi hata üretmesini engellemektir.
>
> Proxmox realm sync timer rolü de son `systemd` enable veya start adımını check mode'da atlar; çünkü unit dosyaları diff aşamasında gösterilse de dry-run sırasında gerçekten yazılmaz.
>
> Linux IPA enrollment da check mode'da atlanır. Depo yine discovery, hostname resolution ve giriş doğrulamasını yapar, ancak upstream `ipaclient` rolü dry-run sırasında çalıştırılmaz.

### 7. Tam yapılandırmayı uygulayın

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

İsteğe bağlı Windows iş akışı açıksa ve `vault-windows.yml` ayrı bir parola kullanıyorsa, aynı playbook'u `--ask-vault-pass` yerine `--vault-id windows@prompt` ile veya PowerShell wrapper içinde `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` ile çalıştırın.

## Yayılım sırası

İlk kurulum için stack'i şu sırada uygulayın:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# İsteğe bağlı, Windows guest yönetiyorsanız:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# İsteğe bağlı, sınırlı Windows FreeIPA helper akışı istiyorsanız:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# İsteğe bağlı, helper akışı için yalnızca doğrulama istiyorsanız:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

Bu sıra, her şeyi aynı anda çalıştırmaya göre sorun ayıklamayı çok daha kolaylaştırır.

Sınırlı bir PowerShell rollout örneği, örneğin tek bir Linux guest için:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Varsayılan rollout kontrolleri tutucudur:

- FreeIPA erişim değişiklikleri `serial: 1` ile çalışır
- Proxmox değişiklikleri `serial: 1` ile çalışır
- Linux hostname resolution, validation ve enrollment `serial: 10` ile çalışır
- Windows management değişiklikleri `serial: 10` ile çalışır
- tüm rollout yollarında varsayılan `max_fail_percentage: 0` kullanılır

Bu değerleri `inventories/production/group_vars/all/15-rollout.yml` içinde ayarlayın.

## Etiket modeli

Daha fazla playbook üretmek yerine, stabil rollout dilimlerini hedeflemek için tag kullanın.

- temel domain'ler: `freeipa`, `proxmox`, `linux`, `validate`
- Windows domain: `windows`, `windows_domain`
- Windows FreeIPA helper alanı: `windows`, `windows_freeipa`
- FreeIPA erişim modeli: `freeipa_access`
- Proxmox alt kümeleri: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux hazırlık adımları: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux enrollment: `linux_enroll`
- event-driven VM akışı: `event`, `linux_refresh`

Örnekler:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Olay güdümlü VM onboarding

Proxmox'un VM açılışı veya migration sonrası Linux discovery ve IPA enrollment'ı hemen tetiklemesini istiyorsanız [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md) içinde anlatılan isteğe bağlı hook ve webhook akışını kullanın.

Bu akış `playbooks/proxmox-vm-event.yml` adlı ayrılmış event playbook'unu kullanır; böylece tetikleyici yol yalnızca Linux ve FreeIPA guest tarafını yönetir. Her VM olayında Proxmox LDAP realm veya RBAC otomasyonunu yeniden çalıştırmaz.

Depo artık bu isteğe bağlı hook ve webhook stack'ini de `proxmox_vm_event_onboarding_enabled: true` ve gerekli webhook değişkenleri verildiğinde `site.yml` veya `proxmox.yml` üzerinden kurabilir.

Proxmox VM hook'ları bağımsız bir `create` aşaması sağlamaz. Pratikte yeni VM'ler ilk `post-start` olayında yakalanır; migration hook'ları ise hem kaynak hem hedef node üzerinde tetiklenebilir.

## Inventory modeli

Bu depo altı tanımlı inventory grubu ve bir üretilen runtime grubu kullanır:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Kendi ek inventory gruplarınızı da tanımlayabilir ve bunları FreeIPA hostgroup tanımlarında referans verebilirsiniz. Hazırlanmış tüm Linux guest setini FreeIPA hostgroup tarafında kullanmak istiyorsanız `linux_ipa_clients_runtime` grubunu referans alın.

> [!IMPORTANT]
> FreeIPA yine de her guest'in nihai host adına ihtiyaç duyar. IP-only hedef veya Proxmox discovery kullanıyorsanız, ya `ipa_hostname` değerini açıkça verin ya da guest içindeki `hostname -f` çıktısının nihai FQDN döndürdüğünden emin olun. Playbook'lar artık FreeIPA hostgroup üyeliği oluşturulmadan önce bu host adını çözer.

> [!TIP]
> Yeniden kullanılabilir golden template'i doğrudan FreeIPA'ya enroll etmeyin. Önce VM'i klonlayın, nihai host adını verin ve sonra oluşan guest'i enroll edin.

### Linux kaynak modları

`linux_ipa_clients` grubunu üç farklı şekilde besleyebilirsiniz.

`1.` Statik inventory hostları

Guest adlarını zaten biliyorsanız normal Ansible inventory girdileri kullanın:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

`2.` Değişken dosyalarında manuel host tanımları

Guest'leri `hosts.yml` dışında tutmak istiyorsanız veya elinizde yalnızca IP varsa `linux_ipa_client_hosts` kullanın:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Notlar:

- `name` çözümlenebilir bir host adı veya FQDN ise `ansible_host` isteğe bağlıdır
- yalnızca IP biliyorsanız `name` için herhangi bir stabil takma ad kullanabilirsiniz
- `ipa_hostname` verilmezse playbook guest içindeki `hostname -f` çıktısına geri düşer

`3.` Proxmox VM auto-discovery

Linux guest'leri bir veya daha fazla Proxmox node üzerinden çekmek istiyorsanız discovery kullanın:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# İsteğe bağlı: discovery ile bulunan guest'leri yalnızca onaylı alt kümeyle sınırla.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# İsteğe bağlı: discovery açık olsa da firewall veya DNS gibi altyapı VM'lerini
# her zaman dışarıda tut.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# İsteğe bağlı ilk erişim SSH ayarları: guest agent henüz çalışmıyorsa ve
# repository QGA kurmak için önce SSH ile girmek zorundaysa kullanılır.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

Notlar:

- discovery ile bulunan VM'ler, playbook'un geri kalanının kullandığı aynı `linux_ipa_clients_runtime` grubuna eklenir
- IP discovery, QEMU Guest Agent'in ağ arayüzü raporlayabilmesine bağlıdır
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` yalnızca zaten FQDN olan VM adlarına güvenir
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` ayarı, `Teleport-Server-1` gibi kısa ve güvenli Proxmox VM adlarını `linux_ipa_identity_hostname_suffix` yardımıyla `teleport-server-1.example.com` gibi hostname hint'lerine dönüştürür
- `linux_ipa_proxmox_discovery_vmids` isteğe bağlıdır ve ağırlıklı olarak event-driven hook veya webhook akışında discovery'yi belirli VMID'lere sınırlamak için kullanılır
- guest'in yine de nihai host adına ihtiyacı vardır; bu ya VM içinde zaten yapılandırılmış olmalı ya da manuel tanımda `ipa_hostname` ile verilmelidir
- guest'in gerçek sistem host adı enrollment için geçerli olmalıdır; `localhost.localdomain` gibi placeholder değerler `linux-clients` veya `site` çalıştırılmadan önce düzeltilmelidir
- guest'ler `app-server-01` gibi kısa host adları kullanıyorsa, `linux_ipa_identity_hostname_suffix` ve isteğe bağlı olarak `linux_freeipa_enroll_manage_hostname: true` ile enrollment öncesi tam host adı çözümlenip guest içine uygulanabilir
- FreeIPA DNS guest host adları için authoritative ise, `linux_freeipa_enroll_manage_authoritative_dns: true` ile ilgili guest'in A ve PTR kayıtları onarılabilir ve enrollment öncesi link-local `fe80::/10` AAAA kayıtları kaldırılabilir
- DNS henüz hazır değilse `linux_ipa_manage_etc_hosts: true` ve `linux_ipa_etc_hosts_entries` kullanılarak IPA sunucuları ve guest FQDN'leri için yönetilen bir `/etc/hosts` bootstrap bloğu eklenebilir
- `guest_qemu_agent_install_enabled`, halihazırda SSH veya WinRM ile erişilebilir guest'lere QEMU Guest Agent kurar; aynı workflow içinde sonradan erişilebilir hale gelen Linux guest'lerde ve Linux enrollment sonrasında tekrar dener; böylece daha sonraki Proxmox agent bağımlı iş akışları bunu kullanabilir
- `linux_ipa_proxmox_discovery_allowlist_enabled: true`, discovery açık kalsın ancak yalnızca sıkı şekilde onaylanmış guest alt kümesi Linux runtime inventory'ye girsin istediğinizde kullanılır; allowlist tam VMID, IP ve isim eşleşmeleri yapabilir
- `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips` veya `linux_ipa_proxmox_discovery_blacklist_names`, firewall veya DNS sunucuları gibi altyapı VM'lerinin hiçbir koşulda Linux IPA otomasyonu almaması için kullanılır; blacklist, geniş discovery veya allowlist üzerinden gelen admission kararını da her zaman geçersiz kılar
- guest agent'i hazır olmayan Proxmox-discovered Linux guest'lerde, repository'nin QEMU Guest Agent kurabilmesi için kullanılabilir ilk erişim SSH yolunu sağlamak amacıyla `linux_ipa_proxmox_discovery_ansible_user` ve bunun yanında `linux_ipa_proxmox_discovery_ansible_password` veya `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file` ayarlanmalıdır
- bu discovered guest'ler `root` olmayan bir SSH kullanıcısı ile yönetilecekse, hesap zaten passwordless sudo kullanmıyorsa `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method` ve `linux_ipa_proxmox_discovery_ansible_become_password` de verilmelidir
- `guest_qemu_agent_install_manage_proxmox_vm_agent`, guest içi kurulumdan önce Proxmox tarafındaki guest-agent iletişim seçeneğini de (`qm set <vmid> --agent 1`) Proxmox-backed Linux guest'ler için etkinleştirebilir
- bu Proxmox VM seçeneği çalışan bir VM üzerinde değişirse, depo varsayılan olarak yalnızca uyarı verir; çünkü Proxmox host'unda guest-agent kanalının kullanılabilmesi için taze bir VM başlangıcı gerekebilir; bunun otomatik reboot yapmasını isterseniz `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` ayarlayın
- `linux_ipa_ssh_host_key_policy` varsayılan olarak `accept_new` gelir; böylece yeni keşfedilen Linux guest'lere host key denetimini tamamen kapatmadan bağlanılabilir; değişmiş host key durumlarında ise yine hata verilir ve operatör incelemesi gerekir
- `linux_ipa_qga_ssh_bootstrap_enabled`, Proxmox-backed guest'ler için tercih edilen no-reboot bootstrap yoludur; çünkü henüz SSH login yokken QEMU Guest Agent üzerinden yalnızca anahtar kullanan ayrılmış bir automation user oluşturabilir
- `linux_ipa_qga_ssh_bootstrap_qm_path` varsayılanı `qm`'dir ve bootstrap akışı başarısız olmadan önce Proxmox node üzerinde yaygın fallback path'leri de dener
- `guest-ping` izinli ama `guest-exec` engelli guest'ler QGA bootstrap sırasında varsayılan olarak atlanır; bunlar için başka bir SSH yolu hazır tutun veya hızlı fail istiyorsanız `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` kullanın
- `linux_ipa_ssh_bootstrap_enabled`, hostname resolution ve enrollment öncesinde kontrolcü SSH public key'ini Linux guest'lere yükleyebilir; `linux_ipa_ssh_bootstrap_password` ise key bootstrap kapalı olsa bile runtime Linux guest'ler için paylaşılan first-touch parola fallback'i olarak da kullanılır
- Linux IPA enrollment, FreeIPA JSON-RPC timeout ile başarısız olan upstream client join işlemlerini yeniden dener ve daha yavaş veya yoğun IPA ortamları için `linux_ipaclient_kinit_attempts` değişkenini açığa çıkarır
- Linux IPA enrollment ayrıca varsayılan olarak `ipa_servers` inventory host adlarını join server listesine birleştirir; böylece client'lar tek bir endpoint yerine tam IPA sunucu setini kullanabilir
- birden fazla IPA sunucusu mevcutsa, her retry turunda Linux client enrollment sırasında bu IPA sunucu adayları teker teker denenir
- birleşik `site` akışı önce FreeIPA hostgroup'ları oluşturur, sonra enrolled runtime host'ları bunlara ekler; böylece henüz enroll edilmemiş guest'ler yüzünden pre-enrollment çalışmaları hostgroup membership adımında hata vermez

## Yapılandırma yüzeyi

Değerlerin büyük kısmı şu dosyalarda yaşar:

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

Dosya bazlı açıklama için [docs/VARIABLES.md](../VARIABLES.md) dosyasına bakın.

Başlıca değişken aileleri:

| Alan | Değişkenler |
| --- | --- |
| FreeIPA access modeli | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Rollout kontrolleri | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| Proxmox LDAP realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux IPA enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Linux readiness report | `linux_readiness_report_*` |
| Windows management | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows FreeIPA helpers | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Ansible connection secrets | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Örnek grup stratejisi

İyi ölçeklenen basit bir desen şudur:

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

Birleşik `site.yml` çalıştırmasının belirli IPA kullanıcılarına otomatik Linux SSH ve `sudo` erişimi vermesini istiyorsanız [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) içinde `freeipa_linux_admin_users` değerini doldurun.

Unutmayın: Proxmox LDAP sync, senkronize grupları şu suffix ile oluşturur:

```text
<group-name>-<realm>
```

FreeIPA grubunuz `proxmox-admins`, Proxmox realm'iniz `ipa` ise, ortaya çıkan senkronize PVE grubu şu olur:

```text
proxmox-admins-ipa
```

## Güvenlik

- tüm sırları düz metin inventory değişken dosyalarında değil, `vault-freeipa.yml` ve `vault-proxmox.yml` içinde saklayın
- Proxmox için mümkünse ayrılmış ve read-only bir LDAP bind hesabı kullanın
- mümkün olduğunda certificate verification açık olacak şekilde TLS tercih edin
- disposable lab ortamları dışında SSH host key denetimini açık bırakın
- Proxmox guest'lerinizde QEMU Guest Agent zaten çalışıyorsa paylaşılan geçici parolalar yerine `linux_ipa_qga_ssh_bootstrap_enabled` kullanın
- `guest_qemu_agent_install_enabled` yalnızca repository'nin guest içine zaten geçerli bir yönetim yolu varsa kullanılmalıdır; Proxmox discovery senaryosunda bu ya QGA'nın zaten çalışıyor olması ya da `linux_ipa_proxmox_discovery_ansible_user` ile parola veya key tabanlı erişimin yapılandırılması anlamına gelir
- Linux SSH bootstrap kullanıyorsanız, paylaşılan bootstrap parolasını vaulted değişkenlerde tutun ve key-based access kurulduktan sonra döndürün veya kaldırın
- IPA admin hesabını Proxmox LDAP bind hesabı olarak tekrar kullanmayın
- üretim rollout öncesinde `proxmox_ldap_filter` ve `proxmox_ldap_group_filter` değerlerini gözden geçirerek gereğinden fazla nesne içe aktarılmasını önleyin

SSH host verification'ı özellikle atlamak istediğiniz disposable bir lab ortamında, repository default'larını değiştirmek yerine bunu shell session bazında kapatın:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## İdempotensi ve notlar

Bu proje tekrar kullanılabilir ve büyük ölçüde idempotent olacak şekilde yazılmıştır; yine de üretim rollout'undan önce laboratuvarda doğrulanmalıdır.

Bilinen dikkat noktaları:

- Proxmox CLI çıktıları sürümler arasında küçük farklılıklar gösterebilir
- FreeIPA dizin yapıları esnektir; bu nedenle LDAP filter'lar ağacınıza göre ayar isteyebilir
- önceden elle yönetilmiş PVE ACL ve role tanımları, otomasyon bunların üzerine uygulanmadan önce karşılaştırılmalıdır
- Proxmox VM auto-discovery, çalışan guest'lere ve QEMU guest-agent ağ verisine bağlıdır
- IP-only guest tanımları yine de guest içinde geçerli bir nihai host adı veya açık bir `ipa_hostname` ister
- Proxmox playbook'ları privilege escalation ile çalışır; bu yüzden `root` olmayan bir SSH kullanıcısının çalışan `sudo` erişimi olması gerekir ve hesap passwordless sudo kullanmıyorsa `-K` ile become parolası vermelisiniz
- `ansible_become_password` değerini `vault-proxmox.yml` içinde saklıyorsanız `-K` kullanmadan da Ansible sudo parolasını şifreli değişkenden okuyabilir

## Doğrulama

Son durumu doğrulamadan rollout'un tamamlandığını varsaymayın.

### FreeIPA içinde

- beklenen kullanıcı gruplarının oluştuğunu doğrulayın
- beklenen hostgroup tanımlarının oluştuğunu doğrulayın
- beklenen HBAC kurallarının var ve etkin olduğunu doğrulayın
- beklenen `sudo` kurallarının var ve etkin olduğunu doğrulayın

### Proxmox'ta

- LDAP realm tanımının oluştuğunu doğrulayın
- ilk sync işleminden sonra beklenen kullanıcı veya grupların içe aktarıldığını doğrulayın
- hedef senkronize grubun beklenen ACL bağına sahip olduğunu doğrulayın

### Linux konuğu üzerinde

- izin verilen IPA kullanıcısının giriş yapabildiğini doğrulayın
- izin verilmeyen kullanıcının HBAC ile engellendiğini doğrulayın
- izin verilen yönetici hesabının `sudo -l` çalıştırabildiğini doğrulayın
- `linux_ipaclient_mkhomedir` açıksa ilk girişte home dizininin oluşturulduğunu doğrulayın

## Depo düzeni

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

## Geliştirme

Depoya dahil başlıca yardımcı dosyalar şunlardır:

- `.editorconfig`, editörler arasında boşluk, encoding ve satır sonu varsayılanlarını tutarlı tutar
- `.gitattributes`, yaygın metin dosyalarını `LF` satır sonu ile sabitler
- `.gitignore`, üretilen inventory, vault verileri, yerel collection'lar ve editör dosyalarının Git'e girmesini engeller
- `.ansible-lint`, vendor collection yollarını dışlar ve yalnızca YAML satır uzunluğu kuralını bastırır
- `.yamllint`, playbook, inventory ve workflow dosyalarında YAML biçim denetimini tutarlı tutar
- `.github/CODEOWNERS`, ana depo alanları için review sahipliğini yönlendirir
- `.github/workflows/ci.yml`, push ve pull request olaylarında lint ve smoke doğrulamasını çalıştırır
- `.pre-commit-config.yaml`, `pre-commit` kuruluysa commit öncesi hızlı lint hook'unu çalıştırır
- `CHANGELOG.md`, kayda değer depo değişikliklerini tek yerde izler
- `docs/VARIABLES.md`, bölünmüş inventory değişken yapısını açıklar
- `docs/i18n/`, çevrilmiş README dosyalarını barındırır; bunların tam İngilizce bölüm yapısını yansıtması gerekir, canonical kaynak ise `README.md` dosyasıdır
- `docs/i18n/TRANSLATION_GUIDE.md`, çeviri README dosyalarının nasıl senkron tutulacağını açıklar
- `scripts/bootstrap.ps1` ve `scripts/bootstrap.sh`, gerekli collection'ı repo içindeki `collections/` yoluna kurar ve ansible-core 2.24+ uyumluluğu için yama uygular
- `scripts/patch_freeipa_collection.py`, sabitlenmiş FreeIPA collection içindeki deprecated import'ları yeniden yazar; böylece gelecekteki ansible-core sürümleriyle uyumluluk korunur
- `scripts/lint.py`, yerel kullanım, CI ve pre-commit için platformlar arası lint giriş noktası sağlar
- `scripts/smoke-test.py`, gerçek altyapıya dokunmadan example inventory doğrulaması ve syntax kontrolü yapar; ayrı Windows playbook'unu da kapsar
- `scripts/check_translations.py`, çevrilmiş README dosyalarını metadata, bölüm yapısı eşliği ve canonical İngilizce README'ye göre minimum içerik kapsamı açısından denetler
- `scripts/lint.ps1` ve `scripts/lint.sh`, yerel lint ve smoke iş akışını birlikte çalıştırır
- `scripts/proxmox_event_webhook.py`, Proxmox VM olayları için isteğe bağlı controller-side webhook servisidir
- `scripts/proxmox-vm-hook.pl`, `post-start` ve `post-migrate` olaylarında controller webhook'una bildirim gönderen isteğe bağlı Proxmox VM hookscript'idir
- `scripts/run-playbook.ps1`, PowerShell kullanıcıları için yaygın `ansible-playbook` çağrılarını sarmalar; ayrı Windows akışını da destekler
- `scripts/vault.ps1` ve `scripts/vault.sh`, FreeIPA, Proxmox ve isteğe bağlı Windows sırları için split-vault işlemlerini sarmalar
- `tests/`, smoke-test dokümantasyonundan başlayarak depo doğrulama yüzeyini barındırır
- `CONTRIBUTING.md`, beklenen katkı ve doğrulama iş akışını açıklar
- `SECURITY.md`, zafiyet bildirimi ve güvenlik hassas bilgilerin ele alınma sürecini açıklar

Kontrol düğümünüzde `ansible-lint` kuruluysa:

```bash
ansible-lint
```

Depo smoke kontrollerini doğrudan çalıştırmak için:

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

Tam yerel lint geçişi için:

```bash
./scripts/lint.sh
```

```powershell
.\scripts\lint.ps1
```

Her commit öncesi hızlı lint hook'unu etkinleştirmek için:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

PowerShell playbook wrapper artık yaygın operatör seçeneklerini doğrudan destekler:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Sonraki genişletmeler

- IPA-ready Linux template'leri için Packer hattı
- AWX job template ve schedule'ları
- ayrı Proxmox tenant ve pool modelleri
- daha geniş Windows local policy veya GPO entegrasyonu

## Lisans

[0BSD License](../../LICENSE) altında yayımlanır.
