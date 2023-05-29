from django.core.validators import MinValueValidator
from django.db import models

from residential.models import Flat, ChessBoard, Complex
from users.models import User


class Announcement(models.Model):
    confirm = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, null=True, blank=True)


class Favorites(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    residential_complex = models.ForeignKey(Complex, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Promotion(models.Model):
    big_announcement = models.BooleanField(default=False)
    up_announcement = models.BooleanField(default=False)
    turbo = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    price = models.FloatField(validators=[MinValueValidator(1.00)])

    class PhraseChoice(models.TextChoices):
        present = ('present', 'Подарок при покупке')
        bargain = ('bargain', 'Возможен торг')
        sea = ('sea', 'Квартира у моря')

    class ColourChoice(models.TextChoices):
        red = 'red'
        green = 'green'

    phrase = models.CharField(max_length=50, choices=PhraseChoice.choices)
    colour = models.CharField(max_length=50, choices=ColourChoice.choices)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)


class AnnouncementRequest(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=True)
    chessboard = models.ForeignKey(ChessBoard, on_delete=models.CASCADE, null=True)
    approve = models.BooleanField(default=False)

