
from django.db import models 

import re

'''
Enumeracion de datos usada para guardar frecuencias
'''
DIASSEMANA = (
    ('LUNES', 'Lunes'),
    ('MARTES', 'Martes'),
    ('MIERCOLES', 'Miercoles'),
    ('JUEVES', 'Jueves'),
    ('VIERNES', 'Viernes'),
    ('SABADO', 'Sabado'),
    ('DOMINGO', 'Domingo'),
)
    
class Empresa(models.Model):
    '''
    Clase que representa a un empresa
    Permite la Agrupacion de lineas, unidades y usuarios
    '''
    idempresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, help_text="Nombre de la empresa")
    mail = models.EmailField()
    
    def __unicode__(self):
        return self.nombre
    
    def getId(self):
        return self.idempresa
    
    def getName(self):
        return self.nombre
    
    def getMail(self):
        return self.mail
    
    def validate(self):
        if self.nombre == "" or self.mail == '' or re.search("[^a-zA-Z0-9]", self.nombre) :
            return False
        self.nombre = self.nombre.strip().rstrip("\n")
        return True
        
    class Meta:
        db_table = 'empresa'
            
class Recorrido(models.Model):
    '''
    Clase que representa el recorrida de una linea
    Posee una relacion uno-muchos con empresa
    '''
    idrecorrido = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
    linea = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa)
    predictable = models.BooleanField()
    
    class Meta:
        db_table = 'recorrido'
    
    def __unicode__(self):
        return self.linea
        
    def validate(self):
        if self.linea == "" or (re.search("[^a-zA-Z0-9]", self.linea)!=None):
            return False
        self.linea = self.linea.strip().rstrip("\n")
        return True
        
    def getId(self):
        return self.idrecorrido
    
    def getLinea(self):
        return self.linea
    
    def getCompany(self):
        return self.empresa
    
    def getPredictable(self):
        return self.predictable

class Parada(models.Model):
    '''
    Clase que Representa cada una de las paradas de una linea
    Posee una relacion uno-muchos con recorrido
    '''
    idparada = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
    orden = models.IntegerField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    linea = models.ForeignKey(Recorrido)
    calle1 = models.CharField(verbose_name="calle1", max_length=100,null=True)
    calle2 = models.CharField(verbose_name="calle2", max_length=100,null=True)
    paradaactiva = models.BooleanField(help_text="Indica si es una parada donde se detiene el colectivo o no")
    sentido = models.CharField(max_length=20)
  
    class Meta:
        db_table = 'parada'
        
    def __unicode__(self):
        nombre = str(self.calle1)
        if self.calle2 != '' and self.calle2 != None:
            nombre = nombre + ' & ' + str(self.calle2) 
        nombre = nombre + ' ('+str(self.sentido)+')'
        return nombre
          
    def getOrder(self):
        return self.orden
    
    def getLat(self):
        return self.latitud
      
    def getLon(self):
        return self.longitud
       
    def upOneOrder(self):
        self.orden = self.orden + 1
        return True
        
    def downOneOrder(self):
        self.orden = self.orden - 1
        return True
    
    def getId(self):
        return self.idparada
    
    def getLinea(self):
        return self.linea
    
    def getStreetName1(self):
        return self.calle1
    
    def getStreetName2(self):
        return self.calle2
    
    def getActive(self):
        return self.paradaactiva
    
    def getDirection(self):
        return self.sentido
    
    def validate(self):
        if self.calle1 == None or self.calle1 == '':
            return False
        if (self.latitud <= 90 and self.latitud >= -90) and (self.longitud <= 180 and self.longitud >= -180):
            self.calle1 = self.calle1.strip().rstrip("\n")
            self.calle2 = self.calle2.strip().rstrip("\n")
            return True
        return False 
        
      
class Unidad(models.Model):
    '''
    Clase que representa cada una de las unidades moviles
    Posee una relacion uno-muchos con Recorrido
    '''
    idunidad = models.AutoField(primary_key=True)
    linea = models.ForeignKey(Recorrido)
    apto_movilidad_reducida = models.BooleanField()
    id_unidad_linea = models.IntegerField()
      
    class Meta:
        db_table = 'unidad'
        
    def __unicode__(self):
        return str(self.getIdByLinea()) + " (" +str(self.linea) + ")"
    
    def getLinea(self):
        return self.linea
    
    def getId(self):
        return self.idunidad
    
    def getIdByLinea(self):
        return self.id_unidad_linea
        
    def getApto(self):
        return self.apto_movilidad_reducida
    
class Frecuencia(models.Model):
    '''
    Clase que representa los horarios de salida de las unidades de la paradas iniciales
    Posee una relacion uno-muchos con Recorrido
    '''
    idfrecuencia = models.AutoField(primary_key=True)
    linea = models.ForeignKey(Recorrido, related_name = "recorrido")
    dia_semana = models.CharField(max_length=10, choices=DIASSEMANA)
    hora = models.TimeField()
    
    def __unicode__(self):
        return str(self.dia_semana) + " " + str(self.hora)
        
    def getLinea(self):
        return self.linea
    
    def getDiaSemana(self):
        return self.dia_semana
    
    def getHora(self):
        return self.hora
        
    def getId(self):
        return self.idfrecuencia
    
    class Meta:
        db_table = 'frecuencia'