import json

from django.shortcuts import render

from .models import Course, Checkin, JoinClass, AppUser
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


@get_user_by_token
def result(request, **kwargs):
    checkin_id = request.GET['id']
    checkin = Checkin.objects.get(id=checkin_id)
    res, stu_list = checkin.result()
    stu_list = [(AppUser.objects.get(id=x[0]), x[1]) for x in stu_list]
    context = {
        'token': kwargs['token'],
        'res': res,
        'stu_list': stu_list,
        'course': checkin.course
    }
    return render(request, 'result.html', context)


@get_user_by_token
def graph(request, **kwargs):
    checkin_id = request.GET['id']
    checkin = Checkin.objects.get(id=checkin_id)
    res, stu_list = checkin.result()
    res = [[x.photographer.id, x.target_id] for x in res]
    stu_name_list = {x: AppUser.objects.get(id=x).name for x,_ in stu_list}
    context = {
        'token': kwargs['token'],
        'course': checkin.course,
        'res': json.dumps(res),
        'stu_name_list': stu_name_list
    }
    return render(request, 'graph.html', context)
