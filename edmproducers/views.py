from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


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
        form = UploadTrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.uploader = request.user
            track.save()
            return redirect('tracks/' + track.slug)
    else:
        form = UploadTrackForm()
    return render(request, 'edmproducers/upload.html', {'form': form})


@login_required
def tracks(request):
    track_list = Track.objects.filter(uploader=request.user)
    return render(request, 'edmproducers/tracks.html', {'track_list': track_list})


def track_detail(request, slug):
    track = Track.objects.get(slug=slug)
    return render(request, 'edmproducers/track-detail.html', {'track': track})


@login_required
def track_edit(request, slug):
    track = get_object_or_404(Track, slug=slug, uploader=request.user)
    if request.method == 'POST':
        form = EditTrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            return redirect('track_detail', slug)
        else:
            return HttpResponse('Invalid entry.')
    else:
        form = EditTrackForm(instance=track)
    return render(request, 'edmproducers/track-edit.html', {'form': form})


@login_required
def track_like(request, slug):
    track = get_object_or_404(Track, slug=slug)
    if request.method == 'POST':
        likes = track.like_set.all()
        if likes.filter(user=request.user).exists():
            like = likes.filter(user=request.user).get()
            like.delete()
        else:
            like = Like(user=request.user, track=track)
            like.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    else:
        return HttpResponse('Invalid entry.')


def profile_detail(request, slug):
    profile = Profile.objects.get(slug=slug)
    return render(request, 'edmproducers/profile-detail.html', {'profile': profile})


@login_required
def profile_edit(request, slug):
    profile = get_object_or_404(Profile, slug=slug, user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            return redirect('profile', profile.slug)
        else:
            return HttpResponse('Invalid entry.')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edmproducers/track-edit.html', {'form': form})


def search(request):
    queryset = Track.objects.all()
    track_list = queryset.filter(slug__icontains=request.GET.get('q').lower())
    return render(request, 'edmproducers/search-result.html', {'track_list': track_list})
