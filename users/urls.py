from django.urls import path, include
from rest_framework import routers
from users.views import UserApiView, NotaryView, MessagesView

router = routers.DefaultRouter()
router.register(r'user', UserApiView, basename='user')
router.register(r'notary', NotaryView, basename='notary')
router.register(r'messages', MessagesView, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]