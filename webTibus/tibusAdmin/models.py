from django.db import models
from django.contrib.auth.models import User
from tibus.models import Empresa
import re


# Create your models here.
class Usuario(User):
    nombre = models.CharField(max_length = 50, primary_key=True)
    mail = models.EmailField()
    categoria = models.CharField(max_length = 50)
    empresa = models.ForeignKey(Empresa, null=True)
    
    def getName(self):
        return self.nombre
    
    def validate(self):
        if self.nombre == "" or self.mail == "" or re.search("[^a-zA-Z0-9]", self.nombre) or (self.empresa == None and self.categoria == 'Empresa'):
            return False
        return True
    
    def getCategory(self):
        return self.categoria
    
    def getCompany(self):
        return self.empresa
    
    def getMail(self):
        return self.mail
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        db_table = 'usuario'
    
    class Admin:
        pass
