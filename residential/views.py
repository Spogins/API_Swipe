
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, decorators, permissions, response, status
from rest_framework.decorators import action

from residential.models import Complex
from residential.serializers import ResidentialSerializer, ResidentialListSerializer


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
        obj = Complex.objects \
            .prefetch_related('gallery__photo_set') \
            .select_related('user') \
            .filter(user=self.request.user).first() # change to one owner can have complex
        return obj

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