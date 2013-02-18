'''
Created on 15/02/2013

@author: diego
'''
from django.conf.urls.defaults import patterns

urlpatterns = patterns('tibusWap.views',
    (r'^wap$', 'index'),
    (r'^windex$', 'index'),
    (r'^wc(?P<companyId>\w+)$', 'company'),
    (r'^wr(?P<routeId>\w+)$', 'route'),
    (r'^ws(?P<stopId>\w+)$', 'result'),
)
