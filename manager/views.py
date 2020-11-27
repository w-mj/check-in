import json

from django.conf.urls import handler403
from django.http import HttpResponse
from django.shortcuts import render
from .utils import token_service
from .models import Course


def course_list(request):
    token = request.GET['token']
    user = token_service.get_user(token)
    if not user or user.role != 0:
        return handler403(request, Exception())
    courses = Course.objects.filter(teacher=user)
    context = {
        'user_json': json.dumps(user.json),
        'token': token,
        'courses': courses,
        'courses_json': json.dumps([x.json for x in courses])
    }
    return render(request, 'course-list.html', context)
