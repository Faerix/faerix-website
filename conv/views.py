import random
import operator
import csv

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.template import loader
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.db.models import F, Sum, Count

from braces.views import LoginRequiredMixin

from faerix.settings import DEBUG

from .models import *
from .forms import *

def not_frozen(view):
    def new_view(request, *args, **kwargs):
        if settings.FROZEN:
            return get_message_view("danger", "Inscriptions gelées", "Il est désormais impossible de modifier ses incriptions : la conv' approche ou est même passée.<br/>Si c'est important, <a href='{% url 'contact' %}'><b>envoyez nous un mail</b></a>.", 403)(request)
        return view(request, *args, **kwargs)
    return new_view

def render(request, template, status=200, **context):
    content = loader.get_template(template)
    response = HttpResponse(content.render(context, request))
    response.status_code = status
    return response

def get_flat_page_view(title):
    return lambda request,year=currentConv(): render(request, "conv/flat_page.html", title=title, year=yeartourl(year))

def get_message_view(type, title, message, status=200):
    return lambda request,year=currentConv(): render(request, "conv/message.html", status=status, type=type, title=title, message=message, year=yeartourl(year))

def index(request):
    return render(request, "conv/index.html")

def news(request,year=currentConv()):
    news = News.objects.filter(visible_from__lte=timezone.now(), visible_up_to__gte=timezone.now()).order_by("-visible_from")
    return render(request, "conv/news.html", news=news, year=yeartourl(year))

def urltoyear(year):
    if year=='':
        return currentConv()
    return int(year)

def yeartourl(year):
    if year==0 or year==currentConv():
        return ''
    return year

def ronde(request, year=currentConv(), ronde=0):
    ronde = int(ronde)
    year=urltoyear(year)
    scenarios = Scenario.objects.filter(ronde=ronde, conv=year, validated=True)
    events = Event.objects.filter(ronde=ronde, conv=year)
    if request.user.is_authenticated():
        type, activity = request.user.get_activity_at_ronde(year,ronde)
    else:
        type, activity = "", None
    if type.endswith("scenario"):
        scenarios = scenarios.exclude(pk=activity.pk)
    if type.endswith("event"):
        events = events.exclude(pk=activity.pk)
    return render(request, "conv/ronde.html", ronde=ronde, scenarios=scenarios, events=events, busy=bool(type), type=type, activity=activity, year=yeartourl(year))

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
@not_frozen
def subscribe(request, year, type, pk, action):
    model = Scenario if type=="scenario" else Event
    object = get_object_or_404(model, pk=pk)
    if action=="in" and request.user.is_busy_at_ronde(object.conv,object.ronde):
        return get_message_view("danger", "Ubiquité", "Vous participez déjà à un scénario pour cette ronde !", 403)(request)
    if action=="in" and object.complet:
        return get_message_view("danger", "Capacité maximale", "Ce scénario est complet", 403)(request)
    if action=="in":
        object.players.add(request.user)
    else:
        object.players.remove(request.user)
    return HttpResponseRedirect(reverse("ronde", args=(object.conv,object.ronde)))

    return render(request, 'conv/signup.html', form=form, year=yeartourl(year))

def editprofile(request):
    msgs = []
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST)

        if form.is_valid(request.user):
            form.checkandsave(request)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'conv/me.html', form=form, msgs=msgs, attending=request.user.get_attending(currentConv()))

def submitscenario(request):
    msgs = []
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ScenarioForm(request.POST)

        if form.is_valid():
            valid,msgs = form.check(request)
            if valid:
                form.save(request)
                return HttpResponseRedirect(reverse("submit_scenario_done"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ScenarioForm()

    return render(request, 'conv/submit_scenario.html', form=form, msgs=msgs)

def optout(request):
    request.user.editions.add(currentConv())
    return render(request, 'conv/opt.html', going=False)

def optin(request):
    request.user.editions.remove(currentConv())
    return render(request, 'conv/opt.html', going=True)    
'''   

class SubmitScenarioView(LoginRequiredMixin, CreateView):
    template_name = "conv/submit_scenario.html"
    model = Scenario
    fields = ['name', 'max_players', 'min_players', 'system', 'description', 'ronde']
    success_url = reverse_lazy("submit_scenario_done")

    def form_valid(self, form):
         user = self.request.user
         form.instance.conv = currentConvObject()
         if user.is_busy_at_ronde(form.instance.conv,form.instance.ronde):
            return get_message_view("danger", "Ubiquité", "Vous participez déjà à un scénario pour cette ronde !", 403)(self.request)
         form.instance.author = user
         if not(DEBUG):
             send_mail(
                     "Scenario à valider",
                     "Un internaute a soumis un scénario intitulé « {} ».\n Rendez vous sur l'interface d'administration : http://www.faerix.net/admin/conv/scenario/.\nCe mail est automatique.".format(form.instance.name),
                     "",
                     list(map(lambda u: u.email, User.objects.filter(is_staff=True))),
                     fail_silently=True
                     )
         return super().form_valid(form)
         
'''

@staff_member_required
def listings(request):
    return render(request, "conv/listings/index.html")

@staff_member_required
def table_listing(request):
    tables = {}
    for i in range(1,4):
        tables[i] = {
            "scenario": Scenario.objects.filter(ronde=i, validated=True),
            "event": Event.objects.filter(ronde=i),
            }

    return render(request, "conv/listings/tables.html", tables=tables)

@staff_member_required
def user_listing(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participants_rrx.csv"'

    writer = csv.writer(response)
    writer.writerow(["Nom", "Prenom", "pseudo", "email", "telephone"])
    for user in User.objects.all():
        writer.writerow([user.first_name, user.last_name, user.username, user.email, user.phone])

    return response

@staff_member_required
def stats(request):
    scenars = {ronde:Scenario.objects.filter(validated=True, ronde=ronde).annotate(n_players=Count("players")).aggregate(max_capacity=Sum(F('max_players')), min_capacity=Sum(F("min_players")), players_sum=Sum("n_players")) for ronde in range(1,4)}
    events = {ronde:Event.objects.filter(ronde=ronde).annotate(n_players=Count("players")).aggregate(max_capacity=Sum(F('max_players')), min_capacity=Sum(F("min_players")), players_sum=Sum("n_players")) for ronde in range(1,4)}
    totaux = {
            "inscrits": User.objects.all().count(),
            "scenars": Scenario.objects.filter(validated=True).count(),
            "events": Event.objects.all().count(),
            }
    return render(request, "conv/stats.html", totaux=totaux, scenars=scenars, events=events)

@staff_member_required
def spam(request):
    # (type de message, texte)
    msg = ("none", "")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MassMailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sender = "{} <{}>".format(form.cleaned_data["sender_name"], settings.DEFAULT_FROM_EMAIL)
            message = form.cleaned_data["message"]
            subject = form.cleaned_data["subject"]
            targets = (request.user.email,) if form.cleaned_data["preview"] else list(map(operator.itemgetter("email"), User.objects.values("email")))
            n_success = send_mass_mail(
                    map(
                        lambda email: (subject, message, sender, (email, )),
                        targets
                    ),
                    fail_silently=True
            )
            if n_success<len(targets):
                msg = ("danger", "{} messages sur {} n'ont pas pu être envoyés.".format(len(targets)-n_success, len(targets)))
            else:
                msg = ("success", "{} messages envoyés.".format(len(targets)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MassMailForm()

    return render(request, 'conv/mass_mail.html', form=form, msg=msg)


