from django.urls import path, include
from rest_framework import routers

from announcements.views import AnnouncementView


router = routers.DefaultRouter()
router.register(r'announcement', AnnouncementView, basename='announcement')


urlpatterns = [
    path('', include(router.urls)),
]