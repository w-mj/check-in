import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from manager.models import AppUser, Course, JoinClass, Checkin, History
from .views import get_user_by_token


def login(request):
    id = request.GET.get('id')
    psw = request.GET.get('psw')
    image = request.GET.get('image')
    if id and psw:
        try:
            user = AppUser.objects.get(id=id)
        except AppUser.DoesNotExist:
            return HttpResponse(json.dumps({"success": False, "message": "账号或密码错误"}))
        if user.password != psw:
            return HttpResponse(json.dumps({"success": False, "message": "密码错误"}))
    else:
        return HttpResponse(json.dumps({"success": False, "message": "???"}))
    return JsonResponse({
        'success': True,
        'user': user.json,
        'courses': [x.course.json for x in JoinClass.objects.filter(user=user)]
    })


@get_user_by_token
def course_list(request, **kwargs):
    user = kwargs['user']
    return JsonResponse({
        'courses': [x.course.json for x in JoinClass.objects.filter(user=user)]
    })


@get_user_by_token
def course_info(request, **kwargs):
    user = kwargs['user']
    course_id = int(request.GET['id'])
    course = Course.objects.get(id=course_id)
    course_json = course.json
    course_json['teacher'] = course.teacher.name
    if course_json['checking']:
        last_check = Checkin.objects.filter(course=course).order_by('-id').first()
        course_json['method'] = last_check.method
        course_json['count'] = last_check.count
        course_json['result'] = [x.json for x in History.objects.filter(Q(photographer=user) | Q(target=user), belong=last_check)]
    return JsonResponse(course_json)


@get_user_by_token
def checkin(request, **kwargs):
    course_id = request.GET['course-id']
    course = Course.objects.get(id=course_id)
    last_check = Checkin.objects.filter(course=course).order_by('-id')
    if len(last_check) == 0 or last_check.first().end_time is not None:
        return JsonResponse({"success": False, "message": "签到已经结束"})
    # TODO: 检测该同学已经签到成功
    last_check = last_check.first()
    image = request.GET['image']
    #  请求腾讯云获得对方user_id
    target_user_id = '100'
    user = kwargs['user']
    his = History()
    his.photographer = user
    his.target_id = target_user_id
    his.belong = last_check
    his.image = image
    his.save()
    return JsonResponse({"success": True})


@get_user_by_token
def upload_image(request, **kwargs):
    user = kwargs['user']
    user.image = request.GET['image']
    user.save()
    return JsonResponse({"success": True})
