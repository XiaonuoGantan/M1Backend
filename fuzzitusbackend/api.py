import json
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse
from tastypie import fields
from tastypie import exceptions as exc
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.bundle import Bundle
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource, Resource
from tastypie.utils import trailing_slash

from fuzzitusbackend import models as m
from fuzzitusbackend import forms
from fuzzitusbackend.auth import GameOwnerAuthorization


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'username', 'email']
        allowed_methods = ['get', 'post']
        resource_name = 'user'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
            url(r'^(?P<resource_name>%s)/signup%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('signup'), name='api_signup'),
        ]

    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json'))
        data['password'] = data.pop('password1')
        data.pop('password2')
        user = User.objects.create_user(**data)
        user.is_staff = True
        user.save()
        return self.create_response(request, {
                'success': True,
                'api_key': user.api_key.key,
            })

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.raw_post_data,
            format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True,
                    'csrf_token': csrf(request),
                    'api_key': user.api_key.key
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        auth = ApiKeyAuthentication()
        self.method_check(request, allowed=['post'])
        if auth.is_authenticated(request):
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)


class WhoAmIResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'whoami'
        excludes = ['email', 'password', 'is_superuser']
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def get_object_list(self, request):
        return User.objects.filter(pk=request.user.pk)

    def get_detail(self, request, **kwargs):
        raise exc.Unauthorized('Unauthorized access')

    def dehydrate(self, bundle):
        if bundle.request.user.pk == bundle.obj.pk:
            bundle.data['email'] = bundle.obj.email
        return bundle


class GameResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        queryset = m.Game.objects.all()
        resource_name = 'game'
        authentication = ApiKeyAuthentication()
        authorization = GameOwnerAuthorization()


class BeaconResource(ModelResource):
    game = fields.ForeignKey(GameResource, 'game')

    @property
    def api_version(self):
        from fuzzitusbackend.urls import v1_api
        canonical_resource_uri = v1_api.canonical_resource_for('beacon')
        return canonical_resource_uri.api_name

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/traits%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_traits'), name='update_traits'),
            url(r'^(?P<resource_name>%s)/instructions%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_instructions'), name='get_instructions'),
        ]

    def update_traits(self, request, **kwargs):
        if request.method == 'GET':
            pk = request.GET['pk']
            beacon = m.Beacon.objects.get(pk=pk)
            traits = ['/api/{0}/trait/{1}/'.format(self.api_version, trait.pk)
                      for trait in beacon.traits.all()]
            return self.create_response(request, {
                'traits': traits,
            })
        elif request.method == 'POST':
            data = json.loads(request.body)
            pk = data['pk']
            beacon = m.Beacon.objects.get(pk=pk)
            trait_pk = data['trait_pk']
            trait = m.Trait.objects.get(pk=trait_pk)
            bti, created = m.BeaconTraitInstruction.objects.get_or_create(
                beacon=beacon, trait=trait)
            bti = '/api/{0}/beacon_trait_instruction/{1}/'.format(
                self.api_version, bti.pk)
            return self.create_response(request, {
                'beacon_trait_instruction': bti,
                'created': created,
            })

    def get_instructions(self, request, **kwargs):
        pk = request.GET['pk']
        trait_pk = request.GET['trait_pk']
        from fuzzitusbackend.urls import v1_api
        canonical_resource_uri = v1_api.canonical_resource_for('beacon')
        api_version = canonical_resource_uri.api_name
        beacon = m.Beacon.objects.get(pk=pk)
        trait = m.Trait.objects.get(pk=trait_pk)
        instructions = beacon.instructions.filter(traits=trait).all()
        instructions = ['/api/{0}/instruction/{1}/'.format(api_version, instruction.pk)
                        for instruction in instructions]
        return self.create_response(request, {
            'instructions': instructions,
        })

    class Meta:
        queryset = m.Beacon.objects.all()
        resource_name = 'beacon'
        authentication = ApiKeyAuthentication()
        authorization = GameOwnerAuthorization()


class TraitTypeResource(ModelResource):
    class Meta:
        queryset = m.TraitType.objects.all()
        resource_name = 'trait_type'
        authentication = ApiKeyAuthentication()
        authorization = GameOwnerAuthorization()


class TraitResource(ModelResource):
    trait_type = fields.ForeignKey(TraitTypeResource, 'trait_type')

    class Meta:
        queryset = m.Trait.objects.all()
        resource_name = 'trait'
        authentication = ApiKeyAuthentication()
        authorization = GameOwnerAuthorization()


class PlayerResource(ModelResource):
    traits = fields.ManyToManyField(TraitResource, 'traits',
                                    related_name='players', null=True)

    class Meta:
        queryset = m.Player.objects.all()
        resource_name = 'player'
        authentication = ApiKeyAuthentication()
        authorization = GameOwnerAuthorization()


class InstructionResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        queryset = m.Instruction.objects.all()
        resource_name = 'instruction'
        authentication = ApiKeyAuthentication()
        authorization = GameOwnerAuthorization()


class BeaconTraitInstructionResource(ModelResource):
    beacon = fields.ForeignKey(BeaconResource, 'beacon')
    trait = fields.ForeignKey(TraitResource, 'trait')
    instruction = fields.ForeignKey(InstructionResource, 'instruction', null=True)

    class Meta:
        queryset = m.BeaconTraitInstruction.objects.all()
        resource_name = 'beacon_trait_instruction'
        authentication = ApiKeyAuthentication()
        authorization = GameOwnerAuthorization()


class FormResource(Resource):
    class Meta:
        allowed_methods = ['get']
        resource_name = 'form'
        object_class = dict

    def obj_get(self, request=None, **kwargs):
        form_pk = kwargs['pk']
        form = forms.FormMapper[form_pk]()
        form_action = forms.FormAction[form_pk]
        return {
            'form': forms.render_form_with_bootstrap(form),
            'action': form_action,
        }

    def dehydrate(self, bundle):
        bundle.data['form'] = bundle.obj['form']
        return bundle



