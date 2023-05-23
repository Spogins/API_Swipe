from django.urls import path, include
from rest_framework import routers

from announcements.views import AnnouncementView, FavoritesView, PromotionView

router = routers.DefaultRouter()
router.register(r'announcement', AnnouncementView, basename='announcement')
router.register(r'favorites', FavoritesView, basename='favorites')
router.register(r'promotion', PromotionView, basename='promotion')


urlpatterns = [
    path('', include(router.urls)),
]