[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('validate', 'site', 'freeipa', 'proxmox', 'linux-clients')]
    [string]$Playbook,

    [string]$Inventory = 'inventories/production/hosts.yml',
    [switch]$AskVaultPass,
    [string[]]$VaultId,
    [switch]$AskBecomePass,
    [switch]$Check,
    [switch]$Diff,
    [switch]$SyntaxCheck,
    [string]$Limit,
    [string[]]$Tags,
    [string[]]$SkipTags,
    [string[]]$ExtraVars,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs
)

$ErrorActionPreference = 'Stop'

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

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python .\scripts\patch_freeipa_collection.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 .\scripts\patch_freeipa_collection.py
} else {
    throw 'python was not found in PATH.'
}

if (-not (Get-Command ansible-playbook -ErrorAction SilentlyContinue)) {
    throw 'ansible-playbook was not found in PATH.'
}

$PlaybookMap = @{
    validate        = 'playbooks/validate.yml'
    site            = 'playbooks/site.yml'
    freeipa         = 'playbooks/freeipa.yml'
    proxmox         = 'playbooks/proxmox.yml'
    'linux-clients' = 'playbooks/linux-clients.yml'
}

$PlaybookPath = $PlaybookMap[$Playbook]
if (-not (Test-Path -LiteralPath $PlaybookPath)) {
    throw "Playbook path does not exist: $PlaybookPath"
}

if (-not (Test-Path -LiteralPath $Inventory)) {
    throw "Inventory path does not exist: $Inventory"
}

$CommandArgs = @(
    '-i'
    $Inventory
    $PlaybookPath
)

if ($SyntaxCheck) {
    $CommandArgs += '--syntax-check'
}

if ($Check) {
    $CommandArgs += '--check'
}

if ($Diff) {
    $CommandArgs += '--diff'
}

if ($AskVaultPass) {
    if ($VaultId) {
        throw 'Use either -AskVaultPass or -VaultId, not both.'
    }

    $CommandArgs += '--ask-vault-pass'
}

if ($VaultId) {
    foreach ($VaultIdentity in $VaultId) {
        $CommandArgs += '--vault-id'
        $CommandArgs += $VaultIdentity
    }
}

if ($AskBecomePass) {
    $CommandArgs += '--ask-become-pass'
}

if ($Limit) {
    $CommandArgs += '--limit'
    $CommandArgs += $Limit
}

if ($Tags) {
    $CommandArgs += '--tags'
    $CommandArgs += ($Tags -join ',')
}

if ($SkipTags) {
    $CommandArgs += '--skip-tags'
    $CommandArgs += ($SkipTags -join ',')
}

if ($ExtraVars) {
    foreach ($ExtraVar in $ExtraVars) {
        $CommandArgs += '--extra-vars'
        $CommandArgs += $ExtraVar
    }
}

if ($ExtraArgs) {
    $CommandArgs += $ExtraArgs
}

Write-Output ("Running: ansible-playbook " + (($CommandArgs | ForEach-Object { Format-CommandArgument -Value $_ }) -join ' '))
& ansible-playbook @CommandArgs
