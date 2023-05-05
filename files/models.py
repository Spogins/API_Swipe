from django.db import models


class Gallery(models.Model):
    name = models.CharField(max_length=30)


class Photo(models.Model):
    image = models.ImageField(upload_to='gallery/photos/')
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)