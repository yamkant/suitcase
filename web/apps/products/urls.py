from django.urls import path
from products.views import ProductViewSet
from django.contrib.auth import views as auth_views

app_name = "products"

urlpatterns = [
    path("", ProductViewSet.as_view({"get": "list", "post": "create"}), name="list"),
    path("<int:id>/", ProductViewSet.as_view({"patch": "update", "delete": "destroy"}), name="detail"),
]