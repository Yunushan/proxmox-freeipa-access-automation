# Proxmox + FreeIPA Zugriffsautomatisierung

Diese Seite bietet eine vollstandige ubersetzte README-Struktur zu [README.md](../../README.md). Die englische Fassung bleibt die verbindliche Quelle, aber diese Ubersetzung deckt dieselben Hauptabschnitte fur deutschsprachige Betreiber ab.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Warum dieses Projekt existiert

Verwenden Sie dieses Repository, wenn bereits vorhanden sind:

- eine funktionierende FreeIPA-Umgebung
- ein Proxmox-VE-Cluster
- Linux-Gaste mit zentraler Authentifizierung
- ein dediziertes FreeIPA-Dienstkonto fur den Proxmox-LDAP-Bind
- ein klares Gruppenmodell fur Administratoren und Operatoren

Das Ziel ist, FreeIPA als Quelle der Wahrheit fur Identitat und Zugriff zu verwenden. Proxmox konsumiert dieses Verzeichnis uber eine LDAP-Realm, Linux-Gaste treten FreeIPA uber die Upstream-Rolle `ipaclient` bei, und SSH-, HBAC- und `sudo`-Steuerung bleiben zentral.

## Was Sie erhalten

- Verwaltung von FreeIPA-Benutzergruppen, Hostgruppen, HBAC-Regeln und `sudo`-Regeln
- Konfiguration einer Proxmox-LDAP-Realm gegen FreeIPA
- periodischen Realm-Sync von einem festgelegten Cluster-Knoten
- Proxmox-RBAC-Bindings fur synchronisierte Verzeichnisgruppen
- Linux-Enrollment uber statisches Inventory, manuelle Hostdefinitionen oder Proxmox-Discovery
- optionales SSH-Bootstrap ohne Reboot uber den QEMU Guest Agent
- optionale Installation des QEMU Guest Agent uber SSH oder WinRM fur erreichbare Gaste
- optionales Initial-Bootstrap fur einen SSH-Public-Key
- automatisches SSSD-Cache-Refresh nach FreeIPA-Anderungen
- optionales ereignisgesteuertes Onboarding uber `post-start` und `post-migrate`

## Umfang

| Enthalten | Nicht enthalten |
| --- | --- |
| FreeIPA-Zugriffsmodell | Windows-Domain-Join |
| Proxmox-LDAP-Realm-Einrichtung | FreeRADIUS-Bereitstellung |
| Proxmox-RBAC aus synchronisierten Gruppen | Vollstandige Benutzer-Lifecycle-Erstellung in FreeIPA |
| Linux-IPA-Enrollment | Vollstandige Abdeckung aller Proxmox-Multitenancy-Kantenfalle |

## Architektur

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

