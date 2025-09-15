"""
URL configuration for portal_fretes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import Http404

def serve_media(request, path):
    """Serve media files with proper authentication and security checks"""
    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator
    from django.views.decorators.cache import never_cache
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        raise Http404("File not found")
    
    # Serve the file
    return serve(request, path, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fretes.urls')),
]

# Serve static files in production
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files with authentication
if not settings.DEBUG:
    # In production, use custom view with authentication
    urlpatterns += [
        path('media/<path:path>', serve_media, name='serve_media'),
    ]
else:
    # In development, use Django's static serve
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)