# Automacao de Acesso Proxmox + FreeIPA

Esta pagina fornece uma traducao completa e estruturalmente fiel de [README.md](../../README.md). A versao em ingles continua sendo a fonte canonica, mas esta versao em portugues deve cobrir o mesmo escopo operacional para operadores lusofonos.

Translation scope: full
Canonical source: ../../README.md
Last synced: 2026-04-15

## Idiomas

A versao em ingles e a fonte canonica da documentacao completa. Voce pode encontrar outras traducoes e o indice de idiomas em [docs/i18n/README.md](README.md).

## Por que este projeto existe

Use este repositorio quando voce ja tiver:

- um ambiente FreeIPA saudavel
- um cluster Proxmox VE
- convidados Linux que devem autenticar de forma centralizada
- uma conta de servico dedicada para o bind LDAP do Proxmox
- um modelo claro de grupos para administradores e operadores

O principio central e tratar o FreeIPA como fonte de verdade para identidade e acesso. O Proxmox consome esse diretorio por meio de um LDAP realm, os convidados Linux entram no FreeIPA com o role upstream `ipaclient`, e as regras de SSH, HBAC e `sudo` permanecem centralizadas em vez de se espalharem por contas locais em cada VM.

## O que voce recebe

- gerenciamento de grupos de usuarios, hostgroups, regras HBAC e regras `sudo` no FreeIPA
- valores padrao de login shell do FreeIPA para administradores Linux
- configuracao do LDAP realm do Proxmox contra o FreeIPA
- sincronizacao recorrente do realm de Proxmox a partir de um no de cluster designado
- bindings RBAC do Proxmox para grupos de diretorio sincronizados
- ingresso de convidados Linux no FreeIPA por inventario estatico, destinos somente por IP ou descoberta de VMs no Proxmox
- bootstrap SSH opcional sem reboot por meio do QEMU Guest Agent do Proxmox
- habilitacao opcional da comunicacao do guest agent no lado Proxmox para convidados Linux apoiados pelo Proxmox
- instalacao opcional por SSH ou WinRM do QEMU Guest Agent como fallback para convidados que ja estao acessiveis, que ficam acessiveis depois do bootstrap ou que sao reprocessados apos o enrollment Linux
- relatorio opcional de readiness Linux para alcance SSH e estado do QEMU Guest Agent do Proxmox
- workflow separado e opcional de associacao de dominio para Windows 10/11 e Windows Server via Active Directory
- workflow opcional e limitado para Windows com consciencia de FreeIPA, voltado a confianca na CA do IPA, bootstrap de hosts e validacoes de alcance ao IPA
- bootstrap opcional de chave publica SSH para o primeiro acesso a convidados Linux
- refresh automatico do cache SSSD em clientes Linux gerenciados apos mudancas no modelo de acesso do FreeIPA
- onboarding Linux opcional dirigido por eventos a partir de hooks de VM do Proxmox e gatilhos webhook

## Escopo

| Incluido | Nao incluido |
| --- | --- |
| Modelo de acesso FreeIPA | Implantacao de FreeRADIUS |
| Configuracao do LDAP realm do Proxmox | Criacao completa do ciclo de vida de usuarios no FreeIPA |
| RBAC do Proxmox com base em grupos sincronizados | Cobertura total de todos os casos multi-tenant do Proxmox |
| Ingresso de clientes Linux no IPA | Login nativo do Windows diretamente contra o FreeIPA |
| Workflow separado de associacao ao dominio AD para Windows | Automacao ampla de objetos AD ou GPO |
| Workflow limitado de helpers FreeIPA para Windows | Fingir que helpers Windows baseados apenas em FreeIPA equivalem a AD |

## Workflow do Windows

O suporte a Windows e implementado como um workflow separado em vez de ser misturado ao enrollment Linux em IPA.

- `windows_qemu_guest_agent_clients` fica reservado para tarefas auxiliares opcionais do QEMU Guest Agent.
- habilite o workflow com `windows_domain_membership_enabled: true` em `10-features.yml`
- `windows_management_clients` e o grupo separado de gerenciamento Windows usado por `playbooks/windows-management.yml` e pela etapa opcional de Windows dentro de `playbooks/site.yml`
- o login real do Windows e tratado por associacao ao dominio Active Directory; em ambientes centrados em FreeIPA, junte os hosts Windows ao lado AD de uma relacao de confianca FreeIPA-AD em vez de tentar ingressar Windows diretamente no FreeIPA

A associacao de Windows apenas com FreeIPA nao e suportada por este repositorio. Sem Active Directory ou sem uma relacao de confianca FreeIPA-AD, o lado Windows fica limitado a tarefas auxiliares como gerenciamento de convidados acessiveis e instalacao opcional do QEMU Guest Agent.

Se voce ainda quiser um caminho limitado e consciente de FreeIPA para Windows sem domain join, habilite `windows_freeipa_helpers_enabled: true` e use `windows_freeipa_helper_clients` com `playbooks/windows-freeipa-helpers.yml`. Esse workflow auxiliar pode confiar na CA do IPA, buscar automaticamente a CA do IPA para bootstrap, fixar opcionalmente o thumbprint esperado da CA, gerenciar entradas opcionais no arquivo hosts, validar DNS do IPA e portas TCP relevantes, validar alcance HTTPS a partir do Windows, validar uma fonte de tempo do Windows contra um endpoint relacionado ao IPA, gerenciar associacoes a grupos locais do Windows e instalar ou expor opcionalmente o OpenSSH Server, mas nao fornece login nativo do Windows contra o FreeIPA.

Se voce quiser uma verificacao de readiness sem fazer alteracoes para esse mesmo grupo auxiliar, execute `playbooks/windows-freeipa-validate.yml`. Ele preserva o caminho de validacao e resumo, mas desabilita para essa execucao a importacao da CA, as mudancas no arquivo hosts, as alteracoes em grupos locais e o gerenciamento do OpenSSH.

