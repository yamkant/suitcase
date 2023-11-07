from django.urls import path
from django.contrib.auth import views as auth_views

from apps.users.views.accounts import JoinAPIView, LoginAPIView

app_name = "accounts"

urlpatterns = [
    path("join/", JoinAPIView.as_view(), name="join"),
    path("login/", LoginAPIView.as_view(), name="login"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]