from django.db import models


from main import settings

# Create your models here.

class Image(models.Model):
    #content = models.ImageField(upload_to='img/')
    content = models.ImageField(null=True, blank=True, upload_to='img/', verbose_name = 'Picture')
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