Esse workflow mira convidados Windows 10/11 e Windows Server acessiveis por WinRM ou PSRP.

## Arquitetura

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

A explicacao de design mais longa esta em [docs/ARCHITECTURE.md](../ARCHITECTURE.md).

## Requisitos

### Controlador

- Ansible Core 2.14 ou superior
- alcance SSH ao no primario do Proxmox, aos servidores IPA e aos clientes Linux
- alcance WinRM ou PSRP aos convidados Windows quando voce usar o workflow Windows
- `sudo` ou `root` onde for necessario
- se o bootstrap SSH por QGA estiver habilitado, o QEMU Guest Agent ja precisa estar em execucao no convidado
- se a instalacao de fallback do guest agent para Windows estiver habilitada, os hosts Windows acessiveis devem estar em `windows_qemu_guest_agent_clients`
- se a associacao de dominio Windows estiver habilitada, os hosts Windows acessiveis devem estar em `windows_management_clients` e voce precisa fornecer credenciais de ingresso em AD
- se as tarefas auxiliares FreeIPA para Windows estiverem habilitadas, os hosts Windows acessiveis devem estar em `windows_freeipa_helper_clients`
- se o bootstrap SSH Linux estiver habilitado, o controlador precisa de um par de chaves SSH e de um caminho inicial de login com senha para a conta do convidado usada pelo Ansible

### Alvos

- Proxmox VE 6.x ou superior no host de `proxmox_primary`
- FreeIPA acessivel a partir do Proxmox e dos clientes Linux
- convidados Windows 10/11 e Windows Server podem ser gerenciados pelo workflow Windows separado quando estiverem acessiveis por WinRM ou PSRP
- DNS e sincronizacao de tempo corretos
- para `proxmox_primary`, use `root` ou um usuario SSH com `sudo` para `pveversion`, `pvesh` e `pveum`
- se voce usar associacao de dominio Windows, os convidados Windows alvo precisam conseguir alcancar os controladores de dominio AD correspondentes
- se voce usar o workflow limitado de helpers FreeIPA para Windows, os convidados Windows alvo precisam conseguir alcancar os servidores IPA correspondentes
- se voce usar auto-descoberta de VMs no Proxmox, os convidados descobertos devem expor um IP utilizavel via QEMU Guest Agent

## Portas de rede

Esta tabela lista as portas de rede usadas pelo controlador deste repositorio, pela automacao LDAP do Proxmox e pelo fluxo de enrollment Linux em IPA.
Ela e intencionalmente limitada ao escopo deste projeto, e nao a matriz completa de replicacao servidor-servidor do FreeIPA.

| Nome | Porta | Protocolo | Origem | Destino | Necessaria quando | Proposito |
| --- | --- | --- | --- | --- | --- | --- |
| SSH | `22` | `TCP` | Controlador Ansible | No Proxmox, servidor IPA, convidado Linux | Sempre | Conectividade Ansible |
| WinRM | `5985`, `5986` | `TCP` | Controlador Ansible | Convidado Windows | Quando o gerenciamento Windows esta habilitado | Conectividade Ansible para convidados Windows |
| DNS | `53` | `TCP`, `UDP` | Convidado Linux | Servidores DNS do IPA | Quando os convidados Linux usam DNS do IPA | Resolver registros do IPA e nomes externos via IPA DNS |
| Kerberos | `88` | `TCP`, `UDP` | Convidado Linux | Servidores IPA | Enrollment e login Linux em IPA | Autenticacao Kerberos |
| LDAP | `389` | `TCP` | Convidado Linux | Servidores IPA | Enrollment e login Linux em IPA | LDAP e descoberta do cliente FreeIPA |
| HTTPS | `linux_freeipa_enroll_https_port`, padrao `443` | `TCP` | Convidado Linux | Servidores IPA | Enrollment Linux em IPA | Verificacao web/API do IPA durante a instalacao do cliente |
| Kerberos Password | `464` | `TCP`, `UDP` | Convidado Linux | Servidores IPA | Enrollment Linux em IPA e operacoes de senha | Operacoes de senha e keytab do Kerberos |
| LDAPS | `636` | `TCP` | No primario do Proxmox | Servidores IPA ou LDAP | Quando o LDAP realm do Proxmox usa o modo padrao `ldaps` | Conexao do LDAP realm do Proxmox |

Notas:

- `LDAPS 636/TCP` e o padrao do repositorio porque `proxmox_ldap_mode` usa `ldaps` por padrao. Se voce mudar o modo ou a porta LDAP, permita em vez disso o `proxmox_ldap_port` configurado.
- `WinRM` normalmente usa `5986/TCP` para HTTPS ou `5985/TCP` para HTTP, conforme a configuracao do transporte Windows.
- `DNS 53/TCP,UDP` so e necessario quando os convidados Linux usam os servidores IPA como resolvers.
- `Kerberos 88` e `Kerberos Password 464` exigem tanto `TCP` quanto `UDP`.
- A associacao ao dominio Active Directory tambem exige o conjunto normal de portas entre Windows e controladores de dominio, mas essa matriz depende do ambiente e nao esta listada aqui de forma exaustiva.
- A sincronizacao de tempo continua sendo necessaria para que o Kerberos funcione com confiabilidade, mas a fonte NTP depende do ambiente e nao e gerenciada por este repositorio.

## Compatibilidade

A automacao de Proxmox neste repositorio foi escrita em torno das interfaces `pveum` e `pvesh` para realm e RBAC usadas pelo Proxmox VE 6.x e posteriores.

