#encoding: utf8
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
    url(r'^ronde/(?P<ronde>\d)$', views.ronde, name='ronde'),
    url(r'^subscribe/(?P<type>scenario|event)/(?P<pk>\d+)/(?P<action>in|out)$', views.subscribe, name='subscribe'),
    url(r'^news$', views.news, name='news'),
    url(r'^conference$', views.conference, name='conference'),

    url(r'^stats$', views.stats, name='stats'),

    url(r'^listings$', views.listings, name="listing!index"),
    url(r'^listings/tables$', views.table_listing, name="listing!tables"),
    url(r'^listings/users$', views.user_listing, name="listing!users"),
    url(r'^listings/cards$', views.cards_listing, name="listing!cards"),
]


flat_pages = {
        "programme" : "Programme",
        "contact" : "Contact",
        "infos" : "Infos Pratiques",
        }

for name, title in flat_pages.items():
    urlpatterns.append(url('^'+name+"$", views.get_flat_page_view(title), name=name))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
