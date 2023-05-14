from django.urls import path, include
from rest_framework import routers

from announcements.views import AnnouncementView, FavoritesView

router = routers.DefaultRouter()
router.register(r'announcement', AnnouncementView, basename='announcement')
router.register(r'favorites', FavoritesView, basename='favorites')


urlpatterns = [
    path('', include(router.urls)),
]