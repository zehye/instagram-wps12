"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from members.views import signup_view


schema_view = get_schema_view(
    openapi.Info(
        title="WPS instagram API",
        contace=openapi.Contact(email="zehye.01@gmail.com"),
        default_version="v1",
    ),
    public=True
)

urlpatterns_apis = [
    path('members/', include('members.urls.apis')),
    path('posts/', include('posts.urls.apis')),
]

urlpatterns = [
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('apis/', include(urlpatterns_apis)),
    path('admin/', admin.site.urls),
    path('', signup_view, name='signup'),
    path('members/', include('members.urls.views')),
    path('posts/', include('posts.urls.views')),
]
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
