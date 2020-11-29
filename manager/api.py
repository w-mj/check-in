import json
from datetime import datetime

from django.conf.urls import handler403
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Course, CourseTime, Checkin, AppUser, JoinClass
from .utils import get_user_by_token
import manager.tencent_service as ts


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
    ts.create_group(course.name, course.id)
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


def get_or_create_student(student_id, student_name):
    try:
        student = AppUser.objects.get(id=student_id)
    except AppUser.DoesNotExist:
        if not student_name:
            raise Exception()
        student = AppUser()
        student.name = student_name
        student.id = student_id
        student.password = student_id
        student.role = 1
        student.save()
    return student


@get_user_by_token
def add_student(request, **kwargs):
    student_id = request.GET['student_id']
    student_name = request.GET.get('student_name')
    try:
        student = get_or_create_student(student_id, student_name)
    except Exception:
        return handler403(request, Exception())
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
    ts.remove_from_group(student_id, course_id)
    return HttpResponse(json.dumps({"success": True}))


def csv_reader(data: str):
    lines = data.split()
    head = lines[0]
    head = head.split(',')
    lines = lines[1:]
    for l in lines:
        ar = l.split(',')
        yield dict(zip(head, ar))


@csrf_exempt
@get_user_by_token
def upload_student_file(request, **kwargs):
    file = request.FILES['file']
    for line in csv_reader(file.read().decode()):
        stu_id = line['id']
        name = line.get('name')
        try:
            student = get_or_create_student(stu_id, name)
            course_id = request.GET['course_id']
            course = Course.objects.get(id=course_id)
            record = JoinClass(course=course, user=student)
            record.save()
        except Exception:
            pass
    return HttpResponse(json.dumps({"success": True}))
