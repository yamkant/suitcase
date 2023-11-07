from django.urls import path
from apps.core.types import APIUrlPatternsType
from apps.products.views.products import ProductBulkViewSet, ProductListView, ProductDetailView
from apps.products.views.profiles import ProductProfileViewSet

app_name = "products"

urlpatterns: APIUrlPatternsType = [
    path("", ProductListView.as_view(), name="list"),
    path("<int:id>/", ProductDetailView.as_view(), name="detail"),

    path("bulk/", ProductBulkViewSet.as_view(), name="bulk"),
    path("profile/", ProductProfileViewSet.as_view({"post": "create"}), name="profile_list"),
]