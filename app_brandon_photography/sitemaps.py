from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost

class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['intro', 'gallery', 'kiskedvenc', 'eskuvo', 'impresszum', 'termek', 'portre', 'video']

    def location(self, item):
        return reverse(item)
        

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.6
    protocol = 'https'
    
    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.updated_at