# для drf-yasg:
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# для остального
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from config import settings

# для drf-yasg:
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls), #admin panel url

    # ckeditor_5
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # swagger api
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API urls - по мере добавления приложений включать их urls.py:
    path('api/common/', include('common.urls')),
    path('api/products/', include('products.urls')),
    # path('api/clinics/', include('clinics.urls')),
]

# для отображения статичных файлов:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
