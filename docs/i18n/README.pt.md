# Automacao de Acesso Proxmox + FreeIPA

Esta pagina fornece uma traducao completa da estrutura de [README.md](../../README.md). A versao em ingles continua sendo a referencia canonica, mas esta traducao cobre as mesmas secoes principais.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-09

## Por que este projeto existe

Use este repositorio quando voce ja tiver:

- um ambiente FreeIPA saudavel
- um cluster Proxmox VE
- convidados Linux que devem autenticar de forma centralizada
- uma conta de servico dedicada para o bind LDAP do Proxmox
- um modelo claro de grupos para administradores e operadores

O principio central e tratar o FreeIPA como fonte de verdade para identidade e acesso. O Proxmox consome esse diretorio por meio de um LDAP realm, os clientes Linux entram no FreeIPA pelo role `ipaclient`, e as politicas de SSH, HBAC e `sudo` permanecem centralizadas.

## O que voce recebe

- gerenciamento de grupos de usuarios, hostgroups, regras HBAC e regras `sudo` no FreeIPA
- configuracao do LDAP realm do Proxmox contra o FreeIPA
- sincronizacao periodica do realm a partir de um no designado do cluster
- ligacoes RBAC do Proxmox para grupos sincronizados
- ingresso de Linux por inventory estatico, definicoes manuais ou descoberta Proxmox
- bootstrap SSH opcional sem reboot por meio do QEMU Guest Agent
- instalacao opcional do QEMU Guest Agent via SSH ou WinRM em convidados acessiveis
- bootstrap opcional de chave publica SSH para o primeiro acesso
- refresh automatico do cache SSSD apos mudancas no modelo de acesso
- onboarding opcional dirigido por eventos `post-start` e `post-migrate`

## Escopo

| Incluido | Nao incluido |
| --- | --- |
| Modelo de acesso FreeIPA | Domain join do Windows |
| Configuracao do LDAP realm do Proxmox | Implantacao de FreeRADIUS |
| RBAC do Proxmox a partir de grupos sincronizados | Criacao completa do ciclo de vida de usuarios no FreeIPA |
| Ingresso de clientes Linux no IPA | Cobertura completa de todos os casos de multi-tenant do Proxmox |

## Arquitetura

```text
FreeIPA users/groups
        |
        +--> Proxmox LDAP realm --> synced PVE users/groups --> PVE ACLs/roles
        |
        +--> Linux IPA clients --> SSSD/PAM/NSS --> HBAC --> SSH/login access
        |
        +--> FreeRADIUS (separate concern, same directory backend)
```

## Requisitos

### Controlador

- Ansible Core 2.14+
- alcance SSH para o no primario do Proxmox, servidores IPA e clientes Linux
- `sudo` ou `root` quando necessario
- se o bootstrap SSH por QGA estiver habilitado, o QEMU Guest Agent ja precisa estar ativo no convidado
- se o fallback para Windows estiver habilitado, os hosts acessiveis devem estar em `windows_qemu_guest_agent_clients`
- se o bootstrap SSH Linux estiver habilitado, o controlador precisa de um par de chaves SSH e de um caminho inicial com senha

### Alvos

- Proxmox VE 6.x ou superior no host em `proxmox_primary`
- FreeIPA acessivel a partir do Proxmox e dos clientes Linux
- DNS e sincronizacao de tempo corretos
- em `proxmox_primary`, use `root` ou um usuario SSH com `sudo` para `pveversion`, `pvesh` e `pveum`
- com descoberta Proxmox, os convidados devem expor um IP utilizavel via QEMU Guest Agent

## Portas de rede

Os principais ports usados por este repositorio sao:

- `22/TCP` para SSH
- `53/TCP,UDP` para DNS do IPA
- `88/TCP,UDP` e `464/TCP,UDP` para Kerberos
- `389/TCP` para LDAP
- `linux_freeipa_enroll_https_port`, padrao `443/TCP`
- `636/TCP` para `ldaps`

## Compatibilidade

- voltado para Proxmox VE 6.x e posteriores
- majors suportados por padrao: `6`, `7`, `8`, `9`, `10`
- ajustavel por `proxmox_supported_major_versions`
- `proxmox_allow_future_major_versions` padrao `true`

