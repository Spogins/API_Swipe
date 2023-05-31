from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    class RoleChoice(models.TextChoices):
        user = ('user', 'Пользователь')
        manager = ('manager', 'Менеджер')
        administrator = ('admin', 'Администратор')
        builder = ('builder', 'Застройщик')

    role = models.CharField(max_length=50, choices=RoleChoice.choices)


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='users/avatar/', blank=True, null=True)
    black_list = models.BooleanField(blank=True, null=True, default=False)
    turn_to_agent = models.BooleanField(blank=True, null=True, default=False)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    agent_first_name = models.CharField(max_length=20, null=True, blank=True)
    agent_last_name = models.CharField(max_length=20, null=True, blank=True)
    agent_phone = models.IntegerField(null=True, blank=True)
    agent_email = models.EmailField(null=True, blank=True)
    REQUIRED_FIELDS = ['password', 'email']

    def __str__(self):
        return self.email


class Messages(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recipient')


class Subscription(models.Model):
    class TypeChoice(models.TextChoices):
        common = 'common'
        lux = 'lux'

    type = models.CharField(max_length=25, choices=TypeChoice.choices)
    sum = models.FloatField(validators=[MinValueValidator(0.00, _('Sum cannot be less than 0.00'))])


class UserSubscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_date = models.DateTimeField(auto_now_add=True)
    auto_pay = models.BooleanField(default=False)


class Notary(models.Model):
    avatar = models.ImageField(upload_to='users/notary/avatar/', blank=True, null=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = models.IntegerField()
    email = models.EmailField()


class SavedFilters(models.Model):
    district = models.CharField(max_length=100, null=True, blank=True)
    micro_district = models.CharField(max_length=100, null=True, blank=True)
    room_amount = models.IntegerField(null=True, blank=True)
    min_price = models.IntegerField(null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)
    min_square = models.IntegerField(null=True, blank=True)
    max_square = models.IntegerField(null=True, blank=True)

    class HouseStatusChoices(models.TextChoices):
        flat = ('flats', 'Квартири')
        cottage = ('cottage', 'Котедж')
        many_floors = ('many-floors', 'Многоэтажка')
        secondary_market = ('secondary-market', 'Вторичный рынок')

    class HouseTypeChoices(models.TextChoices):
        lux = ('lux', 'Люкс')
        elite = ('elite', 'Элитный')
        common = ('common', 'Стандартный')

    class PaymentChoice(models.TextChoices):
        mortgage = ('mortgage', 'Ипотека')
        parent_capital = ('parent-capital', 'Материнский капитал')

    class PropertyChoice(models.TextChoices):
        living_building = ('living_building', 'Жилое Помещение')

    class LivingConditionsChoice(models.TextChoices):
        draft = ('draft', 'Черновая')
        repair_required = ('repair', 'Нужен ремонт')
        good = ('good', 'В жилом состоянии')

    house_status = models.CharField(max_length=30, choices=HouseStatusChoices.choices, default='flats')
    house_type = models.CharField(max_length=30, choices=HouseTypeChoices.choices, default='common')
    property_status = models.CharField(max_length=50, choices=PropertyChoice.choices)
    living_condition = models.CharField(max_length=50, choices=LivingConditionsChoice.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)






