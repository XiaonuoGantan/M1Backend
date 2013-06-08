from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
v1_api = Api(api_name='v1')

from fuzzitusbackend.api import FormResource, WhoAmIResource
v1_api.register(WhoAmIResource())
v1_api.register(FormResource())

from django.views.generic import TemplateView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(v1_api.urls)),
)
