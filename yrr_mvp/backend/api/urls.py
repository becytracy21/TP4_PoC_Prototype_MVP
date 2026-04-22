from django.urls import path

from .views import boats, boat_delete, classes, class_delete

urlpatterns = [
    path('boats', boats),
    path('boats/<str:boat_id>', boat_delete),
    path('classes', classes),
    path('classes/<str:class_id>', class_delete),
]
