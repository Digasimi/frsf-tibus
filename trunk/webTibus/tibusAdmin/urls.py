from django.conf.urls.defaults import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('tibusAdmin.views',
    (r'^admin$', 'tadmin'),
    (r'^recorrido$', 'recorrido'), 
    (r'^recorrido/(?P<idLinea>\w+)/$', 'recorridoLinea'),
    (r'^linea$', 'linea'), 
    (r'^unidad$', 'unidad'), 
    (r'^empresa$', 'empresa'), 
    (r'^usuario$', 'usuario'),
    (r'^password$', 'cambiarpassword'),
)