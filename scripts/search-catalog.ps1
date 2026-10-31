param([string]$Query='', [string]$Category='', [string]$Technology='', [string]$ProjectType='', [string]$Compatibility='')
$catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot '../manifests/catalog.json') -Raw | ConvertFrom-Json
$catalog.skills | Where-Object {
    (-not $Query -or ($_.id + ' ' + $_.description).IndexOf($Query,[StringComparison]::OrdinalIgnoreCase) -ge 0) -and
    (-not $Category -or $_.category -eq $Category) -and
    (-not $Technology -or $Technology -in $_.technologies) -and
    (-not $ProjectType -or $ProjectType -in $_.projectTypes) -and
    (-not $Compatibility -or $Compatibility -in $_.compatibility)
} | Select-Object id,category,description
