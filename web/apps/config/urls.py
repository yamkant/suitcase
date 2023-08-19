from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('client.urls')),
    path('api/users/', include('users.urls.users')),
    path('accounts/', include('users.urls.accounts')),
]
