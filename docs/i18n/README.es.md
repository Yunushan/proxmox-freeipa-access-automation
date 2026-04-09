# Automatizacion de Acceso Proxmox + FreeIPA

Esta pagina ofrece una traduccion completa de la estructura de [README.md](../../README.md). La version en ingles sigue siendo la referencia canonica, pero esta traduccion cubre las mismas secciones principales para operadores hispanohablantes.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Por que existe este proyecto

Use este repositorio cuando ya tenga:

- una implementacion sana de FreeIPA
- un cluster de Proxmox VE
- invitados Linux que deben autenticarse de forma centralizada
- una cuenta de servicio dedicada para el bind LDAP de Proxmox
- un modelo claro de grupos para administradores y operadores

La idea es tratar a FreeIPA como fuente de verdad para identidad y acceso. Proxmox consume ese directorio mediante un LDAP realm, los invitados Linux se unen a FreeIPA con la funcion upstream `ipaclient`, y las reglas de SSH, HBAC y `sudo` permanecen centralizadas.

## Lo que obtiene

- gestion de grupos de usuarios, hostgroups, reglas HBAC y reglas `sudo` en FreeIPA
- configuracion del LDAP realm de Proxmox contra FreeIPA
- sincronizacion periodica del realm desde un nodo de cluster designado
- enlaces RBAC de Proxmox para grupos sincronizados
- inscripcion de Linux desde inventario estatico, definiciones manuales o descubrimiento de Proxmox
- bootstrap opcional de SSH sin reinicio mediante QEMU Guest Agent
- instalacion opcional de QEMU Guest Agent via SSH o WinRM en invitados alcanzables
- bootstrap opcional de clave publica SSH para el primer acceso
- refresco automatico de cache SSSD despues de cambios en el modelo de acceso
- onboarding opcional basado en eventos `post-start` y `post-migrate`

## Alcance

| Incluido | No incluido |
| --- | --- |
| Modelo de acceso FreeIPA | Union de Windows al dominio |
| Configuracion del LDAP realm de Proxmox | Despliegue de FreeRADIUS |
| RBAC de Proxmox desde grupos sincronizados | Creacion completa del ciclo de vida de usuarios en FreeIPA |
| Inscripcion de clientes Linux en IPA | Cobertura completa de todos los casos de multi-tenant de Proxmox |

## Arquitectura

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

