import json
from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .mongo import get_mongo_db


# --- HELPER FUNCTIONS & SERIALIZERS ---

def _serialize_boat(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "handicap_type": doc.get("handicap_type"),
        "handicap_value": doc.get("handicap_value"),
    }


def _serialize_class(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "handicap_type": doc.get("handicap_type"),
        "handicap_value": doc.get("handicap_value"),
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


@api_view(["GET", "POST"])
def classes(request):
    db = get_mongo_db()
    collection = db.classes

    if request.method == "GET":
        classes_list = [_serialize_class(d) for d in collection.find().sort("_id", -1)]
        return Response(classes_list)

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


# --- COURSE VIEWS (from HEAD) ---

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


# --- Inscriptions VIEWS (from HEAD) ---

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


# --- SERIES VIEWS (from origin/US127-JG) ---

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