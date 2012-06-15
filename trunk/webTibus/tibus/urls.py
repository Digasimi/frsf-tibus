from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
from django.contrib.gis import admin

admin.autodiscover()

urlpatterns = patterns('tibus.views',
    (r'^$', 'index'),
    (r'^admin$', 'tadmin'),
    (r'^index$', 'index'),
    (r'^recorrido$', 'recorrido'), 
    (r'^linea$', 'linea'), 
    (r'^unidad$', 'unidad'), 
    (r'^prediccion$', 'prediccion'), 
    (r'^modelo$', 'modelo'), 
    (r'^empresa$', 'empresa'), 
    (r'^ayuda$', 'ayuda'), 
    #(r'^Archivos/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
