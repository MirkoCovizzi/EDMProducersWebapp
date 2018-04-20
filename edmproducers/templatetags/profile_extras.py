from django import template

register = template.Library()


@register.filter(name='check_profile_follow_exists')
def check_profile_follow_exists(profile_object, user):
    followers = profile_object.followers.all()
    return followers.filter(user=user).exists()
