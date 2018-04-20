from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


def root(request):
    if request.user.is_authenticated:
        return redirect('stream')
    else:
        return render(request, 'edmproducers/welcome.html')


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


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadTrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.uploader = request.user
            track.save()
            return redirect('track_detail', profile_slug=request.user.profile.slug, track_slug=track.slug)
    else:
        form = UploadTrackForm()
    return render(request, 'edmproducers/upload.html', {'form': form})


def tracks(request, profile_slug):
    uploader = Profile.objects.get(slug=profile_slug)
    track_list = Track.objects.filter(uploader=uploader.user)
    return render(request, 'edmproducers/tracks.html', {'track_list': track_list})


def track_detail(request, profile_slug, track_slug):
    track = Track.objects.get(slug=track_slug)
    comment_form = CommentTrackForm()
    return render(request, 'edmproducers/track-detail.html', {'track': track, 'comment_form': comment_form})


@login_required
def track_edit(request, profile_slug, track_slug):
    track = get_object_or_404(Track, slug=track_slug, uploader=request.user)
    if request.method == 'POST':
        form = EditTrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            return redirect('track_detail', profile_slug=profile_slug, track_slug=track_slug)
        else:
            return HttpResponse('Invalid entry.')
    else:
        form = EditTrackForm(instance=track)
    return render(request, 'edmproducers/track-edit.html', {'form': form})


@login_required
def track_like(request, profile_slug, track_slug):
    track = get_object_or_404(Track, slug=track_slug)
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


@login_required
def track_comment(request, profile_slug, track_slug):
    track = get_object_or_404(Track, slug=track_slug)
    if request.method == 'POST':
        form = CommentTrackForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.track = track
            comment.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        return HttpResponse('Invalid entry.')


def profile_detail(request, profile_slug):
    profile = get_object_or_404(Profile, slug=profile_slug)
    return render(request, 'edmproducers/profile-detail.html', {'profile': profile})


@login_required
def profile_edit(request, profile_slug):
    profile = get_object_or_404(Profile, slug=profile_slug, user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            return redirect('profile_detail', profile.slug)
        else:
            return HttpResponse('Invalid entry.')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edmproducers/track-edit.html', {'form': form})


@login_required
def profile_follow(request, profile_slug):
    profile = get_object_or_404(Profile, slug=profile_slug)
    if request.method == 'POST':
        followers = profile.followers.all()
        if followers.filter(user=request.user).exists():
            profile.followers.remove(request.user.profile)
            profile.save()
        else:
            profile.followers.add(request.user.profile)
            profile.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    else:
        return HttpResponse('Invalid entry.')


def search(request):
    querystring = request.GET.get('q')
    if querystring:
        queryset = Track.objects.all()
        track_list = queryset.filter(slug__icontains=querystring.lower())
        return render(request, 'edmproducers/search-result.html', {'track_list': track_list})
    else:
        return HttpResponse('Invalid entry.')
