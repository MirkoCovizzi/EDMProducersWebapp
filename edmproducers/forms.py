from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Track


class SignUpForm(UserCreationForm):
    profile_name = forms.CharField(help_text="Required. Insert your public profile name.")

    class Meta:
        model = User
        fields = ('profile_name', 'email', 'password1', 'password2', )


class TrackForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(required=False)

    class Meta:
        model = Track
        exclude = ('slug', 'uploader', )
