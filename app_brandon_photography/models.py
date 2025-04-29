from django.db import models
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile
from django_quill.fields import QuillField
from django.utils.text import slugify

class ImageHandlerMixin():
    def save(self, *args, **kwargs):
        if not self.photo.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        self.photo.delete(save=False)
        self.photo = None

        super(Photos, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo_tumb:
            self.photo_tumb.delete(save=False)
        if self.photo:
            self.photo.delete(save=False)

        super(Photos, self).delete(*args, **kwargs)



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

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Fotó Kategória'
        verbose_name_plural = 'Fotó Kategóriák'

class Review(ImageHandlerMixin, models.Model):
    name = models.CharField(max_length=100)
    stars = models.PositiveSmallIntegerField()  # 1-től 5-ig terjedő érték
    description = models.TextField()
    owner = models.TextField(max_length=200, default="")
    photo = models.ImageField(upload_to='app_brandon_photography/img/photos/', default='app_brandon_photography/img/photos/default.jpg')
    photo_tumb = models.ImageField(upload_to='app_brandon_photography/img/thumbs/',  default='app_brandon_photography/img/photos/default.jpg', editable=False)

    def __str__(self):
        return f"{self.name} ({self.stars} stars)"
    
    class Meta:
        verbose_name = "Vélemény"
        verbose_name_plural = "Vélemények"
    
class Photos(ImageHandlerMixin, models.Model):
    category = models.ForeignKey(PhotoCategory, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='app_brandon_photography/img/photos/')
    photo_tumb = models.ImageField(upload_to='app_brandon_photography/img/thumbs/', editable=False)

    def save(self, *args, **kwargs):
        if not self.photo.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')
            
        self.photo.delete(save=False)
        self.photo = None

        super(Photos, self).save(*args, **kwargs)
   
    def __str__(self):
        return f"{self.category.name} – {os.path.basename(self.photo_tumb.name)}"
    
    class Meta:
        verbose_name = "Fotó"
        verbose_name_plural = "Fotók"

class BlogPost(models.Model):
    main_image = models.ImageField(upload_to='app_brandon_photography/img/photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=200, default="Nagy Ádám")
    title = models.CharField(max_length=200)
    extract = models.CharField(max_length=200)
    content = QuillField()
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatikusan generáljuk a slugot a cím alapján
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Blogposzt'
        verbose_name_plural = 'Blogposztok'

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
    
    class Meta:
        verbose_name = "Elérhetőség"
        verbose_name_plural = "Elérhetőségek"

class Package(ImageHandlerMixin, models.Model):
    photo = models.ImageField(upload_to='app_brandon_photography/img/photos/')
    photo_tumb = models.ImageField(upload_to='app_brandon_photography/img/thumbs/', editable=False)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    duration = models.CharField(max_length=100)
    edited_photos = models.IntegerField()
    extra_photo_price = models.TextField()
    extra_info = models.TextField()
    terms_pdf = models.FileField(upload_to='terms_pdfs/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Csomag"
        verbose_name_plural = "Csomagok"