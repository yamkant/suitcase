from django.urls import path
from client.views import ProductTemplateViewSet, render_fitting, UserTemplateViewSet

app_name = "client"

urlpatterns = [
    path("", ProductTemplateViewSet.as_view(), name="home"),
    path("fitting/", render_fitting, name="fitting"),
    path("browse/", UserTemplateViewSet.as_view(), name="browse"),
]