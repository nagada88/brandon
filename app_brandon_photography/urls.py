from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^$', views.mainpage, name='mainpage'),
    re_path(r'^$', views.foto, name='foto'),
    re_path(r'foto', views.foto, name='foto'),
    re_path(r'video', views.video, name='video'),
    re_path(r'bio', views.bio, name='bio'),
    re_path(r'kapcsolat', views.kapcsolat, name='kapcsolat'),]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)