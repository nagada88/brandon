from django.contrib import admin
from django.urls import path, include, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.foto, name='foto'),
    re_path(r'foto', views.foto, name='foto'),
    re_path(r'video', views.video, name='video'),
    re_path(r'bio', views.bio, name='bio'),
    re_path(r'kapcsolat', views.kapcsolat, name='kapcsolat'),]