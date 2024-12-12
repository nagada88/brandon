from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap, BlogSitemap 
from .views import BlogPostDetailView

sitemaps = {
    'static':StaticSitemap, #add StaticSitemap to the dictionary
    'blog':BlogSitemap #add StaticSitemap to the dictionary
}

urlpatterns = [
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blog_detail'),    
    re_path(r'^$', views.main_site, name='intro'),
    re_path(r'intro', views.main_site, name='intro'),
    re_path(r'kutyafotozas', views.main_site, name='kutyafotozas'),
    re_path(r'impresszum', views.impresszum, name='impresszum'),
    re_path(r'sikeresmail', views.sikeresmail, name='sikeresmail'),
    path('blog/', views.blog, name='blog'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path(r'review', views.review_upload, name='review'),
    path(r'calendar/', views.calendar_view, name='public_calendar'),
    path('mark-unavailable/', views.mark_days_unavailable, name='mark_days_unavailable'),
    path('calendar-partial/', views.calendar_partial_view, name='calendar_partial'),
    re_path(r'kapcsolat', views.kapcsolat, name='kapcsolat'),]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)