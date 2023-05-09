from django.urls import path, include
from rest_framework import routers
from users.views import UserApiView, NotaryView

router = routers.DefaultRouter()
router.register(r'user', UserApiView, basename='user')
router.register(r'notary', NotaryView, basename='notary')

urlpatterns = [
    path('', include(router.urls)),
]