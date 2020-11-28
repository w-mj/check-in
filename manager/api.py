import json

from django.http import HttpResponse

from .models import Course, CourseTime
from .views import get_user_by_token


@get_user_by_token
def add_course(request, **kwargs):
    course_name = request.GET['courseName']
    course_id = request.GET.get('id', None)
    if course_id:
        course = Course.objects.get(id=course_id)
    else:
        course = Course()
    course.name = course_name
    course.teacher = kwargs['user']
    course.save()

    CourseTime.objects.filter(course=course).delete()
    # print(request.GET)
    for i in range(10):
        start_week = request.GET.get(f"start_week{i}")
        end_week = request.GET.get(f"end_week{i}")
        start_time = request.GET.get(f"start_time{i}")
        end_time = request.GET.get(f"end_time{i}")
        day = request.GET.get(f"day{i}")
        if start_time is None:
            break
        new_time = CourseTime(
            start_week=start_week,
            end_week=end_week,
            start_time=start_time,
            end_time=end_time,
            day=day,
            course=course
        )
        new_time.save()
    return HttpResponse(json.dumps({"success": True}))
