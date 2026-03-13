# ============================
# 1. Variables
# ============================
$mongoUrl = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.5.zip"
$zipPath = "$env:USERPROFILE\mongodb.zip"
$mongoDir = "$env:USERPROFILE\mongodb"
$dataDir = "$mongoDir\data"

Write-Host "=== Installation MongoDB Portable ==="

# ============================
# 2. Télécharger MongoDB
# ============================
Write-Host "Téléchargement de MongoDB..."
Invoke-WebRequest -Uri $mongoUrl -OutFile $zipPath

# ============================
# 3. Décompression
# ============================
Write-Host "Décompression..."
Expand-Archive -Path $zipPath -DestinationPath $mongoDir -Force

# ============================
# 4. Création du dossier data
# ============================
Write-Host "Création du dossier data..."
New-Item -ItemType Directory -Force -Path $dataDir | Out-Null

Write-Host "Installation terminée !"
Write-Host "MongoDB est prêt dans : $mongoDir"
