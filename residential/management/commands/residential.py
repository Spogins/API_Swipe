from django.core.management.base import BaseCommand

from announcements.models import Announcement
from files.models import Gallery, Photo
from residential.models import *
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Complex.objects.all():
            gallery = Gallery.objects.create(name='residential')
            user = User.objects.get(role__role='builder')
            res_complex = Complex.objects.create(
                name='RsComplex',
                address='string',
                map_code='string',
                min_price=1000,
                meter_price=1000,
                description='string',
                photo='#',
                sea_distance=5,
                gas=True,
                electricity=True,
                house_status='flats',
                house_type='lux',
                building_technology='frame',
                territory='close',
                ceiling_height=2,
                heating='central',
                sewerage='central',
                water_supply='central',
                arrangement='justice',
                payment='mortgage',
                contract_sum='full',
                property_status='living_building',
                gallery=gallery,
                user=user,
            )
            for ct in range(3):
                photo = Photo.objects.create(
                    image='#',
                    gallery=res_complex.gallery
                )
            print('Residential create')
            for ct in range(3):
                section = Section.objects.create(name=f'{res_complex.name } section{ct}', residential_complex=res_complex)
                print(f'{res_complex.name } section{ct} created')
                corps = Corps.objects.create(name=f'{res_complex.name } corps{ct}', residential_complex=res_complex)
                print(f'{res_complex.name} corps{ct} created')
                floor = Floor.objects.create(name=f'{res_complex.name } floor{ct}', residential_complex=res_complex)
                print(f'{res_complex.name} floor{ct} created')

                for fl in range(3):
                    gallery = Gallery.objects.create(name='flat')
                    flat = Flat.objects.create(
                        room_amount=1+fl,
                        scheme='#',
                        price=5000,
                        square=50,
                        kitchen_square=10,
                        balcony=True,
                        commission=500,
                        district='string',
                        micro_district='string',
                        living_condition='draft',
                        planning='studio-bathroom',
                        corps=corps,
                        section=section,
                        floor=floor,
                        residential_complex=res_complex,
                        user=user,
                        gallery=gallery,
                    )
                    for gal in range(3):
                        photo = Photo.objects.create(
                            image='#',
                            gallery=flat.gallery
                        )
                    print('flat created')
                    print('add flat on chess_board')
                    announcement = Announcement.objects.create(confirm=True, flat=flat)
                    print('announcement created')
            print('OBJECTS CREATED')

