from dj_rest_auth.registration.views import RegisterView
from django.views.generic.base import TemplateResponseMixin, View
from django.utils.translation import gettext_lazy as _
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, response, status
from rest_framework.decorators import action
from users.models import User, Notary
from users.serializers import BuilderRegistrationSerializer, UserAdminApiSerializer, UserApiSerializer, \
    NotaryApiSerializer


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
            print(self.request.user.id)
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


