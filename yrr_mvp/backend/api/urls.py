from django.urls import path

from .views import boats, boat_delete, series, series_delete

urlpatterns = [
    path('boats', boats),
    path('boats/<str:boat_id>', boat_delete),
    path('series', series),
    path('series/<str:series_id>', series_delete),
]
