$ErrorActionPreference = 'Stop'

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonExe = 'python'
    $PythonArgs = @()
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonExe = 'py'
    $PythonArgs = @('-3')
}
else {
    throw 'python or py was not found in PATH.'
}

Write-Output ("Running: " + (($PythonArgs + @('scripts/lint.py')) -join ' ').Insert(0, "$PythonExe "))
& $PythonExe @PythonArgs 'scripts/lint.py'

Write-Output ("Running: " + (($PythonArgs + @('scripts/smoke-test.py')) -join ' ').Insert(0, "$PythonExe "))
& $PythonExe @PythonArgs 'scripts/smoke-test.py'
