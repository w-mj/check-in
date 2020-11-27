from .models import AppUser


class TokenService:
    def get_token(self, uid):
        return uid
    def get_user(self, token):
        return AppUser.objects.get(id=token)

token_service = TokenService()
