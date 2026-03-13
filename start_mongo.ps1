$mongoDir = "$env:USERPROFILE\mongodb"
$dataDir = "$mongoDir\data"

# Trouver mongod.exe dans le dossier portable
$exe = Get-ChildItem -Path $mongoDir -Recurse -Filter "mongod.exe" | Select-Object -First 1

if (-not $exe) {
    Write-Host "ERREUR : MongoDB n'est pas installé. Lance install_mongo.ps1 d'abord."
    exit
}

Write-Host "Lancement de MongoDB..."
Start-Process -FilePath $exe.FullName -ArgumentList "--dbpath `"$dataDir`" --bind_ip 127.0.0.1"

Write-Host "MongoDB est lancé sur : mongodb://localhost:27017"
