from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stream', views.stream, name='stream'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.login, {'template_name': 'edmproducers/login.html'}, name='login'),
    path('logout', auth_views.logout, {'next_page': 'home'}, name='logout'),
    path('upload', views.upload, name='upload'),
    path('tracks', views.tracks, name='tracks'),
    path('tracks/<slug:slug>', views.track_detail, name='track_detail'),
    path('search', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
