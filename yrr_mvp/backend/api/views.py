import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient

# Connexion MongoDB
uri = os.getenv("MONGODB_URI")
if not uri:
    raise RuntimeError("MONGODB_URI environment variable is not set")

client = MongoClient(os.environ["MONGODB_URI"])
db = client["yrr_poc"]

@api_view(["POST"])
def calculate_corrected_time(request):
    # Récupération des données envoyées par Svelte
    elapsed = float(request.data.get("elapsed"))
    handicap = float(request.data.get("handicap"))

    # Calcul TMF
    corrected = elapsed * handicap

    # Sauvegarde dans MongoDB
    entry = {
        "elapsed": elapsed,
        "handicap": handicap,
        "corrected": corrected
    }
    db.race_entries.insert_one(entry)

    # Réponse envoyée au frontend
    return Response({
        "elapsed": elapsed,
        "corrected": corrected,
        "message": "Résultat sauvegardé dans MongoDB"
    })
