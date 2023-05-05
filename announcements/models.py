from django.db import models


class Announcement(models.Model):
    confirm = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)


class Promotion(models.Model):
    big_announcement = models.BooleanField(default=False)
    up_announcement = models.BooleanField(default=False)
    turbo = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

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


