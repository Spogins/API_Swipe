from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/avatar/', blank=True, null=True)
    black_list = models.BooleanField(blank=True, null=True, default=False)
    turn_to_agent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=500)

    class NotificationChoices(models.TextChoices):
        me = 'me'
        me_agent = 'me-agent'
        agent = 'agent'
        disabled = 'disabled'

    notifications = models.CharField(max_length=15, choices=NotificationChoices.choices, default='me')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name', 'surname']

    def __str__(self):
        return self.email
