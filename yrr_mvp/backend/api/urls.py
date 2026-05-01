from django.urls import path

from .views import boats, boat_delete, courses, inscriptions

urlpatterns = [
    path('boats', boats),
    path('boats/<str:boat_id>', boat_delete),
    path('courses', courses),
    path('inscriptions', inscriptions),
]
