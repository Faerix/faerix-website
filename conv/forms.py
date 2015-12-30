from .models import User
from django.forms import ModelForm

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
