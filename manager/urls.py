from django.urls import path, include
import manager.views as v
import manager.api as api
import manager.frontend_api as f

api_urls = [
    path('add-course', api.add_course),
    path('start-checkin', api.start_checkin),
    path('stop-checkin', api.stop_checkin),
    path('add-student', api.add_student),
    path('del-student', api.del_student),
    path('upload_student_file', api.upload_student_file)
]

urlpatterns = [
    path('page/courses', v.course_list),
    path('page/checkin', v.checkin_list),
    path('page/students', v.student_list),
    path('page/result', v.result),
    path('page/graph', v.graph),
    path('api/', include(api_urls)),
    path('login', f.login),
    path('course-list', f.course_list),
    path('course-info', f.course_info),
    path('check-in', f.checkin),
    path('upload-image', f.upload_image)
]
