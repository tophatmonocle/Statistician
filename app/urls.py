from tastypie.api import Api
from api.resources import MetricResource, MetricDataResource,\
    InstrumentResource, EventResource
from django.conf.urls.defaults import patterns, include, url

api_v1 = Api(api_name='v1')

api_v1.register(MetricResource())
api_v1.register(MetricDataResource())
api_v1.register(InstrumentResource())
api_v1.register(EventResource())

urlpatterns = patterns('',
                       url(r'^unauthorized/', 'stats.views.unauthorized'),
                       url(r'^login/$',
                           'django_openid_auth.views.login_begin',
                           name='openid-login'),
                       url(r'^login-complete/$',
                           'django_openid_auth.views.login_complete',
                           name='openid-complete'),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {'next_page': '/'}, name='logout'),
                       (r'^api/', include(api_v1.urls)),
                       url('^(?P<project_slug>[-\w]+)/?.*$',
                           'stats.views.project'),
                       url('^/?$', 'stats.views.index')
                       )
