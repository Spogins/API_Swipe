import os

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from announcements.models import Announcement, AnnouncementRequest, Promotion
from files.models import Gallery
from residential.models import Complex, Section, Corps, Floor, Flat, ChessBoard, News
from swipe.settings import BASE_DIR
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
    return res_complex


def create_flat():
    res_obj = create_res_complex()
    corps = Corps.objects.create(residential_complex=res_obj, name='string')
    section = Section.objects.create(residential_complex=res_obj, name='string')
    floor = Floor.objects.create(residential_complex=res_obj, name='string')
    gallery = Gallery.objects.create(name='flat')
    user = User.objects.get(role__role='builder')
    flat = Flat.objects.create(
        room_amount=1,
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
        residential_complex=res_obj,
        user=user,
        gallery=gallery,
    )
    return flat


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
        elif role == 'manager':
            response = self.client.post(path='/api/auth/login/',
                                        data={'email': 'manager@manager.com', 'password': 'swipe5231'},
                                        format='json')
        else:
            response = self.client.post(path='/api/auth/login/',
                                        data={'email': 'user@user.com', 'password': 'swipe5231'},
                                        format='json')
        return response.data

    def setUp(self) -> None:
        init_scripts()

    # def test_residential_complex_create(self):
    #
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #
    #     response = self.client.post(path='/api/v1/residential_complex/', data={
    #         "photo": image,
    #         "photo_gallery": [
    #             {
    #                 "image": image
    #             }
    #         ],
    #         "name": "string",
    #         "address": "string",
    #         "map_code": "string",
    #         "min_price": 1,
    #         "meter_price": 1,
    #         "description": "string",
    #         "sea_distance": 2147483647,
    #         "gas": True,
    #         "electricity": True,
    #         "house_status": "flats",
    #         "house_type": "lux",
    #         "building_technology": "frame",
    #         "territory": "close",
    #         "ceiling_height": 2,
    #         "heating": "central",
    #         "sewerage": "central",
    #         "water_supply": "central",
    #         "arrangement": "justice",
    #         "payment": "mortgage",
    #         "contract_sum": "full",
    #         "property_status": "living_building"
    #     }, format='json')
    #     assert response.status_code == status.HTTP_201_CREATED
    #
    # def test_complex_delete(self):
    #     obj = create_res_complex()
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     response_d = self.client.delete(path='/api/v1/residential_complex/user/delete/')
    #
    #     assert response_d.status_code == status.HTTP_200_OK
    #
    # def test_complex_update(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     obj = create_res_complex()
    #     response = self.client.patch(path='/api/v1/residential_complex/user/update/', format='json', data={
    #         "photo": image,
    #         "photo_gallery": [
    #             {
    #                 "image": image
    #             }
    #         ],
    #         "name": "string",
    #         "address": "string",
    #         "map_code": "string",
    #         "min_price": 1,
    #         "meter_price": 1,
    #         "description": "string",
    #         "sea_distance": 2147483647,
    #         "gas": True,
    #         "electricity": True,
    #         "house_status": "flats",
    #         "house_type": "lux",
    #         "building_technology": "frame",
    #         "territory": "close",
    #         "ceiling_height": 2,
    #         "heating": "central",
    #         "sewerage": "central",
    #         "water_supply": "central",
    #         "arrangement": "justice",
    #         "payment": "mortgage",
    #         "contract_sum": "full",
    #         "property_status": "living_building"
    #     })
    #     assert response.status_code == status.HTTP_200_OK
    #
    # def test_complex_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     obj = create_res_complex()
    #     response = self.client.get(path='/api/v1/residential_complex/')
    #     assert response.status_code == status.HTTP_200_OK

    # # CORPS TEST
    # def test_corps_create(self):
    #     obj = create_res_complex()
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     response_corps = self.client.post(path='/api/v1/corps/user/create/', data={
    #         "residential_complex": obj.id,
    #         "name": "string"
    #     }, format='json')
    #     assert response_corps.status_code == status.HTTP_201_CREATED
    #
    # def test_corps_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     res_obj = create_res_complex()
    #     corps = Corps.objects.create(residential_complex=res_obj, name='string')
    #     response = self.client.delete(path=f'/api/v1/corps/{corps.id}/')
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #
    # def test_corps_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     res_obj = create_res_complex()
    #     corps = Corps.objects.create(residential_complex=res_obj, name='string')
    #     response = self.client.get(path=f'/api/v1/corps/')
    #     assert response.status_code == status.HTTP_200_OK

    # # SECTION TEST
    # def test_section_create(self):
    #     obj = create_res_complex()
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     response_section = self.client.post(path='/api/v1/section/user/create/', data={
    #         "residential_complex": obj.id,
    #         "name": "string"
    #     }, format='json')
    #     assert response_section.status_code == status.HTTP_201_CREATED
    #
    # def test_section_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     res_obj = create_res_complex()
    #     section = Section.objects.create(residential_complex=res_obj, name='string')
    #     response = self.client.delete(path=f'/api/v1/section/{section.id}/')
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #
    # def test_section_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     res_obj = create_res_complex()
    #     section = Section.objects.create(residential_complex=res_obj, name='string')
    #     response = self.client.get(path=f'/api/v1/section/')
    #     assert response.status_code == status.HTTP_200_OK

    # # FLOOR TEST
    # def test_floor_create(self):
    #     obj = create_res_complex()
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     response_floor = self.client.post(path='/api/v1/floor/user/create/', data={
    #         "residential_complex": obj.id,
    #         "name": "string"
    #     }, format='json')
    #     assert response_floor.status_code == status.HTTP_201_CREATED
    #
    # def test_floor_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     res_obj = create_res_complex()
    #     floor = Floor.objects.create(residential_complex=res_obj, name='string')
    #     response = self.client.delete(path=f'/api/v1/floor/{floor.id}/')
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #
    # def test_floor_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     res_obj = create_res_complex()
    #     floor = Floor.objects.create(residential_complex=res_obj, name='string')
    #     response = self.client.get(path=f'/api/v1/floor/')
    #     assert response.status_code == status.HTTP_200_OK

    # # FLAT TEST
    # def test_flat_creation(self):
    #     res_obj = create_res_complex()
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     corps = Corps.objects.create(residential_complex=res_obj, name='string')
    #     section = Section.objects.create(residential_complex=res_obj, name='string')
    #     floor = Floor.objects.create(residential_complex=res_obj, name='string')
    #     response_flat = self.client.post(path='/api/v1/flat/user/create/',
    #                                      data={
    #                                          "residential_complex": {
    #                                              "name": f'{res_obj.id}'
    #                                          },
    #                                          "section": {
    #                                              "name": f'{section.id}'
    #                                          },
    #                                          "floor": {
    #                                              "name": f'{floor.id}'
    #                                          },
    #                                          "corps": {
    #                                              "name": f'{corps.id}'
    #                                          },
    #                                          "scheme": image,
    #                                          "photo_gallery": [
    #                                              {
    #                                                  "image": image
    #                                              }
    #                                          ],
    #                                          "room_amount": 2147483647,
    #                                          "price": 1,
    #                                          "square": 2147483647,
    #                                          "kitchen_square": 2147483647,
    #                                          "balcony": True,
    #                                          "commission": 2147483647,
    #                                          "district": "string",
    #                                          "micro_district": "string",
    #                                          "living_condition": "draft",
    #                                          "planning": "studio-bathroom"
    #                                      },
    #                                      format='json')
    #
    #     assert response_flat.status_code == status.HTTP_201_CREATED
    #
    # def test_flat_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     flat = create_flat()
    #     response = self.client.delete(path=f'/api/v1/flat/{flat.id}/user/delete/')
    #     assert response.status_code == status.HTTP_200_OK
    #
    # def test_flat_update(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     flat = create_flat()
    #     corps = Corps.objects.create(residential_complex=flat.residential_complex, name='string')
    #     section = Section.objects.create(residential_complex=flat.residential_complex, name='string')
    #     floor = Floor.objects.create(residential_complex=flat.residential_complex, name='string')
    #     response = self.client.patch(path=f'/api/v1/flat/{flat.id}/user/update/', format='json', data={
    #         "residential_complex": {
    #             "name": f"{flat.residential_complex.id}"
    #         },
    #         "section": {
    #             "name": f"{section.id}"
    #         },
    #         "floor": {
    #             "name": f"{floor.id}"
    #         },
    #         "corps": {
    #             "name": f"{corps.id}"
    #         },
    #         "scheme": image,
    #         "photo_gallery": [
    #             {
    #                 "image": image
    #             }
    #         ],
    #         "room_amount": 2147483647,
    #         "price": 1,
    #         "square": 2147483647,
    #         "kitchen_square": 2147483647,
    #         "balcony": True,
    #         "commission": 2147483647,
    #         "district": "string",
    #         "micro_district": "string",
    #         "living_condition": "draft",
    #         "planning": "studio-bathroom"
    #     })
    #     assert response.status_code == status.HTTP_200_OK
    #
    # def test_flat_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     flat = create_flat()
    #     response = self.client.get(path=f'/api/v1/flat/')
    #     assert response.status_code == status.HTTP_200_OK
    #
    # def test_flat_detail(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     flat = create_flat()
    #     response = self.client.get(path=f'/api/v1/flat/{flat.id}/user/detail/')
    #     assert response.status_code == status.HTTP_200_OK

    # # CHESSBOARD TEST
    # def test_chessboard_create(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     res_obj = create_res_complex()
    #     corps = Corps.objects.create(residential_complex=res_obj, name='string')
    #     section = Section.objects.create(residential_complex=res_obj, name='string')
    #     request_chess = self.client.post(path='/api/v1/chess_board/user/create/',
    #                                      data={
    #                                          "section": {
    #                                              "name": f"{section.id}"
    #                                          },
    #                                          "corps": {
    #                                              "name": f"{corps.id}"
    #                                          }
    #                                      },
    #                                      format='json')
    #     assert request_chess.status_code == status.HTTP_201_CREATED
    #
    # def test_chessboard_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     res_obj = create_res_complex()
    #     corps = Corps.objects.create(residential_complex=res_obj, name='string')
    #     section = Section.objects.create(residential_complex=res_obj, name='string')
    #     chess = ChessBoard.objects.create(residential_complex=res_obj, corps=corps, section=section)
    #     request_chess = self.client.delete(path=f'/api/v1/chess_board/{chess.id}/user/delete/')
    #     assert request_chess.status_code == status.HTTP_200_OK
    #
    # def test_chessboard_update(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     res_obj = create_res_complex()
    #     corps = Corps.objects.create(residential_complex=res_obj, name='string')
    #     section = Section.objects.create(residential_complex=res_obj, name='string')
    #     chess = ChessBoard.objects.create(residential_complex=res_obj, corps=corps, section=section)
    #     request_chess = self.client.patch(path=f'/api/v1/chess_board/{chess.id}/user/update/', format='json', data={
    #         "section": {
    #             "name": f"{section.id}"
    #         },
    #         "corps": {
    #             "name": f"{corps.id}"
    #         }
    #     })
    #     assert request_chess.status_code == status.HTTP_200_OK
    #
    # def test_chessboard_list(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     res_obj = create_res_complex()
    #     corps = Corps.objects.create(residential_complex=res_obj, name='string')
    #     section = Section.objects.create(residential_complex=res_obj, name='string')
    #     chess = ChessBoard.objects.create(residential_complex=res_obj, corps=corps, section=section)
    #     request_chess = self.client.get(path='/api/v1/chess_board/user/')
    #     assert request_chess.status_code == status.HTTP_200_OK

    # # ANNOUNCEMENT TEST
    # def test_announcement_request_post(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     flat = create_flat()
    #     announcement = Announcement.objects.create(flat=flat)
    #     announcement_post = self.client.post(path='/api/v1/announcement_approval/add-requests/',
    #                                          data={
    #                                              "announcement": announcement.id
    #                                          },
    #                                          format='json')
    #     assert announcement_post.status_code == status.HTTP_201_CREATED
    #
    # def test_approve_announcement_request(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("manager").get("access_token")}')
    #     flat = create_flat()
    #     announcement = Announcement.objects.create(flat=flat)
    #     chessboard = ChessBoard.objects.create(section=flat.section, corps=flat.corps,
    #                                            residential_complex=flat.residential_complex)
    #     announcement_r = AnnouncementRequest.objects.create(announcement=announcement, chessboard=chessboard)
    #     response = self.client.post(path=f'/api/v1/announcement_approval/{announcement_r.id}/approve-request/')
    #     assert response.status_code == status.HTTP_200_OK
    #
    # def test_announcement_request_get(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     announcement_get = self.client.get(path='/api/v1/announcement_approval/requests-list/')
    #     assert announcement_get.status_code == status.HTTP_200_OK
    #
    # def test_announcement_request_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("manager").get("access_token")}')
    #     flat = create_flat()
    #     announcement = Announcement.objects.create(flat=flat)
    #     chessboard = ChessBoard.objects.create(section=flat.section, corps=flat.corps,
    #                                            residential_complex=flat.residential_complex)
    #     announcement_r = AnnouncementRequest.objects.create(announcement=announcement, chessboard=chessboard)
    #     response = self.client.delete(path=f'/api/v1/announcement_approval/{announcement_r.id}/request/delete/')
    #     assert response.status_code == status.HTTP_200_OK

    # # NEWS TEST
    # def test_news_create(self):
    #     obj = create_res_complex()
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     response = self.client.post(path='/api/v1/news/', format='json', data={
    #         "residential_complex": obj.id,
    #         "title": "string",
    #         "text": "string"
    #     })
    #     assert response.status_code == status.HTTP_201_CREATED
    #
    # def test_news_update(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     obj = create_res_complex()
    #     news = News.objects.create(title='string', text='string', residential_complex=obj)
    #     response = self.client.patch(path=f'/api/v1/news/{news.id}/user/update/', format='json', data={
    #         "residential_complex": obj.id,
    #         "title": "string",
    #         "text": "string"
    #     })
    #     assert response.status_code == status.HTTP_200_OK
    #
    # def test_news_delete(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     obj = create_res_complex()
    #     news = News.objects.create(title='string', text='string', residential_complex=obj)
    #     response = self.client.delete(path=f'/api/v1/news/{news.id}/user/delete/')
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #
    # def test_news_get(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     obj = create_res_complex()
    #     news = News.objects.create(title='string', text='string', residential_complex=obj)
    #     response = self.client.get(path=f'/api/v1/news/user/')
    #     assert response.status_code == status.HTTP_200_OK

    # PROMOTION TEST
    def test_promotion_type_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
        flat = create_flat()
        obj = Announcement.objects.create(flat=flat)
        response = self.client.post(path='/api/v1/promotion/',
                                    data={
                                        "big_announcement": True,
                                        "up_announcement": True,
                                        "turbo": True,
                                        "price": 1,
                                        "phrase": "present",
                                        "colour": "red",
                                        "announcement": obj.id
                                    },
                                    format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_promotion_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
        flat = create_flat()
        obj = Announcement.objects.create(flat=flat)
        promo = Promotion.objects.create(price=4, announcement=obj, phrase='present', colour='red')
        response = self.client.patch(path=f'/api/v1/promotion/{promo.id}/',
                                    data={
                                        "big_announcement": True,
                                        "up_announcement": False,
                                        "turbo": True,
                                        "price": 1,
                                        "phrase": "present",
                                        "colour": "red",
                                        "announcement": obj.id
                                    },
                                    format='json')
        assert response.status_code == status.HTTP_200_OK

    #
    # def test_savedfilters_create(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user().get("access_token")}')
    #     response = self.client.post(path='/api/v1/saved_filters/user/create/',
    #                                 data={
    #                                     "district": "string",
    #                                     "micro_district": "string",
    #                                     "room_amount": 2147483647,
    #                                     "min_price": 2147483647,
    #                                     "max_price": 2147483647,
    #                                     "min_square": 2147483647,
    #                                     "max_square": 2147483647,
    #                                     "house_status": "flats",
    #                                     "house_type": "lux",
    #                                     "property_status": "living_building",
    #                                     "living_condition": "draft"
    #                                 },
    #                                 format='json')
    #     assert response.status_code == status.HTTP_201_CREATED
    #
    # def test_notary_create(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("admin").get("access_token")}')
    #     response = self.client.post(path='/api/v1/notary/',
    #                                 data={
    #                                     "avatar": image,
    #                                     "name": "string",
    #                                     "surname": "string",
    #                                     "phone": 2147483647,
    #                                     "email": "user@example.com"
    #                                 },
    #                                 format='json')
    #     assert response.status_code == status.HTTP_201_CREATED

    # def test_documents_creation(self):
    #     obj = create_res_complex()
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.login_user("builder").get("access_token")}')
    #     response_creation = self.client.post(path='/api/v1/document/user/create/',
    #                                          data={
    #                                              'name': 'test',
    #                                              'residential_complex': obj.id,
    #                                              'document': os.path.join(BASE_DIR, 'files/test_document/test.txt')
    #                                          })
    #     print(response_creation)
    #     assert response_creation.status_code == status.HTTP_201_CREATED
