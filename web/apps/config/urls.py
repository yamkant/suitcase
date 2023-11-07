from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import URLPattern
from core.types import APIUrlPatternsType, UrlCompositePatternsType, UrlPatternsType

api_urlpatterns: UrlPatternsType = [
    # path('admin/', admin.site.urls),
    path('', include('client.urls')),
    path('api/users/', include('users.urls.users')),
    path('api/products/', include('products.urls')),
    path('accounts/', include('users.urls.accounts')),
    path('alarms/', include('alarms.urls')),
]

swagger_urlpatterns: APIUrlPatternsType = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns: UrlCompositePatternsType = api_urlpatterns + swagger_urlpatterns