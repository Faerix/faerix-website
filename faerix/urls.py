"""faerix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from conv import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scenarios$', views.scenarios, name='scenarios'),
    url(r'^programme$', views.programme, name='programme'),
    url(r'^subscribe$', views.subscribe, name='subscribe'),
    url(r'^infos$', views.infos, name='infos'),
    url(r'^news$', views.news, name='news'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^login$', views.login, name='login'),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