- versoes maiores suportadas por padrao: `6`, `7`, `8`, `9`, `10`
- a validacao verifica a versao detectada do Proxmox via `pveversion`
- a lista de versoes suportadas pode ser ajustada com `proxmox_supported_major_versions` caso voce precise restringi-la ou amplia-la em seu ambiente
- `proxmox_allow_future_major_versions` e `true` por padrao, entao versoes maiores acima da ultima versao testada tambem passam na validacao por padrao
- futuras versoes maiores ainda devem ser tratadas como candidatas de compatibilidade ate que a interface publicada do Proxmox seja verificada contra esta automacao
- versoes legadas antigas, como `1` a `5`, nao sao apresentadas como suporte testado por este repositorio publico; se voce as adicionar localmente, trate isso como um override explicito de compatibilidade e valide o workflow completo primeiro em laboratorio

Exemplo de override local para um laboratorio legado:

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

Os exemplos abaixo usam comandos de shell. Equivalentes em PowerShell sao incluidos onde isso costuma importar.

### 1. Copie o inventario de exemplo e os templates de vault

```bash
cp inventories/production/hosts.yml.example inventories/production/hosts.yml
cp inventories/production/group_vars/all/vault-freeipa.yml.example inventories/production/group_vars/all/vault-freeipa.yml
cp inventories/production/group_vars/all/vault-proxmox.yml.example inventories/production/group_vars/all/vault-proxmox.yml
# Opcional quando voce planeja gerenciar convidados Windows:
cp inventories/production/group_vars/all/vault-windows.yml.example inventories/production/group_vars/all/vault-windows.yml
```

```powershell
Copy-Item inventories\production\hosts.yml.example inventories\production\hosts.yml
Copy-Item inventories\production\group_vars\all\vault-freeipa.yml.example inventories\production\group_vars\all\vault-freeipa.yml
Copy-Item inventories\production\group_vars\all\vault-proxmox.yml.example inventories\production\group_vars\all\vault-proxmox.yml
# Opcional quando voce planeja gerenciar convidados Windows:
Copy-Item inventories\production\group_vars\all\vault-windows.yml.example inventories\production\group_vars\all\vault-windows.yml
```

### 2. Edite os arquivos especificos do ambiente

- `inventories/production/hosts.yml`
- `inventories/production/group_vars/all/10-features.yml`
- `inventories/production/group_vars/all/15-rollout.yml`
- `inventories/production/group_vars/all/20-freeipa.yml`
- `inventories/production/group_vars/all/30-linux-clients.yml`
- `inventories/production/group_vars/all/35-windows-clients.yml` quando voce usar gerenciamento Windows
- `inventories/production/group_vars/all/40-proxmox-ldap.yml`
- `inventories/production/group_vars/all/50-proxmox-sync.yml`
- `inventories/production/group_vars/all/60-proxmox-rbac.yml`
- `inventories/production/group_vars/all/vault-freeipa.yml`
- `inventories/production/group_vars/all/vault-proxmox.yml`
- `inventories/production/group_vars/all/vault-windows.yml` quando voce usar gerenciamento Windows

Escolha um modo de origem para convidados Linux, alem das configuracoes de IPA e Proxmox:

- entradas estaticas de inventario sob `linux_ipa_clients`
- entradas `linux_ipa_client_hosts` em `group_vars/all/30-linux-clients.yml`
- descoberta de VMs no Proxmox com `linux_ipa_proxmox_discovery_enabled: true`

Para o enrollment Linux em IPA, mantenha separados os valores de dominio e de servidores:

- `ipaclient_domain` e o dominio DNS compartilhado do IPA, como `example.com`
- `linux_ipa_servers` contem hostnames de servidores IPA, como `ipa01.example.com`

Se voce quiser acessar o Proxmox via SSH com um usuario comum com `sudo`, em vez de `root`, defina isso em `proxmox_primary` dentro de `hosts.yml` e mantenha a senha de sudo em `vault-proxmox.yml`:

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

Nessa configuracao, `vault_proxmox_become_password` e a senha que voce normalmente digita para `sudo` no host Proxmox.

### 3. Criptografe os vaults

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

Adicione `inventories/production/group_vars/all/vault-windows.yml` ao mesmo comando quando habilitar o workflow Windows.

Ou use os wrappers auxiliares, que por padrao empregam vault IDs separados e criam os arquivos de vault de trabalho a partir dos templates de exemplo quando necessario:

```bash
./scripts/vault.sh --action encrypt --domain all
```

```powershell
.\scripts\vault.ps1 -Action encrypt -Domain all
```

Se voce quiser senhas separadas por dominio ao executar os playbooks, prefira vault IDs em vez de `--ask-vault-pass`:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -VaultId freeipa@prompt,proxmox@prompt
```

Se o workflow opcional de Windows tambem usar sua propria senha de vault, adicione `windows@prompt` ao mesmo comando.

Use `-AskVaultPass` apenas quando todos os arquivos vault usados por aquele playbook compartilharem a mesma senha.

### 4. Instale a colecao necessaria

```bash
./scripts/bootstrap.sh
```

```powershell
.\scripts\bootstrap.ps1
```

Ou diretamente:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
python scripts/patch_freeipa_collection.py
```

```powershell
ansible-galaxy collection install -r requirements.yml -p .\collections
python .\scripts\patch_freeipa_collection.py
```

Se voce instalou `freeipa.ansible_freeipa` antes de este repositorio adicionar o patch de compatibilidade, execute novamente um dos helpers de bootstrap ou rode `python .\scripts\patch_freeipa_collection.py` uma vez para corrigir tambem a instalacao da collection no escopo do usuario.

Quando voce usa `scripts/run-playbook.ps1`, ele executa esse helper de patch automaticamente antes de chamar `ansible-playbook`.

### 5. Valide primeiro

```bash
ansible-playbook playbooks/validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook validate -AskVaultPass
```

Se voce quiser validar apenas o caminho helper-only do Windows FreeIPA, sem fazer alteracoes no host:

```bash
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -AskVaultPass
```

Se voce quiser uma auditoria read-only de readiness Linux que mostre quais convidados runtime estao acessiveis via SSH e quais convidados descobertos no Proxmox respondem pelo QEMU Guest Agent:

