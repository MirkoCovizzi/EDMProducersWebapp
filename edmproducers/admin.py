from django.contrib import admin

from .models import Genre, Profile, Track, Like, Comment

# Register your models here.

admin.site.register(Genre)
admin.site.register(Profile)
admin.site.register(Track)
admin.site.register(Like)
admin.site.register(Comment)
