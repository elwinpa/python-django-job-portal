from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class ApplyForm(ModelForm):
    class Meta:
        model=Candidates
        fields="__all__"

class RegisterForm(ModelForm):
    class Meta:
        model=Company
        fields=('position', 'description', 'salary', 'experience', 'Location')
