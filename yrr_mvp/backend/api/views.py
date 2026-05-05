import json
from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password, check_password

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


def _serialize_user(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "email": doc.get("email"),
    }


@api_view(["POST"])
def register(request):
    db = get_mongo_db()
    collection = db.users

    payload = request.data if isinstance(request.data, dict) else {}

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password")

    if not name:
        return Response({"detail": "Le nom complet est requis."}, status=status.HTTP_400_BAD_REQUEST)
    if not email:
        return Response({"detail": "L’adresse e-mail est requise."}, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(password, str) or len(password) < 6:
        return Response(
            {"detail": "Le mot de passe doit contenir au moins 6 caractères."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Unicité email (simple)
    if collection.find_one({"email": email}):
        return Response({"detail": "Cette adresse e-mail est déjà utilisée."}, status=status.HTTP_409_CONFLICT)

    doc = {
        "name": name,
        "email": email,
        # Stockage sécurisé (Django PBKDF2 par défaut)
        "password": make_password(password),
    }

    result = collection.insert_one(doc)
    created = collection.find_one({"_id": result.inserted_id})
    return Response(_serialize_user(created), status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    db = get_mongo_db()
    collection = db.users

    payload = request.data if isinstance(request.data, dict) else {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password")

    if not email:
        return Response({"detail": "L’adresse e-mail est requise."}, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(password, str) or password == "":
        return Response({"detail": "Le mot de passe est requis."}, status=status.HTTP_400_BAD_REQUEST)

    user = collection.find_one({"email": email})
    if not user:
        return Response({"detail": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

    stored = user.get("password")

    ok = False
    # Mot de passe hashé (format Django)
    if isinstance(stored, str) and stored.count('$') >= 2:
        try:
            ok = check_password(password, stored)
        except Exception:
            ok = False
    # Compat: anciens comptes MVP stockés en clair
    elif stored == password:
        ok = True
        # upgrade en hash à la première connexion
        try:
            collection.update_one({"_id": user.get("_id")}, {"$set": {"password": make_password(password)}})
        except Exception:
            pass

    if not ok:
        return Response({"detail": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

    token = str(user.get("_id"))
    return Response({"token": token, "user": _serialize_user(user)}, status=status.HTTP_200_OK)