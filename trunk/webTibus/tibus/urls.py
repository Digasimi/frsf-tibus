from django.conf.urls.defaults import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('tibus.views',
    (r'^$', 'prediction'),
    (r'^index$', 'index'),
    (r'^prediccion$', 'prediction'), 
    (r'^resultado$', 'result'),
    (r'^modelo$', 'model'), 
    (r'^ayuda$', 'tibushelp'), 
)
