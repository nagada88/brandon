from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap 

sitemaps = {
    'static':StaticSitemap #add StaticSitemap to the dictionary
}

urlpatterns = [
    re_path(r'^$', views.intro, name='intro'),
    re_path(r'intro', views.intro, name='intro'),
    re_path(r'gallery', views.gallery, name='gallery'),
    re_path(r'kiskedvenc', views.kiskedvenc, name='kiskedvenc'),
    path(r'eskuvo', views.eskuvo, name='eskuvo'),
    re_path(r'impresszum', views.impresszum, name='impresszum'),
    re_path(r'termek', views.termek, name='termek'),
    re_path(r'portre', views.portre, name='portre'),
    re_path(r'video', views.video, name='video'),
    re_path(r'marketing', views.marketing, name='marketing'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'kapcsolat', views.kapcsolat, name='kapcsolat'),]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)