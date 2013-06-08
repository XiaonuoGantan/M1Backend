import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from tastypie import fields
from tastypie import exceptions as exc
from tastypie.authentication import Authentication, SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, Resource

from fuzzitusbackend import models as m
from fuzzitusbackend import forms


class WhoAmIResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'whoami'
        excludes = ['email', 'password', 'is_superuser']
        allowed_methods = ['get']
        authentication = Authentication()
        authorization = Authorization()

    def get_list(self, request, **kwargs):
        if request.user.is_authenticated():
            data = [request.user]
        else:
            data = []
        data = json.dumps(data)
        return HttpResponse(data, mimetype='application/json', status=200)

    def get_detail(self, request, **kwargs):
        raise exc.Unauthorized('Unauthorized access')

    def dehydrate(self, bundle):
        if bundle.request.user.pk == bundle.obj.pk:
            bundle.data['email'] = bundle.obj.email
        return bundle


class GameResource(ModelResource):
    class Meta:
        queryset = m.Game.objects.all()
        resource_name = 'game'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()


class FormResource(Resource):
    class Meta:
        allowed_methods = ['get']
        resource_name = 'form'
        object_class = dict

    def obj_get(self, request=None, **kwargs):
        form_pk = kwargs['pk']
        form = forms.FormMapper[form_pk]()
        return {'form': forms.render_form_with_bootstrap(form)}

    def dehydrate(self, bundle):
        bundle.data['form'] = bundle.obj['form']
        return bundle

