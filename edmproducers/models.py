from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=35)


class Tag(models.Model):
    word = models.CharField(max_length=35)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=2000)
    following = models.ManyToManyField('self', related_name='followers')


class Song(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=1000)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    description = models.TextField(max_length=2000)
    allow_download = models.BooleanField(default=False)
    producer = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
