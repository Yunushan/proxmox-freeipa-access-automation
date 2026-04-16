# Proxmox + FreeIPA Zugriffsautomatisierung

Diese Seite bietet eine vollstaendige, strukturtreue Uebersetzung von [README.md](../../README.md). Die englische Fassung bleibt die verbindliche Quelle, aber diese deutsche Version soll denselben operativen Umfang fuer deutschsprachige Betreiber abdecken.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-15

## Sprachen

Die englische Fassung ist die kanonische Quelle fuer die vollstaendige Dokumentation. Weitere Sprachversionen und den Uebersetzungsindex finden Sie unter [docs/i18n/README.md](README.md).

## Warum dieses Projekt existiert

Verwenden Sie dieses Repository, wenn Sie bereits ueber Folgendes verfuegen:

- eine gesunde FreeIPA-Umgebung
- ein Proxmox-VE-Cluster
- Linux-Gaeste, die zentral authentifiziert werden sollen
- ein dediziertes FreeIPA-Dienstkonto fuer den Proxmox-LDAP-Bind
- ein klares Benutzer- und Gruppenmodell fuer Administratoren und Operatoren

Das Ziel ist, FreeIPA als Quelle der Wahrheit fuer Identitaet und Zugriff zu verwenden. Proxmox konsumiert dieses Verzeichnis ueber eine LDAP-Realm, Linux-Gaeste treten FreeIPA ueber die Upstream-Rolle `ipaclient` bei, und SSH-, HBAC- und `sudo`-Steuerung bleiben zentral statt ueber lokale Einzelkonten zu zerfasern.

## Was Sie erhalten

- Verwaltung von FreeIPA-Benutzergruppen, Hostgruppen, HBAC-Regeln und `sudo`-Regeln
- automatische FreeIPA-Login-Shell-Defaults fuer Linux-Administratoren
- Konfiguration einer Proxmox-LDAP-Realm gegen FreeIPA
- wiederkehrenden Proxmox-Realm-Sync von einem festgelegten Cluster-Knoten
- Proxmox-RBAC-Bindings fuer synchronisierte Verzeichnisgruppen
- Linux-Enrollment in FreeIPA ueber statisches Inventory, reine IP-Ziele oder Proxmox-VM-Discovery
- optionales SSH-Bootstrap ohne Reboot ueber den Proxmox QEMU Guest Agent
- optionale Aktivierung der Proxmox-seitigen Guest-Agent-Kommunikation fuer Proxmox-basierte Linux-Gaeste
- optionale SSH- oder WinRM-basierte Fallback-Installation des QEMU Guest Agent fuer Gaeste, die bereits erreichbar sind, spaeter erreichbar werden oder nach Linux-Enrollment erneut versucht werden
- optionales Linux-Readiness-Reporting fuer SSH-Erreichbarkeit und Proxmox-QEMU-Guest-Agent-Status
- optionalen separaten Windows-Domain-Membership-Workflow fuer Windows 10/11 und Windows Server ueber Active Directory
- optionalen begrenzten FreeIPA-bewussten Windows-Helfer-Workflow fuer IPA-CA-Trust, Hosts-Bootstrap und IPA-Erreichbarkeitspruefungen
- optionales First-Touch-SSH-Public-Key-Bootstrap fuer Linux-Gaeste
- automatische SSSD-Cache-Aktualisierung auf verwalteten Linux-Clients nach Aenderungen am FreeIPA-Zugriffsmodell
- optionales ereignisgesteuertes Linux-Onboarding ueber Proxmox-VM-Hook und Webhook-Trigger

## Umfang

| Enthalten | Nicht enthalten |
| --- | --- |
| FreeIPA-Zugriffsmodell | FreeRADIUS-Bereitstellung |
| Proxmox-LDAP-Realm-Einrichtung | FreeIPA-Benutzer-Lifecycle-Erstellung |
| Proxmox-RBAC aus synchronisierten Gruppen | Vollstaendige Proxmox-Multitenancy-Policy-Abdeckung |
| Linux-IPA-Client-Enrollment | Nativer Windows-Login direkt gegen FreeIPA |
| Separater Windows-AD-Domain-Membership-Workflow | GPO oder breitere AD-Objekt-Lifecycle-Automatisierung |
| Begrenzter FreeIPA-bewusster Windows-Helfer-Workflow | Das Vorspiegeln, dass FreeIPA-only-Windows-Helfer AD gleichwertig ersetzen |

## Windows-Workflow

Windows-Unterstuetzung wird als separater Workflow umgesetzt und nicht in den Linux-IPA-Enrollment-Pfad eingemischt.

- `windows_qemu_guest_agent_clients` bleibt ausschliesslich fuer optionale QEMU-Guest-Agent-Helferaufgaben reserviert.
- Aktivieren Sie den Workflow mit `windows_domain_membership_enabled: true` in `10-features.yml`.
- `windows_management_clients` ist die separate Windows-Management-Gruppe, die von `playbooks/windows-management.yml` und vom optionalen Windows-Abschnitt in `playbooks/site.yml` verwendet wird.
- Der eigentliche Windows-Login erfolgt ueber Active-Directory-Domain-Membership; in FreeIPA-zentrierten Umgebungen sollten Windows-Hosts an die AD-Seite eines FreeIPA-AD-Trusts angebunden werden, anstatt Windows direkt gegen FreeIPA joinen zu wollen.

