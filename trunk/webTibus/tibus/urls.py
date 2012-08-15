from django.conf.urls.defaults import patterns, include, url
from django.contrib.gis import admin

admin.autodiscover()

urlpatterns = patterns('tibus.views',
    (r'^$', 'index'),
    (r'^admin$', 'tadmin'),
    (r'^index$', 'index'),
    (r'^recorrido$', 'recorrido'), 
    (r'^recorrido/(?P<idLinea>\w+)/$', 'recorridoLinea'),
    (r'^linea$', 'linea'), 
    (r'^unidad$', 'unidad'), 
    (r'^prediccion$', 'prediccion'), 
    (r'^modelo$', 'modelo'), 
    (r'^empresa$', 'empresa'), 
    (r'^usuario$', 'usuario'),
    (r'^ayuda$', 'ayuda'), 
)
