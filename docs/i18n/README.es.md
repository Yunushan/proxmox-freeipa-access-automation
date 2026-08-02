# Automatizacion de Acceso Proxmox + FreeIPA

Esta pagina ofrece una traduccion completa y estructuralmente fiel de [README.md](../../README.md). La version en ingles sigue siendo la fuente canonica, pero esta version en espanol debe cubrir el mismo alcance operativo para operadores hispanohablantes.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-15

## Idiomas

La version en ingles es la fuente canonica de la documentacion completa. Puede encontrar otras traducciones y el indice de traducciones en [docs/i18n/README.md](README.md).

## Por que existe este proyecto

Use este repositorio cuando ya tenga:

- una implementacion sana de FreeIPA
- un cluster de Proxmox VE
- invitados Linux que deben autenticarse de forma centralizada
- una cuenta de servicio dedicada para el bind LDAP de Proxmox
- un modelo claro de usuarios y grupos para administradores y operadores

La idea es tratar a FreeIPA como fuente de verdad para identidad y acceso. Proxmox consume ese directorio mediante un LDAP realm, los invitados Linux se unen a FreeIPA con la funcion upstream `ipaclient`, y las reglas de SSH, HBAC y `sudo` permanecen centralizadas en lugar de dispersarse en cuentas locales dentro de cada VM.

## Lo que obtiene

- gestion de grupos de usuarios, hostgroups, reglas HBAC y reglas `sudo` en FreeIPA
- valores predeterminados automaticos de login shell de FreeIPA para administradores Linux
- configuracion del LDAP realm de Proxmox contra FreeIPA
- sincronizacion recurrente del realm de Proxmox desde un nodo de cluster designado
- enlaces RBAC de Proxmox para grupos de directorio sincronizados
- inscripcion de invitados Linux en FreeIPA mediante inventario estatico, destinos solo por IP o descubrimiento de VMs en Proxmox
- bootstrap opcional de SSH sin reinicio mediante el QEMU Guest Agent de Proxmox
- habilitacion opcional de la comunicacion del guest agent del lado de Proxmox para invitados Linux respaldados por Proxmox
- instalacion opcional por SSH o WinRM del QEMU Guest Agent como fallback para invitados que ya son alcanzables, que se vuelven alcanzables despues del bootstrap o que se reintentan despues del enrolamiento Linux
- reporte opcional de readiness Linux para alcance SSH y estado del QEMU Guest Agent de Proxmox
- workflow opcional separado de membresia a dominio para Windows 10/11 y Windows Server a traves de Active Directory
- workflow opcional limitado y consciente de FreeIPA para Windows, orientado a confianza en la CA de IPA, bootstrap de hosts y comprobaciones de alcance de IPA
- bootstrap opcional de clave publica SSH para el primer acceso a invitados Linux
- refresco automatico de cache SSSD en clientes Linux gestionados despues de cambios en el modelo de acceso de FreeIPA
- onboarding opcional de Linux basado en eventos a partir de hooks de VM de Proxmox y disparadores webhook

## Alcance

| Incluido | No incluido |
| --- | --- |
| Modelo de acceso FreeIPA | Despliegue de FreeRADIUS |
| Configuracion del LDAP realm de Proxmox | Creacion del ciclo de vida de usuarios en FreeIPA |
| RBAC de Proxmox desde grupos sincronizados | Cobertura completa de politicas multi-tenant de Proxmox |
| Inscripcion de clientes Linux en IPA | Inicio de sesion nativo de Windows directamente contra FreeIPA |
| Workflow separado de membresia AD para Windows | Automatizacion amplia de objetos AD o GPO |
| Workflow limitado de helpers FreeIPA para Windows | Pretender que los helpers Windows basados solo en FreeIPA equivalen a AD |

## Flujo de trabajo para Windows

La compatibilidad con Windows se implementa como un workflow separado en lugar de mezclarlo dentro del enrolamiento Linux en IPA.

- `windows_qemu_guest_agent_clients` se mantiene dedicado a tareas auxiliares opcionales del QEMU Guest Agent.
- active el workflow con `windows_domain_membership_enabled: true` en `10-features.yml`
- `windows_management_clients` es el grupo separado de gestion Windows usado por `playbooks/windows-management.yml` y por la etapa opcional de Windows dentro de `playbooks/site.yml`
- el inicio de sesion real de Windows se gestiona mediante membresia a dominio de Active Directory; en entornos centrados en FreeIPA, una los hosts Windows al lado AD de una relacion de confianza FreeIPA-AD en lugar de intentar unir Windows directamente a FreeIPA

