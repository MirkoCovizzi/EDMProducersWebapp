from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm


def home(request):
    return render(request, 'edmproducers/home.html')


@login_required
def stream(request):
    return render(request, 'edmproducers/stream.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('stream')
    else:
        form = SignUpForm()
    return render(request, 'edmproducers/signup.html', {'form': form})
