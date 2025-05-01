from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger UI configuration
schema_view = get_schema_view(
   openapi.Info(
      title="Brain Station 23 Weather API - Fathi",
      default_version='v1',
      description="Welcome to Brain Station 23 Weather API - Fathi",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include your API URLs here
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
