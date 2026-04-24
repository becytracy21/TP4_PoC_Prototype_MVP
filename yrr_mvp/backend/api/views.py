import json
from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .mongo import get_mongo_db


def _serialize_boat(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "class": doc.get("class"),
        "sail_number": doc.get("sail_number"),
        "helmsman": doc.get("helmsman")
    }

@api_view(["GET", "POST"])
def boats(request):
    db = get_mongo_db()
    collection = db.boats

    if request.method == "GET":
        boats_list = [_serialize_boat(d) for d in collection.find().sort("_id", -1)]
        return Response(boats_list)

    # POST
    payload = request.data if isinstance(request.data, dict) else {}

    name = payload.get("name")
    boat_class = payload.get("class")
    sail_number = payload.get("sail_number")
    helmsman = payload.get("helmsman")

    # construire le document en évitant l'utilisation d'une variable non initialisée
    doc = {}

    # ajouter les champs fournis (name est optionnel)
    if name not in (None, ""):
        doc["name"] = str(name)

    if boat_class:
        doc["class"] = boat_class

    if sail_number is not None:
        # accepter 0 et valeurs numériques
        doc["sail_number"] = sail_number

    if helmsman:
        doc["helmsman"] = helmsman

    # si aucun champ n'a été fourni, retourner une erreur
    if not doc:
        return Response({"detail": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

    result = collection.insert_one(doc)
    created = collection.find_one({"_id": result.inserted_id})
    return Response(_serialize_boat(created), status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def boat_delete(request, boat_id: str):
    db = get_mongo_db()
    collection = db.boats

    try:
        oid = ObjectId(boat_id)
    except Exception:
        return Response({"detail": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)

    res = collection.delete_one({"_id": oid})
    if res.deleted_count == 0:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)