```bash
ansible-playbook playbooks/linux-readiness-report.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -AskVaultPass
```

O relatorio de readiness grava `.ansible/linux-readiness-report.json` por padrao.
Interprete os principais campos assim:

- `ssh.ready=true`: o caminho SSH atualmente configurado para o Ansible funcionou a partir do controlador
- `ssh.promptless=true`: a sonda SSH teve sucesso sem `ansible_password`, entao o caminho e nao interativo para o Ansible
- `ssh.auth_mode=password_configured`: a sonda usou `sshpass` porque o host tinha `ansible_password`
- `ssh.auth_mode=key_or_agent`: a sonda teve sucesso em SSH batch mode sem `ansible_password`
- `qga.status=available`: `qm guest ping` teve sucesso no no Proxmox dono da VM
- `qga.status=disabled`: a configuracao da VM no Proxmox nao habilita o QEMU Guest Agent
- `qga.status=configured_unresponsive`: o guest agent esta habilitado na configuracao do Proxmox, mas nao respondeu
- `qga.status=node_unreachable`: o controlador nao conseguiu alcancar o no Proxmox dono da VM para a sonda
- `qga.status=not_applicable`: o host nao foi criado por descoberta Proxmox, entao nenhuma sonda QGA foi tentada

Exemplo de inspecao rapida:

```bash
jq '.summary' .ansible/linux-readiness-report.json
jq '.hosts[] | {inventory_name, ansible_user, ssh_auth_mode: .ssh.auth_mode, ssh_promptless: .ssh.promptless, qga_status: .qga.status}' .ansible/linux-readiness-report.json
```

### 6. Opcional: visualize as mudancas planejadas

```bash
ansible-playbook playbooks/site.yml --check --diff --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Check -Diff -AskVaultPass
```

> [!NOTE]
> Trate o check mode como uma visualizacao parcial, e nao como uma simulacao completa. Este repositorio usa comandos CLI diretos para parte da configuracao do Proxmox e o role upstream do cliente FreeIPA para o enrollment Linux, entao `--check` e util, mas nao autoritativo.
>
> Para regras HBAC do FreeIPA, o check mode valida a etapa de definicao da regra, mas pula a acao posterior de habilitar ou desabilitar. Isso evita falsos erros em que o FreeIPA reportaria a regra como ausente porque ela nao foi realmente criada durante o dry run.
>
> O role do timer de sincronizacao de realm do Proxmox tambem pula a etapa final de `systemd` enable ou start no check mode, porque os unit files aparecem no diff, mas nao sao realmente gravados durante o dry run.
>
> O enrollment Linux em IPA tambem e pulado no check mode. O repositorio ainda faz discovery, resolucao de hostname e validacao de entradas, mas o role upstream `ipaclient` nao e executado durante o dry run.

### 7. Aplique a configuracao completa

```bash
ansible-playbook playbooks/site.yml --ask-vault-pass
```

```powershell
.\scripts\run-playbook.ps1 -Playbook site -AskVaultPass
```

Se o workflow opcional de Windows estiver habilitado e `vault-windows.yml` usar senha separada, execute o mesmo playbook com `--vault-id windows@prompt` ou com o wrapper PowerShell `-VaultId freeipa@prompt,proxmox@prompt,windows@prompt` em vez de `--ask-vault-pass`.

## Ordem de rollout

Para a primeira implantacao, aplique a pilha nesta ordem:

```bash
ansible-playbook playbooks/freeipa.yml --ask-vault-pass
ansible-playbook playbooks/proxmox.yml --ask-vault-pass
ansible-playbook playbooks/linux-clients.yml --ask-vault-pass
# Opcional quando voce gerencia convidados Windows:
ansible-playbook playbooks/windows-management.yml --ask-vault-pass
# Opcional quando voce quer o workflow limitado de helpers Windows FreeIPA:
ansible-playbook playbooks/windows-freeipa-helpers.yml --ask-vault-pass
# Opcional quando voce quer cobertura somente de validacao para o workflow helper:
ansible-playbook playbooks/windows-freeipa-validate.yml --ask-vault-pass
```

Essa sequencia torna a solucao de problemas muito mais facil do que executar tudo de uma vez.

Exemplo de rollout limitado em PowerShell, por exemplo para um unico convidado Linux:

```powershell
.\scripts\run-playbook.ps1 -Playbook linux-clients -Limit rocky-app-01.example.com -AskVaultPass
```

Os controles padrao de rollout sao conservadores:

- mudancas de acesso no FreeIPA executam com `serial: 1`
- mudancas no Proxmox executam com `serial: 1`
- resolucao de hostname, validacao e enrollment Linux executam com `serial: 10`
- mudancas de gerenciamento Windows executam com `serial: 10`
- todos os caminhos de rollout usam `max_fail_percentage: 0` por padrao

Ajuste esses valores em `inventories/production/group_vars/all/15-rollout.yml`.

## Modelo de tags

Use tags para mirar fatias estaveis de rollout em vez de criar mais playbooks.

- dominios centrais: `freeipa`, `proxmox`, `linux`, `validate`
- dominio Windows: `windows`, `windows_domain`
- helpers Windows FreeIPA: `windows`, `windows_freeipa`
- modelo FreeIPA: `freeipa_access`
- subconjuntos Proxmox: `proxmox_ldap`, `proxmox_sync`, `proxmox_rbac`
- preparacao Linux: `inventory`, `discovery`, `hostnames`, `linux_inventory`, `proxmox_discovery`
- enrollment Linux: `linux_enroll`
- tratamento dirigido por eventos de VM: `event`, `linux_refresh`

Exemplos:

