from django.urls import path
from products.views.products import ProductBulkViewSet, ProductListView, ProductDetailView
from products.views.profiles import ProductProfileViewSet
from django.contrib.auth import views as auth_views
from core.types import APIUrlPatternsType

app_name = "products"

urlpatterns: APIUrlPatternsType = [
    path("", ProductListView.as_view(), name="list"),
    path("<int:id>/", ProductDetailView.as_view(), name="detail"),

    path("bulk/", ProductBulkViewSet.as_view(), name="bulk"),
    path("profile/", ProductProfileViewSet.as_view({"post": "create"}), name="profile_list"),
]