Ein FreeIPA-only-Windows-Domain-Join wird von diesem Repository nicht unterstuetzt. Ohne Active Directory oder einen FreeIPA-AD-Trust bleibt der Windows-Workflow auf Hilfsaufgaben wie erreichbares Gast-Management und optionale QEMU-Guest-Agent-Installation beschraenkt.

Wenn Sie trotzdem einen begrenzten FreeIPA-bewussten Pfad fuer Windows ohne Domain-Join wollen, aktivieren Sie `windows_freeipa_helpers_enabled: true` und verwenden Sie `windows_freeipa_helper_clients` mit `playbooks/windows-freeipa-helpers.yml`. Dieser Helfer-Workflow kann der IPA-CA vertrauen, die IPA-CA optional fuer Bootstrap automatisch beziehen, optional den erwarteten Thumbprint der IPA-CA pinnen, optionale Hosts-Datei-Bootstrap-Eintraege verwalten, IPA-DNS und wichtige TCP-Ports pruefen, HTTPS-Erreichbarkeit aus Windows heraus pruefen, eine Windows-Zeitquelle gegen einen IPA-bezogenen Endpunkt validieren, lokale Windows-Gruppenmitgliedschaften verwalten und optional OpenSSH Server installieren oder bereitstellen. Er liefert jedoch keinen nativen Windows-Login gegen FreeIPA.

Wenn Sie dafuer einen nicht mutierenden Readiness-Check moechten, verwenden Sie `playbooks/windows-freeipa-validate.yml`. Dieser Pfad behaelt Validierung und Zusammenfassung bei, erzwingt fuer diesen Lauf aber, dass CA-Import, Hosts-Datei-Aenderungen, lokale Gruppen-Aenderungen und OpenSSH-Verwaltung ausgeschaltet bleiben.

Dieser Workflow richtet sich an Windows-10/11- und Windows-Server-Gaeste, die ueber WinRM oder PSRP erreichbar sind.

## Architektur

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

