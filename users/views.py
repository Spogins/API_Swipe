from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View


# Create your views here.
class ConfirmCongratulationView(TemplateResponseMixin, View):
    template_name = 'account/email/congratulations.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

