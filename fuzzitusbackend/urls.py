from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
v1_api = Api(api_name='v1')

from fuzzitusbackend.api import BeaconResource, BeaconTraitInstructionResource, FormResource, GameResource, InstructionResource, PlayerResource, TraitResource, TraitTypeResource, UserResource, WhoAmIResource
v1_api.register(WhoAmIResource())
v1_api.register(FormResource())
v1_api.register(UserResource())
v1_api.register(GameResource())
v1_api.register(BeaconResource())
v1_api.register(InstructionResource())
v1_api.register(BeaconTraitInstructionResource())
v1_api.register(TraitResource())
v1_api.register(TraitTypeResource())
v1_api.register(PlayerResource())

from fuzzitusbackend.views import FuzzitusTemplateView

urlpatterns = patterns('',
    url(r'^$', FuzzitusTemplateView.as_view(), name='index'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(v1_api.urls)),
    url(r'^api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
)
