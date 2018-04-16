from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, TrackForm
from .models import Track, Profile


def home(request):
    if request.user.is_authenticated:
        return redirect('stream')
    else:
        return render(request, 'edmproducers/home.html')


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


@login_required
def stream(request):
    return render(request, 'edmproducers/stream.html')


@login_required
def upload(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.uploader = request.user
            track.save()
            return redirect('tracks/' + track.slug)
    else:
        form = TrackForm()
    return render(request, 'edmproducers/upload.html', {'form': form})


@login_required
def tracks(request):
    track_list = Track.objects.filter(uploader=request.user)
    return render(request, 'edmproducers/tracks.html', {'track_list': track_list})


def track_detail(request, slug):
    track = Track.objects.get(slug=slug)
    return render(request, 'edmproducers/track-detail.html', {'track': track})


def profile_detail(request, slug):
    profile = Profile.objects.get(slug=slug)
    return render(request, 'edmproducers/profile-detail.html', {'profile': profile})


def search(request):
    queryset = Track.objects.all()
    track_list = queryset.filter(slug__icontains=request.GET.get('q').lower())
    return render(request, 'edmproducers/search-result.html', {'track_list': track_list})
