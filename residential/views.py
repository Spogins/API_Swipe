from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from residential.models import Complex
from residential.serializers import ResidentialSerializer


@extend_schema(tags=['Residential Complex'])
class ResidentialComplexSet(viewsets.ModelViewSet):
    serializer_class = ResidentialSerializer
    queryset = Complex.objects.all()
    permission_classes = [IsAuthenticated]