```powershell
.\scripts\run-playbook.ps1 -Playbook site -Tags freeipa_access -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook proxmox -Tags proxmox_ldap,proxmox_rbac -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook validate -Tags discovery -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook linux-readiness-report -Tags readiness_report -VaultId freeipa@prompt,proxmox@prompt
.\scripts\run-playbook.ps1 -Playbook windows-management -Tags windows_domain -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-helpers -Tags windows_freeipa -VaultId windows@prompt
.\scripts\run-playbook.ps1 -Playbook windows-freeipa-validate -Tags windows_freeipa -VaultId windows@prompt
```

## Onboarding de VM orientado a eventos

Se voce quiser que o Proxmox dispare discovery Linux e enrollment em IPA logo apos a inicializacao da VM ou apos uma migracao, use o fluxo opcional de hook e webhook descrito em [docs/EVENT_DRIVEN_VM_ONBOARDING.md](../EVENT_DRIVEN_VM_ONBOARDING.md).

Esse caminho usa o playbook de evento dedicado `playbooks/proxmox-vm-event.yml`, de modo que o gatilho cuida apenas do lado Linux e FreeIPA do convidado. Ele nao reexecuta a automacao de LDAP realm nem a de RBAC do Proxmox a cada evento de VM.

O repositorio agora tambem pode implantar essa pilha opcional de hook e webhook por meio de `site.yml` ou `proxmox.yml` quando `proxmox_vm_event_onboarding_enabled: true` estiver definido e as variaveis de webhook necessarias tiverem sido fornecidas.

Os hooks de VM do Proxmox nao oferecem uma etapa `create` independente. Na pratica, novas VMs costumam ser capturadas no primeiro evento `post-start`, enquanto hooks de migracao podem ser disparados tanto no no de origem quanto no de destino.

## Modelo de inventario

Este repositorio usa seis grupos de inventario definidos e um grupo gerado em tempo de execucao:

- `ipa_servers`
- `proxmox_primary`
- `linux_ipa_clients`
- `linux_ipa_clients_runtime`
- `windows_qemu_guest_agent_clients`
- `windows_management_clients`
- `windows_freeipa_helper_clients`

Voce tambem pode definir seus proprios grupos extras de inventario e referenci-los em definicoes de hostgroup do FreeIPA. Se voce quiser usar o conjunto completo de convidados Linux preparados no lado de hostgroups do FreeIPA, referencie o grupo `linux_ipa_clients_runtime`.

> [!IMPORTANT]
> O FreeIPA ainda precisa do hostname final de cada convidado. Se voce usa alvos somente por IP ou descoberta via Proxmox, forneca `ipa_hostname` explicitamente ou garanta que `hostname -f` dentro do convidado retorne o FQDN final. Os playbooks agora resolvem esse hostname antes de montar a associacao em hostgroups do FreeIPA.

> [!TIP]
> Nao faca enrollment de um template golden reutilizavel diretamente no FreeIPA. Primeiro clone a VM, atribua o hostname final e so depois faca o enrollment do convidado resultante.

### Modos de origem para convidados Linux

Voce pode alimentar `linux_ipa_clients` de tres maneiras diferentes.

#### 1. Hosts estaticos no inventario

Se voce ja conhece os nomes dos convidados, use entradas normais de inventario Ansible:

```yaml
linux_ipa_clients:
  hosts:
    rocky-app-01.example.com:
      ansible_host: 192.0.2.101
    ubuntu-jump-01.example.com:
      ansible_host: 192.0.2.102
```

#### 2. Definicoes manuais de host em variaveis

Use `linux_ipa_client_hosts` quando quiser manter os convidados fora de `hosts.yml` ou quando tudo que voce tiver for um IP:

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

- se `name` ja for um hostname resolvivel ou um FQDN, `ansible_host` e opcional
- se voce so conhecer o IP, use qualquer alias estavel em `name`
- quando `ipa_hostname` for omitido, o playbook cai de volta para `hostname -f` dentro do convidado

#### 3. Auto-descoberta de VMs no Proxmox

Use discovery quando quiser que o playbook busque convidados Linux a partir de um ou mais nos Proxmox:

```yaml
linux_ipa_proxmox_discovery_enabled: true
linux_ipa_proxmox_discovery_nodes:
  - pve01.example.com
linux_ipa_proxmox_discovery_only_running: true
linux_ipa_proxmox_discovery_skip_missing_ip: true
linux_ipa_proxmox_discovery_ip_preference: ipv4
# Opcional: restrinja a automacao dirigida por discovery apenas aos convidados
# explicitamente aprovados.
# linux_ipa_proxmox_discovery_allowlist_enabled: true
# linux_ipa_proxmox_discovery_allowlist_vmids:
#   - 101
#   - 102
# linux_ipa_proxmox_discovery_allowlist_ips:
#   - 192.0.2.101
# linux_ipa_proxmox_discovery_allowlist_names:
#   - rocky-app-01.example.com
#   - proxmox-pve01-vm101
# Opcional: sempre exclua convidados de infraestrutura ou sensiveis mesmo quando
# a descoberta ampla do no estiver habilitada.
# linux_ipa_proxmox_discovery_blacklist_vmids:
#   - 900
# linux_ipa_proxmox_discovery_blacklist_names:
#   - mikrotik-edge-01
#   - bind-dns-01
# Configuracoes opcionais de SSH para primeiro contato quando o guest agent
# ainda nao estiver em execucao e o repositorio precisar entrar por SSH para
# instala-lo.
# linux_ipa_proxmox_discovery_ansible_user: ubuntu
# linux_ipa_proxmox_discovery_ansible_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
# linux_ipa_proxmox_discovery_ansible_ssh_private_key_file: /home/automation/.ssh/id_ed25519
# linux_ipa_proxmox_discovery_ansible_become: true
# linux_ipa_proxmox_discovery_ansible_become_method: sudo
# linux_ipa_proxmox_discovery_ansible_become_password: "{{ vault_linux_ipa_ssh_bootstrap_password }}"
```

Notas:

