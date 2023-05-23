from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import gettext_lazy as _
from users.permissions import *


# Create your views here.
@extend_schema(tags=['Photo'])
class PhotoAPIDeleteViews(PsqMixin,
                          GenericViewSet):
    serializer_class = None
    http_method_names = ['delete']

    psq_rules = {
        'destroy': [
            Rule([IsAdminPermission]),
            Rule([IsManagerPermission])
        ],
        ('residential_photo_delete', 'flat_photo_delete'): [
            Rule([IsResidentialComplexOrFlatPhotoOwner])
        ],
        'chessboard_flat_photo_delete': [
            Rule([IsChessBoardFlatPhotoOwner])
        ]
    }

    def get_object(self, *args, **kwargs):
        try:
            return Photo.objects.select_related('gallery__residentialcomplex',
                                                'gallery__chessboardflat',
                                                'gallery__flat') \
                .get(pk=self.kwargs.get(self.lookup_field))
        except Photo.DoesNotExist:
            raise ValidationError({'detail': _('Photo does not exist.')})

    def delete_object(self):
        obj = self.get_object()
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        return self.delete_object()

    @action(methods=['DELETE'], detail=True, url_path='residential-complex/delete')
    def residential_photo_delete(self, request, *args, **kwargs):
        return self.delete_object()

    @action(methods=['DELETE'], detail=True, url_path='flat/delete')
    def flat_photo_delete(self, request, *args, **kwargs):
        return self.delete_object()

    @action(methods=['DELETE'], detail=True, url_path='chessboard-flat/delete')
    def chessboard_flat_photo_delete(self, request, *args, **kwargs):
        return self.delete_object()