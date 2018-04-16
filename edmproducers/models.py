from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from .utils import upload_track_to


class Genre(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name


class Tag(models.Model):
    word = models.CharField(max_length=35)

    def __str__(self):
        return self.word


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_name = models.TextField(max_length=35)
    slug = models.SlugField()
    bio = models.TextField(max_length=2000, blank=True)
    following = models.ManyToManyField('self', related_name='followers')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.user.username = slugify(self.profile_name)
        super(Profile, self).save(*args, **kwargs)


class Track(models.Model):
    track = models.FileField(upload_to=upload_track_to)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    description = models.TextField(max_length=2000, blank=True)
    allow_download = models.BooleanField(default=False)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Track, self).save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Track, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
