from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Track, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UploadTrackForm(forms.ModelForm):

    class Meta:
        model = Track
        exclude = ('slug', 'uploader', )


class EditTrackForm(forms.ModelForm):

    class Meta:
        model = Track
        exclude = ('track', 'uploader', )


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user', 'slug', 'following', )
