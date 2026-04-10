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
        "handicap_type": doc.get("handicap_type"),
        "handicap_value": doc.get("handicap_value"),
    }


def _parse_handicap_value(value):
    # handicap_value doit être un nombre (float)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


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
    handicap_type = payload.get("handicap_type")
    handicap_value_raw = payload.get("handicap_value")

    if handicap_type not in {"PY", "TMF"}:
        return Response({"detail": "handicap_type must be 'PY' or 'TMF'"}, status=status.HTTP_400_BAD_REQUEST)

    handicap_value = _parse_handicap_value(handicap_value_raw)
    if handicap_value is None:
        return Response({"detail": "handicap_value must be a number"}, status=status.HTTP_400_BAD_REQUEST)

    doc = {
        "handicap_type": handicap_type,
        "handicap_value": handicap_value,
    }

    # name optionnel
    if name not in (None, ""):
        doc["name"] = str(name)

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
