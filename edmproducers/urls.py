from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stream', views.stream, name='stream'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.login, {'template_name': 'edmproducers/login.html'}, name='login'),
    path('logout', auth_views.logout, {'next_page': 'home'}, name='logout'),
]
