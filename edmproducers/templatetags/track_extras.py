from django import template

register = template.Library()


@register.filter(name='check_track_like_exists')
def check_track_like_exists(track_object, user):
    likes = track_object.like_set.all()
    return likes.filter(user=user).exists()
