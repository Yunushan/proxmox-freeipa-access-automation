# Automatisation d'acces Proxmox + FreeIPA

Cette page fournit une traduction complete et fidele a la structure de [README.md](../../README.md). La version anglaise reste la source canonique, mais cette version francaise doit couvrir le meme perimetre operationnel pour les exploitants francophones.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-15

## Langues

La version anglaise est la source canonique de la documentation complete. Vous trouverez les autres traductions et l'index des traductions dans [docs/i18n/README.md](README.md).

## Pourquoi ce projet existe

Utilisez ce depot lorsque vous disposez deja de :

- un environnement FreeIPA sain
- un cluster Proxmox VE
- des invites Linux qui doivent s'authentifier de facon centralisee
- un compte de service dedie pour le bind LDAP de Proxmox
- un modele clair d'utilisateurs et de groupes pour les administrateurs et les operateurs

L'objectif est de traiter FreeIPA comme source de verite pour l'identite et l'acces. Proxmox consomme cet annuaire via une LDAP realm, les invites Linux rejoignent FreeIPA via le role amont `ipaclient`, et SSH, HBAC et `sudo` restent centralises au lieu d'etre disperses dans des comptes locaux.

## Ce que vous obtenez

- gestion des groupes utilisateurs, hostgroups, regles HBAC et regles `sudo` dans FreeIPA
- valeurs par defaut automatiques de login shell FreeIPA pour les administrateurs Linux
- configuration de la LDAP realm Proxmox vers FreeIPA
- synchronisation recurrente du realm Proxmox depuis un noeud de cluster designe
- liaisons RBAC Proxmox pour les groupes d'annuaire synchronises
- enrollement des invites Linux dans FreeIPA via inventaire statique, cibles IP seules ou decouverte de VM Proxmox
- bootstrap SSH optionnel sans redemarrage via le QEMU Guest Agent de Proxmox
- activation optionnelle de la communication Guest Agent cote Proxmox pour les invites Linux adosses a Proxmox
- installation optionnelle de secours du QEMU Guest Agent via SSH ou WinRM pour les invites deja joignables, qui deviennent joignables apres bootstrap ou qui sont retentes apres l'enrollement Linux
- rapport optionnel de readiness Linux pour la joignabilite SSH et l'etat du QEMU Guest Agent Proxmox
- workflow optionnel separe de membership de domaine Windows pour Windows 10/11 et Windows Server via Active Directory
- workflow optionnel limite et conscient de FreeIPA pour Windows, axe sur la confiance CA IPA, le bootstrap du fichier hosts et les verifications de joignabilite IPA
- bootstrap optionnel de cle publique SSH pour le premier contact avec les invites Linux
- rafraichissement automatique du cache SSSD sur les clients Linux geres apres des changements du modele d'acces FreeIPA
- onboarding Linux optionnel pilote par les evenements via hook et webhook de VM Proxmox

## Perimetre

| Inclus | Non inclus |
| --- | --- |
| Modele d'acces FreeIPA | Deploiement FreeRADIUS |
| Configuration de la LDAP realm Proxmox | Creation du cycle de vie des utilisateurs dans FreeIPA |
| RBAC Proxmox depuis des groupes synchronises | Couverture complete des politiques multi-tenant Proxmox |
| Enrollement des clients Linux dans IPA | Connexion native Windows directement contre FreeIPA |
| Workflow separe de membership AD pour Windows | Automatisation large des objets AD ou des GPO |
| Workflow limite de helpers FreeIPA pour Windows | Faire croire que des helpers Windows FreeIPA-only equivaluent a AD |

## Workflow Windows

La prise en charge de Windows est implemente comme un workflow separe au lieu d'etre melangee dans l'enrollement Linux IPA.

- `windows_qemu_guest_agent_clients` reste dedie aux taches auxiliaires optionnelles autour du QEMU Guest Agent.
- activez le workflow avec `windows_domain_membership_enabled: true` dans `10-features.yml`
- `windows_management_clients` est le groupe separe de gestion Windows utilise par `playbooks/windows-management.yml` et par l'etape Windows optionnelle de `playbooks/site.yml`
- la connexion Windows reelle passe par l'appartenance a un domaine Active Directory ; dans les environnements centres sur FreeIPA, joignez les hotes Windows au cote AD d'une relation de confiance FreeIPA-AD plutot que d'essayer de joindre Windows directement a FreeIPA

