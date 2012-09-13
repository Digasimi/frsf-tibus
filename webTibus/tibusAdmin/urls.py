from django.conf.urls.defaults import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('tibusAdmin.views',
    (r'^admin$', 'tadmin'),
    (r'^recorrido(?P<routeId>\w+)$', 'stop'),
    (r'^linea$', 'route'), 
    (r'^unidad$', 'bus'), 
    (r'^empresa$', 'company'), 
    (r'^usuario$', 'user'),
    (r'^password$', 'changepassword'),
)