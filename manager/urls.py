from django.urls import path, include
import manager.views as v
import manager.api as api

api_urls = [
    path('add-course', api.add_course),
    path('start-checkin', api.start_checkin),
    path('stop-checkin', api.stop_checkin),
    path('add-student', api.add_student),
    path('del-student', api.del_student)
]

urlpatterns = [
    path('courses', v.course_list),
    path('checkin', v.checkin_list),
    path('students', v.student_list),
    path('api/', include(api_urls))
]
