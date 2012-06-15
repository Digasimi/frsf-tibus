from tibus.models import Recorrido
from tibus.models import Parada
from tibus.models import Unidad
from django.contrib.gis import admin
#from django.contrib import admin

#class recorridoAdmin(admin.ModelAdmin):
#   fieldsets = [
#        (None,               {'fields': ['linea', 'frecuencia']}),
#    ]

admin.site.register(Recorrido, admin.OSMGeoAdmin)
admin.site.register(Parada)
admin.site.register(Unidad)