## Inicio rapido

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

Edite os arquivos `hosts.yml`, `10-features.yml`, `15-rollout.yml`, `20-freeipa.yml`, `30-linux-clients.yml`, `40-proxmox-ldap.yml`, `50-proxmox-sync.yml`, `60-proxmox-rbac.yml`, `vault-freeipa.yml` e `vault-proxmox.yml` para a sua infraestrutura.

## Ordem de rollout

Para a primeira implantacao:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
```

O padrao e conservador: `serial: 1` para FreeIPA e Proxmox, `serial: 10` para Linux e `max_fail_percentage: 0`.

## Modelo de tags

- `freeipa`, `proxmox`, `linux`, `validate`
- `freeipa_access`
- `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- `linux_enroll`
- `event`, `linux_refresh`

## Onboarding de VM orientado a eventos

Se quiser disparar descoberta Linux e ingresso IPA logo apos `post-start` ou `post-migrate`, use o fluxo opcional hook/webhook descrito em [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md). Esse caminho usa `playbooks/proxmox-vm-event.yml`, nao reexecuta LDAP realm ou RBAC a cada evento e captura novas VMs no primeiro `post-start`.

## Modelo de inventory

Grupos principais:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`

Mesmo com IP-only ou descoberta Proxmox, o convidado ainda precisa de FQDN final via `ipa_hostname` ou `hostname -f`.

### Modos de origem Linux

1. hosts estaticos no inventory
2. definicoes manuais em `linux_ipa_client_hosts`
3. descoberta Proxmox por `linux_ipa_proxmox_discovery_*`

Notas importantes: descoberta depende de QEMU Guest Agent, `linux_ipa_proxmox_discovery_vmids` e util no fluxo por eventos, `linux_ipa_identity_hostname_suffix` e `linux_freeipa_enroll_manage_hostname` ajudam com nomes curtos, `linux_freeipa_enroll_manage_authoritative_dns` pode corrigir DNS autoritativo, e `linux_ipa_manage_etc_hosts` ajuda quando o DNS ainda nao esta pronto.

## Superficie de configuracao

As principais configuracoes ficam em:

- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`

## Exemplo de estrategia de grupos

- `proxmox-admins`
- `linux-ssh-admins`
- `linux-all`
- `allow-linux-ssh-admins`
- `allow-linux-ssh-admins-sudo`
- `proxmox-admins-ipa`

## Seguranca

- guarde segredos apenas nos vaults
- prefira uma conta LDAP somente leitura para o Proxmox
- prefira TLS com verificacao de certificado
- nao desative host key checking fora de laboratorios descartaveis

## Idempotencia e observacoes

O projeto busca ser reutilizavel e amplamente idempotente, mas deve ser validado em laboratorio antes da producao. Limitacoes conhecidas incluem variacoes do CLI do Proxmox, necessidade de ajustar filtros LDAP, dependencia de QEMU Guest Agent para descoberta e exigencia de hostname final valido para definicoes baseadas em IP.

## Verificacao

- no FreeIPA, confirme grupos, hostgroups, regras HBAC e `sudo`
- no Proxmox, confirme LDAP realm, sync inicial e bindings ACL
- em um convidado Linux, teste login permitido, bloqueio HBAC, `sudo -l` e criacao do home

## Layout do repositorio

```text
README.md
docs/
inventories/
playbooks/
roles/
scripts/
tests/
```

## Desenvolvimento

O repositorio inclui `.editorconfig`, `.gitattributes`, `.gitignore`, `.ansible-lint`, `.yamllint`, workflows de CI, `scripts/bootstrap.*`, `scripts/lint.*`, `scripts/smoke-test.py`, `scripts/proxmox_event_webhook.py`, `scripts/proxmox-vm-hook.pl`, `scripts/run-playbook.ps1` e `scripts/vault.*`.

```bash
ansible-lint
python scripts/smoke-test.py
./scripts/lint.sh
```

## Proximas extensoes

- pipeline Packer para templates Linux prontos para IPA
- templates e agendamentos do AWX
- modelos separados de tenant e pool no Proxmox
- fluxo Windows ou AD trust para ambientes orientados a RDP

## Licenca

Publicado sob a [MIT License](../../LICENSE).
