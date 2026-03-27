[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('validate', 'site', 'freeipa', 'proxmox', 'linux-clients')]
    [string]$Playbook,

    [switch]$AskVaultPass,
    [switch]$Check,
    [switch]$Diff,
    [switch]$SyntaxCheck,
    [string]$Limit,
    [string[]]$ExtraArgs
)

$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

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

$CommandArgs = @($PlaybookMap[$Playbook])

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
    $CommandArgs += '--ask-vault-pass'
}

if ($Limit) {
    $CommandArgs += '--limit'
    $CommandArgs += $Limit
}

if ($ExtraArgs) {
    $CommandArgs += $ExtraArgs
}

Write-Output ("Running: ansible-playbook " + ($CommandArgs -join ' '))
& ansible-playbook @CommandArgs
