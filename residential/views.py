from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, decorators, permissions, response, status
from rest_framework.decorators import action

from residential.models import *
from residential.serializers import *
from users.permissions import *


@extend_schema(tags=['Residential Complex'], )
class ResidentialComplexSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = ResidentialSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    psq_rules = {
        ('list',): [
            Rule([CustomIsAuthenticated], ResidentialSerializer)
        ],
        ('retrieve',): [
            Rule([CustomIsAuthenticated])
        ],
        ('create',): [
            Rule([IsBuilderPermission])
        ],
        ('destroy',): [
            Rule([IsAdminPermission]),
            Rule([IsManagerPermission])
        ],
        ('res_user',): [
            Rule([IsBuilderPermission])
        ],
        ('update_res_user', 'delete_res_user'): [
            Rule([IsBuilderPermission])
        ],
    }

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
                .get(user_id=self.request.user.id)
            return obj
        except:
            return response.Response(data={'data': 'на застройщика не зарегистрирован ЖК'}, status=status.HTTP_400_BAD_REQUEST)

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
        obj = self.user_object()
        obj.delete()
        return response.Response(data={'response': 'ЖК удалён'}, status=status.HTTP_200_OK)




@extend_schema(tags=['Section'])
class SectionView(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = SectionApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    psq_rules = {
        ('list', 'destroy'):
            [Rule([IsAdminPermission], SectionApiSerializer), Rule([IsManagerPermission], SectionApiSerializer)],
        ('section', 'create_section', 'delete_section'):
            [Rule([IsBuilderPermission, IsOwnerPermission], SectionApiSerializer)],
        'retrieve':
            [Rule([CustomIsAuthenticated], SectionApiSerializer)]
    }

    def get_object(self, *args, **kwargs):
        try:
            return Section.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Section.DoesNotExist:
            raise ValidationError({'detail': _('Указаный Section не сужествует')})

    def get_queryset(self):
        queryset = Section.objects.all()
        return queryset

    def get_residential_complex(self):
        try:
            return Complex.objects.get(user=self.request.user)
        except:
            raise ValidationError({'detail': _('ЖК не зарегестрирован')})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='user')
    def section(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(residential_complex__user=request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_section(self, request, *args, **kwargs):
        residential_complex = self.get_residential_complex()
        serializer = self.get_serializer(data=request.data,
                                         context={'residential_complex': residential_complex, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_section(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(residential_complex__user=request.user)
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Corps'])
class CorpsView(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = CorpsApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    psq_rules = {
        ('list', 'destroy'): [
            Rule([IsAdminPermission]),
            Rule([IsManagerPermission])
        ],
        ('corps', 'create_corps'): [
            Rule([IsBuilderPermission])
        ],
        'delete_corps': [
            Rule([IsBuilderPermission, IsOwnerPermission])
        ],
        'retrieve':
            [Rule([CustomIsAuthenticated])]
    }

    def get_object(self, *args, **kwargs):
        try:
            return Corps.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Corps.DoesNotExist:
            raise ValidationError({'detail': _('Указаный corps не сужествует')})

    def get_queryset(self):
        queryset = Corps.objects.all()
        return queryset

    def get_residential_complex(self):
        try:
            return Complex.objects.get(user=self.request.user)
        except:
            raise ValidationError({'detail': _('ЖК не зарегестрирован')})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='user')
    def corps(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(residential_complex__user=request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_corps(self, request, *args, **kwargs):
        residential_complex = self.get_residential_complex()
        serializer = self.get_serializer(data=request.data,
                                         context={'residential_complex': residential_complex, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_corps(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(residential_complex__user=request.user)
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Floor'])
class FloorView(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = FloorApiSerializer
    psq_rules = {
        ('list', 'destroy'):
            [Rule([IsAdminPermission], FloorApiSerializer), Rule([IsManagerPermission], FloorApiSerializer)],
        ('floors_list', 'floors_create', 'floors_delete'):
            [Rule([IsBuilderPermission, IsOwnerPermission], FloorApiSerializer)],
        'retrieve':
            [Rule([CustomIsAuthenticated], FloorApiSerializer)]
    }
    
    def get_object(self, *args, **kwargs):
        try:
            return Floor.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Floor.DoesNotExist:
            raise ValidationError({'detail': _('Указаный этаж не сужествует')})

    def get_queryset(self):
        queryset = Floor.objects.all()
        return queryset

    def get_residential_complex(self):
        try:
            return Complex.objects.get(user=self.request.user)
        except:
            raise ValidationError({'detail': _('ЖК не зарегестрирован')})

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='user')
    def floor(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(residential_complex__user=request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_floor(self, request, *args, **kwargs):
        residential_complex = self.get_residential_complex()
        serializer = self.get_serializer(data=request.data, context={'residential_complex': residential_complex, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_floor(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(residential_complex__user=request.user)
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Documents'])
class DocumentView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = DocumentApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = Documents.objects.all()




@extend_schema(tags=['News'])
class NewsView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = NewsApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = News.objects.all()


@extend_schema(tags=['Flats'])
class FlatView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = FlatApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    psq_rules = {
        'list': [
            Rule([CustomIsAuthenticated], FlatApiSerializer)
        ],
        'retrieve': [
            Rule([CustomIsAuthenticated])
        ],
        ('partial_update', 'destroy'): [
            Rule([IsAdminPermission]), Rule([IsManagerPermission])
        ],
        'flat_user': [
            Rule([IsBuilderPermission, IsOwnerPermission], FlatApiSerializer)
        ],
        ('create_flat_user', 'update_flat_user', 'delete_flat_user'): [
            Rule([IsBuilderPermission, IsOwnerPermission])
        ]
    }


    def get_queryset(self):
        queryset = Flat.objects \
            .prefetch_related('gallery__photo_set') \
            .select_related('corps', 'section', 'floor', 'residential_complex', 'gallery') \
            .all()
        return queryset

    def get_user_obj(self):
        queryset = Flat.objects.filter(residential_complex__user=self.request.user)
        return queryset

    def get_residential_complex(self):
        try:
            return Complex.objects.get(user=self.request.user)
        except:
            raise ValidationError({'detail': _('ЖК не зарегестрирован')})

    @action(methods=['GET'], detail=False, url_path='user')
    def flat_user(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_user_obj())
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_flat_user(self, request, *args, **kwargs):
        residential_complex = self.get_residential_complex()
        serializer = self.get_serializer(data=request.data, context={'residential_complex': residential_complex, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PATCH'], detail=True, url_path='user/update')
    def update_flat_user(self, request, *args, **kwargs):
        obj = self.get_user_obj()
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_flat_user(self, request, *args, **kwargs):
        obj = self.get_user_obj()
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['ChessBoard'])
class ChessBoardView(PsqMixin, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = ChessBoardApiSerializer
    # http_method_names = ['get', 'patch', 'post', 'delete']
    psq_rules = {
        'chessboard_list': [
            Rule([CustomIsAuthenticated], ChessBoardApiSerializer)
        ],
        'retrieve': [
            Rule([CustomIsAuthenticated])
        ],
        'destroy': [
            Rule([IsAdminPermission]),
            Rule([IsManagerPermission])
        ],
        ('chessboard_user', 'create_chessboard_user', 'delete_chessboard_user'): [
            Rule([IsBuilderPermission, IsOwnerPermission])
        ]
    }

    def get_queryset(self):
        queryset = ChessBoard.objects \
            .select_related('corps', 'section', 'residential_complex') \
            .all()
        return queryset

    def get_residential_complex(self):
        try:
            return Complex.objects.get(user=self.request.user)
        except:
            raise ValidationError({'detail': _('ЖК не зарегестрирован')})

    def get_user_obj(self):
        queryset = ChessBoard.objects.filter(residential_complex__user=self.request.user)
        return queryset

    @action(methods=['GET'], detail=False, url_path='list')
    def chessboard_list(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data) 

    @action(methods=['GET'], detail=False, url_path='user')
    def chessboard_user(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_user_obj())
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_chessboard_user(self, request, *args, **kwargs):
        residential_complex = self.get_residential_complex()
        serializer = self.get_serializer(data=request.data, context={'residential_complex': residential_complex, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PATCH'], detail=False, url_path='user/update')
    def update_chessboard_user(self, request, *args, **kwargs):
        obj = self.get_user_obj()
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False, url_path='user/delete')
    def delete_chessboard_user(self, request, *args, **kwargs):
        obj = self.get_user_obj()
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)