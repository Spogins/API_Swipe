from django.urls import path, include
from rest_framework import routers
from users.views import *

router = routers.DefaultRouter()
router.register(r'user', UserApiView, basename='user')
router.register(r'notary', NotaryView, basename='notary')
router.register(r'messages', MessagesView, basename='messages')
router.register(r'saved_filters', SavedFiltersView, basename='saved_filters')
router.register(r'subscription', SubscriptionAPIViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]