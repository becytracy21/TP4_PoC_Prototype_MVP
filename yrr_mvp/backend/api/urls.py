from django.urls import path
from .views import calculate_corrected_time

urlpatterns = [
    path('calculate/', calculate_corrected_time),
]
