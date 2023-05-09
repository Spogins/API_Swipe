
from django.shortcuts import render
from drf_psq import PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, decorators, permissions, response, status
from rest_framework.decorators import action

from residential.models import *
from residential.serializers import *


@extend_schema(tags=['Residential Complex'], )
class ResidentialComplexSet(viewsets.ModelViewSet):
    serializer_class = ResidentialSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Complex.objects \
            .prefetch_related('gallery__photo_set') \
            .select_related('user') \
            .all()
        return queryset

    def user_object(self):
        try:
            obj = Complex.objects \
                .prefetch_related('gallery__photo_set') \
                .select_related('user') \
                .get(user=self.request.user)
            return obj
        except:
            return response.Response(data={'data': 'something go wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path='user')
    def res_user(self, request, *args, **kwargs):
        obj = self.user_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=False, url_path='user/update')
    def update_res_user(self, request, *args, **kwargs):
        obj = self.user_object()
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False, url_path='user/delete')
    def delete_res_user(self, request, *args, **kwargs):
        try:
            obj = self.user_object()
            obj.delete()
            return response.Response(data={'response': 'ЖК удалён'}, status=status.HTTP_200_OK)
        except:
            return response.Response(data={'response': 'что то пошло не так'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Section'])
class SectionView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = SectionApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = Section.objects.all()


@extend_schema(tags=['Corps'])
class CorpsView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = CorpsApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = Corps.objects.all()


@extend_schema(tags=['Floor'])
class FloorView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = FloorApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = Floor.objects.all()

