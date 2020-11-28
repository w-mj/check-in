import json

from django.conf.urls import handler403
from django.shortcuts import render
from .utils import token_service
from .models import Course, Checkin, History, JoinClass


def get_user_by_token(func):
    def _f(request, *args, **kwargs):
        token = request.GET.get('token')
        if not token:
            return handler403(request, Exception())
        user = token_service.get_user(token)
        if not user or user.role != 0:
            return handler403(request, Exception())
        return func(request, user=user, token=token)
    return _f


@get_user_by_token
def course_list(request, **kwargs):
    user = kwargs['user']
    courses = Course.objects.filter(teacher=user)
    context = {
        'user_json': json.dumps(user.json),
        'token': kwargs['token'],
        'courses': courses,
        'user': user,
        'courses_json': json.dumps([x.json for x in courses])
    }
    return render(request, 'course-list.html', context)


@get_user_by_token
def checkin_list(request, **kwargs):
    course_id = request.GET['course']
    course = Course.objects.get(id=course_id)
    checks = Checkin.objects.filter(course=course)
    context = {
        'checkinList': checks,
        'token': kwargs['token'],
        'course': course
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
        'course': course
    }
    return render(request, 'student-list.html', context)
