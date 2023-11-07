from django.urls import path
from apps.users.views.users import UserViewSet

app_name = "users"

urlpatterns = [
    path("", UserViewSet.as_view({"get": "list"}), name="list"),
    # path("<int:user_id>/", UserViewSet.as_view({"get": "retrieve", "patch": "update", "delete": "delete"}), name="retrieve-update"),
]