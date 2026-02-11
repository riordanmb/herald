"""
URL configuration for Herald project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1
    path('api/v1/', include([
        path('manuscripts/', include('apps.manuscripts.urls')),
        path('heraldry/', include('apps.heraldry.urls')),
        path('recession/', include('apps.recession.urls')),
        path('transcription/', include('apps.transcription.urls')),
        path('markup/', include('apps.markup.urls')),
        path('search/', include('apps.search.urls')),
    ])),

    # Authentication
    path('api/auth/', include('apps.authentication.urls')),
    path('api/auth/', include('rest_framework.urls')),  # Browsable API login
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Customize admin site
admin.site.site_header = 'Herald Administration'
admin.site.site_title = 'Herald Admin'
admin.site.index_title = 'Heraldic Manuscript Management'
