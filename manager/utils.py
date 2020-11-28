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
