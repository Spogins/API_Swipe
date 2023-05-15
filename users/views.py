from dj_rest_auth.registration.views import RegisterView
from django.views.generic.base import TemplateResponseMixin, View
from django.utils.translation import gettext_lazy as _
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, response, status, generics
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from users.models import User, Notary, Messages, SavedFilters
from users.serializers import BuilderRegistrationSerializer, UserAdminApiSerializer, UserApiSerializer, \
    NotaryApiSerializer, MessageApiSerializer, SavedFiltersApiSerializer


class ConfirmCongratulationView(TemplateResponseMixin, View):
    template_name = 'account/email/congratulations.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class BuilderRegisterView(RegisterView):
    serializer_class = BuilderRegistrationSerializer


@extend_schema(tags=['User'])
class UserApiView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = UserApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    psq_rules = {
        'create': [
            Rule(serializer_class=UserAdminApiSerializer)
        ]
    }

    def profile_obj(self):
        try:
            obj = User.objects.get(id=self.request.user.id)
            return obj
        except:
            return response.Response(data={'data': 'something go wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path='profile')
    def profile_usr(self, request, *args, **kwargs):
        obj = self.profile_obj()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=False, url_path='profile/update')
    def profile_update(self, request, *args, **kwargs):
        obj = self.profile_obj()
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Notary'])
class NotaryView(PsqMixin, viewsets.ModelViewSet):
    serializer_class = NotaryApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [permissions.AllowAny]
    queryset = Notary.objects.all()


@extend_schema(tags=['Messages'])
class MessagesView(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = MessageApiSerializer
    permission_classes = [permissions.AllowAny]

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
        obj = self.get_queryset().filter(residential_complex__user=request.user)
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Saved Filters'])
class SavedFiltersView(PsqMixin, generics.ListAPIView, viewsets.GenericViewSet):
    serializer_class = SavedFiltersApiSerializer
    permission_classes = [permissions.AllowAny]

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
    def create_messages(self, request, *args, **kwargs):
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