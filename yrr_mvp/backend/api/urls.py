from django.urls import path

from .views import boats, boat_delete
from .views import register

urlpatterns = [
    path('boats', boats),
    path('boats/<str:boat_id>', boat_delete),
    path('users/register', register),
]
