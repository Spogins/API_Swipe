from django.urls import path, include
from rest_framework import routers
from users.views import UserApiView

router = routers.DefaultRouter()
router.register(r'user', UserApiView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]