- a discovery adiciona as VMs ao mesmo grupo `linux_ipa_clients_runtime` usado pelo restante dos playbooks
- a descoberta de IP depende de o QEMU guest agent relatar interfaces de rede
- `linux_ipa_proxmox_discovery_use_vm_name_as_hint` so confia em nomes de VM que ja sejam FQDNs
- defina `linux_ipa_proxmox_discovery_complete_short_vm_names_with_suffix: true` quando voce tambem quiser promover automaticamente nomes curtos e seguros do Proxmox, como `Teleport-Server-1`, para hints de hostname como `teleport-server-1.example.com` por meio de `linux_ipa_identity_hostname_suffix`
- `linux_ipa_proxmox_discovery_vmids` e opcional e e usado principalmente pelo workflow dirigido por hook ou webhook para limitar a discovery a um ou mais VMIDs especificos
- o convidado ainda precisa de um hostname final, ja configurado dentro da VM ou fornecido com `ipa_hostname` por uma definicao manual
- o hostname real do sistema do convidado tambem precisa ser valido para o enrollment; valores de placeholder, como `localhost.localdomain`, devem ser substituidos na VM antes de executar `linux-clients` ou `site`
- quando os convidados usam hostnames curtos, como `app-server-01`, voce pode definir `linux_ipa_identity_hostname_suffix` e opcionalmente `linux_freeipa_enroll_manage_hostname: true` para que o projeto resolva e aplique um hostname completo, como `app-server-01.example.net`, antes do enrollment
- quando o DNS do FreeIPA e autoritativo para os hostnames dos convidados, voce pode definir `linux_freeipa_enroll_manage_authoritative_dns: true` para que o projeto repare os registros A e PTR do convidado e remova registros AAAA link-local `fe80::/10` antes do enrollment
- quando o DNS ainda nao estiver pronto, voce pode definir `linux_ipa_manage_etc_hosts: true` e fornecer `linux_ipa_etc_hosts_entries` para que o role adicione um bloco bootstrap gerenciado em `/etc/hosts` para servidores IPA e FQDNs dos convidados antes das verificacoes de enrollment
- `guest_qemu_agent_install_enabled` instala o QEMU Guest Agent em convidados que ja estao acessiveis via SSH ou WinRM, tenta novamente em convidados Linux que ficam acessiveis mais tarde no mesmo workflow e tenta de novo apos o enrollment Linux, para que workflows futuros dependentes do agent no Proxmox possam usa-lo
- defina `linux_ipa_proxmox_discovery_allowlist_enabled: true` quando quiser manter a discovery ligada, mas permitir que apenas um subconjunto estritamente aprovado de convidados entre no inventario runtime Linux; a allowlist pode casar VMIDs, IPs e nomes exatos
- defina `linux_ipa_proxmox_discovery_blacklist_vmids`, `linux_ipa_proxmox_discovery_blacklist_ips` ou `linux_ipa_proxmox_discovery_blacklist_names` quando os nos com discovery tambem hospedarem VMs de infraestrutura, como firewalls ou servidores DNS, que nunca devem receber automacao Linux IPA; os acertos da blacklist sempre vencem a admissao via discovery ampla ou allowlist
- para convidados Linux descobertos no Proxmox que ainda nao tenham um guest agent funcional, defina `linux_ipa_proxmox_discovery_ansible_user` e tambem `linux_ipa_proxmox_discovery_ansible_password` ou `linux_ipa_proxmox_discovery_ansible_ssh_private_key_file`, para que o repositorio tenha um caminho SSH utilizavel de primeiro contato e possa instalar o QEMU Guest Agent
- quando esses convidados descobertos usarem um usuario SSH nao root, defina tambem `linux_ipa_proxmox_discovery_ansible_become`, `linux_ipa_proxmox_discovery_ansible_become_method` e `linux_ipa_proxmox_discovery_ansible_become_password`, a menos que essa conta ja tenha `sudo` sem senha
- `guest_qemu_agent_install_manage_proxmox_vm_agent` tambem habilita a comunicacao do guest agent no lado Proxmox (`qm set <vmid> --agent 1`) para convidados Linux apoiados pelo Proxmox antes que a instalacao do lado do convidado seja executada
- quando essa opcao da VM do Proxmox muda em uma VM em execucao, o repositorio apenas avisa por padrao, porque o Proxmox pode exigir um novo boot da VM antes de o host conseguir usar o canal do guest agent; defina `guest_qemu_agent_install_reboot_after_proxmox_vm_agent_enable: true` se quiser que o repositorio reinicie essas VMs automaticamente
- `linux_ipa_ssh_host_key_policy` usa `accept_new` por padrao para conexoes a convidados Linux, permitindo contato com VMs recem-descobertas sem desligar totalmente a verificacao de host key; host keys alteradas ainda falham e exigem revisao do operador
- `linux_ipa_qga_ssh_bootstrap_enabled` e o caminho de bootstrap sem reboot preferido para convidados apoiados pelo Proxmox porque consegue criar um usuario de automacao dedicado e somente com chave pelo QEMU Guest Agent antes de existir qualquer login SSH
- `linux_ipa_qga_ssh_bootstrap_qm_path` usa `qm` por padrao, e o fluxo de bootstrap tambem sonda caminhos alternativos comuns no no Proxmox antes de falhar
- convidados que aceitam `guest-ping` mas rejeitam `guest-exec` sao pulados por padrao durante o bootstrap QGA; mantenha outro caminho SSH disponivel para eles ou defina `linux_ipa_qga_ssh_bootstrap_fail_on_guest_exec_blocked: true` para falhar rapido
- `linux_ipa_ssh_bootstrap_enabled` instala opcionalmente a chave publica SSH do controlador nos convidados Linux antes da resolucao de hostname e do enrollment; `linux_ipa_ssh_bootstrap_password` tambem e usado como fallback de senha compartilhada de primeiro contato para convidados runtime Linux mesmo quando o bootstrap por chave esta desativado
- o enrollment Linux em IPA repete joins de cliente upstream que falham com timeout JSON-RPC do FreeIPA e expoe `linux_ipaclient_kinit_attempts` para ambientes IPA mais lentos ou ocupados
- o enrollment Linux em IPA tambem mescla por padrao os hostnames do inventario `ipa_servers` na lista de servidores de join, para que os clientes possam usar o conjunto completo de servidores IPA em vez de um unico endpoint configurado
- quando mais de um servidor IPA esta disponivel, cada rodada de retry tenta esses candidatos de servidor IPA um de cada vez durante o enrollment do cliente Linux
- o workflow combinado `site` cria primeiro os hostgroups do FreeIPA, depois adiciona os hosts runtime ja enrolled, de modo que execucoes pre-enrollment nao falhem na etapa de associacao a hostgroup por causa de convidados ainda nao enrolled

