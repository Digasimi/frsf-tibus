from django.conf.urls.defaults import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('tibus.views',
    (r'^$', 'index'),
    (r'^index$', 'index'),
    (r'^prediccion$', 'prediccion'), 
    (r'^modelo$', 'modelo'), 
    (r'^ayuda$', 'ayuda'), 
)
