from django.core.validators import MinValueValidator
from django.db import models

from files.models import Gallery
from users.models import User


# from users.models import User


class Complex(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    map_code = models.TextField()
    min_price = models.FloatField(validators=[MinValueValidator(1.00)])
    meter_price = models.FloatField(validators=[MinValueValidator(1.00)])
    description = models.TextField()
    photo = models.ImageField(upload_to='residential_complex/photos/')
    sea_distance = models.IntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    gas = models.BooleanField(default=True)
    electricity = models.BooleanField(default=True)

    class HouseStatusChoices(models.TextChoices):
        flat = ('flats', 'Квартири')
        cottage = ('cottage', 'Котедж')
        many_floors = ('many-floors', 'Многоэтажка')
        secondary_market = ('secondary-market', 'Вторичный рынок')

    class HouseTypeChoices(models.TextChoices):
        lux = ('lux', 'Люкс')
        elite = ('elite', 'Элитный')
        common = ('common', 'Стандартный')

    class BuildingTechnologyChoices(models.TextChoices):
        frame = ('frame', 'Монолитный каркас')
        foam = ('foam', 'Пенобетон')
        brick = ('brick', 'Керпич')

    class TerritoryChoices(models.TextChoices):
        close = ('close', 'Закрытая')
        open = ('open', 'Открытая')
        protected = ('protected', 'Охраняемая')

    class CeilingChoices(models.IntegerChoices):
        two = 2
        there = 3

    class HeatingChoices(models.TextChoices):
        central = ('central', 'Центральное')

    class SewerageChoices(models.TextChoices):
        central = ('central', 'Центральное')

    class WaterSuplyChoices(models.TextChoices):
        central = ('central', 'Центральное')

    class ArrangementChoice(models.TextChoices):
        justice = ('justice', 'Юстиція')

    class PaymentChoice(models.TextChoices):
        mortgage = ('mortgage', 'Ипотека')
        parent_capital = ('parent-capital', 'Материнский капитал')

    class ContractSumChoice(models.TextChoices):
        full = ('full', 'Полная')
        part = ('part', 'Частями')

    class PropertyChoice(models.TextChoices):
        living_building = ('living_building', 'Жилое Помещение')

    house_status = models.CharField(max_length=30, choices=HouseStatusChoices.choices, default='flats')
    house_type = models.CharField(max_length=30, choices=HouseTypeChoices.choices, default='common')
    building_technology = models.CharField(max_length=30, choices=BuildingTechnologyChoices.choices, default='brick')
    territory = models.CharField(max_length=30, choices=TerritoryChoices.choices, default='close')
    ceiling_height = models.IntegerField(choices=CeilingChoices.choices, default=2)
    heating = models.CharField(max_length=30, choices=HeatingChoices.choices, default='central')
    sewerage = models.CharField(max_length=30, choices=SewerageChoices.choices, default='central')
    water_supply = models.CharField(max_length=30, choices=WaterSuplyChoices.choices, default='central')
    arrangement = models.CharField(max_length=50, choices=ArrangementChoice.choices)
    payment = models.CharField(max_length=50, choices=PaymentChoice.choices)
    contract_sum = models.CharField(max_length=50, choices=ContractSumChoice.choices)
    property_status = models.CharField(max_length=50, choices=PropertyChoice.choices)

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    gallery = models.ForeignKey(Gallery, on_delete=models.PROTECT)