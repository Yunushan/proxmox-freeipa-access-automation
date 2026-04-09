# Automatisation d'acces Proxmox + FreeIPA

Cette page fournit une traduction complete de la structure de [README.md](../../README.md). La version anglaise reste la source canonique, mais cette traduction couvre les memes sections principales pour les exploitants francophones.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Pourquoi ce projet existe

Utilisez ce depot lorsque vous disposez deja de :

- un environnement FreeIPA sain
- un cluster Proxmox VE
- des invites Linux qui doivent s'authentifier de facon centralisee
- un compte de service dedie pour le bind LDAP de Proxmox
- un modele clair de groupes pour les administrateurs et les operateurs

L'objectif est de traiter FreeIPA comme source de verite pour l'identite et l'acces. Proxmox consomme cet annuaire via une LDAP realm, les invites Linux rejoignent FreeIPA via le role amont `ipaclient`, et SSH, HBAC et `sudo` restent centralises.

## Ce que vous obtenez

- gestion des groupes utilisateurs, hostgroups, regles HBAC et regles `sudo` dans FreeIPA
- configuration de la LDAP realm Proxmox vers FreeIPA
- synchronisation periodique du realm depuis un noeud de cluster designe
- liaisons RBAC Proxmox pour les groupes d'annuaire synchronises
- enrollement Linux depuis un inventaire statique, des definitions manuelles ou la decouverte Proxmox
- bootstrap SSH optionnel sans redemarrage via le QEMU Guest Agent
- installation optionnelle du QEMU Guest Agent via SSH ou WinRM sur les invites joignables
- bootstrap optionnel d'une cle publique SSH pour le premier acces
- rafraichissement automatique du cache SSSD apres les changements de modele d'acces
- onboarding optionnel pilote par les evenements `post-start` et `post-migrate`

## Perimetre

| Inclus | Non inclus |
| --- | --- |
| Modele d'acces FreeIPA | Jonction Windows au domaine |
| Configuration de la LDAP realm Proxmox | Deploiement FreeRADIUS |
| RBAC Proxmox depuis des groupes synchronises | Creation complete du cycle de vie des utilisateurs dans FreeIPA |
| Enrollement des clients Linux dans IPA | Couverture complete de tous les cas limites multi-tenant de Proxmox |

## Architecture

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

