param(
  [Parameter(Mandatory = $true)]
  [string]$Root,
  [switch]$SkipDbmlCompile
)

$ErrorActionPreference = 'Stop'
$rootPath = (Resolve-Path -LiteralPath $Root).Path
$validator = Join-Path $rootPath 'skills\figma-to-ocl-specs\scripts\validate_specs.ps1'

if (-not (Test-Path -LiteralPath $validator)) {
  throw "Repository validator not found: $validator"
}

$forbiddenRootArtifacts = @(
  'FIGMA.md',
  'CONTEXT.md',
  'ASSUMPTIONS.md',
  'coverage-report.md',
  'schema.dbml',
  'uc',
  'api'
)

foreach ($name in $forbiddenRootArtifacts) {
  $candidate = Join-Path $rootPath $name
  if (Test-Path -LiteralPath $candidate) {
    throw "Specification artifact must be inside a Figma package, not repository root: $candidate"
  }
}

$packages = @(Get-ChildItem -LiteralPath $rootPath -Directory |
  Where-Object {
    $_.Name -ne 'skills' -and
    (Test-Path -LiteralPath (Join-Path $_.FullName 'FIGMA.md'))
  })

if ($packages.Count -eq 0) {
  throw 'No Figma specification packages found.'
}

foreach ($package in $packages) {
  Write-Output "Validating package: $($package.Name)"
  & $validator -Root $package.FullName -SkipDbmlCompile:$SkipDbmlCompile
  if (-not $?) {
    throw "Validation failed for package: $($package.Name)"
  }
}

Write-Output "PASS: $($packages.Count) Figma specification package(s)."
