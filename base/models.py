from django.db import models
import uuid

# Create your models here.
class Meme(models.Model):
    photo = models.ImageField(upload_to="media/")
    caption = models.CharField(max_length=50000)
    meme_text = models.CharField(max_length=50000)