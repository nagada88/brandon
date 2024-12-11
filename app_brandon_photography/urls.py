from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap, BlogSitemap 

sitemaps = {
    'static':StaticSitemap, #add StaticSitemap to the dictionary
    'blog':BlogSitemap #add StaticSitemap to the dictionary
}

urlpatterns = [
    re_path(r'^$', views.kiskedvenc, name='intro'),
    re_path(r'intro', views.kiskedvenc, name='intro'),
    re_path(r'gallery', views.gallery, name='gallery'),
    re_path(r'kutyafotozas', views.kiskedvenc, name='kutyafotozas'),
    path(r'eskuvo', views.eskuvo, name='eskuvo'),
    re_path(r'impresszum', views.impresszum, name='impresszum'),
    re_path(r'sikeresmail', views.sikeresmail, name='sikeresmail'),
    re_path(r'termek', views.termek, name='termek'),
    re_path(r'portre', views.portre, name='portre'),
    re_path(r'video', views.video, name='video'),
    re_path(r'marketing', views.marketing, name='marketing'),
    path(r'blog', views.blog, name='blog'),
    re_path(r'blogpost', views.blogpost, name='blogpost'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path(r'review', views.review_upload, name='review'),
    path(r'calendar/', views.calendar_view, name='public_calendar'),
    # path('edit/<str:date>/', views.edit_availability, name='edit_availability'),
    path('mark-unavailable/', views.mark_days_unavailable, name='mark_days_unavailable'),
    path('calendar-partial/', views.calendar_partial_view, name='calendar_partial'),
    re_path(r'kapcsolat', views.kapcsolat, name='kapcsolat'),]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)