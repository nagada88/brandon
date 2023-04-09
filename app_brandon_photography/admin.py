from django.contrib import admin
from app_brandon_photography.models import PhotoCategory, Photos
from .models import BlogPost


class PhotosAdmin(admin.ModelAdmin):
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True
    list_display = ('priority', 'thumbnail_preview', 'category', 'main_site_visibility')

# Register your models here.
admin.site.register(Photos, PhotosAdmin)
admin.site.register(PhotoCategory)
admin.site.register(BlogPost)