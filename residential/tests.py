from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from announcements.models import Announcement
from files.models import Gallery
from residential.models import Complex, Section, Corps, Floor, Flat
from users.models import User
from users.tests import init_scripts, image


def create_res_complex():
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


class ComplexTests(APITestCase):

    def login_user(self, role=None):
        if role == 'admin':
            response = self.client.post(path='/api/auth/login/',
                                        data={'email': 'admin@admin.com', 'password': 'swipe5231'},
                                        format='json')
        elif role == 'builder':
            response = self.client.post(path='/api/auth/login/',
                                        data={'email': 'builder@builder.com', 'password': 'swipe5231'},
                                        format='json')
        else:
            response = self.client.post(path='/api/auth/login/',
                                        data={'email': 'user@user.com', 'password': 'swipe5231'},
                                        format='json')
        return response.data

    def setUp(self) -> None:
        init_scripts()

    def test_residential_complex_create(self):

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.login_user("builder").get("access_token")}')

        response = self.client.post(path='/api/v1/residential_complex/', data={
            "photo": image,
            "photo_gallery": [
                {
                    "image": image
                }
            ],
            "name": "string",
            "address": "string",
            "map_code": "string",
            "min_price": 1,
            "meter_price": 1,
            "description": "string",
            "sea_distance": 2147483647,
            "gas": True,
            "electricity": True,
            "house_status": "flats",
            "house_type": "lux",
            "building_technology": "frame",
            "territory": "close",
            "ceiling_height": 2,
            "heating": "central",
            "sewerage": "central",
            "water_supply": "central",
            "arrangement": "justice",
            "payment": "mortgage",
            "contract_sum": "full",
            "property_status": "living_building"
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_res_items(self):
        create_res_complex()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.login_user("builder").get("access_token")}')
        response_corps = self.client.post('/api/v1/corps/user/create/', data={
            "residential_complex": 1,
            "name": "string"
        }, format='json')
        assert response_corps.status_code == status.HTTP_201_CREATED

        response_section = self.client.post('/api/v1/section/user/create/', data={
            "residential_complex": 1,
            "name": "string"
        }, format='json')
        assert response_section.status_code == status.HTTP_201_CREATED

        response_floor = self.client.post('/api/v1/floor/user/create/', data={
            "residential_complex": 1,
            "name": "string"
        }, format='json')
        assert response_floor.status_code == status.HTTP_201_CREATED

        response_flat = self.client.post('/api/v1/flat/user/create/',
                                         data={
                                             "residential_complex": {
                                                 "name": '1'
                                             },
                                             "section": {
                                                 "name": '1'
                                             },
                                             "floor": {
                                                 "name": '1'
                                             },
                                             "corps": {
                                                 "name": '1'
                                             },
                                             "scheme": image,
                                             "photo_gallery": [
                                                 {
                                                     "image": image
                                                 }
                                             ],
                                             "room_amount": 2147483647,
                                             "price": 1,
                                             "square": 2147483647,
                                             "kitchen_square": 2147483647,
                                             "balcony": True,
                                             "commission": 2147483647,
                                             "district": "string",
                                             "micro_district": "string",
                                             "living_condition": "draft",
                                             "planning": "studio-bathroom"
                                         },
                                         format='json')

        assert response_flat.status_code == status.HTTP_201_CREATED

        request_chess = self.client.post('/api/v1/chess_board/user/create/',
                                         data={
                                             "section": {
                                                 "name": "1"
                                             },
                                             "corps": {
                                                 "name": "1"
                                             }
                                         },
                                         format='json')
        assert request_chess.status_code == status.HTTP_201_CREATED

        announcement_post = self.client.post('/api/v1/announcement_approval/add-requests/',
                                             data={
                                                 "announcement": 1
                                             },
                                             format='json')
        assert announcement_post.status_code == status.HTTP_201_CREATED

        response = self.client.post('/api/v1/promotion/',
                                    data={
                                        "big_announcement": True,
                                        "up_announcement": True,
                                        "turbo": True,
                                        "price": 1,
                                        "phrase": "present",
                                        "colour": "red",
                                        "announcement": 1
                                    },
                                    format='json')
        print(response)
        assert response.status_code == status.HTTP_201_CREATED

    def test_announcement_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.login_user("admin").get("access_token")}')
        announcement_get = self.client.get('/api/v1/announcement_approval/requests-list/')
        assert announcement_get.status_code == status.HTTP_200_OK

    # def test_promotion_type_creation(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.login_user("admin").get("access_token")}')
    #     response = self.client.post('/api/v1/promotion/',
    #                                 data={
    #                                     "big_announcement": True,
    #                                     "up_announcement": True,
    #                                     "turbo": True,
    #                                     "price": 1,
    #                                     "phrase": "present",
    #                                     "colour": "red",
    #                                     "announcement": 1
    #                                 },
    #                                 format='json')
    #     print(response)
    #     assert response.status_code == status.HTTP_201_CREATED
