from django.urls import path
from .views import (
    boats, boat_delete, boat_update, 
    classes, class_delete, 
    courses, course_delete, 
    inscriptions, 
    series, series_delete,
    register, login
)

urlpatterns = [
    # Boats
    path('boats', boats),
    path('boats/<str:boat_id>', boat_update),
    
    # Classes
    path('classes', classes),
    path('classes/<str:class_id>', class_delete),
    
    # Courses
    path('courses', courses),
    path('courses/<str:course_id>', course_delete),
    
    # Inscriptions
    path('inscriptions', inscriptions),
    
    # Series
    path('series', series),
    path('series/<str:series_id>', series_delete),
    
    # Users / Auth
    path('users/register', register),
    path('users/login', login),
]