from django.db import models

# Create your models here.

class Image(models.Model):
    content = models.ImageField(upload_to='img/')
    description = models.TextField()
    size = models.CharField(max_length = 200)
    predominant_color = models.CharField(max_length = 200)
    average_color = models.CharField(max_length = 200)
    color_palette = models.CharField(max_length = 200)
