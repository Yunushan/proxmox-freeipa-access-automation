$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

ansible-galaxy collection install -r requirements.yml

Write-Output 'Collections installed successfully.'
