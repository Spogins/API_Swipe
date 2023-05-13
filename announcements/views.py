from django.shortcuts import render
from drf_psq import PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, permissions

from announcements.models import Announcement
from announcements.serializers import AnnouncementApiSerializer


# Create your views here.
@extend_schema(tags=['Announcement'], )
class AnnouncementView(viewsets.ModelViewSet):
    serializer_class = AnnouncementApiSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = Announcement.objects.all()



