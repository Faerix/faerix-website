from .models import User, Scenario, Event
from django.forms import ModelForm

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email')

## check that a user can't subscribe to several activities via django admin

class CheckingEventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"

    def clean(self):
        super().clean()
        for player in self.cleaned_data.get("players"):
            player.get_activity_at_ronde(self.cleaned_data.get("ronde"))
        return self.cleaned_data

class CheckingScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        fields = "__all__"

    def clean(self):
        super().clean()
        for player in self.cleaned_data.get("players"):
            player.get_activity_at_ronde(self.cleaned_data.get("ronde"))
        return self.cleaned_data

