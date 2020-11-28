from django.urls import path, include
import manager.views as v
import manager.api as api

api_urls = [
    path('add-course', api.add_course)
]

urlpatterns = [
    path('courses', v.course_list),
    path('checkin', v.checkin_list),
    path('students', v.student_list),
    path('api/', include(api_urls))
]
