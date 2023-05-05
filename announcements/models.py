from django.db import models


class Announcement(models.Model):
    confirm = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

