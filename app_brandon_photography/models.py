from django.db import models

# Create your models here.

class PhotoCategory(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Photos(models.Model):
    
    category = models.ForeignKey(PhotoCategory, on_delete=models.CASCADE)
    main_site_visibility = models.BooleanField()
    category_cover = models.BooleanField()
    caption = models.TextField()
    img_url = models.ImageField(upload_to='static/img/')

