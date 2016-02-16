from .models import User, Scenario, Event
from django.conf import settings
from django.core.exceptions import ValidationError
import django.forms

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
            player.get_activity_at_ronde(self.cleaned_data.get("ronde"))
        if len(self.cleaned_data.get("players"))>self.cleaned_data.get("max_players"):
            raise ValidationError("Too many players")
        return self.cleaned_data

class CheckingScenarioForm(django.forms.ModelForm):
    class Meta:
        model = Scenario
        fields = "__all__"

    def clean(self):
        super().clean()
        for player in self.cleaned_data.get("players"):
            player.get_activity_at_ronde(self.cleaned_data.get("ronde"))
        if len(self.cleaned_data.get("players"))>self.cleaned_data.get("max_players"):
            raise ValidationError("Too many players")
        self.cleaned_data.get("author").get_activity_at_ronde(self.cleaned_data.get("ronde"))
        return self.cleaned_data


class MassMailForm(django.forms.Form):
    sender_name = django.forms.CharField(max_length=100, initial="RRX", label="Nom apparent de l'auteur ({})".format(settings.DEFAULT_FROM_EMAIL))
    subject = django.forms.CharField(max_length=100, label="Sujet")
    preview = django.forms.BooleanField(required=False, initial=True, label="Preview (n'envoyer le mail qu'à vous pour une dernière relecture)")
    message = django.forms.CharField(widget=django.forms.Textarea, label="Texte")

