from django.urls import path
from users.views.accounts import JoinAPIView
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("join/", JoinAPIView.as_view(), name="join"),
]