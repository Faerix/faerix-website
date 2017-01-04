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


handler404 = views.get_message_view("danger", "404", """<b>404</b> Cette page n'existe pas.""", status=404)
handler500 = views.get_message_view("danger", "500", """<b>500</b> Une erreur est survenue en traitant votre demande. Réessayez ultérieurement.""", status=500)
handler403 = views.get_message_view("danger", "403", """<b>403</b> Accès refusé""", status=403)
handler400 = views.get_message_view("danger", "400", """<b>400</b> Votre navigateur a fait une requête incompréhensible. Désolé.""", status=400)

urlpatterns = [
    url(r'^$', views.get_flat_page_view("Les Rencontres Rôlistes de l'X"), name='index'),
    url(r'^old/(?P<year>[0-9]{4})/',include('faerix.urls.extra')),

    url(r'^scenarios/submit$', views.not_frozen(views.submitscenario), name='submit_scenario'),
    url(r'^scenarios/submit/done$', views.get_message_view("success", "Propostion enregistrée", """Votre scénario a bien été enregistré. Il sera relu et validé très prochainement."""), name='submit_scenario_done'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/done$', views.get_message_view("success", "Compte créé", """Votre compte a été créé avec succès. Pour l'activer et choisir votre mot de passe, passez par le <a class=alert-link href="{% url 'password_reset' %}">formulaire « mot de passe perdu »</a>"""), name='signup_done'),
    url(r'^me$', views.editprofile, name='me'),
    url(r'^me/opt-out$', views.optout, name="opt-out"),
    url(r'^me/opt-in$', views.optin, name="opt-in"),
    url(r'^stats$', views.stats, name='stats'),
    url(r'^spam$', views.spam, name='spam'),

    url(r'^listings$', views.listings, name="listing!index"),
    url(r'^listings/tables$', views.table_listing, name="listing!tables"),
    url(r'^listings/users$', views.user_listing, name="listing!users"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^front-edit/', include('front.urls')),
    url(r'^hijack/', include('hijack.urls')),

    url(r'^(?P<year>)',include('faerix.urls.extra')),
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
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

