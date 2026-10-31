[CmdletBinding()]
param([Parameter(Mandatory=$true)][string[]]$Roots, [Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$rgCommand = (Get-Command rg -ErrorAction Stop).Source
$outputRoot = [IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $outputRoot) { throw 'Choose a new private output directory; prior audit files are preserved.' }
[IO.Directory]::CreateDirectory($outputRoot) | Out-Null
$names = @('SKILL.md','AGENTS.md','AGENTS.override.md','CLAUDE.md','GEMINI.md','.goosehints','.cursorrules','*.instructions.md','.mcp.json','mcp.json','skills-lock.json','.skill-lock.json')
$statuses = @()
$index = 0
foreach ($root in $Roots) {
    $index++
    $fullRoot = [IO.Path]::GetFullPath($root)
    $label = if ($fullRoot -match '^([A-Za-z]):[\\/]$') { $Matches[1].ToUpperInvariant() } else { "root$index" }
    $argsList = @('--files','--hidden','--no-ignore')
    foreach ($name in $names) { $argsList += @('--glob',$name) }
    $argsList += $fullRoot
    $start = Get-Date
    # ripgrep exit 2 reports partial traversal; preserve diagnostics and continue other roots.
    $ErrorActionPreference = 'Continue'
    & $rgCommand @argsList 1> (Join-Path $outputRoot "$label-paths.txt") 2> (Join-Path $outputRoot "$label-errors.txt")
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    $status = [ordered]@{drive=$label;root=$fullRoot;exit_code=$exitCode;matches=@(Get-Content -LiteralPath (Join-Path $outputRoot "$label-paths.txt")).Count;error_lines=@(Get-Content -LiteralPath (Join-Path $outputRoot "$label-errors.txt")).Count;seconds=[Math]::Round(((Get-Date)-$start).TotalSeconds,1)}
    $status | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $outputRoot "$label-status.json") -Encoding utf8
    $statuses += $status
    Write-Host "$label : $($status.matches) matches, $($status.error_lines) diagnostic lines."
}
$statuses | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $outputRoot 'scan-status.json') -Encoding utf8
Write-Host "Private discovery saved to $outputRoot. Audit it with scripts/audit-local.py --discovery."
