from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('client.urls')),
    path('api/users/', include('users.urls.users')),
    path('api/products/', include('products.urls')),
    path('accounts/', include('users.urls.accounts')),
    path('alarms/', include('alarms.urls')),
]

urlpatterns += [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]