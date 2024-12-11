from django.db import models
from PIL import Image
from io import BytesIO
import os
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html
from django.conf import settings
from django.conf.urls.static import static
from django_quill.fields import QuillField
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class ImageHandlerMixin():
    def save(self, *args, **kwargs):
        if not self.photo.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(ImageHandlerMixin, self).save(*args, **kwargs)


    def make_thumbnail(self):

        image = Image.open(self.photo)
        image.thumbnail((1000,1000), Image.BICUBIC)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.photo_tumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True   


class PhotoCategory(models.Model):

    name = models.CharField(max_length=200)
    priority = models.IntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(1)])
    category_cover = models.ImageField(default = 'app_brandon_photography/img/photos/IMG_3266.JPG/', upload_to='app_brandon_photography/img/photos/')

    def __str__(self):
        return self.name

class Review(ImageHandlerMixin, models.Model):
    name = models.CharField(max_length=100)
    stars = models.PositiveSmallIntegerField()  # 1-től 5-ig terjedő érték
    description = models.TextField()
    owner = models.TextField(max_length=200, default="")
    photo = models.ImageField(upload_to='app_brandon_photography/img/photos/', default='app_brandon_photography/img/photos/default.jpg')
    photo_tumb = models.ImageField(upload_to='app_brandon_photography/img/thumbs/',  default='app_brandon_photography/img/photos/default.jpg', editable=False)

    def __str__(self):
        return f"{self.name} ({self.stars} stars)"
    
class Photos(models.Model):
    category = models.ForeignKey(PhotoCategory, on_delete=models.CASCADE)
    main_site_visibility = models.BooleanField()
    priority = models.IntegerField(default=99, validators=[MaxValueValidator(1000), MinValueValidator(1)] )
    photo = models.ImageField(upload_to='app_brandon_photography/img/photos/')
    photo_tumb = models.ImageField(upload_to='app_brandon_photography/img/thumbs/', editable=False)

    def save(self, *args, **kwargs):
        if not self.photo.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(Photos, self).save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.photo)
        image.thumbnail((1000,1000), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.photo_tumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

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


class BlogPost(models.Model):
    main_image = models.ImageField(upload_to='app_brandon_photography/img/photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=200, default="Nagy Ádám")
    title = models.CharField(max_length=200)
    extract = models.CharField(max_length=200)
    content = QuillField()

    def get_absolute_url(self):
        return "/blogpost.html?blogpost_id=%i" % self.id


class Availability(models.Model):
    AVAILABLE = 'green'
    PARTIALLY_BOOKED = 'yellow'
    UNAVAILABLE = 'red'
    
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (PARTIALLY_BOOKED, 'Partially Booked'),
        (UNAVAILABLE, 'Unavailable'),
    ]

    date = models.DateField(unique=True)  # Egyedi dátum
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=AVAILABLE)
    notes = models.TextField(blank=True, null=True)  # Opcionális jegyzetek az admin számára

    def __str__(self):
        return f"{self.date} - {self.get_status_display()}"











#
# class Photos(models.Model):
#
#     category = models.ForeignKey(PhotoCategory, on_delete=models.CASCADE)
#     main_site_visibility = models.BooleanField()
#     category_cover = models.BooleanField()
#     priority = models.IntegerField(default=99, validators=[MaxValueValidator(100), MinValueValidator(1)] )
#     # caption = models.TextField()
#     photo = models.ImageField(upload_to='app_brandon_photography/img/photos/')
#     photo_tumb = models.ImageField(upload_to='app_brandon_photography/img/thumbs/', editable=False, default=photo.url)
#     # photo_tumb = photo
#
#     def save(self):
#         super().save()  # saving image first
#
#         img = Image.open(self.photo_tumb.path) # Open image using self
#
#         if img.height > 300 or img.width > 300:
#             new_img = (500, 500)
#             img.thumbnail(new_img)
#             img.save(os.path.splitext(self.photo.path))
#
#     @property
#     def thumbnail_preview(self):
#         if self.photo:
#             _thumbnail = get_thumbnail(self.photo,
#                                    '300x300',
#                                        upscale=False,
#                                        crop=False,
#                                        quality=100)
#             return format_html('<img src="{}" width="{}" height="{}">'.format(_thumbnail.url, _thumbnail.width, _thumbnail.height))
#         return ""
