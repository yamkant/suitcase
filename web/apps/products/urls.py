from django.urls import path
from products.views.products import ProductViewSet, ProductBulkViewSet
from products.views.profiles import ProductProfileViewSet
from django.contrib.auth import views as auth_views
from core.types import APIUrlPatternsType

app_name = "products"

urlpatterns: APIUrlPatternsType = [
    path("", ProductViewSet.as_view({"get": "list", "post": "create"}), name="list"),
    path("<int:id>/", ProductViewSet.as_view({"patch": "update", "delete": "destroy"}), name="detail"),
    path("bulk/", ProductBulkViewSet.as_view({"patch": "bulk_update", "delete": "bulk_delete"}), name="bulk"),
    path("profile/", ProductProfileViewSet.as_view({"post": "create"}), name="profile_list"),
]