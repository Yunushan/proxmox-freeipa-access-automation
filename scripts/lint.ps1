$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

$RequiredCommands = @('ansible-lint', 'yamllint', 'ansible-playbook')
foreach ($Command in $RequiredCommands) {
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        throw "$Command was not found in PATH."
    }
}

$LintInventoryRoot = Join-Path $RootDir '.ansible\lint-inventory'
$LintInventoryGroupVars = Join-Path $LintInventoryRoot 'group_vars\all'
$LintInventoryFile = Join-Path $LintInventoryRoot 'hosts.yml'

New-Item -ItemType Directory -Force -Path $LintInventoryGroupVars | Out-Null
Copy-Item 'inventories\production\hosts.yml.example' $LintInventoryFile -Force
Copy-Item 'inventories\production\group_vars\all\main.yml' (Join-Path $LintInventoryGroupVars 'main.yml') -Force
Copy-Item 'inventories\production\group_vars\all\vault.yml.example' (Join-Path $LintInventoryGroupVars 'vault.yml') -Force

$PreviousInventory = $env:ANSIBLE_INVENTORY
$env:ANSIBLE_INVENTORY = $LintInventoryFile

try {
    Write-Output 'Running: ansible-lint'
    & ansible-lint

    Write-Output 'Running: yamllint .'
    & yamllint .

    $Playbooks = @(
        'playbooks/freeipa.yml',
        'playbooks/proxmox.yml',
        'playbooks/linux-clients.yml',
        'playbooks/site.yml',
        'playbooks/validate.yml'
    )

    foreach ($Playbook in $Playbooks) {
        Write-Output "Running: ansible-playbook --syntax-check -i $LintInventoryFile $Playbook"
        & ansible-playbook --syntax-check -i $LintInventoryFile $Playbook
    }
}
finally {
    if ($null -eq $PreviousInventory) {
        Remove-Item Env:ANSIBLE_INVENTORY -ErrorAction SilentlyContinue
    }
    else {
        $env:ANSIBLE_INVENTORY = $PreviousInventory
    }

    if (Test-Path $LintInventoryRoot) {
        Remove-Item -Recurse -Force $LintInventoryRoot
    }
}
