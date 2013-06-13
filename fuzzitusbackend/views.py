from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from fuzzitusbackend.settings import SERVER_ROOT_URL


class FuzzitusTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(FuzzitusTemplateView, self).get_context_data(**kwargs)
        context['server_root_url'] = SERVER_ROOT_URL
        return context

