
from django.db import models 
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
            
class Recorrido(models.Model):
    idrecorrido = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
    linea = models.CharField(verbose_name="nombre", max_length=50)
    frecuencia = models.IntegerField()
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
        return self.idrecorrido

class Parada(models.Model):
    idparada = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
    orden = models.IntegerField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    linea = models.ForeignKey(Recorrido)
    calle1 = models.CharField(verbose_name="calle1", max_length=100,null=True) #debe sacarse, no puede ser null
    calle2 = models.CharField(verbose_name="calle2", max_length=100,null=True)
    paradaactiva = models.BooleanField()
  
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
    
    def id(self):
        return self.idparada
      
class Unidad(models.Model):
    idunidad = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
    linea = models.ForeignKey(Recorrido)
    aptoMovilidadReducida = models.BooleanField()
    id_unidad_linea = models.IntegerField()
      
    class Meta:
        db_table = 'unidad'
    
class TiempoRecorrido(models.Model):
    promedio = models.FloatField()
    desstd = models.FloatField()
    parada= models.ForeignKey(Parada,  related_name = "parada_origen", primary_key=True)
    orden = models.IntegerField()
    
    class Meta:
        db_table = 'promedios'
    
    def _unicode_(self): 
        return self.promedio

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
    lat = 0
    lon = 0
    
    def __init__ (self, c, t, la, lo):
        self.colectivo = c
        self.tiempo = t
        self.lat = float(la)
        self.lon = float(lo)

    def __unicode__(self):
        return self.colectivo
    
class PresponseHandler(ContentHandler):
    lista = []
    isColeElement= 0
    isTiempoElement = 0
    islatElement = 0
    islonElement = 0
    isTimeStampElement = 0
    isErrorElemet = 0
    colectivo = ""
    tiempo = ""
    lat = ""
    lon = "" 
    timestamp = ""
    error = ""
    
    def __init__ (self):
        self.lista = []
        self.isColeElement= 0
        self.isTiempoElement = 0
        self.islatElement = 0
        self.islonElement = 0
        self.isTimeStampElement = 0
        self.isErrorElemet = 0
        self.colectivo = ""
        self.tiempo = ""
        self.lat = ""
        self.lon = ""
        self.timestamp = ""
        self.error = ""
    
    def startElement(self, name, attrs):
        if name == 'busId':
            self.isColeElement= 1
            self.colectivo = ""
        elif name == 'timeSec':
            self.isTiempoElement = 1
            self.tiempo = ""
        elif name == 'lat':
            self.islatElement = 1
            self.lat = ""
        elif name == 'lon':
            self.islonElement = 1
            self.lon = ""
        elif name == 'timestamp':
            self.isTimeStampElement = 1
            self.timestamp = ""
        elif name == "error":
            self.isErrorElemet = 1
            self.error = ""   
    
    def characters (self, ch):
        if self.isColeElement== 1:
            self.colectivo += ch
        if self.isTiempoElement == 1:
            self.tiempo += ch
        if self.islatElement == 1:
            self.lat += ch
        if self.islonElement == 1:
            self.lon += ch
        if self.isTimeStampElement == 1:
            self.timestamp += ch
        if self.isErrorElemet == 1:
            self.error += ch
    
    def endElement(self, name):
        if name == 'busId':
            self.isColeElement= 0
        if name == 'timeSec':
            self.isTiempoElement = 0
        if name == 'lat':
            self.islatElement = 0
        if name == 'lon':
            self.islonElement = 0
        if name == 'prediction':
            self.lista = self.lista + [Presponse(self.colectivo, self.tiempo,self.lat, self.lon)]
        if name == 'timestamp':
            self.isTimeStampElement = 0
        if name == "error":
            self.isErrorElemet = 0
        if name == 'prediction-responde':
            print self.lista
    
    def obtenerLista(self):
        return self.lista
    
    def obtenerTimeStamp(self):
        return self.timestamp
    
    def obtenerError(self):
        return self.error