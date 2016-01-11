from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.template import loader
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
import random

from braces.views import LoginRequiredMixin

from .models import *
from .forms import *

def render(request, template, status=200, **context):
    content = loader.get_template(template)
    response = HttpResponse(content.render(context, request))
    response.status_code = status
    return response

def get_flat_page_view(title):
    return lambda request: render(request, "conv/flat_page.html", title=title)

def get_message_view(type, title, message, status=200):
    return lambda request: render(request, "conv/message.html", status=status, type=type, title=title, message=message)

def index(request):
    return render(request, "conv/index.html")

def news(request):
    news = News.objects.filter(visible_from__lte=timezone.now(), visible_up_to__gte=timezone.now()).order_by("-visible_from")
    return render(request, "conv/news.html", news=news)

def ronde(request, ronde):
    ronde = int(ronde)
    scenarios = Scenario.objects.filter(ronde=ronde, validated=True)
    events = Event.objects.filter(ronde=ronde)
    if request.user.is_authenticated():
        type, activity = request.user.get_activity_at_ronde(ronde)
    else:
        type, activity = "", None
    if type.endswith("scenario"):
        scenarios = scenarios.exclude(pk=activity.pk)
    if type.endswith("event"):
        events = events.exclude(pk=activity.pk)
    return render(request, "conv/ronde.html", ronde=ronde, scenarios=scenarios, events=events, busy=bool(type), type=type, activity=activity)

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

@login_required(redirect_field_name='src')
@require_POST
def subscribe(request, type, pk, action):
    model = Scenario if type=="scenario" else Event
    object = get_object_or_404(model, pk=pk)
    if action=="in" and request.user.is_busy_at_ronde(object.ronde):
        return get_message_view("danger", "Ubiquité", "Vous participez déjà à un scénario pour cette ronde !", 403)(self.request)
    if action=="in":
        object.players.add(request.user)
    else:
        object.players.remove(request.user)
    return HttpResponseRedirect(reverse("ronde", args=(object.ronde,)))

    return render(request, 'conv/signup.html', form=form)

class SubmitScenarioView(LoginRequiredMixin, CreateView):
    template_name = "conv/submit_scenario.html"
    model = Scenario
    fields = ['name', 'max_players', 'min_players', 'universe', 'description', 'ronde']
    success_url = reverse_lazy("submit_scenario_done")
    
    def form_valid(self, form):
         user = self.request.user
         if user.is_busy_at_ronde(form.instance.ronde):
            return get_message_view("danger", "Ubiquité", "Vous participez déjà à un scénario pour cette ronde !", 403)(self.request)
         form.instance.author = user
         return super().form_valid(form)
