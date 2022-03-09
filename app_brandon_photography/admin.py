from django.contrib import admin

from app_brandon_photography.models import PhotoCategory, Photos

# Register your models here.
admin.site.register(Photos)
admin.site.register(PhotoCategory)