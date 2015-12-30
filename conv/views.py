from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.template import loader
from django.core.urlresolvers import reverse, reverse_lazy
import datetime
import random

from braces.views import LoginRequiredMixin

from .models import *
from .forms import *

def render(request, template, **context):
    content = loader.get_template(template)
    return HttpResponse(content.render(context, request))

def get_flat_page_view(title):
    return lambda request: render(request, "conv/flat_page.html", title=title)

def get_message_view(type, title, message):
    return lambda request: render(request, "conv/message.html", type=type, title=title, message=message)

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
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect(reverse("signup_done"))
    else:
        form = SignUpForm() 

    return render(request, 'conv/signup.html', form=form)

def subscribe(request):
    return HttpResponse("Placeholder")

class SubmitScenarioView(LoginRequiredMixin, CreateView):
    template_name = "conv/submit_scenario.html"
    model = Scenario
    fields = ['name', 'max_players', 'min_players', 'universe', 'description']
    success_url = reverse_lazy("signup_done")
    
    def form_valid(self, form):
         user = self.request.user
         form.instance.author = user
         return super().form_valid(form)
