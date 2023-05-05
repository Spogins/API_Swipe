from django.urls import path, include
from rest_framework import routers

from residential.views import ResidentialComplexSet

router = routers.DefaultRouter()
router.register(r'residential_complex', ResidentialComplexSet, basename='residential_complex')

urlpatterns = [
    path('', include(router.urls)),
]