La union de Windows solo con FreeIPA no esta soportada por este repositorio. Sin Active Directory o sin una relacion de confianza FreeIPA-AD, el workflow de Windows queda limitado a tareas auxiliares como gestion de invitados alcanzables e instalacion opcional de QEMU Guest Agent.

Si aun desea una via limitada y consciente de FreeIPA para Windows sin domain join, active `windows_freeipa_helpers_enabled: true` y utilice `windows_freeipa_helper_clients` con `playbooks/windows-freeipa-helpers.yml`. Ese workflow auxiliar puede confiar en la CA de IPA, obtener automaticamente la CA de IPA para bootstrap, fijar opcionalmente el thumbprint esperado de la CA, gestionar entradas opcionales en el archivo hosts, validar DNS de IPA y puertos TCP clave, validar alcance HTTPS desde Windows, validar una fuente horaria de Windows contra un endpoint relacionado con IPA, gestionar membresias de grupos locales de Windows e instalar o exponer opcionalmente OpenSSH Server, pero no proporciona inicio de sesion nativo de Windows contra FreeIPA.

Si quiere una comprobacion de readiness que no haga cambios para ese mismo grupo auxiliar, ejecute `playbooks/windows-freeipa-validate.yml`. Mantiene la ruta de validacion y resumen, pero fuerza a que para ese run se desactiven la importacion de CA, los cambios del archivo hosts, los cambios de grupos locales y la gestion de OpenSSH.

Este workflow apunta a invitados Windows 10/11 y Windows Server alcanzables mediante WinRM o PSRP.

## Arquitectura

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

