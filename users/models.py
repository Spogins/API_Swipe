from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField(blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatar/', blank=True, null=True)
    black_list = models.BooleanField(blank=True, null=True, default=False)
    turn_to_agent = models.BooleanField(blank=True, null=True, default=False)
    is_active = models.BooleanField(blank=True, null=True, default=True)

    class NotificationChoices(models.TextChoices):
        me = 'me'
        me_agent = 'me-agent'
        agent = 'agent'
        disabled = 'disabled'

    notifications = models.CharField(max_length=15, choices=NotificationChoices.choices, default='me', blank=True, null=True,)

    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return self.email
