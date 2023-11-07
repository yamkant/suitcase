from django.urls import path
from apps.users.views.users import UserViewSet

app_name = "users"

urlpatterns = [
    path("", UserViewSet.as_view({"get": "list"}), name="list"),
    path("<int:id>/", UserViewSet.as_view({"patch": "update"}), name="detail"),
]