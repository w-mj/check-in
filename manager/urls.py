from django.urls import path
import manager.views as v

urlpatterns = [
    path('courses', v.course_list),
    path('checkin', v.checkin_list),
    path('students', v.student_list)
]
