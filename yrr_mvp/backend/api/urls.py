from django.urls import path

from .views import boats, boat_detail

urlpatterns = [
    path('boats', boats),
    path('boats/<str:boat_id>', boat_detail),
]
