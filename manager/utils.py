from django.conf.urls import handler403
from django.http import JsonResponse

from .models import AppUser


class TokenService:
    def get_token(self, uid):
        return uid
    def get_user(self, token):
        try:
            return AppUser.objects.get(id=token)
        except AppUser.DoesNotExist:
            return None

token_service = TokenService()


def get_user_by_token(func):
    def _f(request, *args, **kwargs):
        token = request.GET.get('token', request.POST.get('token'))
        if not token:
            return JsonResponse({"success": False, "message": f"need `token` parameter"})
        user = token_service.get_user(token)
        if not user:
            return JsonResponse({"success": False, "message": f"token error"})
        return func(request, user=user, token=token)
    return _f


def check_parameter(*para):
    def _w(func):
        def _f(request, *args, **kwargs):
            for x in para:
                if x not in request.GET and x not in request.POST:
                    return JsonResponse({"success": False, "message": f"need `{x}` parameter"})
            return func(request, *args, **kwargs)
        return _f
    return _w
