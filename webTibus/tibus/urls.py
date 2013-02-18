from django.conf.urls.defaults import patterns

urlpatterns = patterns('tibus.views',
    (r'^$', 'prediction'),
    (r'^index$', 'index'),
    (r'^prediccion$', 'prediction'), 
    (r'^viaje', 'travelPrediction'),
    (r'^resultado$', 'arriveResult'),
    (r'^rViaje$', 'travelResult'),
    (r'^modelo$', 'model'), 
    (r'^contacto$', 'contact'),
    (r'^recorridos$', 'itinerary'), 
)
