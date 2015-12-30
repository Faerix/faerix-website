from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
import datetime
import random

from .models import *
from .forms import *

def render(request, template, **context):
    content = loader.get_template(template)
    return HttpResponse(content.render(context, request))

def get_flat_page_view(title):
    return lambda request: render(request, "conv/flat_page.html", title=title)

def index(request):
    return render(request, "conv/index.html")

def news(request):
    news = News.objects.filter(visible_from__lte=datetime.datetime.now(), visible_up_to__gte=datetime.datetime.now()).order_by("-visible_from")
    return render(request, "conv/news.html", news=news)


def scenarios(request):
    scenarios = Scenario.objects.filter(validated=True)
    return render(request, "conv/scenarios.html", scenarios=scenarios)

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect(reverse("signup_done"))
    else:
        form = SignUpForm() 

    return render(request, 'conv/signup.html', form=form)

def signup_done(request):
    return render(request, 'conv/signup_done.html')
def subscribe(request):
    return HttpResponse("Placeholder")

def login(request):
    return HttpResponse("Placeholder")

def programme(request):
    return HttpResponse("Placeholder")

def infos(request):
    return HttpResponse("Placeholder")