Le domain join Windows en mode FreeIPA-only n'est pas pris en charge par ce depot. Sans Active Directory ou sans relation de confiance FreeIPA-AD, le workflow Windows reste limite a des taches auxiliaires comme la gestion d'invites joignables et l'installation optionnelle du QEMU Guest Agent.

Si vous voulez malgre tout une voie limitee et consciente de FreeIPA pour Windows sans domain join, activez `windows_freeipa_helpers_enabled: true` et utilisez `windows_freeipa_helper_clients` avec `playbooks/windows-freeipa-helpers.yml`. Ce workflow auxiliaire peut faire confiance a la CA IPA, recuperer automatiquement la CA IPA pour le bootstrap, fixer en option le thumbprint attendu de la CA IPA, gerer des entrees de bootstrap optionnelles dans le fichier hosts, valider le DNS IPA et des ports TCP critiques, valider la joignabilite HTTPS depuis Windows, valider une source horaire Windows contre un endpoint lie a IPA, gerer des memberships de groupes locaux Windows et installer ou exposer OpenSSH Server en option, mais il ne fournit pas de connexion native Windows contre FreeIPA.

Si vous voulez pour ce meme groupe une verification de readiness sans mutation, lancez `playbooks/windows-freeipa-validate.yml`. Il conserve la route de validation et de resume, mais force la desactivation de l'import CA, des modifications du fichier hosts, des modifications de groupes locaux et de la gestion OpenSSH pour ce run.

Ce workflow vise les invites Windows 10/11 et Windows Server joignables via WinRM ou PSRP.

## Architecture

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

