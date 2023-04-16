
"""core URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Read Newspapers By Topic System API",
        default_version="v1",
        description="Read Newspapers By Topic System api documentation",
        JSON_EDITOR=True,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path(r"api/v1/auth/", include("api_auth.urls")),
        path(r"api/v1/users/", include("api_user.urls")),
        url(r"api/v1/newspaper/", include('api_post.urls')),
    ]
)


urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    url(r"api/v1/auth/", include('api_auth.urls')),
    url(r"api/v1/users/", include('api_user.urls')),
    url(r"api/v1/newspaper/", include('api_post.urls'))
]
