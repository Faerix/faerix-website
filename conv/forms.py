from .models import *
from django.conf import settings
from django.core.exceptions import ValidationError
import django.forms

from faerix.settings import DEBUG

class SignUpForm(django.forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email')

## check that a user can't subscribe to several activities via django admin

class CheckingEventForm(django.forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"

    def clean(self):
        super().clean()
        for player in self.cleaned_data.get("players"):
            player.get_activity_at_ronde(self.cleaned_data.get("conv"),self.cleaned_data.get("ronde"))
        if len(self.cleaned_data.get("players"))>self.cleaned_data.get("max_players"):
            raise ValidationError("Too many players")
        return self.cleaned_data

class ProfileForm(django.forms.ModelForm):
    password = django.forms.CharField(label="Entrer votre mot de passe pour sauvegarder les changements",max_length=32, widget=django.forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone','password')

    def is_valid(self,user):
        valid = super(ProfileForm, self).is_valid()

        try:
            if user.check_password(self.cleaned_data["password"]):
                return valid

        except KeyError:
            self._errors['password']="Il faut entrer votre mot de passe."
            return False

        self._errors['password']="Le mot de passe que vous avez entré est incorrect."
        return False

    def checkandsave(self,request):
        if not request.user.check_password(self.cleaned_data["password"]):
            return ""


class ScenarioForm(django.forms.Form):
    name = django.forms.CharField(label="Titre", max_length=200)
    min_players = django.forms.IntegerField(label="Nombre minimal de PJ")
    max_players = django.forms.IntegerField(label="Nombre maximal de PJ")
    system = django.forms.CharField(label="Système", max_length=200, initial="D&D, Appel de Cthulu ou autre...")
    description = django.forms.CharField(label="Description",widget=django.forms.Textarea, max_length=10000)
    #ronde = django.forms.IntegerField("Ronde", choices=((1, "1 : Samedi 14h−20h"), (2, "2 : Samedi à partir de 20h"), (3, "3 : Dimanche 10h-16h")))
    ronde1 = django.forms.BooleanField(label="Ronde 1 (Samedi 14h−20h)", initial=False, required=False)
    ronde2 = django.forms.BooleanField(label="Ronde 2 (Samedi à partir de 20h)", initial=False, required=False)
    ronde3 = django.forms.BooleanField(label="Ronde 3 (Dimanche 10h-16h)", initial=False, required=False)

    def check(self,request):
        msgs=[]
        user = request.user
        conv = currentConvObject()
        if(self.cleaned_data['ronde1']):
            if user.is_busy_at_ronde(conv,1):
                msgs.append("Vous participez déjà à un scénario pendant la ronde 1 !")
        if(self.cleaned_data['ronde2']):
            if user.is_busy_at_ronde(conv,2):
                msgs.append("Vous participez déjà à un scénario pendant la ronde 2 !")
        if(self.cleaned_data['ronde3']):
            if user.is_busy_at_ronde(conv,3):
                msgs.append("Vous participez déjà à un scénario pendant la ronde 3 !")
        if(not(self.cleaned_data['ronde1'] or self.cleaned_data['ronde2'] or self.cleaned_data['ronde3'])):
            msgs.append("Vous devez séléctionner au moins une ronde !")
        return (msgs==[],msgs)

    def save_ronde(self,request,_ronde):
        scenario = Scenario(
            name=self.cleaned_data['name'],
            min_players=self.cleaned_data['min_players'],
            max_players=self.cleaned_data['max_players'],
            description=self.cleaned_data['description'],
            system=self.cleaned_data['system'],
            author=request.user,
            conv=currentConvObject(),
            ronde=_ronde,
            validated=False,
        )
        scenario.save()

    def save(self,request):
        if(self.cleaned_data['ronde1']):
            self.save_ronde(request,1)
        if(self.cleaned_data['ronde2']):
            self.save_ronde(request,2)
        if(self.cleaned_data['ronde3']):
            self.save_ronde(request,3)
        if not(DEBUG):
            send_mail(
                "Scenario à valider",
                "Un internaute a soumis un scénario intitulé « {} ».\n Rendez vous sur l'interface d'administration : http://www.faerix.net/admin/conv/scenario/.\nCe mail est automatique.".format(request),
                "",
                list(map(lambda u: u.email, User.objects.filter(is_staff=True))),
                fail_silently=True
            )

class CheckingScenarioForm(django.forms.ModelForm):
    class Meta:
        model = Scenario
        fields = "__all__"

    def clean(self):
        super().clean()
        for player in self.cleaned_data.get("players"):
            player.get_activity_at_ronde(self.cleaned_data.get("conv"),self.cleaned_data.get("ronde"))
        if len(self.cleaned_data.get("players"))>self.cleaned_data.get("max_players"):
            raise ValidationError("Too many players")
        self.cleaned_data.get("author").get_activity_at_ronde(self.cleaned_data.get("conv"),self.cleaned_data.get("ronde"))
        return self.cleaned_data

class MassMailForm(django.forms.Form):
    sender_name = django.forms.CharField(max_length=100, initial="RRX", label="Nom apparent de l'auteur ({})".format(settings.DEFAULT_FROM_EMAIL))
    subject = django.forms.CharField(max_length=100, label="Sujet")
    preview = django.forms.BooleanField(required=False, initial=True, label="Preview (n'envoyer le mail qu'à vous pour une dernière relecture)")
    message = django.forms.CharField(widget=django.forms.Textarea, label="Texte")

