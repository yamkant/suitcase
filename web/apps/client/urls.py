from django.urls import path
from client import views

app_name = "client"

urlpatterns = [
    path("", views.render_home, name="home"),
    path("fitting/", views.render_fitting, name="fitting"),
]