## Superficie de configuracao

As principais configuracoes ficam em:

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

Para o detalhamento arquivo a arquivo, veja [docs/VARIABLES.md](../VARIABLES.md).

Principais familias de variaveis:

| Area | Variaveis |
| --- | --- |
| Modelo de acesso FreeIPA | `freeipa_user_groups`, `freeipa_hostgroups`, `freeipa_hbac_rules`, `freeipa_sudo_rules` |
| Controles de rollout | `freeipa_access_serial`, `freeipa_access_max_fail_percentage`, `proxmox_rollout_serial`, `proxmox_rollout_max_fail_percentage`, `linux_freeipa_enroll_serial`, `linux_freeipa_enroll_max_fail_percentage`, `windows_management_serial`, `windows_management_max_fail_percentage` |
| LDAP realm do Proxmox | `proxmox_ldap_realm_id`, `proxmox_ldap_server1`, `proxmox_ldap_base_dn`, `proxmox_ldap_group_dn`, `proxmox_ldap_bind_dn`, `proxmox_ldap_bind_password`, `proxmox_ldap_sync_attributes`, `proxmox_ldap_sync_defaults` |
| RBAC do Proxmox | `proxmox_custom_roles`, `proxmox_acl_bindings` |
| Enrollment Linux em IPA | `ipaclient_domain`, `ipaclient_realm`, `linux_ipa_servers`, `linux_ipaclient_mkhomedir`, `linux_ipasssd_permit`, `linux_sssd_refresh_enabled`, `guest_qemu_agent_install_*`, `linux_ipa_client_hosts`, `linux_ipa_qga_ssh_bootstrap_*`, `linux_ipa_ssh_bootstrap_*`, `linux_ipa_proxmox_discovery_*` |
| Relatorio de readiness Linux | `linux_readiness_report_*` |
| Gerenciamento Windows | `windows_domain_membership_*`, `windows_domain_membership_enabled`, `windows_management_clients` |
| Helpers Windows FreeIPA | `windows_freeipa_helpers_*`, `windows_freeipa_helpers_enabled`, `windows_freeipa_helper_clients` |
| Segredos de conexao Ansible | `vault_proxmox_become_password`, `vault_windows_admin_password`, `vault_windows_domain_admin_password` |

## Exemplo de estrategia de grupos

Um padrao simples que escala bem:

- grupo de usuarios FreeIPA `proxmox-admins`
- grupo de usuarios FreeIPA `linux-ssh-admins`
- hostgroup FreeIPA `linux-all`
- regra HBAC `allow-linux-ssh-admins`
- regra sudo `allow-linux-ssh-admins-sudo`
- binding ACL do Proxmox para o grupo sincronizado `proxmox-admins-ipa`

Preencha `freeipa_linux_admin_users` em [`inventories/production/group_vars/all/20-freeipa.yml`](../../inventories/production/group_vars/all/20-freeipa.yml) quando voce quiser que a execucao combinada de `site.yml` conceda automaticamente a usuarios IPA especificos acesso Linux por SSH e sudo por meio do grupo gerenciado `linux-ssh-admins`.

Lembre-se de que a sincronizacao LDAP do Proxmox cria grupos sincronizados com o sufixo:

```text
<group-name>-<realm>
```

Se o seu grupo FreeIPA for `proxmox-admins` e o realm do Proxmox for `ipa`, o grupo PVE sincronizado resultante sera:

```text
proxmox-admins-ipa
```

## Seguranca

- armazene todos os segredos em `vault-freeipa.yml` e `vault-proxmox.yml`, e nao em arquivos de variaveis de inventario em texto claro
- prefira uma conta LDAP bind dedicada e somente leitura para o Proxmox
- prefira TLS com verificacao de certificado habilitada
- mantenha o SSH host key checking habilitado fora de laboratorios descartaveis
- prefira `linux_ipa_qga_ssh_bootstrap_enabled` a senhas temporarias compartilhadas quando seus convidados Proxmox ja tiverem um QEMU Guest Agent funcional
- use `guest_qemu_agent_install_enabled` apenas quando o repositorio ja tiver um caminho valido de gerenciamento para dentro do convidado; para discovery no Proxmox isso significa que o QGA ja esta em execucao ou que `linux_ipa_proxmox_discovery_ansible_user` mais senha ou acesso por chave ja foram configurados
- se voce habilitar o bootstrap SSH Linux, guarde qualquer senha bootstrap compartilhada em variaveis sob vault e troque ou remova essa senha assim que o acesso por chave estiver estabelecido
- nao reutilize a conta admin do IPA como conta LDAP bind do Proxmox
- revise `proxmox_ldap_filter` e `proxmox_ldap_group_filter` antes do rollout em producao para evitar importar objetos em excesso

Para um laboratorio descartavel em que voce queira explicitamente ignorar a verificacao de host key do SSH, desabilite isso por sessao de shell em vez de alterar os defaults do repositorio:

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

```powershell
$env:ANSIBLE_HOST_KEY_CHECKING = 'False'
```

