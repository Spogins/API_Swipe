from dj_rest_auth.registration.views import RegisterView
from django.views.generic.base import TemplateResponseMixin, View
from django.utils.translation import gettext_lazy as _
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import viewsets, permissions, response, status, generics
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView

from users.permissions import *
from users.serializers import *



class UerEmailCheck(viewsets.GenericViewSet):
    serializer_class = UerEmailCheckSerializer
    http_method_names = ['post']
    @action(detail=False, methods=['POST'])
    def check(self, request, *args, **kwargs):
        email = request.data['email']
        try:
            if User.objects.get(email=email):
                return response.Response(data={'check': True}, status=status.HTTP_200_OK)
            else:
                return response.Response(data={'check': False}, status=status.HTTP_200_OK)
        except:
            return response.Response(data={'check': False}, status=status.HTTP_200_OK)


class ConfirmCongratulationView(TemplateResponseMixin, View):
    template_name = 'account/email/congratulations.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class BuilderRegisterView(RegisterView):
    serializer_class = BuilderRegistrationSerializer


@extend_schema(tags=['User'])
class UserApiView(PsqMixin, generics.ListCreateAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = UserApiSerializer
    parser_classes = [JSONParser, MultiPartParser]
    # http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    permission_classes = [IsAdminPermission]

    psq_rules = {
        ('list', 'block', 'unblock'): [Rule([IsManagerPermission | IsAdminPermission], UserAdminApiSerializer)],
        ('profile_usr', 'profile_update'): [Rule([IsAuthenticated], UserApiSerializer)],
        'create': [Rule([IsAdminPermission], UserAdminApiSerializer)],
        'managers_list': [Rule([CustomIsAuthenticated], UserRegistrationSerializer)]
    }

    def change_serializer(self, request):
        content_type = request.content_type
        if 'application/json' in content_type:
            return UserApi64Serializer
        elif 'multipart/form-data' in content_type:
            return UserApiSerializer


    def profile_obj(self):
        try:
            obj = User.objects.get(id=self.request.user.id)
            return obj
        except:
            return response.Response(data={'data': 'something go wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, *args, **kwargs):
        try:
            return User.objects.get(pk=self.kwargs.get('pk'))
        except User.DoesNotExist:
            raise ValidationError({'detail': _('error.')})


    def create(self, request, *args, **kwargs):
        serializer = self.change_serializer(request)(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)






    @action(detail=True, methods=['POST'])
    def block(self, request, *args, **kwargs):
        user = self.get_object()
        if user.black_list:
            return response.Response(data={'detail': _('Пользователь уже заблокирован.')}, status=status.HTTP_400_BAD_REQUEST)
        if user.role.role == 'admin':
            return response.Response(data={'detail': _('Вы не можете заблокировать этого пользователя.')},
                            status=status.HTTP_403_FORBIDDEN)
        user.black_list = True
        user.save()
        return response.Response(data={'detail': _('Пользователь заблокирован.')}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST'])
    def unblock(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.black_list:
            return response.Response(data={'detail': _('Пользователь не заблокирован.')}, status=status.HTTP_400_BAD_REQUEST)
        user.black_list = False
        user.save()
        return response.Response({'detail': _('Пользователь розблокирован')}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='profile')
    def profile_usr(self, request, *args, **kwargs):
        obj = self.profile_obj()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=False, url_path='profile/update')
    def profile_update(self, request, *args, **kwargs):
        obj = self.profile_obj()
        serializer = self.change_serializer(request)(data=request.data, instance=obj, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Notary'])
class NotaryView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = NotaryApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Notary.objects.all()

    psq_rules = {
        ('list', 'create', 'retrieve', 'destroy'):
            [Rule([IsAdminPermission]), Rule([IsManagerPermission])],
        ('partial_update',):
            [Rule([IsAdminPermission], NotaryApiSerializer), Rule([IsManagerPermission], NotaryApiSerializer)]
    }


@extend_schema(tags=['Messages'])
class MessagesView(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = MessageApiSerializer
    psq_rules = {
        'send_to_manager': [
            Rule([IsUserPermission])
        ],
        ('create_messages', 'messages', 'delete_messages'): [
            Rule([IsAdminPermission | IsManagerPermission | IsAuthenticated])
        ],
        ('retrieve',): [
            Rule([IsManagerPermission | IsAdminPermission | IsUserPermission], MessageApiSerializer)
        ]
    }

    def get_object(self, *args, **kwargs):
        try:
            return Messages.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Messages.DoesNotExist:
            raise ValidationError({'detail': _('Указаный Messages не сужествует')})

    def get_queryset(self):
        queryset = Messages.objects.all()
        return queryset

    @action(methods=['GET'], detail=False, url_path='user')
    def messages(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(sender=request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_messages(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_messages(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Saved Filters'])
class SavedFiltersView(PsqMixin, generics.ListAPIView, viewsets.GenericViewSet):
    serializer_class = SavedFiltersApiSerializer
    psq_rules = {
        ('list', 'create_filter', 'profile_update', 'delete_messages'): [
            Rule([IsUserPermission, IsOwnerPermission])
        ]
    }

    def get_queryset(self):
        queryset = SavedFilters.objects.all()
        return queryset

    def profile_obj(self):
        try:
            obj = SavedFilters.objects.get(user=self.request.user)
            return obj
        except:
            return response.Response(data={'data': 'something go wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_filter(self, request, *args, **kwargs):
        if not SavedFilters.objects.filter(user=self.request.user):
            serializer = self.get_serializer(data=request.data, context={'user': request.user, 'request': request})
            if serializer.is_valid():
                serializer.save()
                return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response(data={'filter': 'У пользователя есть SavedFilters'}, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=False, url_path='user/update')
    def profile_update(self, request, *args, **kwargs):
        obj = self.profile_obj()
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False, url_path='user/delete')
    def delete_messages(self, request, *args, **kwargs):
        obj = self.profile_obj()
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Subscription'])
class SubscriptionAPIViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = SubscriptionApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Subscription.objects.all()

    # psq_rules = {
    #     ('list', 'retrieve'): [
    #         Rule([CustomIsAuthenticated])
    #     ],
    #     ('create', 'partial_update', 'destroy'): [
    #         Rule([IsAdminPermission]),
    #         Rule([IsManagerPermission])
    #     ]
    # }


@extend_schema(tags=['User Subscription'])
class UserSubscriptionAPIView(PsqMixin, viewsets.GenericViewSet):

    serializer_class = UserSubscriptionSerializer
    psq_rules = {
        ('list', 'create', 'partial_update', 'destroy'): [
            Rule([IsUserPermission])
        ]
    }

    def get_object(self, *args, **kwargs):
        try:
            return UserSubscription.objects.get(user=self.request.user)
        except UserSubscription.DoesNotExist:
            raise ValidationError({'detail': _('У вас ще немає підписки.')})

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, instance=self.get_object(), partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj_to_delete: UserSubscription = self.get_object()
        obj_to_delete.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)