Die laengere Design-Erklaerung finden Sie unter [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Anforderungen

### Controller

- Ansible Core 2.14+
- SSH-Erreichbarkeit zu Ihrem Proxmox-Primary-Node, IPA-Server und Linux-Clients
- WinRM- oder PSRP-Erreichbarkeit zu Windows-Gaesten, wenn Sie den Windows-Workflow verwenden
- `sudo` oder `root`, wo erforderlich
- wenn Linux-QGA-SSH-Bootstrap aktiviert ist, muss der Proxmox Guest Agent bereits im Gast aktiv sein
- wenn die Guest-Agent-Fallback-Installation fuer Windows aktiviert ist, muessen erreichbare Windows-Hosts in `windows_qemu_guest_agent_clients` stehen
- wenn Windows-Domain-Membership aktiviert ist, muessen erreichbare Windows-Hosts in `windows_management_clients` stehen und Sie muessen AD-Join-Zugangsdaten bereitstellen
- wenn Windows-FreeIPA-Helferaufgaben aktiviert sind, muessen erreichbare Windows-Hosts in `windows_freeipa_helper_clients` stehen
- wenn Linux-SSH-Bootstrap aktiviert ist, benoetigt der Controller ein SSH-Schluesselpaar und einen initialen passwortfaehigen Login-Pfad fuer das von Ansible verwendete Gastkonto

### Ziele

- Proxmox VE 6.x oder neuer auf dem Host in `proxmox_primary`
- FreeIPA muss von Proxmox und Linux-Clients aus erreichbar sein
- Windows 10/11 und Windows Server koennen ueber den separaten Windows-Workflow verwaltet werden, wenn sie ueber WinRM oder PSRP erreichbar sind
- sinnvolle DNS- und Zeit-Synchronisation
- fuer `proxmox_primary` entweder Verbindung als `root` oder ein SSH-Benutzer, der `sudo` fuer `pveversion`, `pvesh` und `pveum` verwenden kann
- wenn Sie Windows-Domain-Membership nutzen, muessen die Ziel-Windows-Gaeste die relevanten AD-Domain-Controller erreichen koennen
- wenn Sie den begrenzten Windows-FreeIPA-Helfer-Workflow nutzen, muessen die Ziel-Windows-Gaeste die relevanten IPA-Server erreichen koennen
- wenn Sie Proxmox-VM-Auto-Discovery verwenden, muessen gefundene Gaeste eine verwendbare IP ueber den QEMU Guest Agent liefern

## Netzwerkports

Diese Tabelle listet die Netzwerkports auf, die vom Controller dieses Repositorys, von der Proxmox-LDAP-Automatisierung und vom Linux-IPA-Enrollment-Pfad verwendet werden.
Sie ist absichtlich auf dieses Projekt begrenzt und bildet nicht die vollstaendige FreeIPA-Server-zu-Server-Replikationsmatrix ab.

| Name | Port | Protokoll | Quelle | Ziel | Erforderlich wenn | Zweck |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Ansible-Controller | Proxmox-Node, IPA-Server, Linux-Gast | Immer | Ansible-Konnektivitaet |
| WinRM | `5985`, `5986` | `TCP` | Ansible-Controller | Windows-Gast | Wenn Windows-Management aktiviert ist | Ansible-Konnektivitaet zu Windows-Gaesten |
| DNS | `53` | `TCP`, `UDP` | Linux-Gast | IPA-DNS-Server | Wenn Linux-Gaeste IPA-DNS verwenden | IPA-Records und externe Namen ueber IPA-DNS aufloesen |
| Kerberos | `88` | `TCP`, `UDP` | Linux-Gast | IPA-Server | Linux-IPA-Enrollment und Login | Kerberos-Authentifizierung |
| LDAP | `389` | `TCP` | Linux-Gast | IPA-Server | Linux-IPA-Enrollment und Login | LDAP und FreeIPA-Client-Discovery |
| HTTPS | `linux_freeipa_enroll_https_port` Standard `443` | `TCP` | Linux-Gast | IPA-Server | Linux-IPA-Enrollment | IPA-Web/API-Validierung waehrend der Client-Installation |
| Kerberos Password | `464` | `TCP`, `UDP` | Linux-Gast | IPA-Server | Linux-IPA-Enrollment und Passwort-Operationen | Kerberos-Passwort- und Keytab-Operationen |
| LDAPS | `636` | `TCP` | Proxmox-Primary-Node | IPA- oder LDAP-Server | Proxmox-LDAP-Realm im Default-Modus `ldaps` | Proxmox-LDAP-Realm-Verbindung |

Hinweise:

- `LDAPS 636/TCP` ist der Repository-Default, weil `proxmox_ldap_mode` standardmaessig `ldaps` ist. Wenn Sie LDAP-Modus oder Port aendern, erlauben Sie stattdessen den konfigurierten `proxmox_ldap_port`.
- `WinRM` verwendet je nach Windows-Transport-Setup haeufig `5986/TCP` fuer HTTPS oder `5985/TCP` fuer HTTP.
- `DNS 53/TCP,UDP` wird nur benoetigt, wenn Linux-Gaeste die IPA-Server als Resolver verwenden.
- `Kerberos 88` und `Kerberos Password 464` benoetigen sowohl `TCP` als auch `UDP`.
- Ein Active-Directory-Domain-Join benoetigt ausserdem den ueblichen Windows-zu-Domain-Controller-Portsatz; diese Matrix ist jedoch umgebungsspezifisch und hier absichtlich nicht vollstaendig aufgefuehrt.
- Zeitsynchronisation bleibt fuer zuverlaessiges Kerberos weiterhin erforderlich, aber die NTP-Quelle ist umgebungsspezifisch und wird von diesem Repository nicht verwaltet.

## Kompatibilitaet

Die Proxmox-Automatisierung in diesem Repository ist um die `pveum`- und `pvesh`-Schnittstellen fuer Realm und RBAC herum geschrieben, wie sie in Proxmox VE 6.x und spaeteren Releases verwendet werden.

- standardmaessig unterstuetzte Major-Versionen: `6`, `7`, `8`, `9`, `10`
- die Validierung prueft die erkannte Proxmox-Version ueber `pveversion`
- die Liste der unterstuetzten Versionen kann ueber `proxmox_supported_major_versions` angepasst werden, wenn Sie sie in Ihrer Umgebung einengen oder erweitern muessen
- `proxmox_allow_future_major_versions` steht standardmaessig auf `true`, daher bestehen auch Major-Versionen oberhalb der hoechsten gelisteten getesteten Version die Validierung standardmaessig
- kuenftige Major-Versionen sollten dennoch als Kompatibilitaetskandidaten behandelt werden, bis die veroeffentlichte Proxmox-Schnittstelle gegen diese Automatisierung geprueft wurde
- aeltere Legacy-Majors wie `1` bis `5` werden von diesem oeffentlichen Repository nicht als getestete Unterstuetzung beansprucht; wenn Sie sie lokal hinzufuegen, behandeln Sie das als ausdruecklichen Kompatibilitaets-Override und validieren Sie den kompletten Workflow zuerst in einem Labor

Beispiel fuer einen lokalen Override in einer Legacy-Lab-Umgebung:

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

## Schnellstart

Die folgenden Beispiele verwenden Shell-Befehle. PowerShell-Aequivalente sind dort enthalten, wo das voraussichtlich relevant ist.

### 1. Beispiel-Inventory und Vault-Dateien kopieren

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Optional, wenn Sie Windows-Gaeste verwalten wollen:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Optional, wenn Sie Windows-Gaeste verwalten wollen:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Umgebungsspezifische Dateien bearbeiten

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml`, wenn Sie Windows-Management verwenden
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml`, wenn Sie Windows-Management verwenden

Waehlen Sie neben den IPA- und Proxmox-Einstellungen genau einen Linux-Gast-Quellmodus:

- statische Inventory-Eintraege unter `linux_ipa_clients`
- `linux_ipa_client_hosts`-Eintraege in `group_vars/all/30-linux-clients.yml`
- Proxmox-VM-Discovery mit `linux_ipa_proxmox_discovery_enabled: true`

Halten Sie fuer Linux-IPA-Enrollment Domain- und Serverwerte getrennt:

- `ipaclient_domain` ist die gemeinsame IPA-DNS-Domain, zum Beispiel `example.com`
- `linux_ipa_servers` enthaelt IPA-Server-Hostnamen, zum Beispiel `ipa01.example.com`

Wenn Sie statt `root` einen normalen sudo-faehigen Benutzer fuer SSH auf Proxmox nutzen wollen, setzen Sie dies in `hosts.yml` unter `proxmox_primary` und halten Sie das sudo-Passwort in `vault-proxmox.yml`:

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

In dieser Konfiguration ist `vault_proxmox_become_password` das Passwort, das Sie normalerweise fuer `sudo` auf dem Proxmox-Host eintippen wuerden.

### 3. Vault-Dateien verschlusseln

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

Fuegen Sie `inventories/production/group_vars/all/vault-windows.yml` zum selben Befehl hinzu, wenn Sie den Windows-Workflow aktivieren.

Oder verwenden Sie die Helper-Wrapper, die standardmaessig getrennte Vault-IDs verwenden und die Arbeits-Vault-Dateien bei Bedarf aus den Beispiel-Templates erzeugen:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Wenn Sie beim Ausfuehren der Playbooks getrennte Passwoerter pro Bereich verwenden wollen, bevorzugen Sie Vault-IDs gegenueber `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Wenn der optionale Windows-Workflow ebenfalls ein eigenes Vault-Passwort verwendet, fuegen Sie demselben Befehl `windows@prompt` hinzu.

Verwenden Sie `-AskVaultPass` nur dann, wenn alle von diesem Playbook verwendeten Vault-Dateien dasselbe Passwort teilen.

### 4. Benotigte Collection installieren

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Oder direkt:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

Wenn Sie `freeipa.ansible_freeipa` installiert haben, bevor dieses Repository den Kompatibilitaets-Patch hinzufuegte, fuehren Sie einen der Bootstrap-Helper erneut aus oder rufen Sie `python .\scripts\patch_freeipa_collection.py` einmal direkt auf, um auch die bestehende benutzerspezifische Collection-Installation zu patchen.

Wenn Sie `scripts/run-playbook.ps1` verwenden, wird der Patch-Helper vor `ansible-playbook` automatisch ausgefuehrt.

### 5. Zuerst validieren

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Wenn Sie nur den helper-only-Windows-FreeIPA-Pfad validieren wollen, ohne Hosts zu veraendern:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Wenn Sie einen read-only Linux-Readiness-Audit wollen, der meldet, welche Runtime-Gaeste ueber SSH erreichbar sind und welche Proxmox-entdeckten Gaeste ueber den QEMU Guest Agent antworten:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Der Readiness-Report schreibt standardmaessig `.ansible/linux-readiness-report.json`.
Interpretieren Sie die wichtigsten Felder wie folgt:

- `ssh.ready=true`: der aktuell konfigurierte Ansible-SSH-Pfad funktionierte vom Controller aus
- `ssh.promptless=true`: der SSH-Probe war ohne `ansible_password` erfolgreich, also ist der Pfad fuer Ansible nicht interaktiv
- `ssh.auth_mode=password_configured`: der Probe verwendete `sshpass`, weil der Host `ansible_password` gesetzt hatte
- `ssh.auth_mode=key_or_agent`: der Probe war im SSH-Batch-Modus ohne `ansible_password` erfolgreich
- `qga.status=available`: `qm guest ping` war auf dem besitzenden Proxmox-Node erfolgreich
- `qga.status=disabled`: in der Proxmox-VM-Konfiguration ist QEMU Guest Agent nicht aktiviert
- `qga.status=configured_unresponsive`: der Guest Agent ist in Proxmox konfiguriert, reagierte aber nicht
- `qga.status=node_unreachable`: der Controller konnte den besitzenden Proxmox-Node fuer die Probe nicht erreichen
- `qga.status=not_applicable`: der Host wurde nicht ueber Proxmox-Discovery erzeugt, daher wurde kein QGA-Probe versucht

Beispiel fuer eine schnelle Auswertung:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. Anderungen optional im Voraus ansehen

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Behandeln Sie den Check-Mode als Teilvorschau, nicht als vollstaendige Simulation. Dieses Repository verwendet fuer Teile der Proxmox-Konfiguration direkte CLI-Befehle und fuer Linux-Enrollment die Upstream-FreeIPA-Client-Rolle, daher ist `--check` nuetzlich, aber nicht absolut massgeblich.
>
> Bei FreeIPA-HBAC-Regeln validiert der Check-Mode den Regeldefinitions-Schritt, ueberspringt aber die anschliessende Enable- oder Disable-Aktion. Das vermeidet Scheinausfaelle, bei denen FreeIPA meldet, die Regel sei nicht vorhanden, obwohl sie im Dry Run gar nicht angelegt wurde.
>
> Die Proxmox-Realm-Sync-Timer-Rolle ueberspringt im Check-Mode ebenfalls den finalen `systemd`-Enable- oder Start-Schritt, weil Unit-Dateien zwar diffbar sind, waehrend des Dry Runs aber nicht wirklich geschrieben werden.
>
> Linux-IPA-Enrollment wird im Check-Mode ebenfalls uebersprungen. Das Repository fuehrt Discovery, Hostname-Aufloesung und Eingabevalidierung trotzdem durch, die Upstream-Rolle `ipaclient` wird im Dry Run jedoch nicht ausgefuehrt.

### 7. Vollstandige Konfiguration anwenden

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

Wenn der optionale Windows-Workflow aktiviert ist und `vault-windows.yml` ein separates Passwort verwendet, rufen Sie dasselbe Playbook statt mit `--ask-vault-pass` mit `--vault-id windows@prompt` auf oder nutzen im PowerShell-Wrapper `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt`.

## Rollout-Reihenfolge

Wenden Sie den Stack fuer die erste Bereitstellung in dieser Reihenfolge an:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Optional, wenn Sie Windows-Gaeste verwalten:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Optional, wenn Sie den begrenzten Windows-FreeIPA-Helfer-Workflow wollen:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Optional, wenn Sie nur Validierung fuer den Helfer-Workflow wollen:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

Diese Reihenfolge macht die Fehlersuche erheblich einfacher, als alles gleichzeitig auszufuehren.

Fuer einen begrenzten PowerShell-Rollout, zum Beispiel nur fuer einen Linux-Gast:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Die Standard-Rollout-Steuerung ist bewusst konservativ:

- FreeIPA-Anderungen mit `serial: 1`
- Proxmox-Anderungen mit `serial: 1`
- Linux-Discovery, Hostname-Auflosung und Enrollment mit `serial: 10`
- Windows-Management-Aenderungen mit `serial: 10`
- `max_fail_percentage: 0` auf allen Pfaden

Passen Sie diese Werte in `inventories/production/group_vars/all/15-rollout.yml` an.

## Tag-Modell

- Verwenden Sie Tags, um stabile Rollout-Slices gezielt anzusprechen, anstatt immer mehr Playbooks zu erstellen.
- Kerndomaenen: `freeipa`, `proxmox`, `linux`, `validate`
- Windows-Bereich: `windows`, `windows_domain`
- Windows-FreeIPA-Helfer: `windows`, `windows_freeipa`
- FreeIPA-Modell: `freeipa_access`
- Proxmox-Teilbereiche: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- Linux-Vorbereitung: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- Linux-Enrollment: `linux_enroll`
- Event-Pfad: `event`, `linux_refresh`

Beispiele:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Ereignisgesteuertes VM-Onboarding

Wenn Proxmox Linux-Discovery und IPA-Enrollment unmittelbar nach VM-Starts oder Migrationen ausloesen soll, verwenden Sie den optionalen Hook- und Webhook-Workflow aus [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

Dieser Workflow verwendet ein dediziertes Event-Playbook unter `playbooks/proxmox-vm-event.yml`, sodass der Trigger-Pfad nur die Linux- und FreeIPA-Gastseite behandelt. Er rollt weder Proxmox-LDAP-Realm noch RBAC bei jedem VM-Ereignis erneut aus.

Das Repository kann diesen optionalen Hook- und Webhook-Stack inzwischen auch aus `site.yml` oder `proxmox.yml` heraus ausbringen, wenn `proxmox_vm_event_onboarding_enabled: true` gesetzt ist und die erforderlichen Webhook-Variablen bereitstehen.

Proxmox-VM-Hooks besitzen keine eigenstaendige `create`-Phase. In der Praxis werden neue VMs ueber ihr erstes `post-start`-Ereignis erfasst, und Migrations-Hooks koennen sowohl auf Quell- als auch auf Ziel-Node ausloesen.

## Inventory-Modell

Dieses Repository verwendet sechs deklarierte Inventory-Gruppen plus eine generierte Runtime-Gruppe:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Sie koennen eigene Inventory-Gruppen hinzufuegen und sie in FreeIPA-Hostgruppen-Definitionen referenzieren. Wenn Sie den kompletten vorbereiteten Linux-Gast-Satz in FreeIPA-Hostgruppen verwenden wollen, referenzieren Sie `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> FreeIPA benoetigt weiterhin den finalen Hostnamen jedes Gasts. Wenn Sie reine IP-Ziele oder Proxmox-Discovery verwenden, setzen Sie entweder `ipa_hostname` explizit oder stellen Sie sicher, dass `hostname -f` im Gast den finalen FQDN liefert. Die Playbooks loesen diesen Hostnamen jetzt auf, bevor die FreeIPA-Hostgruppen-Mitgliedschaft aufgebaut wird.

> [!TIP]
> Enrollen Sie keine wiederverwendbare Golden Template direkt in FreeIPA. Klonen Sie die VM zuerst, vergeben Sie den finalen Hostnamen und enrollen Sie dann den resultierenden Gast.

### Linux-Quellmodi

Sie koennen `linux_ipa_clients` auf drei verschiedene Arten befuellen.

`1.` Statische Inventory-Hosts

Verwenden Sie normale Ansible-Inventory-Eintraege, wenn Sie die Gastnamen bereits kennen:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

`2.` Manuelle Hostdefinitionen in Variablen

Verwenden Sie `linux_ipa_client_hosts`, wenn Sie Gaeste nicht in `hosts.yml` fuehren wollen oder wenn Ihnen nur eine IP vorliegt:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Hinweise:

- wenn `name` ein aufloesbarer Hostname oder FQDN ist, ist `ansible_host` optional
- wenn Sie nur die IP kennen, verwenden Sie fuer `name` einen stabilen Alias
- wenn `ipa_hostname` fehlt, faellt das Playbook auf `hostname -f` im Gast zurueck

`3.` Proxmox-VM-Auto-Discovery

Verwenden Sie Discovery, wenn das Playbook Linux-Gaeste von einem oder mehreren Proxmox-Nodes einsammeln soll:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Optional: discovery-getriebene Automatisierung nur auf freigegebene Gaeste begrenzen.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Optional: Infrastruktur- oder sensible Gaeste immer ausnehmen, selbst wenn
# breite Node-Discovery aktiviert ist.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
```

Wichtige Hinweise:

- Discovery fuegt VMs derselben `linux_ipa_clients_runtime`-Gruppe hinzu, die vom Rest der Playbooks verwendet wird
- die IP-Discovery haengt davon ab, dass der QEMU Guest Agent Netzwerkschnittstellen meldet
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` vertraut nur VM-Namen, die bereits FQDNs sind
- setzen Sie `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true`, wenn Sie auch sichere kurze Proxmox-VM-Namen automatisch ueber `linux_ipa_identity_hostname_suffix` in FQDN-Hinweise umwandeln wollen
- `linux_ipa_proxmox_discovery_vmids` ist optional und wird vor allem im event-gesteuerten Hook- und Webhook-Workflow verwendet, um Discovery auf bestimmte VMIDs einzugrenzen
- der Gast benoetigt weiterhin einen finalen Hostnamen, entweder bereits im System gesetzt oder ueber `ipa_hostname` in einer manuellen Definition
- der reale System-Hostname des Gasts muss fuer das Enrollment gueltig sein; Platzhalter wie `localhost.localdomain` muessen vor dem Lauf von `linux-clients` oder `site` ersetzt werden
- wenn Gaeste kurze Hostnamen verwenden, koennen Sie `linux_ipa_identity_hostname_suffix` und optional `linux_freeipa_enroll_manage_hostname: true` setzen, damit das Projekt vor dem Enrollment einen vollstaendigen Hostnamen aufloest und anwendet
- wenn FreeIPA-DNS fuer Ihre Gast-Hostnamen autoritativ ist, koennen Sie `linux_freeipa_enroll_manage_authoritative_dns: true` setzen, damit das Projekt A- und PTR-Records repariert und Link-Local-AAAA-Records vor dem Enrollment entfernt
- wenn DNS noch nicht bereit ist, koennen Sie `linux_ipa_manage_etc_hosts: true` und `linux_ipa_etc_hosts_entries` verwenden, um einen verwalteten Bootstrap-Block in `/etc/hosts` zu schreiben
- `guest_qemu_agent_install_enabled` installiert den QEMU Guest Agent auf Gaesten, die bereits ueber SSH oder WinRM erreichbar sind, versucht es spaeter im selben Workflow erneut und wiederholt den Versuch nach Linux-Enrollment
- setzen Sie `linux_ipa_proxmox_discovery_allowlist_enabled: true`, wenn Discovery aktiv bleiben soll, aber nur eine eng freigegebene Teilmenge von Proxmox-Gaesten in das Linux-Runtime-Inventory aufgenommen werden darf
- setzen Sie `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips` oder `linux_ipa_proxmox_discovery_blacklist_names`, wenn Discovery-faehige Nodes auch Infrastruktur-VMs hosten, die niemals Linux-IPA-Automatisierung erhalten duerfen; Blacklist-Matches gewinnen immer gegen breite Discovery oder Allowlist-Zulassung
- `linux_ipa_qga_ssh_bootstrap_enabled` ist der bevorzugte No-Reboot-Bootstrap-Pfad fuer Proxmox-basierte Gaeste
- `linux_ipa_ssh_bootstrap_enabled` installiert optional den SSH-Public-Key des Controllers vor Hostname-Aufloesung und Enrollment
- Linux-IPA-Enrollment wiederholt Upstream-Client-Joins, die mit FreeIPA-JSON-RPC-Timeout fehlschlagen
- der kombinierte `site`-Workflow erzeugt FreeIPA-Hostgruppen vor dem Linux-Enrollment und fuegt die enrolled Runtime-Hosts danach hinzu

## Konfigurationsoberflache

Die meisten Werte liegen in:

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

Fur die dateibasierte Aufteilung siehe [docs/VARIABLES.md](../VARIABLES.md).

Wichtige Variablenfamilien:

| Bereich | Variablen |
| --- | --- |
| FreeIPA-Zugriffsmodell | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Rollout-Steuerung | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| Proxmox-LDAP-Realm | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| Proxmox-RBAC | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Linux-IPA-Enrollment | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Linux-Readiness-Reporting | `linux_readiness_report_*` |
| Windows-Management | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Windows-FreeIPA-Helfer | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Ansible-Verbindungs-Geheimnisse | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Beispiel fur eine Gruppenstrategie

Ein einfaches Muster, das gut skaliert:

- FreeIPA-Benutzergruppe `proxmox-admins`
- FreeIPA-Benutzergruppe `linux-ssh-admins`
- FreeIPA-Hostgruppe `linux-all`
- HBAC-Regel `allow-linux-ssh-admins`
- `sudo`-Regel `allow-linux-ssh-admins-sudo`
- Proxmox-ACL-Binding fur die synchronisierte Gruppe `proxmox-admins-ipa`

Belegen Sie `freeipa_linux_admin_users` in [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml), wenn ein kombinierter `site.yml`-Lauf bestimmten IPA-Benutzern automatisch Linux-SSH- und `sudo`-Zugriff ueber die verwaltete Gruppe `linux-ssh-admins` geben soll.

Denken Sie daran, dass Proxmox-LDAP-Sync synchronisierte Gruppen mit folgendem Suffix erzeugt:

```text
<group-name>-<realm>
```

Wenn Ihre FreeIPA-Gruppe `proxmox-admins` heisst und die Proxmox-Realm `ipa` ist, ergibt sich daraus in PVE:

```text
proxmox-admins-ipa
```

## Sicherheit

- speichern Sie alle Geheimnisse in `vault-freeipa.yml` und `vault-proxmox.yml`, nicht in unverschluesselten Inventory-Variablen
- verwenden Sie fuer Proxmox nach Moeglichkeit ein dediziertes Read-only-LDAP-Bind-Konto
- bevorzugen Sie TLS mit aktivierter Zertifikatspruefung
- lassen Sie SSH-Host-Key-Pruefung ausserhalb von Wegwerf-Laboren aktiviert
- bevorzugen Sie `linux_ipa_qga_ssh_bootstrap_enabled` gegenueber gemeinsam genutzten temporaeren Passwoertern, wenn Ihre Proxmox-Gaeste bereits einen funktionierenden QEMU Guest Agent haben
- verwenden Sie `guest_qemu_agent_install_enabled` nur dann, wenn das Repository bereits einen gueltigen Management-Pfad in den Gast besitzt
- wenn Sie Linux-SSH-Bootstrap aktivieren, speichern Sie jedes gemeinsame Bootstrap-Passwort in verschluesselten Variablen und rotieren oder entfernen Sie es, sobald Key-basierter Zugriff steht
- verwenden Sie nicht das IPA-Admin-Konto erneut als Proxmox-LDAP-Bind-Konto
- pruefen Sie `proxmox_ldap_filter` und `proxmox_ldap_group_filter` vor dem Produktions-Rollout, damit nicht zu viele Objekte importiert werden

Wenn Sie in einem Wegwerf-Labor SSH-Host-Verifikation bewusst umgehen wollen, deaktivieren Sie sie pro Shell-Session statt die Repository-Defaults zu veraendern:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Idempotenz und Hinweise

Dieses Projekt ist auf Wiederverwendbarkeit und weitgehende Idempotenz ausgelegt, sollte vor dem Produktiveinsatz aber trotzdem im Labor getestet werden.

Bekannte Einschraenkungen:

- Proxmox-CLI-Ausgaben variieren leicht je nach Version
- FreeIPA-Verzeichnislayouts sind flexibel, daher muessen LDAP-Filter eventuell an Ihren Baum angepasst werden
- bereits manuell gepflegte PVE-ACLs und Rollen sollten vor einem Automatisierungs-Rollout mit den Zielwerten verglichen werden
- Proxmox-VM-Auto-Discovery haengt von laufenden Gaesten und QEMU-Guest-Agent-Netzwerkdaten ab
- reine IP-Gastdefinitionen benoetigen weiterhin einen gueltigen finalen Hostnamen im Gast oder einen expliziten `ipa_hostname`
- die Proxmox-Playbooks laufen mit Privileg-Eskalation; ein nicht-root-SSH-Benutzer benoetigt daher funktionierendes `sudo`, und Sie muessen mit `-K` ein Become-Passwort angeben, sofern dieser Benutzer kein passwordless sudo besitzt
- wenn Sie `ansible_become_password` in `vault-proxmox.yml` speichern, koennen Sie `-K` ueberspringen, weil Ansible das sudo-Passwort aus der verschluesselten Variable liest

## Verifikation

Validieren Sie den resultierenden Zustand nach einem erfolgreichen Rollout, anstatt anzunehmen, dass jeder Zugriffspfad korrekt funktioniert.

### In FreeIPA

- bestaetigen Sie, dass die erwarteten Benutzergruppen existieren
- bestaetigen Sie, dass die erwarteten Hostgruppen existieren
- bestaetigen Sie, dass die erwarteten HBAC-Regeln existieren und aktiviert sind
- bestaetigen Sie, dass die erwarteten `sudo`-Regeln existieren und aktiviert sind

### In Proxmox

- bestaetigen Sie, dass die LDAP-Realm existiert
- bestaetigen Sie, dass der initiale Sync die erwarteten Benutzer oder Gruppen importiert hat
- bestaetigen Sie, dass die beabsichtigte synchronisierte Gruppe das erwartete ACL-Binding besitzt

### Auf einem Linux-Gast

- bestaetigen Sie, dass sich ein erlaubter IPA-Benutzer anmelden kann
- bestaetigen Sie, dass ein nicht erlaubter Benutzer durch HBAC blockiert wird
- bestaetigen Sie, dass ein erlaubter IPA-Admin `sudo -l` ausfuehren kann
- bestaetigen Sie, dass ein Home-Verzeichnis beim ersten Login angelegt wird, wenn `linux_ipaclient_mkhomedir` aktiviert ist

## Repository-Struktur

<details>
<summary>Repository-Struktur anzeigen</summary>

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

## Entwicklung

Enthaltene Repository-Helferdateien:

- `.editorconfig` haelt Whitespace-, Encoding- und Zeilenend-Defaults ueber verschiedene Editoren hinweg konsistent
- `.gitattributes` haelt gaengige Textdateien auf `LF`-Zeilenenden
- `.gitignore` verhindert, dass generiertes Inventory, Vault-Daten, lokale Collections und Editor-Dateien in Git landen
- `.ansible-lint` schliesst mitgelieferte Collections aus und unterdrueckt nur die YAML-Zeilenlaengen-Regel
- `.yamllint` sorgt fuer konsistente YAML-Formatpruefungen ueber Playbooks, Inventories und Workflow-Dateien hinweg
- `.github/CODEOWNERS` steuert Review-Zustaendigkeiten fuer die wichtigsten Repository-Bereiche
- `.github/workflows/ci.yml` fuehrt Repository-Lint-Pruefungen und Smoke-Validierung bei Pushes und Pull Requests aus
- `.pre-commit-config.yaml` fuehrt den schnellen Lint-Hook vor Commits aus, wenn `pre-commit` installiert ist
- `CHANGELOG.md` fuehrt bemerkenswerte Repository-Aenderungen an einer zentralen Stelle
- `docs/VARIABLES.md` erklaert das aufgeteilte Inventory-Variablenlayout
- `docs/i18n/` enthaelt uebersetzte README-Dateien, die die vollstaendige englische Abschnittsstruktur spiegeln sollen, waehrend `README.md` die kanonische Quelle bleibt
- `docs/i18n/TRANSLATION_GUIDE.md` erklaert, wie uebersetzte README-Dateien synchron gehalten werden sollen
- `scripts/bootstrap.ps1` und `scripts/bootstrap.sh` installieren die benoetigte Collection in den repository-lokalen Pfad `collections/` und patchen sie fuer ansible-core-2.24+-Kompatibilitaet
- `scripts/patch_freeipa_collection.py` schreibt veraltete Imports in der fest gepinnten FreeIPA-Collection um, damit sie mit kuenftigen ansible-core-Versionen kompatibel bleibt
- `scripts/lint.py` stellt den plattformuebergreifenden Lint-Einstiegspunkt fuer lokale Nutzung, CI und pre-commit bereit
- `scripts/smoke-test.py` validiert das Beispiel-Inventory und fuehrt Syntax-Pruefungen aus, ohne echte Infrastruktur zu beruehren, einschliesslich des separaten Windows-Playbooks
- `scripts/check_translations.py` auditiert uebersetzte README-Dateien auf Metadaten, Abschnittsstruktur-Paritaet und minimale Inhaltsabdeckung gegenueber dem kanonischen englischen README
- `scripts/lint.ps1` und `scripts/lint.sh` fuehren den kombinierten lokalen Lint- und Smoke-Workflow aus
- `scripts/proxmox_event_webhook.py` betreibt den optionalen controllerseitigen Webhook fuer Proxmox-VM-Ereignisse
- `scripts/proxmox-vm-hook.pl` ist das optionale Proxmox-VM-Hookscript, das den Controller-Webhook bei `post-start` und `post-migrate` benachrichtigt
- `scripts/run-playbook.ps1` kapselt gaengige `ansible-playbook`-Aufrufe fuer PowerShell-Benutzer, einschliesslich des separaten Windows-Workflows
- `scripts/vault.ps1` und `scripts/vault.sh` kapseln uebliche Split-Vault-Operationen fuer FreeIPA-, Proxmox- und optionale Windows-Geheimnisse
- `tests/` enthaelt die Verifikationsoberflaeche des Repositorys, beginnend mit der Smoke-Test-Dokumentation
- `CONTRIBUTING.md` dokumentiert den erwarteten Beitrags- und Validierungsablauf
- `SECURITY.md` beschreibt, wie Sicherheitsluecken gemeldet und sicherheitssensible Informationen behandelt werden sollen

```bash
ansible-lint
python scripts/smoke-test.py
python scripts/check_translations.py
python scripts/check_translations.py --strict
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
python .\scripts\check_translations.py
python .\scripts\check_translations.py --strict
.\scripts\lint.ps1
```

Um den schnellen Lint-Hook vor jedem Commit zu aktivieren:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Der PowerShell-Playbook-Wrapper unterstuetzt inzwischen auch haeufige Operator-Optionen direkt:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Mogliche nachste Erweiterungen

Typische spaetere Folgeverbesserungen:

- Packer-Image-Pipeline fuer IPA-faehige Linux-Templates
- AWX-Job-Templates und Zeitplaene
- getrennte Proxmox-Tenant- und Pool-Modelle
- breitere Windows-Local-Policy- oder GPO-Integration

## Lizenz

Freigegeben unter der [MIT License](../../LICENSE).
