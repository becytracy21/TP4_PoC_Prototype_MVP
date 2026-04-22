param(
  [string]$HostName = 'yachtracingresults.yrr',
  [string]$Ip = '127.0.0.1',
  [switch]$NoStartCaddy
)

$ErrorActionPreference = 'Stop'

# Assure un affichage correct des accents dans la console
try {
  [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
} catch {}

function Test-Admin {
  $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
  $principal = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
  return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Auto-élévation : si pas admin, relance le script en admin puis quitte
if (-not (Test-Admin)) {
  $argsList = @(
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-File', ('"' + $PSCommandPath + '"'),
    '-HostName', ('"' + $HostName + '"'),
    '-Ip', ('"' + $Ip + '"')
  )

  Start-Process -FilePath 'powershell.exe' -Verb RunAs -ArgumentList ($argsList -join ' ')
  exit 0
}

$hostsPath = Join-Path $env:WINDIR 'System32\drivers\etc\hosts'

if (-not (Test-Path $hostsPath)) {
  throw "Fichier hosts introuvable : $hostsPath"
}

$tabIndent = "`t"
$desiredLine = "$tabIndent$Ip$tabIndent$HostName"

# Matche une entrée (commentée ou non) pour ce HostName
$entryRegex = "^\s*#?\s*\d{1,3}(?:\.\d{1,3}){3}\s+" + [Regex]::Escape($HostName) + "(?:\s+#.*)?\s*$"

$lines = Get-Content -Path $hostsPath -Encoding UTF8

$updatedLines = New-Object System.Collections.Generic.List[string]
$replaced = $false

foreach ($line in $lines) {
  if ($line -match $entryRegex) {
    if (-not $replaced) {
      $updatedLines.Add($desiredLine)
      $replaced = $true
    }
    continue
  }

  $updatedLines.Add($line)
}

if (-not $replaced) {
  # Insère juste après la ligne '#\t127.0.0.1       localhost' si trouvée,
  # sinon en fin de fichier (avec une ligne vide si nécessaire)
  $insertAfterRegex = '^\s*#\s*127\.0\.0\.1\s+localhost\s*$'
  $insertIndex = -1
  for ($i = 0; $i -lt $updatedLines.Count; $i++) {
    if ($updatedLines[$i] -match $insertAfterRegex) {
      $insertIndex = $i + 1
      break
    }
  }

  if ($insertIndex -ge 0) {
    $updatedLines.Insert($insertIndex, $desiredLine)
  } else {
    if ($updatedLines.Count -gt 0 -and $updatedLines[$updatedLines.Count - 1].Trim().Length -ne 0) {
      $updatedLines.Add('')
    }
    $updatedLines.Add($desiredLine)
  }
}

# Nettoyage: supprime les lignes vides en trop en fin de fichier
while ($updatedLines.Count -gt 0 -and $updatedLines[$updatedLines.Count - 1].Trim().Length -eq 0) {
  $updatedLines.RemoveAt($updatedLines.Count - 1)
}

Set-Content -Path $hostsPath -Value $updatedLines -Encoding UTF8

# Messages sans dépendre de l'encodage de la console (accents) :
$okMsg = "OK : entr" + [char]0x00E9 + "e hosts configur" + [char]0x00E9 + "e -> $desiredLine"
$tipMsg = "Astuce : si le navigateur ne r" + [char]0x00E9 + "sout pas tout de suite, ex" + [char]0x00E9 + "cute : ipconfig /flushdns"

Write-Host $okMsg -ForegroundColor Green
Write-Host $tipMsg -ForegroundColor Yellow

# Par défaut on lance Caddy; utiliser -NoStartCaddy pour ne faire que hosts
if ($NoStartCaddy) {
  exit 0
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$caddyExe = Join-Path $repoRoot 'caddy_windows_amd64.exe'
$caddyfile = Join-Path $repoRoot 'Caddyfile'

if (-not (Test-Path $caddyExe)) {
  Write-Host "Caddy non trouvé: $caddyExe" -ForegroundColor Red
  exit 1
}
if (-not (Test-Path $caddyfile)) {
  Write-Host "Caddyfile non trouvé: $caddyfile" -ForegroundColor Red
  exit 1
}

Write-Host "Configuration HTTPS (trust) puis lancement de Caddy..." -ForegroundColor Cyan

# Tente d'installer la confiance CA (idempotent côté Caddy)
& $caddyExe trust | Out-Host

$argsList = @(
  '-NoProfile',
  '-ExecutionPolicy', 'Bypass',
  '-Command', ('& "' + $caddyExe + '" run --config "' + $caddyfile + '"')
)

# Lance Caddy dans une nouvelle fenêtre admin (non bloquante)
Start-Process -FilePath 'powershell.exe' -Verb RunAs -ArgumentList ($argsList -join ' ')