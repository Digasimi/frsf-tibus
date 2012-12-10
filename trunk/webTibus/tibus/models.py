
from django.db import models 

import re

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
            return True
            
        class Meta:
            db_table = 'empresa'
            
class Recorrido(models.Model):
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
    idparada = models.AutoField(primary_key=True) #agregado para el cambio de tablespace
    orden = models.IntegerField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    linea = models.ForeignKey(Recorrido)
    calle1 = models.CharField(verbose_name="calle1", max_length=100,null=True)
    calle2 = models.CharField(verbose_name="calle2", max_length=100,null=True)
    paradaactiva = models.BooleanField(help_text="Indica si es una parada donde se detiene el colectivo o no")
  
    class Meta:
        db_table = 'parada'
        
    def __unicode__(self):
        nombre = str(self.calle1)
        if self.calle2 != '' and self.calle2 != None:
            nombre = nombre + ' & ' + str(self.calle2) 
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
      
class Unidad(models.Model):
    idunidad = models.AutoField(primary_key=True)
    linea = models.ForeignKey(Recorrido)
    apto_movilidad_reducida = models.BooleanField()
    id_unidad_linea = models.IntegerField()
      
    class Meta:
        db_table = 'unidad'
    
    def getLinea(self):
        return self.linea
    
    def getId(self):
        return self.idunidad
    
    def getIdByLinea(self):
        return self.id_unidad_linea
        
    def getApto(self):
        return self.apto_movilidad_reducida
    
class Frecuencia(models.Model):
    idfrecuencia = models.AutoField(primary_key=True)
    linea = models.ForeignKey(Recorrido, related_name = "recorrido")
    dia_semana = models.CharField(max_length=10, choices=DIASSEMANA)
    hora = models.TimeField()
    
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