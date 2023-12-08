"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, re_path, include

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

#All main URLs for the backend also needs to be set in the nginx.conf file from the NGINX Container
urlpatterns = [
    path('endpoint/api/', include('api.urls')),
    path('endpoint/test_db/', include('test_db.urls')),
    path('endpoint/auth/', include("auth.urls")),
    re_path(r'^endpoint/oauth/', include('social_django.urls', namespace='social')),
]

# Enable admin panel if ADMIN_PANEL_ENABLED (in .env-file) is set to True
admin_panel = os.environ.get('ADMIN_PANEL_ENABLED', 'False').lower() == 'true'
if admin_panel:
    urlpatterns.append(path('endpoint/admin/', admin.site.urls))


SOCIAL_AUTH_URL_NAMESPACE = 'social'