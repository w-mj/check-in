from django.urls import path
import manager.views as v

urlpatterns = [
    path('courses', v.course_list)
]
