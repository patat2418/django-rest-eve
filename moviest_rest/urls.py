"""moviest_rest URL Configuration

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
from rest_framework import routers

from django.urls import include, path

import movies_rest_app
from movies_rest_app import views
from movies_rest_app.views_generic import *
router = routers.DefaultRouter()
router.register('api/imdb/movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/imdb/', include('movies_rest_app.urls'))
    path('api/version', views.get_version)
]
urlpatterns.extend(router.urls)
router.register('api/imdb/oscars', OscarViewSet, basename='oscar')
urlpatterns.extend(router.urls)
print(urlpatterns)