La explicacion de diseno mas larga esta en [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Requisitos

### Controlador

- Ansible Core 2.14 o superior
- alcance SSH al nodo primario de Proxmox, al servidor IPA y a los clientes Linux
- alcance WinRM o PSRP a invitados Windows cuando use el workflow de Windows
- `sudo` o `root` donde corresponda
- si habilita QGA SSH bootstrap, el Proxmox guest agent ya debe estar activo dentro del invitado
- si habilita la instalacion de fallback del guest agent para Windows, los hosts Windows alcanzables deben estar en `windows_qemu_guest_agent_clients`
- si habilita membresia de dominio para Windows, los hosts Windows alcanzables deben estar en `windows_management_clients` y debe proporcionar credenciales de union a AD
- si habilita tareas auxiliares de FreeIPA para Windows, los hosts Windows alcanzables deben estar en `windows_freeipa_helper_clients`
- si habilita el bootstrap SSH de Linux, el controlador necesita un par de claves SSH y una ruta inicial de login con capacidad de usar contrasena para la cuenta del invitado que usa Ansible

### Destinos

- Proxmox VE 6.x o posterior en el host de `proxmox_primary`
- FreeIPA accesible desde Proxmox y desde los clientes Linux
- los invitados Windows 10/11 y Windows Server pueden gestionarse mediante el workflow separado de Windows cuando son alcanzables por WinRM o PSRP
- DNS y sincronizacion horaria correctos
- para `proxmox_primary`, use `root` o un usuario SSH con `sudo` para `pveversion`, `pvesh` y `pveum`
- si usa membresia de dominio para Windows, los invitados Windows objetivo deben poder llegar a los controladores de dominio AD correspondientes
- si usa el workflow limitado de helpers FreeIPA para Windows, los invitados Windows objetivo deben poder llegar a los servidores IPA correspondientes
- si usa auto-descubrimiento de VMs en Proxmox, los invitados descubiertos deben exponer una IP util mediante QEMU Guest Agent

## Puertos de red

Esta tabla enumera los puertos de red usados por el controlador de este repositorio, la automatizacion LDAP de Proxmox y el flujo de inscripcion Linux en IPA.
Esta intencionalmente acotada a este proyecto, no a la matriz completa de replicacion servidor-servidor de FreeIPA.

| Nombre | Puerto | Protocolo | Origen | Destino | Requerido cuando | Proposito |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Controlador Ansible | Nodo Proxmox, servidor IPA, invitado Linux | Siempre | Conectividad Ansible |
| WinRM | `5985`, `5986` | `TCP` | Controlador Ansible | Invitado Windows | Cuando la gestion Windows esta habilitada | Conectividad Ansible hacia invitados Windows |
| DNS | `53` | `TCP`, `UDP` | Invitado Linux | Servidores DNS de IPA | Cuando los invitados Linux usan DNS de IPA | Resolver registros de IPA y nombres externos a traves de IPA DNS |
| Kerberos | `88` | `TCP`, `UDP` | Invitado Linux | Servidores IPA | Inscripcion y login Linux en IPA | Autenticacion Kerberos |
| LDAP | `389` | `TCP` | Invitado Linux | Servidores IPA | Inscripcion y login Linux en IPA | LDAP y descubrimiento del cliente FreeIPA |
| HTTPS | `linux_freeipa_enroll_https_port` por defecto `443` | `TCP` | Invitado Linux | Servidores IPA | Inscripcion Linux en IPA | Verificacion web/API de IPA durante la instalacion del cliente |
| Kerberos Password | `464` | `TCP`, `UDP` | Invitado Linux | Servidores IPA | Inscripcion Linux en IPA y operaciones de password | Operaciones de password y keytab de Kerberos |
| LDAPS | `636` | `TCP` | Nodo primario de Proxmox | Servidores IPA o LDAP | Cuando el LDAP realm de Proxmox usa el modo por defecto `ldaps` | Conexion del LDAP realm de Proxmox |

Notas:

- `LDAPS 636/TCP` es el valor por defecto del repositorio porque `proxmox_ldap_mode` usa `ldaps` por defecto. Si cambia el modo o el puerto LDAP, permita en su lugar el `proxmox_ldap_port` configurado.
- `WinRM` usa habitualmente `5986/TCP` para HTTPS o `5985/TCP` para HTTP, segun su configuracion de transporte Windows.
- `DNS 53/TCP,UDP` solo se necesita cuando los invitados Linux usan los servidores IPA como resolvers.
- `Kerberos 88` y `Kerberos Password 464` requieren tanto `TCP` como `UDP`.
- La union a dominio de Active Directory tambien requiere el conjunto normal de puertos entre Windows y controladores de dominio, pero esa matriz depende del entorno y no se enumera aqui de forma exhaustiva.
- La sincronizacion horaria sigue siendo necesaria para que Kerberos funcione con fiabilidad, pero la fuente NTP depende del entorno y no esta gestionada por este repositorio.

## Compatibilidad

La automatizacion de Proxmox en este repositorio esta escrita alrededor de las interfaces `pveum` y `pvesh` para realm y RBAC usadas por Proxmox VE 6.x y versiones posteriores.

- versiones mayores soportadas por defecto: `6`, `7`, `8`, `9`, `10`
- la validacion comprueba la version detectada de Proxmox mediante `pveversion`
- la lista de versiones soportadas puede ajustarse mediante `proxmox_supported_major_versions` si necesita estrecharla o ampliarla en su entorno
- `proxmox_allow_future_major_versions` es `true` por defecto, de modo que las versiones mayores superiores a la ultima version probada listada tambien pasan la validacion por defecto
- las futuras versiones mayores deben seguir tratandose como candidatas de compatibilidad hasta verificar la interfaz publicada de Proxmox frente a esta automatizacion
- las versiones legacy anteriores, como `1` a `5`, no se presentan como soporte probado por este repositorio publico; si las agrega localmente, tratelo como un override explicito de compatibilidad y valide el workflow completo primero en laboratorio

Ejemplo de override local para un laboratorio legacy:

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

## Inicio rapido

Los ejemplos siguientes usan comandos de shell. Se incluyen equivalentes en PowerShell donde tiene sentido.

### 1. Copie el inventario y los vaults de ejemplo

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Opcional, si planea gestionar invitados Windows:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Opcional, si planea gestionar invitados Windows:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Edite los archivos especificos del entorno

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` si usa gestion Windows
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` si usa gestion Windows

Ademas de los ajustes de IPA y Proxmox, elija un modo de origen para los invitados Linux:

- entradas estaticas de inventario bajo `linux_ipa_clients`
- entradas `linux_ipa_client_hosts` en `group_vars/all/30-linux-clients.yml`
- descubrimiento de VMs de Proxmox con `linux_ipa_proxmox_discovery_enabled: true`

Para la inscripcion Linux en IPA, mantenga separados los valores de dominio y de servidores:

- `ipaclient_domain` es el dominio DNS compartido de IPA, por ejemplo `example.com`
- `linux_ipa_servers` contiene hostnames de servidores IPA, por ejemplo `ipa01.example.com`

Si quiere conectarse por SSH a Proxmox con un usuario normal con `sudo` en lugar de `root`, configurenlo bajo `proxmox_primary` en `hosts.yml` y mantenga la contrasena de sudo en `vault-proxmox.yml`:

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

En esa configuracion, `vault_proxmox_become_password` es la contrasena que normalmente escribiria para usar `sudo` en el host Proxmox.

### 3. Cifre los vaults

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

Agregue `inventories/production/group_vars/all/vault-windows.yml` al mismo comando cuando habilite el workflow de Windows.

O use los wrappers auxiliares, que por defecto emplean vault IDs separados y crean los archivos de vault de trabajo a partir de los templates de ejemplo si hace falta:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Si quiere contrasenas separadas por dominio al ejecutar los playbooks, prefiera vault IDs en lugar de `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Si el workflow opcional de Windows tambien usa su propia contrasena de vault, agregue `windows@prompt` al mismo comando.

Use `-AskVaultPass` solo cuando todos los archivos de vault implicados por ese playbook compartan la misma contrasena.

### 4. Instale la coleccion requerida

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

O directamente:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

Si instaló `freeipa.ansible_freeipa` antes de que este repositorio agregara el parche de compatibilidad, vuelva a ejecutar uno de los helpers bootstrap o ejecute `python .\scripts\patch_freeipa_collection.py` una vez para parchear tambien la instalacion existente a nivel de usuario.

Cuando use `scripts/run-playbook.ps1`, el helper de parche se ejecuta automaticamente antes de `ansible-playbook`.

### 5. Valide primero

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Si quiere validar solo la ruta auxiliar de FreeIPA para Windows sin hacer cambios en los hosts:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Si quiere una auditoria read-only de readiness Linux que informe que invitados runtime son alcanzables por SSH y que invitados descubiertos desde Proxmox responden por QEMU Guest Agent:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

El reporte de readiness escribe por defecto `.ansible/linux-readiness-report.json`.
Interprete los campos principales asi:

- `ssh.ready=true`: la ruta SSH configurada actualmente para Ansible funciono desde el controlador
- `ssh.promptless=true`: la sonda SSH tuvo exito sin `ansible_password`, por lo que la ruta es no interactiva para Ansible
- `ssh.auth_mode=password_configured`: la sonda uso `sshpass` porque el host tenia definido `ansible_password`
- `ssh.auth_mode=key_or_agent`: la sonda tuvo exito en modo batch SSH sin `ansible_password`
- `qga.status=available`: `qm guest ping` tuvo exito en el nodo Proxmox propietario
- `qga.status=disabled`: la configuracion de la VM en Proxmox no habilita QEMU Guest Agent
- `qga.status=configured_unresponsive`: el guest agent esta habilitado en Proxmox, pero no respondio
- `qga.status=node_unreachable`: el controlador no pudo alcanzar el nodo Proxmox propietario para la sonda
- `qga.status=not_applicable`: el host no fue creado por descubrimiento de Proxmox, asi que no se intento ninguna sonda QGA

Ejemplo de inspeccion rapida:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. Vista previa opcional

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Trate el modo check como una vista previa parcial, no como una simulacion completa. Este repositorio usa comandos CLI directos para parte de la configuracion de Proxmox y la funcion upstream del cliente FreeIPA para el enrolamiento Linux, por lo que `--check` es util pero no es una garantia absoluta.
>
> Para las reglas HBAC de FreeIPA, el modo check valida el paso de definicion de la regla pero omite la accion posterior de habilitarla o deshabilitarla. Eso evita fallos falsos en los que FreeIPA informa que la regla no existe porque realmente no se creo durante el dry run.
>
> El rol del temporizador de sincronizacion del realm de Proxmox tambien omite el paso final de `systemd` para enable o start en modo check, porque los archivos unit se muestran en diff pero no se escriben de verdad durante el dry run.
>
> El enrolamiento Linux en IPA tambien se omite en modo check. El repositorio sigue haciendo discovery, resolucion de hostname y validacion de entradas, pero la funcion upstream `ipaclient` no se ejecuta durante el dry run.

### 7. Aplique la configuracion completa

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

Si el workflow opcional de Windows esta habilitado y `vault-windows.yml` usa una contrasena separada, ejecute el mismo playbook con `--vault-id windows@prompt` o use el wrapper PowerShell con `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` en lugar de `--ask-vault-pass`.

## Orden de despliegue

Para el primer despliegue, aplique la pila en este orden:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Opcional, si gestiona invitados Windows:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Opcional, si quiere el workflow limitado de helpers FreeIPA para Windows:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Opcional, si quiere solo validacion para el workflow auxiliar:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

Esta secuencia facilita mucho mas la resolucion de problemas que ejecutar todo a la vez.

Ejemplo de rollout acotado en PowerShell, por ejemplo para un solo invitado Linux:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Los controles de despliegue por defecto son conservadores:

- cambios de FreeIPA con `serial: 1`
- cambios de Proxmox con `serial: 1`
- preparacion, resolucion y enrolamiento Linux con `serial: 10`
- cambios de gestion Windows con `serial: 10`
- `max_fail_percentage: 0` en todos los recorridos

Ajuste estos valores en `inventories/production/group_vars/all/15-rollout.yml`.

## Modelo de tags

- Use tags para apuntar a cortes estables del despliegue en lugar de crear mas playbooks.
- dominios base: `freeipa`, `proxmox`, `linux`, `validate`
- dominio Windows: `windows`, `windows_domain`
- helpers FreeIPA para Windows: `windows`, `windows_freeipa`
- modelo de acceso FreeIPA: `freeipa_access`
- subconjuntos de Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- preparacion Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- enrolamiento Linux: `linux_enroll`
- eventos: `event`, `linux_refresh`

Ejemplos:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Onboarding de VM basado en eventos

Si quiere que Proxmox dispare el descubrimiento Linux y el enrolamiento IPA inmediatamente despues de arranques o migraciones de VM, use el flujo opcional de hook y webhook documentado en [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

Ese workflow usa un playbook de eventos dedicado en `playbooks/proxmox-vm-event.yml`, de forma que la ruta disparada se limita al lado Linux y FreeIPA del invitado. No vuelve a ejecutar la automatizacion del LDAP realm ni RBAC de Proxmox en cada evento de VM.

El repositorio tambien puede desplegar esta pila opcional de hook y webhook desde `site.yml` o `proxmox.yml` cuando `proxmox_vm_event_onboarding_enabled: true` y las variables webhook requeridas estan definidas.

Los hooks de VM de Proxmox no exponen una fase `create` independiente. En la practica, las VMs nuevas se capturan en su primer evento `post-start`, y los hooks de migracion pueden dispararse tanto en el nodo origen como en el destino.

## Modelo de inventario

Este repositorio usa seis grupos declarados de inventario mas un grupo runtime generado:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Puede agregar sus propios grupos de inventario y referenciarlos desde las definiciones de hostgroups de FreeIPA. Si quiere el conjunto completo de invitados Linux preparados dentro de hostgroups de FreeIPA, referencie `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> FreeIPA sigue necesitando el hostname final de cada invitado. Si usa destinos solo por IP o descubrimiento de Proxmox, defina `ipa_hostname` explicitamente o asegurese de que `hostname -f` dentro del invitado devuelve el FQDN final. Los playbooks ahora resuelven ese hostname antes de construir la membresia de hostgroups en FreeIPA.

> [!TIP]
> No inscriba una golden template reutilizable en FreeIPA. Clone primero la VM, asigne el hostname final e inscriba despues el invitado resultante.

### Modos de origen para invitados Linux

Puede poblar `linux_ipa_clients` de tres formas distintas.

`1.` Hosts estaticos en el inventario

Use entradas normales del inventario de Ansible cuando ya conoce los nombres de los invitados:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

`2.` Definiciones manuales de hosts en variables

Use `linux_ipa_client_hosts` cuando quiera mantener los invitados fuera de `hosts.yml` o cuando solo disponga de una IP:

```yaml
linux_ipa_client_hosts:
  - name: rocky-app-01.example.com
  - name: vm-102
    ansible_host: 192.0.2.102
  - name: vm-103
    ansible_host: 192.0.2.103
    ipa_hostname: ubuntu-jump-01.example.com
```

Notas:

- si `name` es un hostname o FQDN resoluble, `ansible_host` es opcional
- si solo conoce la IP, use cualquier alias estable para `name`
- si se omite `ipa_hostname`, el playbook recurrira a `hostname -f` dentro del invitado

`3.` Auto-descubrimiento de VMs de Proxmox

Use discovery cuando quiera que el playbook extraiga invitados Linux desde uno o varios nodos Proxmox:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Opcional: limite la automatizacion basada en discovery a invitados aprobados.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Opcional: excluya siempre invitados de infraestructura o sensibles aunque
# el descubrimiento del nodo sea amplio.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
```

Notas clave:

- discovery agrega las VMs al mismo grupo `linux_ipa_clients_runtime` usado por el resto de los playbooks
- el descubrimiento de IP depende de que QEMU Guest Agent reporte interfaces de red
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` solo confia en nombres de VM que ya son FQDN
- `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` permite promover nombres cortos y seguros de VMs de Proxmox a pistas de hostname completandolos con `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` es opcional y se usa sobre todo para acotar discovery a VMIDs concretos dentro del flujo de hooks y webhooks basado en eventos
- el invitado sigue necesitando un hostname final, ya sea configurado en el propio sistema o proporcionado con `ipa_hostname`
- el hostname real del sistema invitado debe ser valido para el enrolamiento; valores de marcador de posicion como `localhost.localdomain` deben corregirse antes de ejecutar `linux-clients` o `site`
- si los invitados usan hostnames cortos, puede definir `linux_ipa_identity_hostname_suffix` y opcionalmente `linux_freeipa_enroll_manage_hostname: true` para resolver y aplicar un FQDN antes del enrolamiento
- si el DNS de FreeIPA es autoritativo para los hostnames de sus invitados, puede usar `linux_freeipa_enroll_manage_authoritative_dns: true` para reparar registros A y PTR y eliminar entradas AAAA link-local antes del enrolamiento
- si DNS aun no esta listo, puede usar `linux_ipa_manage_etc_hosts: true` y `linux_ipa_etc_hosts_entries` para escribir un bloque administrado de bootstrap en `/etc/hosts`
- `guest_qemu_agent_install_enabled` instala QEMU Guest Agent en invitados ya alcanzables por SSH o WinRM, reintenta sobre invitados Linux que se vuelven alcanzables mas tarde en el mismo workflow y vuelve a intentarlo tras el enrolamiento Linux
- active `linux_ipa_proxmox_discovery_allowlist_enabled: true` cuando quiera mantener discovery activo pero permitir que solo un subconjunto muy aprobado de invitados entre al inventario runtime Linux
- use `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips` o `linux_ipa_proxmox_discovery_blacklist_names` cuando los nodos con discovery tambien alojan VMs de infraestructura que nunca deben recibir automatizacion Linux IPA; las coincidencias de blacklist siempre prevalecen sobre discovery amplio o allowlist
- `linux_ipa_qga_ssh_bootstrap_enabled` es la ruta preferida sin reinicio para invitados respaldados por Proxmox
- `linux_ipa_ssh_bootstrap_enabled` instala opcionalmente la clave publica SSH del controlador antes de la resolucion de hostname y del enrolamiento
- el enrolamiento Linux en IPA reintenta joins del cliente upstream que fallan por timeout de JSON-RPC de FreeIPA
- el workflow combinado `site` crea primero los hostgroups de FreeIPA y luego agrega a los hosts runtime ya enrolados

## Superficie de configuracion

La mayoria de variables vive en:

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

Para el desglose archivo por archivo vea [docs/VARIABLES.md](../VARIABLES.md).

Familias principales de variables:

| Area | Variables |
| --- | --- |
| Modelo de acceso FreeIPA | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Controles de rollout | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| LDAP realm de Proxmox | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| RBAC de Proxmox | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Inscripcion Linux en IPA | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Reporte de readiness Linux | `linux_readiness_report_*` |
| Gestion Windows | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Helpers FreeIPA para Windows | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Secretos de conexion Ansible | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Ejemplo de estrategia de grupos

Un patron simple que escala bien:

- grupo FreeIPA `proxmox-admins`
- grupo FreeIPA `linux-ssh-admins`
- hostgroup FreeIPA `linux-all`
- regla HBAC `allow-linux-ssh-admins`
- regla `sudo` `allow-linux-ssh-admins-sudo`
- binding ACL de Proxmox para el grupo sincronizado `proxmox-admins-ipa`

Rellene `freeipa_linux_admin_users` en [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) si quiere que un run combinado de `site.yml` conceda automaticamente acceso Linux por SSH y `sudo` a usuarios concretos de IPA a traves del grupo gestionado `linux-ssh-admins`.

Recuerde que la sincronizacion LDAP de Proxmox crea grupos sincronizados con este sufijo:

```text
<group-name>-<realm>
```

Si su grupo de FreeIPA es `proxmox-admins` y el realm de Proxmox es `ipa`, el grupo sincronizado resultante en PVE sera:

```text
proxmox-admins-ipa
```

## Seguridad

- guarde todos los secretos en `vault-freeipa.yml` y `vault-proxmox.yml`, no en archivos de variables de inventario en texto plano
- prefiera una cuenta de bind LDAP dedicada y de solo lectura para Proxmox
- prefiera TLS con verificacion de certificados activada
- mantenga activada la verificacion de host keys SSH fuera de laboratorios desechables
- prefiera `linux_ipa_qga_ssh_bootstrap_enabled` antes que contrasenas temporales compartidas cuando sus invitados de Proxmox ya disponen de un QEMU Guest Agent operativo
- use `guest_qemu_agent_install_enabled` solo cuando el repositorio ya tenga una ruta de gestion valida hacia el invitado
- si habilita el bootstrap SSH de Linux, almacene cualquier contrasena compartida de bootstrap en variables cifradas y rotenla o eliminela una vez establecido el acceso por clave
- no reutilice la cuenta admin de IPA como cuenta de bind LDAP de Proxmox
- revise `proxmox_ldap_filter` y `proxmox_ldap_group_filter` antes de un rollout en produccion para evitar importar mas objetos de los necesarios

Para un laboratorio desechable en el que quiera omitir deliberadamente la verificacion de host SSH, desactive esa comprobacion por sesion de shell en lugar de cambiar los valores por defecto del repositorio:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Idempotencia y advertencias

Este proyecto esta pensado para ser reutilizable y en gran medida idempotente, pero aun asi debe validarse en laboratorio antes de un rollout en produccion.

Limitaciones y advertencias conocidas:

- la salida CLI de Proxmox puede variar entre versiones
- los filtros LDAP pueden necesitar ajuste segun la estructura de su arbol
- cualquier ACL o rol de PVE gestionado manualmente deberia compararse antes de superponer la automatizacion encima
- el auto-descubrimiento depende de invitados en ejecucion y de datos del QEMU Guest Agent
- las definiciones solo por IP siguen requiriendo un hostname final valido dentro del invitado o un `ipa_hostname` explicito
- los playbooks de Proxmox usan elevacion de privilegios, por lo que un usuario SSH distinto de `root` necesita `sudo` funcional y tendra que pasar `-K` salvo que el usuario disponga de passwordless sudo
- si guarda `ansible_become_password` dentro de `vault-proxmox.yml`, puede omitir `-K` porque Ansible leera la contrasena de sudo desde la variable cifrada

## Verificacion

Valide el estado resultante despues de un rollout exitoso en lugar de asumir que todos los caminos de acceso quedaron correctos.

### En FreeIPA

- confirme que existen los grupos de usuarios esperados
- confirme que existen los hostgroups esperados
- confirme que las reglas HBAC esperadas existen y estan habilitadas
- confirme que las reglas `sudo` esperadas existen y estan habilitadas

### En Proxmox

- confirme que existe el LDAP realm
- confirme que la sincronizacion inicial importo los usuarios o grupos esperados
- confirme que el grupo sincronizado previsto tiene el binding ACL esperado

### En un invitado Linux

- confirme que un usuario IPA permitido puede iniciar sesion
- confirme que un usuario no permitido queda bloqueado por HBAC
- confirme que un administrador IPA permitido puede ejecutar `sudo -l`
- confirme que se crea el directorio home en el primer login si `linux_ipaclient_mkhomedir` esta habilitado

## Estructura del repositorio

<details>
<summary>Mostrar estructura del repositorio</summary>

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

## Desarrollo

El repositorio incluye estos archivos auxiliares principales:

- `.editorconfig` mantiene coherentes los valores de espacios, encoding y finales de linea entre editores
- `.gitattributes` mantiene archivos de texto comunes con finales de linea `LF`
- `.gitignore` evita que inventarios generados, datos de vault, collections locales y archivos de editor entren en Git
- `.ansible-lint` excluye collections vendorizadas y solo suprime la regla de longitud de linea YAML
- `.yamllint` mantiene consistentes las comprobaciones de formato YAML en playbooks, inventarios y workflows
- `.github/CODEOWNERS` enruta la propiedad de revisiones para las principales areas del repositorio
- `.github/workflows/ci.yml` ejecuta comprobaciones de lint y validacion smoke en pushes y pull requests
- `.pre-commit-config.yaml` ejecuta el hook rapido de lint antes de cada commit cuando `pre-commit` esta instalado
- `CHANGELOG.md` registra en un unico lugar los cambios destacables del repositorio
- `docs/VARIABLES.md` explica el layout dividido de variables de inventario
- `docs/i18n/` contiene archivos README traducidos que deben reflejar la estructura completa del README en ingles mientras `README.md` sigue siendo la fuente canonica
- `docs/i18n/TRANSLATION_GUIDE.md` explica como mantener sincronizados los README traducidos
- `scripts/bootstrap.ps1` y `scripts/bootstrap.sh` instalan la collection requerida en la ruta local `collections/` del repositorio y la parchean para compatibilidad con ansible-core 2.24+
- `scripts/patch_freeipa_collection.py` reescribe imports obsoletos en la collection FreeIPA fijada para que siga siendo compatible con futuras versiones de ansible-core
- `scripts/lint.py` proporciona el punto de entrada multiplataforma para lint, CI y pre-commit
- `scripts/smoke-test.py` valida el inventario de ejemplo y ejecuta comprobaciones de sintaxis sin tocar infraestructura real, incluido el playbook separado de Windows
- `scripts/check_translations.py` audita los README traducidos respecto a metadatos, paridad estructural de secciones y cobertura minima de contenido frente al README canonico en ingles
- `scripts/lint.ps1` y `scripts/lint.sh` ejecutan el workflow combinado de lint local y smoke
- `scripts/proxmox_event_webhook.py` ejecuta el webhook opcional del lado del controlador para eventos de VMs de Proxmox
- `scripts/proxmox-vm-hook.pl` es el hookscript opcional de Proxmox que notifica al webhook del controlador en eventos `post-start` y `post-migrate`
- `scripts/run-playbook.ps1` envuelve comandos comunes de `ansible-playbook` para usuarios de PowerShell, incluido el workflow separado de Windows
- `scripts/vault.ps1` y `scripts/vault.sh` envuelven operaciones comunes de split-vault para secretos de FreeIPA, Proxmox y Windows opcional
- `tests/` contiene la superficie de verificacion del repositorio, empezando por la documentacion smoke-test
- `CONTRIBUTING.md` documenta el flujo esperado de contribucion y validacion
- `SECURITY.md` documenta como informar vulnerabilidades y tratar informacion sensible de seguridad

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

Para habilitar el hook rapido de lint antes de cada commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

El wrapper de PowerShell para playbooks ya admite tambien opciones operativas habituales:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Inventory inventories\production\hosts.yml -Tags freeipa,proxmox -AskVaultPass
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskBecomePass -ExtraVars ipaclient_domain=example.com
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -VaultId windows@prompt
```

## Siguientes extensiones

- mejoras posteriores comunes:
- pipeline Packer para plantillas Linux listas para IPA
- job templates y schedules de AWX
- modelos separados de tenants y pools de Proxmox
- integracion mas amplia con politicas locales de Windows o GPO

## Licencia

Publicado bajo la [0BSD License](../../LICENSE).
