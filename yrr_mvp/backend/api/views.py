import json
from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Imports pour l'authentification
from django.contrib.auth.hashers import make_password, check_password

from .mongo import get_mongo_db


# --- HELPER FUNCTIONS & SERIALIZERS ---

def _serialize_boat(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "sail_number": doc.get("sail_number"),
        "helmsman": doc.get("helmsman"),
        "class_id": str(doc.get("class_id")) if doc.get("class_id") else None,
        "class_name": doc.get("class_name"),
    }


def _serialize_class(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "handicap_type": doc.get("handicap_type"),
        "handicap_value": doc.get("handicap_value"),
    }


def _serialize_user(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "email": doc.get("email"),
    }


def _parse_handicap_value(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _serialize_series(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "classe": doc.get("classe"),
        "races": doc.get("races"),
        "counted": doc.get("counted"),
    }


def _serialize_course(doc):
    return {
        "id": str(doc.get("_id")),
        "od": doc.get("od"),
        "class_name": doc.get("class_name"),
        "date": doc.get("date"),
        "time": doc.get("time"),
        "name": doc.get("name"),
        "course": doc.get("course"),
        "series_id": str(doc.get("series_id")) if doc.get("series_id") else None,
    }


# --- BOAT VIEWS ---

@api_view(["GET", "POST"])
def boats(request):
    db = get_mongo_db()
    collection = db.boats

    if request.method == "GET":
        boats_list = [_serialize_boat(d) for d in collection.find().sort("_id", -1)]
        return Response(boats_list)

    payload = request.data if isinstance(request.data, dict) else {}
    name = payload.get("name")
    sail_number_raw = payload.get("sail_number")
    helmsman = payload.get("helmsman")
    class_id_raw = payload.get("class_id") or payload.get("class") or payload.get("classe")
    class_name_raw = payload.get("class_name") or payload.get("className")

    sail_number = _parse_int(sail_number_raw)
    if sail_number_raw not in (None, "") and sail_number is None:
        return Response({"detail": "sail_number must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    doc = {}

    if name not in (None, ""):
        doc["name"] = str(name)

    if sail_number is not None:
        doc["sail_number"] = sail_number

    if helmsman not in (None, ""):
        doc["helmsman"] = str(helmsman)

    if class_id_raw not in (None, ""):
        try:
            doc["class_id"] = ObjectId(str(class_id_raw))
        except Exception:
            return Response({"detail": "Invalid class_id"}, status=status.HTTP_400_BAD_REQUEST)

    if class_name_raw not in (None, ""):
        class_name = str(class_name_raw).strip()
        if class_name:
            existing = db.classes.find_one({"name": class_name})
            if existing:
                doc["class_id"] = existing.get("_id")
                doc["class_name"] = existing.get("name")
            else:
                created = db.classes.insert_one({
                    "name": class_name,
                    "handicap_type": "PY",
                    "handicap_value": 1.0,
                })
                doc["class_id"] = created.inserted_id
                doc["class_name"] = class_name

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


@api_view(["PUT", "PATCH", "DELETE"])
def boat_update(request, boat_id: str):
    db = get_mongo_db()
    collection = db.boats

    try:
        oid = ObjectId(boat_id)
    except Exception:
        return Response({"detail": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        res = collection.delete_one({"_id": oid})
        if res.deleted_count == 0:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    payload = request.data if isinstance(request.data, dict) else {}
    update_doc = {}

    if "name" in payload:
        name = payload.get("name")
        if name in (None, ""):
            update_doc["name"] = None
        else:
            update_doc["name"] = str(name)

    if "sail_number" in payload:
        sail_raw = payload.get("sail_number")
        if sail_raw in (None, ""):
            update_doc["sail_number"] = None
        else:
            sail = _parse_int(sail_raw)
            if sail is None:
                return Response({"detail": "sail_number must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
            update_doc["sail_number"] = sail

    if "helmsman" in payload:
        helmsman = payload.get("helmsman")
        if helmsman in (None, ""):
            update_doc["helmsman"] = None
        else:
            update_doc["helmsman"] = str(helmsman)

    if "class_id" in payload or "class" in payload or "classe" in payload:
        raw = payload.get("class_id") or payload.get("class") or payload.get("classe")
        if raw in (None, ""):
            update_doc["class_id"] = None
            update_doc["class_name"] = None
        else:
            try:
                cid = ObjectId(str(raw))
            except Exception:
                return Response({"detail": "Invalid class_id"}, status=status.HTTP_400_BAD_REQUEST)
            found = db.classes.find_one({"_id": cid})
            if not found:
                return Response({"detail": "Class not found"}, status=status.HTTP_400_BAD_REQUEST)
            update_doc["class_id"] = cid
            update_doc["class_name"] = found.get("name")

    if not update_doc:
        return Response({"detail": "No data provided for update"}, status=status.HTTP_400_BAD_REQUEST)

    set_doc = {k: v for k, v in update_doc.items() if v is not None}
    unset_keys = [k for k, v in update_doc.items() if v is None]

    ops = {}
    if set_doc:
        ops["$set"] = set_doc
    if unset_keys:
        ops["$unset"] = {k: "" for k in unset_keys}

    res = collection.update_one({"_id": oid}, ops)
    if res.matched_count == 0:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    updated = collection.find_one({"_id": oid})
    return Response(_serialize_boat(updated))


# --- CLASS VIEWS ---

@api_view(["GET", "POST"])
def classes(request):
    db = get_mongo_db()
    collection = db.classes

    if request.method == "GET":
        classes_list = [_serialize_class(d) for d in collection.find().sort("_id", -1)]
        return Response(classes_list)

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

    if name not in (None, ""):
        doc["name"] = str(name)

    result = collection.insert_one(doc)
    created = collection.find_one({"_id": result.inserted_id})
    return Response(_serialize_class(created), status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def class_delete(request, class_id: str):
    db = get_mongo_db()
    collection = db.classes

    try:
        oid = ObjectId(class_id)
    except Exception:
        return Response({"detail": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)

    res = collection.delete_one({"_id": oid})
    if res.deleted_count == 0:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)


# --- COURSE VIEWS ---

@api_view(["GET", "POST"])
def courses(request):
    db = get_mongo_db()
    collection = db.courses

    if request.method == "GET":
        courses_list = [_serialize_course(d) for d in collection.find().sort("_id", -1)]
        return Response(courses_list)

    payload = request.data if isinstance(request.data, dict) else {}
    od = payload.get("od")
    class_name = payload.get("class_name")
    date = payload.get("date")
    time = payload.get("time")
    name = payload.get("name")
    course = payload.get("course")
    series_id = payload.get("series_id")

    if not all([od, class_name, date, time, name, course, series_id]):
        return Response({"detail": "Tous les champs sont obligatoires (y compris la série)"}, status=status.HTTP_400_BAD_REQUEST)

    doc = {
        "od": str(od),
        "class_name": str(class_name),
        "date": str(date),
        "time": str(time),
        "name": str(name),
        "course": str(course),
        "series_id": series_id,
    }
    result = collection.insert_one(doc)
    created = collection.find_one({"_id": result.inserted_id})
    return Response(_serialize_course(created), status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def course_delete(request, course_id: str):
    db = get_mongo_db()
    collection = db.courses

    try:
        oid = ObjectId(course_id)
    except Exception:
        return Response({"detail": "Invalid course ID."}, status=status.HTTP_400_BAD_REQUEST)

    res = collection.delete_one({"_id": oid})
    if res.deleted_count == 0:
        return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)


# --- INSCRIPTIONS VIEWS ---

@api_view(["GET", "POST"])
def inscriptions(request):
    db = get_mongo_db()
    collection = db.inscriptions

    if request.method == "GET":
        result = []
        for d in collection.find().sort("_id", -1):
            result.append({
                "id": str(d.get("_id")),
                "bateauId": str(d.get("boat")),
                "courseId": str(d.get("course")),
                "resultat": d.get("resultat")
            })
        return Response(result)

    payload = request.data if isinstance(request.data, dict) else {}
    boat_id = payload.get("boat") or payload.get("boat_id") or payload.get("bateauId")
    course_id = payload.get("course") or payload.get("course_id") or payload.get("courseId")
    resultat = payload.get("resultat")

    if not all([boat_id, course_id, resultat]):
        return Response({"detail": "Champs obligatoires manquants"}, status=status.HTTP_400_BAD_REQUEST)

    doc = {
        "boat": ObjectId(boat_id),
        "course": ObjectId(course_id),
        "resultat": str(resultat)
    }
    result = collection.insert_one(doc)
    created = collection.find_one({"_id": result.inserted_id})
    return Response({
        "id": str(created.get("_id")),
        "bateauId": str(created.get("boat")),
        "courseId": str(created.get("course")),
        "resultat": created.get("resultat")
    }, status=status.HTTP_201_CREATED)


# --- SERIES VIEWS ---

@api_view(["GET", "POST"])
def series(request):
    db = get_mongo_db()
    collection = db.series

    if request.method == "GET":
        series_list = [_serialize_series(d) for d in collection.find().sort("_id", -1)]
        return Response(series_list)

    payload = request.data if isinstance(request.data, dict) else {}
    name = (payload.get("name") or "").strip()
    classe = (payload.get("classe") or "").strip()
    counted = _parse_int(payload.get("counted"))
    counted = counted if isinstance(counted, int) else 0

    if not name:
        return Response({"detail": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not classe:
        return Response({"detail": "classe is required"}, status=status.HTTP_400_BAD_REQUEST)
    if counted < 1:
        return Response({"detail": "counted must be >= 1"}, status=status.HTTP_400_BAD_REQUEST)

    doc = {"name": name, "classe": classe, "counted": counted}
    result = collection.insert_one(doc)
    created = collection.find_one({"_id": result.inserted_id})
    return Response(_serialize_series(created), status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def series_delete(request, series_id: str):
    db = get_mongo_db()
    collection = db.series

    try:
        oid = ObjectId(series_id)
    except Exception:
        return Response({"detail": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)

    res = collection.delete_one({"_id": oid})
    if res.deleted_count == 0:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)


# --- AUTHENTICATION VIEWS ---

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

    if collection.find_one({"email": email}):
        return Response({"detail": "Cette adresse e-mail est déjà utilisée."}, status=status.HTTP_409_CONFLICT)

    doc = {
        "name": name,
        "email": email,
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

    if isinstance(stored, str) and stored.count('$') >= 2:
        try:
            ok = check_password(password, stored)
        except Exception:
            ok = False
    elif stored == password:
        ok = True
        try:
            collection.update_one({"_id": user.get("_id")}, {"$set": {"password": make_password(password)}})
        except Exception:
            pass

    if not ok:
        return Response({"detail": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

    token = str(user.get("_id"))
    return Response({"token": token, "user": _serialize_user(user)}, status=status.HTTP_200_OK)