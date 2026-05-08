from django.urls import path

from .views import boats, boat_delete,classes, class_delete, courses, course_delete, inscriptions, series, series_delete

urlpatterns = [
    path('boats', boats),
    path('boats/<str:boat_id>', boat_delete),
    path('classes', classes),
    path('classes/<str:class_id>', class_delete),
    path('courses', courses),
    path('courses/<str:course_id>', course_delete),
    path('inscriptions', inscriptions),
    path('series', series),
    path('series/<str:series_id>', series_delete),
]