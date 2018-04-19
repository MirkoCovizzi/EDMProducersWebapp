from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import random
import string

from .utils import upload_track_to


class Genre(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    name = models.CharField(max_length=35)
    slug = models.SlugField()
    bio = models.TextField(max_length=2000, blank=True)
    following = models.ManyToManyField('self', related_name='followers')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        name = 'user' + ''.join([random.choice(string.digits) for n in range(9)])
        Profile.objects.create(user=instance, name=name)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Track(models.Model):
    track = models.FileField(upload_to=upload_track_to)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, blank=True)
    image = models.ImageField(blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Track, self).save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'track'), )


class Comment(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
