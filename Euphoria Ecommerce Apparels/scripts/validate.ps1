param()
$ErrorActionPreference = 'Stop'
$packagePath = Split-Path -Parent $PSScriptRoot
$repositoryPath = Split-Path -Parent $packagePath
$specValidator = Join-Path $repositoryPath 'skills\figma-to-ocl-specs\scripts\validate_specs.ps1'
$repositoryValidator = Join-Path $repositoryPath 'skills\figma-to-ocl-specs\scripts\validate_repository.ps1'

& $specValidator -Root $packagePath
if (-not $?) { exit 1 }
& $repositoryValidator -Root $repositoryPath
if (-not $?) { exit 1 }
python (Join-Path $PSScriptRoot 'check_consistency.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
