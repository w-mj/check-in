import json
import time
from datetime import datetime, timezone

from django.conf.urls import handler403
from django.http import HttpResponse

from .models import Course, CourseTime, Checkin, AppUser, JoinClass
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


@get_user_by_token
def start_checkin(request, **kwargs):
    method = request.GET['method']
    count = request.GET['count']
    course = Course.objects.get(id=request.GET['course'])
    checkin = Checkin()
    checkin.method = int(method)
    checkin.count = count
    checkin.course = course
    checkin.start_time = datetime.now()
    checkin.end_time = None
    checkin.save()
    return HttpResponse(json.dumps({"success": True}))


@get_user_by_token
def stop_checkin(request, **kwargs):
    course = Course.objects.get(id=request.GET['course'])
    checkin = Checkin.objects.get(course=course, end_time=None)
    checkin.end_time = datetime.now()
    checkin.save()
    return HttpResponse(json.dumps({"success": True}))


@get_user_by_token
def add_student(request, **kwargs):
    student_id = request.GET['student_id']
    student_name = request.GET.get('student_name')
    try:
        student = AppUser.objects.get(id=student_id)
    except AppUser.DoesNotExist:
        if not student_name:
            return handler403(request, Exception())
        student = AppUser()
        student.name = student_name
        student.id = student_id
        student.password = student_id
        student.role = 1
        student.save()
    course_id = request.GET['course_id']
    course = Course.objects.get(id=course_id)
    record = JoinClass(course=course, user=student)
    record.save()
    return HttpResponse(json.dumps({"success": True}))


@get_user_by_token
def del_student(request, **kwargs):
    student_id = request.GET['student_id']
    course_id = request.GET['course_id']
    JoinClass.objects.get(course_id=course_id, user_id=student_id).delete()
    return HttpResponse(json.dumps({"success": True}))
