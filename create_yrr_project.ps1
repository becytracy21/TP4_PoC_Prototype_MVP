# ================================
# CONFIG
# ================================
$PROJECT_NAME = "yrr_project"
$DJANGO_APP = "api"
$FRONT_NAME = "frontend"

Write-Host "🚀 Création du projet Django + Svelte : $PROJECT_NAME"

# ================================
# STRUCTURE
# ================================
New-Item -ItemType Directory -Path $PROJECT_NAME | Out-Null
Set-Location $PROJECT_NAME

# ================================
# PYTHON / DJANGO
# ================================
Write-Host "📦 Installation environnement Python"
python -m venv venv

# Activation venv
.\venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install django djangorestframework pymongo djongo

Write-Host "📁 Création projet Django"
django-admin startproject backend
Set-Location backend
python manage.py startapp $DJANGO_APP

# ================================
# CONFIG DJANGO
# ================================
Write-Host "⚙️ Configuration Django"

$SETTINGS_FILE = "backend\settings.py"

# Ajout des apps
(Get-Content $SETTINGS_FILE) `
    -replace "'django.contrib.staticfiles',", "'django.contrib.staticfiles',`n    'rest_framework',`n    '$DJANGO_APP'," |
    Set-Content $SETTINGS_FILE

# Ajout config MongoDB
@"
# ============================
# MongoDB Configuration
# ============================
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'yrr_poc',
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
        }
    }
}
"@ | Add-Content $SETTINGS_FILE

# ================================
# API DJANGO
# ================================
Write-Host "🧩 Création API Django"

@"
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

@api_view(['POST'])
def calculate_corrected_time(request):
    start = datetime.fromisoformat(request.data['start'])
    finish = datetime.fromisoformat(request.data['finish'])
    handicap_type = request.data['handicap_type']
    handicap_value = float(request.data['handicap_value'])

    elapsed = (finish - start).total_seconds()

    if handicap_type == "PY":
        corrected = elapsed * 1000 / handicap_value
    else:
        corrected = elapsed * handicap_value

    return Response({
        "elapsed": elapsed,
        "corrected": round(corrected)
    })
"@ | Set-Content "$DJANGO_APP\views.py"

@"
from django.urls import path
from .views import calculate_corrected_time

urlpatterns = [
    path('calculate/', calculate_corrected_time),
]
"@ | Set-Content "$DJANGO_APP\urls.py"

@"
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('$DJANGO_APP.urls')),
]
"@ | Set-Content "backend\urls.py"

Set-Location ..

# ================================
# SVELTE
# ================================
Write-Host "🎨 Installation Svelte"

npm create vite@latest $FRONT_NAME -- --template svelte
Set-Location $FRONT_NAME
npm install

# Ajout App.svelte
@"
<script>
    let start = "";
    let finish = "";
    let handicap_type = "PY";
    let handicap_value = 1000;
    let result = null;

    async function calculate() {
        const res = await fetch("http://localhost:8000/api/calculate/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ start, finish, handicap_type, handicap_value })
        });
        result = await res.json();
    }
</script>

<h1>Calcul Temps Corrigé</h1>

<label>Départ</label>
<input type="datetime-local" bind:value={start} />

<label>Arrivée</label>
<input type="datetime-local" bind:value={finish} />

<label>Type handicap</label>
<select bind:value={handicap_type}>
    <option value="PY">PY</option>
    <option value="TMF">TMF</option>
</select>

<label>Valeur handicap</label>
<input type="number" bind:value={handicap_value} />

<button on:click={calculate}>Calculer</button>

{#if result}
    <h2>Résultat</h2>
    <p>Temps écoulé : {result.elapsed}s</p>
    <p>Temps corrigé : {result.corrected}s</p>
{/if}
"@ | Set-Content "src\App.svelte"

Set-Location ..

Write-Host "🎉 Projet créé avec succès !"
Write-Host "➡️ Backend : $PROJECT_NAME\backend"
Write-Host "➡️ Frontend : $PROJECT_NAME\$FRONT_NAME"
Write-Host ""
Write-Host "Pour lancer Django :"
Write-Host "  cd backend"
Write-Host "  ..\venv\Scripts\Activate.ps1"
Write-Host "  python manage.py runserver"
Write-Host ""
Write-Host "Pour lancer Svelte :"
Write-Host "  cd $FRONT_NAME"
Write-Host "  npm run dev"
