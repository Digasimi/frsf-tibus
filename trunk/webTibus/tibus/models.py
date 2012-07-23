
from django.contrib.gis.db import models 
from django.contrib.auth.models import User
from xml.sax.handler import ContentHandler

import re

class Empresa(models.Model):
        idempresa = models.AutoField(primary_key=True)
        nombre = models.CharField(verbose_name="nombre", max_length=50)
        mail = models.EmailField()
        
        def __unicode__(self):
            return self.nombre
            
        class Meta:
            db_table = 'empresa'


class Usuario(User):
        nombre = models.CharField(max_length = 50,  primary_key=True)
        mail = models.EmailField()
        categoria = models.CharField(max_length = 50)
        empresa = models.ForeignKey(Empresa,  null=True)
    
        def __unicode__(self):
            return self.username
    
        class Meta:
            db_table = 'usuario'
        
        class Admin:
            pass

# Create your models here.

class Recorrido(models.Model):
        idrecorrido = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
        linea = models.CharField(verbose_name="nombre", max_length=50)
        frecuencia = models.IntegerField()
        objects = models.GeoManager()
        empresa = models.ForeignKey(Empresa)
        
        class Meta:
            db_table = 'recorrido'
        
        def __unicode__(self):
            return self.linea
            
        def validar(self):
            if self.linea == "" or self.frecuencia == "" or re.search("[^a-zA-Z0-9]", self.linea) :
                return False
            return True
            
        def id(self):
            return idrecorrido


class Parada(models.Model):
       idparada = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
       orden = models.IntegerField()
       objects = models.GeoManager()
       latitud = models.FloatField()
       longitud = models.FloatField()
       coordenadas = models.PointField(srid=4326)
       linea = models.ForeignKey(Recorrido)
       calle1 = models.CharField(verbose_name="calle1", max_length=100)
       calle2 = models.CharField(verbose_name="calle2", max_length=100)
       proximaparada = models.IntegerField()
  
       class Meta:
          db_table = 'parada'
        
       def _unicode_(self):
          return self.orden
          
       def ordenParada(self):
          return self.orden

       def latitudParada(self):
          return self.latitud
         
       def longitudParada(self):
          return self.longitud
          
       def aumentarOrden(self):
           self.orden = self.orden + 1
           return True
           
       def disminuirOrden(self):
           self.orden = self.orden - 1
           return True
      
class Unidad(models.Model):
      idunidad = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
      linea = models.ForeignKey(Recorrido)
      aptoMovilidadReducida = models.BooleanField()
      id_unidad_linea = models.IntegerField()
      
      class Meta:
          db_table = 'unidad'
    
class PosicionActual(models.Model):
      latitud = models.FloatField()
      longitud = models.FloatField()
      paradaasociada= models.ForeignKey(Parada,  related_name = "parada_asociada")
      unidad = models.ForeignKey(Unidad,  related_name = "numero_unidad", primary_key=True)
      tiempo = models.DateTimeField(primary_key=True)
      class Meta:
         db_table = 'posicionActual'
         db_tablespace = 'motorprediccion'
          
      def _unicode_(self): 
          return model_id

class Estimacion():
    tiempo = 0
    desviacion = 0
    unidad = 0
    paradaasociada = 0
    
    def _unicode_(self): 
      return unidad      
    
    def acumular(self, tiempoNew,  desviacionNew):
        self.tiempo = self.tiempo + tiempoNew
        self.desviacion = self.desviacion + desviacionNew

    def tiempoInicial(self):
        return (self.tiempo-self.desviacion)/60

    def tiempoFinal(self):
        return (self.tiempo+self.desviacion)/60
        
    def __init__(self, newUnidad, newParada):
        self.unidad = newUnidad
        self.paradaasociada = newParada
        
    
class TiempoRecorrido(models.Model):
      promedio = models.FloatField()
      desstd = models.FloatField()
      parada= models.ForeignKey(Parada,  related_name = "parada_origen", primary_key=True)
      orden = models.IntegerField()
      class Meta:
         db_table = 'promedios'
         db_tablespace = 'motorprediccion'            
      def _unicode_(self): 
          return promedio

class WorldBorders(models.Model):
        # Regular Django fields corresponding to the attributes in the
        # world borders shapefile.
        name = models.CharField(max_length=50)
        area = models.IntegerField()
        pop2005 = models.IntegerField('Population 2005')
        fips = models.CharField('FIPS Code', max_length=2)
        iso2 = models.CharField('2 Digit ISO', max_length=2)
        iso3 = models.CharField('3 Digit ISO', max_length=3)
        un = models.IntegerField('United Nations Code')
        region = models.IntegerField('Region Code')
        subregion = models.IntegerField('Sub-Region Code')
        lon = models.FloatField()
        lat = models.FloatField()

        # GeoDjango-specific: a geometry field (MultiPolygonField), and
        # overriding the default manager with a GeoManager instance.
        mpoly = models.MultiPolygonField()
        objects = models.GeoManager()

        # So the model is pluralized correctly in the admin.
        class Meta:
            verbose_name_plural = "World Borders"

        # Returns the string representation of the model.
        def __unicode__(self):
            return self.name

class MyListener(object):
    mensaje = ''
  
    def on_error(self, headers, message):
        print ('received an error %s' % message)

    def on_message(self, headers, message):
        print ('received a message %s' % message)
        self.mensaje = message
        
    def getMensaje(self):
      return self.mensaje

class Presponse(object):
    colectivo = ''
    tiempo = 0
     
    def __init__ (self, c, t):
        self.colectivo = c
        self.tiempo = t
        
    def __unicode__(self):
        return self.colectivo
    
class PresponseHandler(ContentHandler):
 lista = []
 isColeElement= 0;
 isTiempoElement = 0;
 colectivo = 0;
 tiempo = 0;
 
 def __init__ (self):
   self.lista = []
   self.isColeElement= 0;
   self.isTiempoElement = 0;
   self.colectivo = 0;
   self.tiempo = 0;
   
 def startElement(self, name, attrs):
   if name == 'colectivo':     
     self.isColeElement= 1;
     self.colectivo = "";
   elif name == 'tiempo':
     self.isTiempoElement = 1;
     self.tiempo = "";
   return

 def characters (self, ch):
   if self.isColeElement== 1:
     self.colectivo += ch
   if self.isTiempoElement == 1:
     self.tiempo += ch

 def endElement(self, name):
   if name == 'colectivo':
     self.isColeElement= 0
   if name == 'tiempo':
     self.inTiempoContent = 0
   if name == 'prediction':
       self.lista = self.lista + [Presponse(self.colectivo, self.tiempo)]
   if name == 'prediction-responde':
       print self.lista
   
 def obtenerLista(self):
   return self.lista
