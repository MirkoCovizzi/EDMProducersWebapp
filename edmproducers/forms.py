from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UploadTrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = ('track', 'title', 'genre', 'description', )


class CommentTrackForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )


class EditTrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = ('title', 'genre', 'description', )


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'bio', )
