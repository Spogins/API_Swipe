from django.urls import path, include
from rest_framework import routers

from residential.views import *

router = routers.DefaultRouter()
router.register(r'residential_complex', ResidentialComplexSet, basename='residential_complex')
router.register(r'section', SectionView, basename='section')
router.register(r'corps', CorpsView, basename='corps')
router.register(r'floor', FloorView, basename='floor')
router.register(r'flat', FlatView, basename='flat')
router.register(r'document', DocumentView, basename='floor')
router.register(r'news', NewsView, basename='news')
router.register(r'chess_board', ChessBoardView, basename='chess_board')

urlpatterns = [
    path('', include(router.urls)),
]