L'explication d'architecture plus longue se trouve dans [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Exigences

### Controleur

- Ansible Core 2.14 ou plus recent
- acces SSH au noeud Proxmox principal, aux serveurs IPA et aux clients Linux
- `sudo` ou `root` la ou c'est necessaire
- si le bootstrap SSH via QGA est active, QEMU Guest Agent doit deja etre actif dans l'invite
- si l'installation de secours pour Windows est activee, les hotes joignables doivent etre dans `windows_qemu_guest_agent_clients`
- si le bootstrap SSH Linux est active, le controleur doit disposer d'une paire de cles SSH et d'un chemin initial avec mot de passe

### Cibles

- Proxmox VE 6.x ou plus recent sur l'hote declare dans `proxmox_primary`
- FreeIPA joignable depuis Proxmox et les clients Linux
- DNS et synchronisation horaire corrects
- pour `proxmox_primary`, utilisez `root` ou un utilisateur SSH pouvant executer `sudo` pour `pveversion`, `pvesh` et `pveum`
- si vous utilisez la decouverte Proxmox, les invites doivent exposer une IP exploitable via QEMU Guest Agent

## Ports reseau

La matrice complete des ports reste dans le README anglais. Les ports principaux utilises ici sont :

- `22/TCP` pour SSH depuis le controleur vers Proxmox, IPA et Linux
- `53/TCP,UDP` des invites Linux vers les serveurs DNS IPA si le DNS IPA est utilise
- `88/TCP,UDP` et `464/TCP,UDP` pour Kerberos
- `389/TCP` pour LDAP lors de l'enrollement Linux
- `linux_freeipa_enroll_https_port`, par defaut `443/TCP`, pour les verifications Web/API d'IPA
- `636/TCP` pour la LDAP realm Proxmox quand le mode est `ldaps`

## Compatibilite

- cible Proxmox VE 6.x et versions suivantes
- versions majeures supportees par defaut : `6`, `7`, `8`, `9`, `10`
- extensible via `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions` vaut `true` par defaut

## Demarrage rapide

### 1. Copier l'inventaire et les vaults d'exemple

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

### 2. Modifier les fichiers specifiques a l'environnement

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

Choisissez aussi une source pour les invites Linux : inventaire statique, `linux_ipa_client_hosts` ou decouverte Proxmox.

### 3. Chiffrer les vaults

```bash
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
```

### 4. Installer la collection requise

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

### 5. Valider d'abord

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

### 6. Previsualiser les changements en option

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

### 7. Appliquer la configuration complete

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## Ordre de deploiement

Pour le premier deploiement :

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Par defaut :

- changements FreeIPA avec `serial: 1`
- changements Proxmox avec `serial: 1`
- preparation, resolution et enrollement Linux avec `serial: 10`
- `max_fail_percentage: 0` sur tous les parcours

## Modele de tags

- domaines principaux : `freeipa`, `proxmox`, `linux`, `validate`
- modele d'acces FreeIPA : `freeipa_access`
- sous-ensembles Proxmox : `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- preparation Linux : `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- enrollement Linux : `linux_enroll`
- chemin evenementiel : `event`, `linux_refresh`

## Onboarding de VM pilote par evenements

Si vous voulez que Proxmox declenche la decouverte Linux et l'enrollement IPA immediatement apres un demarrage ou une migration, utilisez le workflow hook/webhook optionnel de [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

- le chemin evenementiel utilise `playbooks/proxmox-vm-event.yml`
- il ne relance pas LDAP realm ni RBAC Proxmox a chaque evenement
- Proxmox n'expose pas de phase `create` separee ; en pratique les nouvelles VMs sont prises en compte au premier `post-start`
- le depot peut aussi deployer cette pile optionnelle depuis `site.yml` ou `proxmox.yml`

## Modele d'inventaire

Les groupes principaux sont :

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

Si vous utilisez uniquement des IP ou la decouverte Proxmox, l'invite doit tout de meme disposer d'un FQDN final valable via `ipa_hostname` ou `hostname -f`.

### Modes de source pour les invites Linux

1. hotes statiques dans l'inventaire
2. definitions manuelles dans `linux_ipa_client_hosts`
3. auto-decouverte Proxmox via `linux_ipa_proxmox_discovery_*`

Notes importantes :

- la decouverte depend des donnees reseau du QEMU Guest Agent
- `linux_ipa_proxmox_discovery_vmids` est surtout utile pour le workflow evenementiel
- `linux_ipa_identity_hostname_suffix` peut etre combine avec `linux_freeipa_enroll_manage_hostname: true`
- si le DNS FreeIPA est autoritatif, utilisez `linux_freeipa_enroll_manage_authoritative_dns: true`
- si le DNS n'est pas encore pret, utilisez `linux_ipa_manage_etc_hosts: true` avec `linux_ipa_etc_hosts_entries`
- `linux_ipa_qga_ssh_bootstrap_enabled` est le chemin prefere sans redemarrage

## Surface de configuration

La plupart des valeurs vivent dans :

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

Pour le detail fichier par fichier, voir [docs/VARIABLES.md](../VARIABLES.md).

## Exemple de strategie de groupes

- groupe FreeIPA `proxmox-admins`
- groupe FreeIPA `linux-ssh-admins`
- hostgroup FreeIPA `linux-all`
- regle HBAC `allow-linux-ssh-admins`
- regle `sudo` `allow-linux-ssh-admins-sudo`
- liaison ACL Proxmox pour le groupe synchronise `proxmox-admins-ipa`

## Securite

- stockez les secrets uniquement dans les vaults
- preferez un compte LDAP de liaison dedie et en lecture seule pour Proxmox
- privilegiez TLS avec verification de certificat
- conservez la verification des cles d'hote SSH hors laboratoires jetables
- privilegiez `linux_ipa_qga_ssh_bootstrap_enabled` plutot que des mots de passe temporaires partages

## Idempotence et limites

Le projet vise une forte reutilisabilite et une bonne idempotence, mais doit etre valide en laboratoire avant la production. Limites connues :

- la sortie CLI Proxmox peut varier selon les versions
- les filtres LDAP peuvent demander des ajustements
- la decouverte Proxmox depend d'invites en cours d'execution et de donnees QGA
- les definitions seulement IP ont toujours besoin d'un nom d'hote final valide

## Verification

Apres un deploiement reussi, verifiez :

- dans FreeIPA : groupes, hostgroups, regles HBAC et regles `sudo`
- dans Proxmox : LDAP realm, synchronisation initiale et liaisons ACL
- sur un invite Linux : connexion autorisee, blocage HBAC, `sudo -l`, creation du home si `mkhomedir` est active

## Organisation du depot

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

L'arborescence complete reste detaillee dans le README anglais.

## Developpement

Fichiers d'aide inclus :

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

Commandes utiles :

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
.\scripts\lint.ps1
```

## Extensions suivantes

- pipeline Packer pour des templates Linux prets pour IPA
- job templates et planifications AWX
- modeles separes de tenants et de pools Proxmox
- parcours Windows ou AD trust pour des environnements orientés RDP

## Licence

Publie sous la [MIT License](../../LICENSE).
