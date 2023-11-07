from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from apps.core.types import APIUrlPatternsType, UrlCompositePatternsType, UrlPatternsType

api_urlpatterns: UrlPatternsType = [
    # path('admin/', admin.site.urls),
    path('', include('apps.client.urls')),
    path('api/users/', include('apps.users.urls.users')),
    path('api/products/', include('apps.products.urls')),
    path('accounts/', include('apps.users.urls.accounts')),
    path('alarms/', include('apps.alarms.urls')),
]

swagger_urlpatterns: APIUrlPatternsType = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns: UrlCompositePatternsType = api_urlpatterns + swagger_urlpatterns