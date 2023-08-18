from django.urls import path
from users.views.accounts import JoinAPIView, LoginAPIView
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("join/", JoinAPIView.as_view(), name="join"),
    path("login/", LoginAPIView.as_view(), name="login"),
]