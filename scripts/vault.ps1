[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('encrypt', 'decrypt', 'view')]
    [string]$Action,

    [ValidateSet('freeipa', 'proxmox', 'windows', 'all')]
    [string[]]$Domain = @('all'),

    [string]$Environment = 'production',
    [string]$FreeipaVaultId = 'freeipa@prompt',
    [string]$ProxmoxVaultId = 'proxmox@prompt',
    [string]$WindowsVaultId = 'windows@prompt'
)

$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

if (-not (Get-Command ansible-vault -ErrorAction SilentlyContinue)) {
    throw 'ansible-vault was not found in PATH.'
}

function Format-CommandArgument {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    if ($Value -notmatch '[\s"]') {
        return $Value
    }

    return '"' + $Value.Replace('"', '\"') + '"'
}

function Test-VaultEncrypted {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }

    $FirstLine = Get-Content -LiteralPath $Path -TotalCount 1 -ErrorAction Stop
    return $FirstLine -like '$ANSIBLE_VAULT*'
}

$DomainMap = @{
    freeipa = @{
        Path        = "inventories/$Environment/group_vars/all/vault-freeipa.yml"
        ExamplePath = "inventories/$Environment/group_vars/all/vault-freeipa.yml.example"
        VaultId     = $FreeipaVaultId
    }
    proxmox = @{
        Path        = "inventories/$Environment/group_vars/all/vault-proxmox.yml"
        ExamplePath = "inventories/$Environment/group_vars/all/vault-proxmox.yml.example"
        VaultId     = $ProxmoxVaultId
    }
    windows = @{
        Path        = "inventories/$Environment/group_vars/all/vault-windows.yml"
        ExamplePath = "inventories/$Environment/group_vars/all/vault-windows.yml.example"
        VaultId     = $WindowsVaultId
    }
}

$DomainsToProcess = if ($Domain -contains 'all') {
    @('freeipa', 'proxmox', 'windows')
}
else {
    $Domain
}

foreach ($CurrentDomain in $DomainsToProcess) {
    $CurrentConfig = $DomainMap[$CurrentDomain]
    $VaultPath = $CurrentConfig.Path
    $VaultExamplePath = $CurrentConfig.ExamplePath
    $VaultIdSpec = $CurrentConfig.VaultId

    if ($Action -eq 'encrypt' -and -not (Test-Path -LiteralPath $VaultPath)) {
        if (-not (Test-Path -LiteralPath $VaultExamplePath)) {
            throw "Vault example file does not exist: $VaultExamplePath"
        }

        Copy-Item -LiteralPath $VaultExamplePath -Destination $VaultPath -Force
    }

    if (-not (Test-Path -LiteralPath $VaultPath)) {
        throw "Vault file does not exist: $VaultPath"
    }

    $IsEncrypted = Test-VaultEncrypted -Path $VaultPath

    if ($Action -eq 'encrypt' -and $IsEncrypted) {
        Write-Output "Skipping already encrypted $CurrentDomain vault: $VaultPath"
        continue
    }

    if ($Action -eq 'decrypt' -and -not $IsEncrypted) {
        Write-Output "Skipping plaintext $CurrentDomain vault: $VaultPath"
        continue
    }

    if ($Action -eq 'view' -and -not $IsEncrypted) {
        Write-Output "Contents of plaintext $CurrentDomain vault: $VaultPath"
        Get-Content -LiteralPath $VaultPath
        continue
    }

    $CommandArgs = @($Action, '--vault-id', $VaultIdSpec, $VaultPath)
    Write-Output ("Running: ansible-vault " + (($CommandArgs | ForEach-Object { Format-CommandArgument -Value $_ }) -join ' '))
    & ansible-vault @CommandArgs
}