Die langere Architekturerklarung steht in [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Anforderungen

### Controller

- Ansible Core 2.14 oder neuer
- SSH-Erreichbarkeit zu Proxmox-Primarknoten, IPA-Servern und Linux-Clients
- `sudo` oder `root`, wo erforderlich
- bei aktiviertem QGA-SSH-Bootstrap muss der Proxmox Guest Agent im Gast bereits laufen
- bei aktiviertem Windows-QGA-Fallback mussen erreichbare Windows-Systeme in `windows_qemu_guest_agent_clients` stehen
- bei aktiviertem Linux-SSH-Bootstrap braucht der Controller ein SSH-Schlusselpaar und einen initialen Passwortpfad

### Ziele

- Proxmox VE 6.x oder neuer auf dem Host in `proxmox_primary`
- FreeIPA muss von Proxmox und Linux-Clients aus erreichbar sein
- DNS und Zeitsynchronisation mussen stimmen
- fur `proxmox_primary` entweder `root` oder ein SSH-Benutzer mit `sudo` fur `pveversion`, `pvesh` und `pveum`
- bei Proxmox-Discovery mussen Gaste eine nutzbare IP uber den QEMU Guest Agent liefern

## Netzwerkports

Die vollstandige Portmatrix bleibt im englischen README. Fur dieses Projekt sind besonders wichtig:

- `22/TCP` fur SSH vom Controller zu Proxmox, IPA und Linux-Gasten
- `53/TCP,UDP` von Linux-Gasten zu IPA-DNS-Servern, wenn IPA-DNS genutzt wird
- `88/TCP,UDP` und `464/TCP,UDP` fur Kerberos
- `389/TCP` fur LDAP im Linux-Enrollment
- `linux_freeipa_enroll_https_port`, standardmassig `443/TCP`, fur IPA-Web/API-Prufungen
- `636/TCP` als Standard fur die Proxmox-LDAP-Realm bei `ldaps`

## Kompatibilitat

- ausgelegt auf Proxmox VE 6.x und neuer
- standardmassig getestete Major-Versionen: `6`, `7`, `8`, `9`, `10`
- anpassbar uber `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions` ist standardmassig `true`

## Schnellstart

### 1. Beispiel-Inventory und Vault-Dateien kopieren

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
```

### 2. Umgebungsspezifische Dateien bearbeiten

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

Wahlen Sie zusatzlich eine Linux-Quellmethode: statische Hosts, `linux_ipa_client_hosts` oder Proxmox-Discovery.

### 3. Vault-Dateien verschlusseln

```bash
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
```

### 4. Benotigte Collection installieren

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

### 5. Zuerst validieren

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

### 6. Anderungen optional im Voraus ansehen

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

### 7. Vollstandige Konfiguration anwenden

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## Rollout-Reihenfolge

Fur die erste Bereitstellung:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Standardmassig gilt:

- FreeIPA-Anderungen mit `serial: 1`
- Proxmox-Anderungen mit `serial: 1`
- Linux-Discovery, Hostname-Auflosung und Enrollment mit `serial: 10`
- `max_fail_percentage: 0` auf allen Pfaden

## Tag-Modell

- Kerndomanen: `freeipa`, `proxmox`, `linux`, `validate`
- FreeIPA-Modell: `freeipa_access`
- Proxmox-Teilbereiche: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux-Vorbereitung: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux-Enrollment: `linux_enroll`
- Event-Pfad: `event`, `linux_refresh`

## Ereignisgesteuertes VM-Onboarding

Wenn Proxmox Linux-Discovery und IPA-Enrollment direkt nach Start oder Migration auslosen soll, verwenden Sie den optionalen Hook/Webhook-Workflow aus [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

- der Event-Pfad verwendet `playbooks/proxmox-vm-event.yml`
- Proxmox-LDAP-Realm und RBAC werden dabei nicht bei jedem Event erneut ausgerollt
- Proxmox-Hooks haben keinen separaten `create`-Phase-Hook; neue VMs werden praktisch beim ersten `post-start` erfasst
- der optionale Stack kann auch aus `site.yml` oder `proxmox.yml` bereitgestellt werden

## Inventory-Modell

Die zentralen Gruppen sind:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

Wenn Sie nur IPs oder Proxmox-Discovery nutzen, braucht jeder Gast trotzdem den endgultigen FQDN uber `ipa_hostname` oder `hostname -f`.

### Linux-Quellmodi

1. statische Inventory-Hosts
2. manuelle Definitionen in `linux_ipa_client_hosts`
3. automatische Proxmox-Discovery uber `linux_ipa_proxmox_discovery_*`

Wichtige Hinweise:

- Discovery hangt von Netzwerkinformationen aus dem QEMU Guest Agent ab
- `linux_ipa_proxmox_discovery_vmids` ist vor allem fur den Event-Workflow gedacht
- mit `linux_ipa_identity_hostname_suffix` und `linux_freeipa_enroll_manage_hostname: true` lassen sich kurze Hostnamen auf volle FQDNs erweitern
- mit `linux_freeipa_enroll_manage_authoritative_dns: true` kann autoritatives IPA-DNS fur Gaste vor dem Enrollment repariert werden
- wenn DNS noch nicht bereit ist, helfen `linux_ipa_manage_etc_hosts: true` und `linux_ipa_etc_hosts_entries`
- `linux_ipa_qga_ssh_bootstrap_enabled` ist der bevorzugte No-Reboot-Bootstrap-Pfad

## Konfigurationsoberflache

Die meisten Werte liegen in:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

Fur die dateibasierte Aufteilung siehe [docs/VARIABLES.md](../VARIABLES.md).

## Beispiel fur eine Gruppenstrategie

- FreeIPA-Benutzergruppe `proxmox-admins`
- FreeIPA-Benutzergruppe `linux-ssh-admins`
- FreeIPA-Hostgruppe `linux-all`
- HBAC-Regel `allow-linux-ssh-admins`
- `sudo`-Regel `allow-linux-ssh-admins-sudo`
- Proxmox-ACL-Binding fur die synchronisierte Gruppe `proxmox-admins-ipa`

## Sicherheit

- Geheimnisse nur in Vault-Dateien speichern
- fur Proxmox nach Moglichkeit ein dediziertes Read-only-LDAP-Bind-Konto verwenden
- TLS mit Zertifikatsprufung bevorzugen
- SSH-Host-Key-Prufung ausserhalb von Wegwerf-Laboren aktiviert lassen
- nach Moglichkeit `linux_ipa_qga_ssh_bootstrap_enabled` statt gemeinsamer Bootstrap-Passworter nutzen

## Idempotenz und Hinweise

Das Projekt ist weitgehend wiederverwendbar und idempotent, sollte aber vor Produktiveinsatz im Labor validiert werden. Bekannte Grenzen:

- Proxmox-CLI-Ausgaben variieren leicht je nach Version
- LDAP-Filter mussen eventuell an Ihre Verzeichnisstruktur angepasst werden
- Proxmox-Discovery hangt von laufenden Gasten und QGA-Netzdaten ab
- IP-only-Definitionen benotigen trotzdem einen gultigen finalen Hostnamen

## Verifikation

Nach erfolgreichem Rollout prufen Sie:

- in FreeIPA: Gruppen, Hostgruppen, HBAC-Regeln und `sudo`-Regeln
- in Proxmox: LDAP-Realm, initialen Sync und ACL-Bindings
- auf Linux-Gasten: erlaubter Login, geblockter unerlaubter Benutzer, `sudo -l`, Home-Verzeichnis bei erstem Login

## Repository-Struktur

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

Die vollstandige Baumansicht bleibt im englischen README dokumentiert.

## Entwicklung

Hilfsdateien im Repository:

- `.editorconfig`, `.gitattributes`, `.gitignore`
- `.ansible-lint`, `.yamllint`
- `.github/workflows/ci.yml`
- `scripts/bootstrap.ps1`, `scripts/bootstrap.sh`
- `scripts/lint.py`, `scripts/lint.ps1`, `scripts/lint.sh`
- `scripts/smoke-test.py`
- `scripts/proxmox_event_webhook.py`
- `scripts/proxmox-vm-hook.pl`
- `scripts/run-playbook.ps1`
- `scripts/vault.ps1`, `scripts/vault.sh`

Nutzliche Befehle:

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
.\scripts\lint.ps1
```

## Mogliche nachste Erweiterungen

- Packer-Pipeline fur IPA-fertige Linux-Templates
- AWX-Job-Templates und Zeitplane
- getrennte Proxmox-Tenant- und Pool-Modelle
- Windows- oder AD-Trust-Pfade fur RDP-orientierte Umgebungen

## Lizenz

Freigegeben unter der [MIT License](../../LICENSE).
