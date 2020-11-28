import json

from django.shortcuts import render

from .models import Course, Checkin, JoinClass
from .utils import get_user_by_token


@get_user_by_token
def course_list(request, **kwargs):
    user = kwargs['user']
    courses = Course.objects.filter(teacher=user)
    context = {
        'user_json': json.dumps(user.json),
        'token': kwargs['token'],
        'courses': courses,
        'user': user,
        'courses_json': json.dumps([x.json for x in courses]),
    }
    return render(request, 'course-list.html', context)


@get_user_by_token
def checkin_list(request, **kwargs):
    course_id = request.GET['course']
    course = Course.objects.get(id=course_id)
    checks = Checkin.objects.filter(course=course)
    checking = any([x.end_time is None for x in checks])
    context = {
        'checkinList': checks,
        'token': kwargs['token'],
        'course': course,
        'course_json': json.dumps(course.json),
        'checking': checking
    }
    return render(request, 'checkin.html', context)


@get_user_by_token
def student_list(request, **kwargs):
    course_id = request.GET['course']
    course = Course.objects.get(id=course_id)
    students = JoinClass.objects.filter(course=course)
    students = [x.user for x in students]
    context = {
        'students': students,
        'token': kwargs['token'],
        'course': course,
        'course_json': json.dumps(course.json)
    }
    return render(request, 'student-list.html', context)
