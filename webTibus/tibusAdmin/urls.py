from django.conf.urls.defaults import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('tibusAdmin.views',
    (r'^admin$', 'tadmin'),
    (r'^linea$', 'route'),
    (r'^recorrido(?P<routeId>\w+)$', 'stop'),
    (r'^stops(?P<routeId>\w+)$', 'stopList'),
    (r'^frecuencydata(?P<routeId>\w+)$', 'frecuencydata'),
    (r'^frecuency(?P<routeId>\w+)$', 'frecuency'),
    (r'^stopdata(?P<stopId>\w+)$', 'stopdata'),
    (r'^unidad$', 'bus'), 
    (r'^unidaddata(?P<busId>\w+)$', 'busdata'),
    (r'^empresa$', 'company'),
    (r'^empresadata(?P<companyId>\w+)$', 'companydata'),
    (r'^usuario$', 'user'),
    (r'^usuariodata(?P<userId>\w+)$', 'userdata'),
    (r'^eliminar$', 'eliminar'),
    (r'^password$', 'changepassword'),
)