import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from manager.models import AppUser, Course, JoinClass, Checkin, History
from manager.utils import get_user_by_token, check_parameter
import manager.tencent_service as ts


def login(request):
    id = request.GET.get('id')
    psw = request.GET.get('psw')
    image = request.GET.get('image')
    if id and psw:
        try:
            user = AppUser.objects.get(id=id)
        except AppUser.DoesNotExist:
            return JsonResponse({"success": False, "message": "账号或密码错误"})
        if user.password != psw:
            return JsonResponse({"success": False, "message": "密码错误"})
    else:
        if image:
            user_id = ts.checkin("all", image)
            if user_id:
                user = AppUser.objects.get(id=id)
            else:
                return JsonResponse({"success": False, "message": "人脸识别失败"})
        else:
            return JsonResponse({"success": False, "message": "无图片"})
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


@check_parameter('id')
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


@csrf_exempt
@check_parameter('course-id', 'image')
@get_user_by_token
def checkin(request, **kwargs):
    course_id = request.POST['course-id']
    course = Course.objects.get(id=course_id)
    last_check = Checkin.objects.filter(course=course).order_by('-id')
    if len(last_check) == 0 or last_check.first().end_time is not None:
        return JsonResponse({"success": False, "message": "签到已经结束"})
    # TODO: 检测该同学已经签到成功
    last_check = last_check.first()
    image = request.POST['image']
    #  请求腾讯云获得对方user_id
    target_user_id = ts.checkin(course_id, image)

    user = kwargs['user']
    his = History()
    his.photographer = user
    his.target_id = target_user_id
    his.belong = last_check
    his.image = image
    his.save()
    if not his.target_id:
        return JsonResponse({"success": False, "message": "人脸识别失败"})
    return JsonResponse({"success": True})


@csrf_exempt
@get_user_by_token
def upload_image(request, **kwargs):
    user = kwargs['user']
    user.image = request.POST['image']
    user.save()
    ts.upload_image(user.id, user.image)
    return JsonResponse({"success": True})
