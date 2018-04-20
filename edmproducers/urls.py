from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('stream', views.stream, name='stream'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.login, {'template_name': 'edmproducers/login.html'}, name='login'),
    path('logout', auth_views.logout, {'next_page': 'root'}, name='logout'),
    path('upload', views.upload, name='upload'),
    path('search', views.search, name='search'),
    path('<slug:profile_slug>', views.profile_detail, name='profile_detail'),
    path('<slug:profile_slug>/edit', views.profile_edit, name='profile_edit'),
    path('<slug:profile_slug>/tracks', views.tracks, name='tracks'),
    path('<slug:profile_slug>/follow', views.profile_follow, name='profile_follow'),
    path('<slug:profile_slug>/<slug:track_slug>', views.track_detail, name='track_detail'),
    path('<slug:profile_slug>/<slug:track_slug>/edit', views.track_edit, name='track_edit'),
    path('<slug:profile_slug>/<slug:track_slug>/like', views.track_like, name='track_like'),
    path('<slug:profile_slug>/<slug:track_slug>/comment', views.track_comment, name='track_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
