from django.http import HttpResponse
from django.template import loader
import datetime
import random

from .models import *

def render(request, template, **context):
    content = loader.get_template(template)
    context["sponsor_logos"]=list(Sponsor.objects.filter(active=True))
    random.shuffle(context["sponsor_logos"])
    return HttpResponse(content.render(context, request))

def index(request):
    return render(request, "conv/news.html", news=[])

def news(request):
    news = News.objects.filter(visible_from__lte=datetime.datetime.now(), visible_up_to__gte=datetime.datetime.now()).order_by("-visible_from")
    return render(request, "conv/news.html", news=news)

def contact(request):
    return HttpResponse("Placeholder")

def scenarios(request):
    scenarios = Scenario.objects.filter(validated=True)
    return render(request, "conv/scenarios.html", scenarios=scenarios)

def subscribe(request):
    return HttpResponse("Placeholder")

def login(request):
    return HttpResponse("Placeholder")

def programme(request):
    return HttpResponse("Placeholder")

def infos(request):
    return HttpResponse("Placeholder")
