from django.urls import path
from .views import SignUpAPI,SignInAPI,RefreshTokenAPI
urlpatterns = [
    path("refresh_token/",RefreshTokenAPI.as_view(),name="refresh-token"),
    path("signup/",SignUpAPI.as_view(),name="signup"),
    path("signin/",SignInAPI.as_view(),name="signin"),
]