La explicacion de diseno mas larga esta en [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Requisitos

### Controlador

- Ansible Core 2.14 o superior
- alcance SSH al nodo primario de Proxmox, al servidor IPA y a los clientes Linux
- `sudo` o `root` donde corresponda
- si habilita QGA SSH bootstrap, QEMU Guest Agent ya debe estar activo en el invitado
- si habilita el fallback de instalacion para Windows, los hosts alcanzables deben estar en `windows_qemu_guest_agent_clients`
- si habilita el bootstrap SSH de Linux, el controlador necesita un par de claves SSH y una ruta inicial con contrasena

### Destinos

- Proxmox VE 6.x o posterior en el host de `proxmox_primary`
- FreeIPA accesible desde Proxmox y desde los clientes Linux
- DNS y sincronizacion horaria correctos
- para `proxmox_primary`, use `root` o un usuario SSH con `sudo` para `pveversion`, `pvesh` y `pveum`
- si usa auto-descubrimiento de Proxmox, los invitados deben exponer una IP util via QEMU Guest Agent

## Puertos de red

La matriz completa sigue estando en el README canonico. Los puertos mas importantes para este repositorio son:

- `22/TCP` para SSH del controlador hacia Proxmox, IPA y Linux
- `53/TCP,UDP` desde clientes Linux hacia DNS de IPA cuando se usa DNS de IPA
- `88/TCP,UDP` y `464/TCP,UDP` para Kerberos
- `389/TCP` para LDAP durante la inscripcion Linux
- `linux_freeipa_enroll_https_port`, por defecto `443/TCP`, para verificaciones web/API de IPA
- `636/TCP` para el LDAP realm de Proxmox cuando el modo es `ldaps`

## Compatibilidad

- orientado a Proxmox VE 6.x y superiores
- versiones mayores admitidas por defecto: `6`, `7`, `8`, `9`, `10`
- se puede ajustar con `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions` es `true` por defecto

## Inicio rapido

### 1. Copie el inventario y los vaults de ejemplo

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

### 2. Edite los archivos especificos del entorno

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

Ademas elija una fuente para los invitados Linux: hosts estaticos, `linux_ipa_client_hosts` o descubrimiento de Proxmox.

### 3. Cifre los vaults

```bash
ansible-vault encrypt \
  inventories/production/group_vars/all/vault-freeipa.yml \
  inventories/production/group_vars/all/vault-proxmox.yml
```

### 4. Instale la collection requerida

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

### 5. Valide primero

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

### 6. Vista previa opcional

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

### 7. Aplique la configuracion completa

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## Orden de despliegue

Para el primer despliegue:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

Valores conservadores por defecto:

- cambios de FreeIPA con `serial: 1`
- cambios de Proxmox con `serial: 1`
- preparacion, resolucion y enrolamiento Linux con `serial: 10`
- `max_fail_percentage: 0` en todos los recorridos

## Modelo de tags

- dominios base: `freeipa`, `proxmox`, `linux`, `validate`
- modelo de acceso FreeIPA: `freeipa_access`
- subconjuntos de Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- preparacion Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- enrolamiento Linux: `linux_enroll`
- eventos: `event`, `linux_refresh`

## Onboarding de VM basado en eventos

Si quiere que Proxmox dispare el descubrimiento Linux y el enrolamiento IPA justo despues de un arranque o una migracion, use el flujo opcional hook/webhook descrito en [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

- el camino de eventos usa `playbooks/proxmox-vm-event.yml`
- no vuelve a ejecutar LDAP realm ni RBAC de Proxmox en cada evento
- Proxmox no expone una fase `create` separada; en la practica las VMs nuevas se toman en su primer `post-start`
- el repositorio tambien puede desplegar este stack opcional desde `site.yml` o `proxmox.yml`

## Modelo de inventario

Los grupos principales son:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

Si usa destinos solo por IP o descubrimiento de Proxmox, el invitado aun necesita un hostname final valido mediante `ipa_hostname` o `hostname -f`.

### Modos de origen para invitados Linux

1. hosts estaticos en el inventario
2. definiciones manuales en `linux_ipa_client_hosts`
3. auto-descubrimiento en Proxmox con `linux_ipa_proxmox_discovery_*`

Notas clave:

- el descubrimiento depende de los datos de red del QEMU Guest Agent
- `linux_ipa_proxmox_discovery_vmids` es especialmente util para el flujo basado en eventos
- puede combinar `linux_ipa_identity_hostname_suffix` con `linux_freeipa_enroll_manage_hostname: true`
- si FreeIPA DNS es autoritativo, puede usar `linux_freeipa_enroll_manage_authoritative_dns: true`
- si DNS aun no esta listo, use `linux_ipa_manage_etc_hosts: true` con `linux_ipa_etc_hosts_entries`
- `linux_ipa_qga_ssh_bootstrap_enabled` es la ruta preferida sin reinicio

## Superficie de configuracion

La mayoria de variables vive en:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

Para el desglose archivo por archivo vea [docs/VARIABLES.md](../VARIABLES.md).

## Ejemplo de estrategia de grupos

- grupo FreeIPA `proxmox-admins`
- grupo FreeIPA `linux-ssh-admins`
- hostgroup FreeIPA `linux-all`
- regla HBAC `allow-linux-ssh-admins`
- regla `sudo` `allow-linux-ssh-admins-sudo`
- binding ACL de Proxmox para el grupo sincronizado `proxmox-admins-ipa`

## Seguridad

- guarde secretos solo en los vaults
- prefiera una cuenta de bind LDAP dedicada y de solo lectura para Proxmox
- prefiera TLS con verificacion de certificados
- mantenga activada la verificacion de host keys SSH fuera de laboratorios desechables
- prefiera `linux_ipa_qga_ssh_bootstrap_enabled` antes que contrasenas compartidas temporales

## Idempotencia y advertencias

El proyecto busca ser reutilizable e idempotente, pero debe probarse en laboratorio antes de produccion. Limitaciones conocidas:

- la salida CLI de Proxmox puede variar entre versiones
- los filtros LDAP pueden necesitar ajuste segun su arbol
- el auto-descubrimiento depende de invitados en ejecucion y de datos del QEMU Guest Agent
- las definiciones solo por IP siguen requiriendo un hostname final valido

## Verificacion

Despues de un despliegue exitoso compruebe:

- en FreeIPA: grupos, hostgroups, reglas HBAC y reglas `sudo`
- en Proxmox: LDAP realm, sincronizacion inicial y enlaces ACL
- en un invitado Linux: login permitido, bloqueo HBAC, `sudo -l` y creacion del home si `mkhomedir` esta habilitado

## Estructura del repositorio

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

El arbol completo permanece documentado en el README en ingles.

## Desarrollo

El repositorio incluye archivos auxiliares como:

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

Comandos utiles:

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
.\scripts\lint.ps1
```

## Siguientes extensiones

- pipeline Packer para plantillas Linux listas para IPA
- job templates y schedules de AWX
- modelos separados de tenants y pools de Proxmox
- flujo Windows o AD trust para entornos orientados a RDP

## Licencia

Publicado bajo la [MIT License](../../LICENSE).
