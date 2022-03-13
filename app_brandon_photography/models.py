from django.db import models
from PIL import Image
import os
from django.core.validators import MaxValueValidator, MinValueValidator
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html
# Create your models here.

class PhotoCategory(models.Model):

    name = models.CharField(max_length=200)
    priority = models.IntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(1)])

    def __str__(self):
        return self.name

class Photos(models.Model):
    
    category = models.ForeignKey(PhotoCategory, on_delete=models.CASCADE)
    main_site_visibility = models.BooleanField()
    category_cover = models.BooleanField()
    priority = models.IntegerField(default=99, validators=[MaxValueValidator(100), MinValueValidator(1)] )
    # caption = models.TextField()
    photo = models.ImageField(upload_to='app_brandon_photography/img/photos/')
    photo_tumb = models.ImageField(upload_to='app_brandon_photography/img/thumbs/', editable=False, null=True)
    photo_tumb = photo

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.photo_tumb.path) # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(os.path.splitext(self.photo.path))

    @property
    def thumbnail_preview(self):
        if self.photo:
            _thumbnail = get_thumbnail(self.photo,
                                   '300x300',
                                       upscale=False,
                                       crop=False,
                                       quality=100)
            return format_html('<img src="{}" width="{}" height="{}">'.format(_thumbnail.url, _thumbnail.width, _thumbnail.height))
        return ""
