'''
Created on 20/02/2013

@author: diego
'''
from django.conf.urls.defaults import patterns

urlpatterns = patterns('tibussphone.views',
    (r'^sindex$', 'sindex'), 
    (r'^sprediccion$', 'sprediction'), 
    (r'^sviaje', 'stravelPrediction'),
    (r'^sresultado$', 'sarriveResult'),
    (r'^srViaje$', 'stravelResult'),
)