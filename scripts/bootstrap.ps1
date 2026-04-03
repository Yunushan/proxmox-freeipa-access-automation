$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

$CollectionPath = Join-Path $RootDir 'collections'

ansible-galaxy collection install -r requirements.yml -p $CollectionPath
python .\scripts\patch_freeipa_collection.py

Write-Output 'Collections installed and patched successfully.'
