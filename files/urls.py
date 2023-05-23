from django.urls import path, include
from rest_framework import routers

from files.views import PhotoAPIDeleteViews

router = routers.DefaultRouter()
router.register(r'photo', PhotoAPIDeleteViews, basename='photo')


urlpatterns = [
    path('', include(router.urls)),
]