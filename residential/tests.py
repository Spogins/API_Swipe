from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from announcements.models import Announcement
from users.tests import init_scripts, image


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
                                                 "name": ' 1'
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

        announcement_post = self.client.post('/api/v1/announcement_approval/add-requests/',
                                    data={
                                        "announcement": 1
                                    },
                                    format='json')
        assert announcement_post.status_code == status.HTTP_201_CREATED

        # announcement_get = self.client.get('/api/v1/announcement_approval/requests-list/')
        # print(announcement_get)
        # assert announcement_get.status_code == status.HTTP_200_OK

        # announcement_approve = self.client.post(f'/api/v1/announcement_approval/{1}/approve-request/', )
        # print(announcement_approve)
        # assert announcement_approve.status_code == status.HTTP_200_OK





















