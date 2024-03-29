from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, permissions, response, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from announcements.models import Announcement, Favorites, Promotion
from announcements.serializers import *
from users.permissions import IsAdminPermission, IsManagerPermission, IsBuilderPermission, IsOwnerPermission


# Create your views here.
@extend_schema(tags=['Announcement'], )
class AnnouncementView(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = AnnouncementApiSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self, *args, **kwargs):
        try:
            return Announcement.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Announcement.DoesNotExist:
            raise ValidationError({'detail': _('Указаный Announcement не сужествует')})

    def get_queryset(self):
        queryset = Announcement.objects.all()
        return queryset

    @action(methods=['GET'], detail=False, url_path='user')
    def announcement(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(flat__user_id=request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['PATCH'], detail=True, url_path='user/update')
    def update_announcement(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_announcement(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(residential_complex__user=request.user)
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Favorite Announcement'])
class FavoritesView(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = FavoritesApiSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self, *args, **kwargs):
        try:
            return Favorites.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Favorites.DoesNotExist:
            raise ValidationError({'detail': _('Указаный Messages не сужествует')})

    def get_queryset(self):
        queryset = Favorites.objects.all()
        return queryset

    @action(methods=['GET'], detail=False, url_path='user')
    def favorites(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(user=request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_favorites(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'user': request.user, 'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_favorites(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(residential_complex__user=request.user)
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Promotion Announcement'])
class PromotionView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = PromotionApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = Promotion.objects.all()


@extend_schema(tags=['AnnouncementOnChessboard'])
class AnnouncementOnChessboard(PsqMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = AddRequestAnnouncement

    psq_rules = {
        ('requests_list', 'add_request', 'delete_favorites'): [
            Rule([IsAdminPermission]),
            Rule([IsManagerPermission])
        ],
        'create_req':
            [Rule([IsBuilderPermission | IsAdminPermission | IsManagerPermission | IsOwnerPermission, permissions.IsAuthenticated])]
    }

    def get_object(self, *args, **kwargs):
        try:
            return AnnouncementRequest.objects.get(pk=self.kwargs.get(self.lookup_field))
        except AnnouncementRequest.DoesNotExist:
            raise ValidationError({'detail': _('Указаный запрос на ддобавление не сужествует')})

    @action(methods=['POST'], detail=False, url_path='add-requests')
    def create_req(self, request):
        serializer = AddRequestAnnouncement(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path='requests-list')
    def requests_list(self, request):
        obj = self.paginate_queryset(AnnouncementRequest.objects.filter(approve=False))
        serializer = RequestAnnouncementSerializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=True, url_path='approve-request')
    def add_request(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            chess_board = obj.chessboard
            chess_board.flat.add(obj.announcement.flat)
            chess_board.save()
            obj.approve = True
            obj.save()
            return response.Response(data={'detail': _('Обьявление добавленно в шахматку')}, status=status.HTTP_200_OK)
        except:
            return response.Response(data={'detail': _('Error')}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['DELETE'], detail=True, url_path='request/delete')
    def delete_favorites(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)