## Idempotencia e observacoes

Este projeto foi escrito para ser reutilizavel e em grande parte idempotente, mas ainda assim deve ser testado em laboratorio antes do rollout em producao.

Observacoes conhecidas:

- a saida do CLI do Proxmox pode variar levemente entre versoes
- o layout de diretorio do FreeIPA e flexivel, entao filtros LDAP podem precisar de ajuste para a sua arvore
- ACLs e roles do PVE mantidos manualmente devem ser comparados antes de aplicar automacao sobre eles
- a auto-descoberta de VMs no Proxmox depende de convidados em execucao e de dados de rede do QEMU guest agent
- definicoes de convidados somente por IP ainda exigem um hostname final valido dentro do convidado ou um `ipa_hostname` explicito
- os plays do Proxmox rodam com privilege escalation, entao um usuario SSH nao root precisa ter `sudo` funcional e voce deve fornecer uma senha become com `-K`, a menos que esse usuario tenha `sudo` sem senha
- se voce armazenar `ansible_become_password` em `vault-proxmox.yml`, podera pular `-K` porque o Ansible lera a senha de sudo a partir da variavel criptografada

## Verificacao

Apos um rollout bem-sucedido, valide o estado final em vez de assumir que todos os caminhos de acesso estao corretos.

### No FreeIPA

- confirme que os grupos de usuarios esperados existem
- confirme que os hostgroups esperados existem
- confirme que as regras HBAC esperadas existem e estao habilitadas
- confirme que as regras `sudo` esperadas existem e estao habilitadas

### No Proxmox

- confirme que o LDAP realm existe
- confirme que a sincronizacao inicial importou os usuarios ou grupos esperados
- confirme que o grupo sincronizado pretendido recebeu o binding ACL esperado

### Em um convidado Linux

- confirme que um usuario IPA permitido consegue fazer login
- confirme que um usuario nao permitido e bloqueado por HBAC
- confirme que um administrador IPA permitido consegue executar `sudo -l`
- confirme que um diretorio home e criado no primeiro login se `linux_ipaclient_mkhomedir` estiver habilitado

## Layout do repositorio

<details>
<summary>Mostrar o layout do repositorio</summary>

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

## Desenvolvimento

Os principais arquivos auxiliares incluidos no repositorio sao:

- `.editorconfig`, para manter defaults consistentes de espacos, encoding e fim de linha entre editores
- `.gitattributes`, para fixar arquivos de texto comuns em finais de linha `LF`
- `.gitignore`, para impedir que inventarios gerados, dados de vault, collections locais e lixo de editor entrem no Git
- `.ansible-lint`, para excluir caminhos de collections vendorizadas e suprimir apenas a regra de comprimento de linha YAML
- `.yamllint`, para manter a validacao YAML consistente em playbooks, inventarios e workflows
- `.github/CODEOWNERS`, para direcionar ownership de revisao nas principais areas do repositorio
- `.github/workflows/ci.yml`, para executar validacoes de lint e smoke em eventos de push e pull request
- `.pre-commit-config.yaml`, para rodar o hook rapido de lint antes do commit quando `pre-commit` estiver instalado
- `CHANGELOG.md`, para registrar em um unico lugar as mudancas relevantes do repositorio
- `docs/VARIABLES.md`, para explicar a estrutura dividida de variaveis de inventario
- `docs/i18n/`, para hospedar os READMEs traduzidos; eles devem espelhar a estrutura completa de secoes do `README.md` em ingles
- `docs/i18n/TRANSLATION_GUIDE.md`, para explicar como manter os READMEs traduzidos sincronizados
- `scripts/bootstrap.ps1` e `scripts/bootstrap.sh`, para instalar a collection necessaria no caminho local `collections/` e aplicar o patch de compatibilidade para ansible-core 2.24+
- `scripts/patch_freeipa_collection.py`, para reescrever imports obsoletos dentro da collection FreeIPA fixada e preservar compatibilidade com versoes futuras do ansible-core
- `scripts/lint.py`, para fornecer um ponto de entrada de lint multiplataforma usado localmente, no CI e no pre-commit
- `scripts/smoke-test.py`, para executar validacao de inventario de exemplo e checagens de sintaxe sem tocar infraestrutura real, incluindo cobertura do playbook Windows separado
- `scripts/check_translations.py`, para auditar os READMEs traduzidos quanto a metadados, paridade de estrutura de secoes e cobertura minima de conteudo em relacao ao README canonico em ingles
- `scripts/lint.ps1` e `scripts/lint.sh`, para agrupar o workflow local de lint e smoke
- `scripts/proxmox_event_webhook.py`, para servir como webhook opcional no lado do controlador para eventos de VM do Proxmox
- `scripts/proxmox-vm-hook.pl`, para atuar como hook opcional de VM instalado nos nos do Proxmox
- `scripts/run-playbook.ps1`, para fornecer um wrapper consistente de `ansible-playbook` em ambientes Windows e PowerShell
- `scripts/vault.ps1` e `scripts/vault.sh`, para ajudar a criar, editar, visualizar e criptografar arquivos de vault separados por dominio
- `tests/README.md` e `tests/smoke/README.md`, para documentar convencoes de teste e smoke do repositorio

```bash
ansible-lint
python scripts/smoke-test.py
python scripts/check_translations.py
./scripts/lint.sh
```

```powershell
python .\scripts\smoke-test.py
python .\scripts\check_translations.py
.\scripts\lint.ps1
```

## Proximas extensoes

Extensoes comuns que fazem sentido depois:

- pipeline Packer para templates Linux ja preparados para IPA
- templates de job e agendamento no AWX ou Automation Controller para rollouts unificados
- modelos mais fortes de tenant e pool no Proxmox
- workflows de AD trust para Windows RDP ou ambientes de identidade hibrida

## Licenca

Publicado sob a [0BSD License](../../LICENSE).