L'explication d'architecture plus longue se trouve dans [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Exigences

### Controleur

- Ansible Core 2.14 ou plus recent
- acces SSH au noeud Proxmox principal, aux serveurs IPA et aux clients Linux
- acces WinRM ou PSRP aux invites Windows quand vous utilisez le workflow Windows
- `sudo` ou `root` la ou c'est necessaire
- si le bootstrap SSH Linux via QGA est active, le Proxmox Guest Agent doit deja etre actif dans l'invite
- si l'installation de secours du Guest Agent pour Windows est activee, les hotes Windows joignables doivent etre places dans `windows_qemu_guest_agent_clients`
- si le membership de domaine Windows est active, les hotes Windows joignables doivent etre places dans `windows_management_clients` et vous devez fournir les identifiants de jonction AD
- si les taches auxiliaires FreeIPA pour Windows sont activees, les hotes Windows joignables doivent etre places dans `windows_freeipa_helper_clients`
- si le bootstrap SSH Linux est active, le controleur doit disposer d'une paire de cles SSH et d'un chemin de connexion initial capable d'utiliser un mot de passe pour le compte invite utilise par Ansible

### Cibles

- Proxmox VE 6.x ou plus recent sur l'hote declare dans `proxmox_primary`
- FreeIPA joignable depuis Proxmox et les clients Linux
- les invites Windows 10/11 et Windows Server peuvent etre geres via le workflow Windows separe lorsqu'ils sont joignables par WinRM ou PSRP
- DNS et synchronisation horaire corrects
- pour `proxmox_primary`, utilisez `root` ou un utilisateur SSH pouvant executer `sudo` pour `pveversion`, `pvesh` et `pveum`
- si vous utilisez le membership de domaine Windows, les invites Windows cibles doivent pouvoir joindre les controleurs de domaine AD correspondants
- si vous utilisez le workflow limite de helpers FreeIPA pour Windows, les invites Windows cibles doivent pouvoir joindre les serveurs IPA correspondants
- si vous utilisez l'auto-decouverte de VM Proxmox, les invites decouverts doivent exposer une IP exploitable via le QEMU Guest Agent

## Ports reseau

Ce tableau liste les ports reseau utilises par le controleur de ce depot, l'automatisation LDAP de Proxmox et le flux d'enrollement Linux IPA.
Il est volontairement limite a ce projet et ne couvre pas la matrice complete de replication serveur-a-serveur FreeIPA.

| Nom | Port | Protocole | Source | Destination | Requis quand | Objectif |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Controleur Ansible | Noeud Proxmox, serveur IPA, invite Linux | Toujours | Connectivite Ansible |
| WinRM | `5985`, `5986` | `TCP` | Controleur Ansible | Invite Windows | Quand la gestion Windows est activee | Connectivite Ansible vers les invites Windows |
| DNS | `53` | `TCP`, `UDP` | Invite Linux | Serveurs DNS IPA | Quand les invites Linux utilisent le DNS IPA | Resoudre les enregistrements IPA et les noms externes via le DNS IPA |
| Kerberos | `88` | `TCP`, `UDP` | Invite Linux | Serveurs IPA | Enrollement Linux IPA et connexion | Authentification Kerberos |
| LDAP | `389` | `TCP` | Invite Linux | Serveurs IPA | Enrollement Linux IPA et connexion | LDAP et decouverte du client FreeIPA |
| HTTPS | `linux_freeipa_enroll_https_port` par defaut `443` | `TCP` | Invite Linux | Serveurs IPA | Enrollement Linux IPA | Verification Web/API IPA pendant l'installation du client |
| Kerberos Password | `464` | `TCP`, `UDP` | Invite Linux | Serveurs IPA | Enrollement Linux IPA et operations de mot de passe | Operations de mot de passe et keytab Kerberos |
| LDAPS | `636` | `TCP` | Noeud primaire Proxmox | Serveurs IPA ou LDAP | Quand la LDAP realm Proxmox utilise le mode `ldaps` par defaut | Connexion de la LDAP realm Proxmox |

Notes :

- `LDAPS 636/TCP` est la valeur par defaut du depot parce que `proxmox_ldap_mode` vaut `ldaps` par defaut. Si vous changez le mode ou le port LDAP, ouvrez a la place le `proxmox_ldap_port` configure.
- `WinRM` utilise couramment `5986/TCP` pour HTTPS ou `5985/TCP` pour HTTP, selon votre configuration de transport Windows.
- `DNS 53/TCP,UDP` n'est necessaire que lorsque les invites Linux utilisent les serveurs IPA comme resolvers.
- `Kerberos 88` et `Kerberos Password 464` necessitent a la fois `TCP` et `UDP`.
- Le domain join Active Directory requiert aussi l'ensemble habituel de ports entre Windows et les controleurs de domaine, mais cette matrice depend de l'environnement et n'est pas listee ici de maniere exhaustive.
- La synchronisation horaire reste necessaire pour que Kerberos fonctionne de maniere fiable, mais la source NTP depend de l'environnement et n'est pas geree par ce depot.

## Compatibilite

L'automatisation Proxmox de ce depot est ecrite autour des interfaces `pveum` et `pvesh` pour realm et RBAC telles qu'elles sont utilisees par Proxmox VE 6.x et les versions suivantes.

- versions majeures prises en charge par defaut : `6`, `7`, `8`, `9`, `10`
- la validation verifie la version Proxmox detectee avec `pveversion`
- la liste des versions prises en charge peut etre ajustee via `proxmox_supported_major_versions` si vous devez la restreindre ou l'etendre dans votre environnement
- `proxmox_allow_future_major_versions` vaut `true` par defaut, de sorte que les versions majeures superieures a la plus haute version testee listee passent aussi la validation par defaut
- les futures versions majeures doivent tout de meme etre traitees comme des candidates de compatibilite tant que l'interface Proxmox publiee n'a pas ete verifiee contre cette automatisation
- les anciennes versions legacy comme `1` a `5` ne sont pas revendiquees comme supportees et testees par ce depot public ; si vous les ajoutez localement, traitez cela comme un override explicite de compatibilite et validez d'abord le workflow complet en laboratoire

Exemple d'override local pour un environnement de laboratoire legacy :

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

## Demarrage rapide

Les exemples ci-dessous utilisent des commandes shell. Les equivalents PowerShell sont inclus lorsque cela est pertinent.

### 1. Copier l'inventaire et les vaults d'exemple

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Optionnel si vous comptez gerer des invites Windows :
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Optionnel si vous comptez gerer des invites Windows :
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Modifier les fichiers specifiques a l'environnement

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` si vous utilisez la gestion Windows
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` si vous utilisez la gestion Windows

Choisissez en plus des reglages IPA et Proxmox un mode de source pour les invites Linux :

- entrees d'inventaire statiques sous `linux_ipa_clients`
- entrees `linux_ipa_client_hosts` dans `group_vars/all/30-linux-clients.yml`
- decouverte de VM Proxmox avec `linux_ipa_proxmox_discovery_enabled: true`

Pour l'enrollement Linux dans IPA, gardez distinctes les valeurs de domaine et de serveurs :

- `ipaclient_domain` est le domaine DNS IPA partage, par exemple `example.com`
- `linux_ipa_servers` contient les hostnames des serveurs IPA, par exemple `ipa01.example.com`

Si vous voulez vous connecter a Proxmox en SSH avec un utilisateur normal disposant de `sudo` plutot qu'avec `root`, configurez-le sous `proxmox_primary` dans `hosts.yml` et gardez le mot de passe sudo dans `vault-proxmox.yml` :

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

Dans cette configuration, `vault_proxmox_become_password` est le mot de passe que vous taperiez normalement pour utiliser `sudo` sur l'hote Proxmox.

### 3. Chiffrer les vaults

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

Ajoutez `inventories/production/group_vars/all/vault-windows.yml` a la meme commande lorsque vous activez le workflow Windows.

Vous pouvez aussi utiliser les wrappers utilitaires, qui emploient par defaut des vault IDs separes et creent les fichiers de travail a partir des templates d'exemple si necessaire :

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Si vous souhaitez des mots de passe distincts par domaine lors de l'execution des playbooks, preferez les vault IDs a `--ask-vault-pass` :

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Si le workflow Windows optionnel utilise lui aussi un mot de passe de vault distinct, ajoutez `windows@prompt` a la meme commande.

N'utilisez `-AskVaultPass` que lorsque tous les fichiers de vault utilises par ce playbook partagent le meme mot de passe.

### 4. Installer la collection requise

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Ou directement :

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

Si vous avez installe `freeipa.ansible_freeipa` avant que ce depot n'ajoute le patch de compatibilite, relancez l'un des helpers bootstrap ou executez `python .\scripts\patch_freeipa_collection.py` une fois pour patcher aussi l'installation existante au niveau utilisateur.

Quand vous utilisez `scripts/run-playbook.ps1`, le helper de patch est execute automatiquement avant `ansible-playbook`.

### 5. Valider d'abord

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Si vous voulez valider uniquement le chemin helper-only FreeIPA pour Windows sans modifier les hotes :

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Si vous voulez un audit read-only de readiness Linux qui indique quels hotes runtime sont joignables en SSH et quels invites decouverts depuis Proxmox repondent via le QEMU Guest Agent :

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

Le rapport de readiness ecrit `.ansible/linux-readiness-report.json` par defaut.
Interpretez les principaux champs de la facon suivante :

- `ssh.ready=true` : le chemin SSH actuellement configure pour Ansible a fonctionne depuis le controleur
- `ssh.promptless=true` : la sonde SSH a reussi sans `ansible_password`, donc le chemin est non interactif pour Ansible
- `ssh.auth_mode=password_configured` : la sonde a utilise `sshpass` parce que l'hote avait `ansible_password`
- `ssh.auth_mode=key_or_agent` : la sonde a reussi en mode batch SSH sans `ansible_password`
- `qga.status=available` : `qm guest ping` a reussi sur le noeud Proxmox proprietaire
- `qga.status=disabled` : la configuration de la VM dans Proxmox n'active pas QEMU Guest Agent
- `qga.status=configured_unresponsive` : le Guest Agent est active dans Proxmox mais n'a pas repondu
- `qga.status=node_unreachable` : le controleur n'a pas pu joindre le noeud Proxmox proprietaire pour la sonde
- `qga.status=not_applicable` : l'hote n'a pas ete cree via la decouverte Proxmox, donc aucune sonde QGA n'a ete tentee

Exemple d'inspection rapide :

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. Previsualiser les changements en option

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Traitez le mode check comme une previsualisation partielle et non comme une simulation complete. Ce depot utilise des commandes CLI directes pour une partie de la configuration Proxmox et le role client FreeIPA amont pour l'enrollement Linux ; `--check` est donc utile mais non absolu.
>
> Pour les regles HBAC FreeIPA, le mode check valide l'etape de definition de la regle mais saute l'action suivante d'activation ou de desactivation. Cela evite les echecs trompeurs ou FreeIPA signale que la regle est absente alors qu'elle n'a tout simplement pas ete creee pendant le dry run.
>
> Le role du timer de synchronisation de realm Proxmox saute lui aussi l'etape finale `systemd` d'activation ou de demarrage en mode check, car les fichiers unit sont diffes mais ne sont pas reellement ecrits pendant le dry run.
>
> L'enrollement Linux IPA est egalement saute en mode check. Le depot continue a faire la decouverte, la resolution de hostname et la validation des entrees, mais le role amont `ipaclient` n'est pas execute pendant le dry run.

### 7. Appliquer la configuration complete

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

Si le workflow Windows optionnel est active et que `vault-windows.yml` utilise un mot de passe distinct, executez le meme playbook avec `--vault-id windows@prompt` ou utilisez le wrapper PowerShell avec `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` au lieu de `--ask-vault-pass`.

## Ordre de deploiement

Pour le premier deploiement, appliquez la pile dans cet ordre :

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Optionnel si vous gerez des invites Windows :
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Optionnel si vous voulez le workflow limite de helpers FreeIPA pour Windows :
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Optionnel si vous voulez uniquement la validation du workflow helper :
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

Cette sequence simplifie beaucoup le diagnostic par rapport a un lancement de toute la pile en une seule fois.

Exemple de rollout limite en PowerShell, par exemple pour un seul invite Linux :

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Les controles de deploiement par defaut sont conservateurs :

- changements FreeIPA avec `serial: 1`
- changements Proxmox avec `serial: 1`
- preparation, resolution et enrollement Linux avec `serial: 10`
- changements de gestion Windows avec `serial: 10`
- `max_fail_percentage: 0` sur tous les parcours

Ajustez ces valeurs dans `inventories/production/group_vars/all/15-rollout.yml`.

## Modele de tags

- Utilisez des tags pour cibler des tranches de deploiement stables au lieu de multiplier les playbooks.
- domaines principaux : `freeipa`, `proxmox`, `linux`, `validate`
- domaine Windows : `windows`, `windows_domain`
- helpers FreeIPA pour Windows : `windows`, `windows_freeipa`
- modele d'acces FreeIPA : `freeipa_access`
- sous-ensembles Proxmox : `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- preparation Linux : `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- enrollement Linux : `linux_enroll`
- chemin evenementiel : `event`, `linux_refresh`

Exemples :

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Onboarding de VM pilote par evenements

Si vous voulez que Proxmox declenche la decouverte Linux et l'enrollement IPA immediatement apres un demarrage ou une migration de VM, utilisez le workflow optionnel hook et webhook documente dans [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

Ce workflow utilise un playbook d'evenement dedie dans `playbooks/proxmox-vm-event.yml`, de sorte que le chemin declenche ne gere que la partie Linux et FreeIPA cote invite. Il ne relance pas l'automatisation de la LDAP realm ni du RBAC Proxmox a chaque evenement de VM.

Le depot peut aussi deployer cette pile optionnelle de hook et webhook depuis `site.yml` ou `proxmox.yml` quand `proxmox_vm_event_onboarding_enabled: true` est defini et que les variables webhook necessaires sont presentes.

Les hooks de VM Proxmox n'exposent pas de phase `create` autonome. En pratique, les nouvelles VMs sont captees lors de leur premier evenement `post-start`, et les hooks de migration peuvent se declencher aussi bien sur le noeud source que sur le noeud cible.

## Modele d'inventaire

Ce depot utilise six groupes d'inventaire declares plus un groupe runtime genere :

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Vous pouvez ajouter vos propres groupes d'inventaire et les referencer depuis les definitions de hostgroups FreeIPA. Si vous voulez utiliser l'ensemble complet des invites Linux prepares dans les hostgroups FreeIPA, referencez `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> FreeIPA a toujours besoin du hostname final de chaque invite. Si vous utilisez des cibles IP seules ou la decouverte Proxmox, definissez `ipa_hostname` explicitement ou assurez-vous que `hostname -f` dans l'invite renvoie bien le FQDN final. Les playbooks resolvent maintenant ce hostname avant de construire la membership aux hostgroups FreeIPA.

> [!TIP]
> N'enrollez pas une golden template reutilisable directement dans FreeIPA. Clonez d'abord la VM, attribuez-lui le hostname final, puis enrollez l'invite resultant.

### Modes de source pour les invites Linux

Vous pouvez alimenter `linux_ipa_clients` de trois facons differentes.

`1.` Hotes statiques dans l'inventaire

Utilisez des entrees d'inventaire Ansible normales si vous connaissez deja les noms des invites :

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

`2.` Definitions manuelles d'hotes dans les variables

Utilisez `linux_ipa_client_hosts` si vous voulez garder les invites hors de `hosts.yml` ou si vous ne connaissez qu'une IP :

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Notes :

- si `name` est un hostname ou un FQDN resolvable, `ansible_host` est optionnel
- si vous ne connaissez que l'IP, utilisez n'importe quel alias stable pour `name`
- quand `ipa_hostname` est omis, le playbook retombe sur `hostname -f` dans l'invite

`3.` Auto-decouverte de VM Proxmox

Utilisez la decouverte si vous voulez que le playbook recupere des invites Linux depuis un ou plusieurs noeuds Proxmox :

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Optionnel : limitez l'automatisation issue de la decouverte aux seuls invites approuves.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Optionnel : excluez toujours les invites d'infrastructure ou sensibles meme
# si la decouverte du noeud est large.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
```

Notes importantes :

- la decouverte ajoute les VMs au meme groupe `linux_ipa_clients_runtime` que celui utilise par le reste des playbooks
- la decouverte d'IP depend du fait que le QEMU Guest Agent rapporte les interfaces reseau
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` ne fait confiance qu'aux noms de VM qui sont deja des FQDN
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` permet de promouvoir des noms courts et surs de VM Proxmox en indices de hostname en les completant avec `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` est optionnel et sert surtout a restreindre la decouverte a certains VMID dans le workflow base sur hooks et webhooks
- l'invite a toujours besoin d'un hostname final, deja configure dans le systeme ou fourni via `ipa_hostname`
- le vrai hostname systeme de l'invite doit etre valide pour l'enrollement ; des valeurs de type `localhost.localdomain` doivent etre corrigees avant l'execution de `linux-clients` ou `site`
- si les invites utilisent des hostnames courts, vous pouvez definir `linux_ipa_identity_hostname_suffix` et eventuellement `linux_freeipa_enroll_manage_hostname: true` pour resoudre et appliquer un FQDN avant l'enrollement
- si le DNS FreeIPA est autoritatif pour vos hostnames d'invites, vous pouvez utiliser `linux_freeipa_enroll_manage_authoritative_dns: true` pour reparer les enregistrements A et PTR et supprimer les enregistrements AAAA link-local avant l'enrollement
- si le DNS n'est pas encore pret, vous pouvez utiliser `linux_ipa_manage_etc_hosts: true` et `linux_ipa_etc_hosts_entries` pour ecrire un bloc de bootstrap gere dans `/etc/hosts`
- `guest_qemu_agent_install_enabled` installe le QEMU Guest Agent sur les invites deja joignables par SSH ou WinRM, retente pour les invites Linux qui deviennent joignables plus tard dans le workflow et retente apres l'enrollement Linux
- activez `linux_ipa_proxmox_discovery_allowlist_enabled: true` lorsque vous voulez garder la decouverte active tout en n'autorisant qu'un sous-ensemble tres approuve d'invites a entrer dans l'inventaire runtime Linux
- utilisez `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips` ou `linux_ipa_proxmox_discovery_blacklist_names` lorsque les noeuds avec decouverte hebergent aussi des VMs d'infrastructure qui ne doivent jamais recevoir l'automatisation Linux IPA ; les correspondances de blacklist gagnent toujours contre la decouverte large ou l'allowlist
- `linux_ipa_qga_ssh_bootstrap_enabled` est le chemin prefere sans redemarrage pour les invites adosses a Proxmox
- `linux_ipa_ssh_bootstrap_enabled` installe en option la cle publique SSH du controleur avant la resolution de hostname et l'enrollement
- l'enrollement Linux IPA retente les joins du client amont qui echouent a cause d'un timeout JSON-RPC FreeIPA
- le workflow combine `site` cree d'abord les hostgroups FreeIPA puis ajoute ensuite les hotes runtime enrols

## Surface de configuration

La plupart des valeurs vivent dans :

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

Pour le detail fichier par fichier, voir [docs/VARIABLES.md](../VARIABLES.md).

Grandes familles de variables :

| Zone | Variables |
| --- | --- |
| Modele d'acces FreeIPA | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Controles de deploiement | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| LDAP realm Proxmox | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| RBAC Proxmox | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Enrollement Linux IPA | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Rapport de readiness Linux | `linux_readiness_report_*` |
| Gestion Windows | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Helpers FreeIPA pour Windows | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Secrets de connexion Ansible | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Exemple de strategie de groupes

Un schema simple qui passe bien a l'echelle :

- groupe FreeIPA `proxmox-admins`
- groupe FreeIPA `linux-ssh-admins`
- hostgroup FreeIPA `linux-all`
- regle HBAC `allow-linux-ssh-admins`
- regle `sudo` `allow-linux-ssh-admins-sudo`
- liaison ACL Proxmox pour le groupe synchronise `proxmox-admins-ipa`

Renseignez `freeipa_linux_admin_users` dans [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) si vous voulez qu'un run combine `site.yml` accorde automatiquement l'acces SSH Linux et `sudo` a des utilisateurs IPA precis via le groupe gere `linux-ssh-admins`.

Rappelez-vous que la synchronisation LDAP de Proxmox cree des groupes synchronises avec le suffixe suivant :

```text
<group-name>-<realm>
```

Si votre groupe FreeIPA s'appelle `proxmox-admins` et que la realm Proxmox est `ipa`, le groupe PVE synchronise devient :

```text
proxmox-admins-ipa
```

## Securite

- stockez tous les secrets dans `vault-freeipa.yml` et `vault-proxmox.yml`, pas dans des fichiers de variables d'inventaire en clair
- preferez un compte LDAP de liaison dedie et en lecture seule pour Proxmox
- privilegiez TLS avec verification de certificat activee
- conservez la verification des cles d'hote SSH en dehors des laboratoires jetables
- preferez `linux_ipa_qga_ssh_bootstrap_enabled` a des mots de passe temporaires partages quand vos invites Proxmox disposent deja d'un QEMU Guest Agent fonctionnel
- utilisez `guest_qemu_agent_install_enabled` uniquement lorsque le depot dispose deja d'un chemin de gestion valide vers l'invite
- si vous activez le bootstrap SSH Linux, stockez tout mot de passe de bootstrap partage dans des variables chiffre es et faites-le tourner ou supprimez-le une fois l'acces par cle etabli
- ne reutilisez pas le compte admin IPA comme compte de bind LDAP Proxmox
- examinez `proxmox_ldap_filter` et `proxmox_ldap_group_filter` avant un deploiement de production pour eviter d'importer trop d'objets

Pour un laboratoire jetable ou vous souhaitez explicitement contourner la verification des hotes SSH, desactivez-la a l'echelle de la session shell plutot que de modifier les valeurs par defaut du depot :

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Idempotence et limites

Ce projet est concu pour etre reutilisable et largement idempotent, mais il doit tout de meme etre valide en laboratoire avant un deploiement en production.

Limites et points d'attention connus :

- la sortie CLI Proxmox peut varier selon les versions
- les filtres LDAP peuvent demander des ajustements selon votre arborescence
- les ACL et roles PVE deja geres manuellement doivent etre compares avant d'appliquer l'automatisation par-dessus
- la decouverte Proxmox depend d'invites en cours d'execution et de donnees QGA
- les definitions seulement IP ont toujours besoin d'un nom d'hote final valide dans l'invite ou d'un `ipa_hostname` explicite
- les playbooks Proxmox utilisent l'elevation de privileges ; un utilisateur SSH non-root a donc besoin d'un `sudo` fonctionnel et vous devrez fournir `-K` sauf s'il dispose deja d'un passwordless sudo
- si vous stockez `ansible_become_password` dans `vault-proxmox.yml`, vous pouvez eviter `-K` parce qu'Ansible lira le mot de passe `sudo` depuis la variable chiffree

## Verification

Validez l'etat obtenu apres un deploiement reussi au lieu de supposer que tous les chemins d'acces sont corrects.

### Dans FreeIPA

- confirmez que les groupes d'utilisateurs attendus existent
- confirmez que les hostgroups attendus existent
- confirmez que les regles HBAC attendues existent et sont actives
- confirmez que les regles `sudo` attendues existent et sont actives

### Dans Proxmox

- confirmez que la LDAP realm existe
- confirmez que la synchronisation initiale a importe les utilisateurs ou groupes attendus
- confirmez que le groupe synchronise vise possede bien la liaison ACL attendue

### Sur un invite Linux

- confirmez qu'un utilisateur IPA autorise peut se connecter
- confirmez qu'un utilisateur non autorise est bloque par HBAC
- confirmez qu'un administrateur IPA autorise peut executer `sudo -l`
- confirmez qu'un repertoire home est cree a la premiere connexion si `linux_ipaclient_mkhomedir` est active

## Organisation du depot

<details>
<summary>Afficher l'organisation du depot</summary>

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

## Developpement

Fichiers et utilitaires importants inclus dans le depot :

- `.editorconfig` maintient des valeurs coherentes pour les espaces, l'encodage et les fins de ligne entre les editeurs
- `.gitattributes` garde les fichiers texte courants en fins de ligne `LF`
- `.gitignore` evite que les inventaires generes, les donnees de vault, les collections locales et les fichiers d'editeur n'entrent dans Git
- `.ansible-lint` exclut les collections vendories et ne supprime que la regle de longueur de ligne YAML
- `.yamllint` maintient des verifications de format YAML coherentes a travers les playbooks, inventaires et workflows
- `.github/CODEOWNERS` distribue la responsabilite des revues sur les zones principales du depot
- `.github/workflows/ci.yml` execute les controles de lint et la validation smoke sur les pushes et pull requests
- `.pre-commit-config.yaml` execute le hook de lint rapide avant chaque commit quand `pre-commit` est installe
- `CHANGELOG.md` suit les changements notables du depot en un point unique
- `docs/VARIABLES.md` explique le decoupage des variables d'inventaire
- `docs/i18n/` contient les README traduits qui doivent refleter la structure complete du README anglais tandis que `README.md` reste la source canonique
- `docs/i18n/TRANSLATION_GUIDE.md` explique comment garder les README traduits synchronises
- `scripts/bootstrap.ps1` et `scripts/bootstrap.sh` installent la collection requise dans le chemin local `collections/` du depot et la patchent pour la compatibilite avec ansible-core 2.24+
- `scripts/patch_freeipa_collection.py` reecrit les imports obsoletes dans la collection FreeIPA epinglee pour la garder compatible avec les futures versions d'ansible-core
- `scripts/lint.py` fournit le point d'entree lint multiplateforme pour l'usage local, la CI et pre-commit
- `scripts/smoke-test.py` valide l'inventaire d'exemple et execute des controles de syntaxe sans toucher a une infrastructure reelle, y compris le playbook Windows separe
- `scripts/check_translations.py` audite les README traduits sur les metadonnees, la parite structurelle des sections et la couverture minimale de contenu par rapport au README anglais canonique
- `scripts/lint.ps1` et `scripts/lint.sh` executent le workflow combine de lint local et smoke
- `scripts/proxmox_event_webhook.py` execute le webhook optionnel cote controleur pour les evenements de VM Proxmox
- `scripts/proxmox-vm-hook.pl` est le hookscript Proxmox optionnel qui notifie le webhook du controleur sur les evenements `post-start` et `post-migrate`
- `scripts/run-playbook.ps1` encapsule les usages courants de `ansible-playbook` pour les utilisateurs PowerShell, y compris le workflow Windows separe
- `scripts/vault.ps1` et `scripts/vault.sh` encapsulent les operations split-vault courantes pour les secrets FreeIPA, Proxmox et Windows optionnels
- `tests/` contient la surface de verification du depot, en commencant par la documentation smoke-test
- `CONTRIBUTING.md` documente le workflow attendu de contribution et de validation
- `SECURITY.md` documente la maniere de signaler les vulnerabilites et de traiter les informations sensibles de securite

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

Pour activer le hook de lint rapide avant chaque commit :

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Le wrapper PowerShell des playbooks prend aussi en charge des options operateur courantes :

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Extensions suivantes

- evolutions frequentes a envisager plus tard :
- pipeline Packer pour des templates Linux prets pour IPA
- job templates et planifications AWX
- modeles separes de tenants et de pools Proxmox
- integration plus large avec les politiques locales Windows ou les GPO

## Licence

Publie sous la [MIT License](../../LICENSE).
