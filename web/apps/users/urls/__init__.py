from django.urls import path
from users.views.users import UserViewSet
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("", UserViewSet.as_view({"get": "list"}), name="list"),
    # path("<int:user_id>/", UserViewSet.as_view({"get": "retrieve", "patch": "update", "delete": "delete"}), name="retrieve-update"),
]