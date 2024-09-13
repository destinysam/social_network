from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

def get_refresh_token_for_user(user)-> RefreshToken:
    refresh = RefreshToken.for_user(user)
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    return refresh


def get_login_token(request,user):
    refresh = get_refresh_token_for_user(user)
    data = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "access_exp_at": refresh.access_token["exp"],
        "refresh_exp_at": refresh["exp"]
    }
    return data


def get_token_from_refresh_token(refresh_token: RefreshToken):
    refresh = RefreshToken(token=refresh_token)
    data = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "access_exp_at": refresh.access_token["exp"],
        "refresh_exp_at": refresh["exp"]
    }
    return data