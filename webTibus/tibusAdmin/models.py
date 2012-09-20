from django.db import models
from django.contrib.auth.models import User
from tibus.models import Empresa


# Create your models here.
class Usuario(User):
    nombre = models.CharField(max_length = 50,  primary_key=True)
    mail = models.EmailField()
    categoria = models.CharField(max_length = 50)
    empresa = models.ForeignKey(Empresa,  null=True)
    
    def getName(self):
        return self.nombre
    
    def getCategory(self):
        return self.categoria
    
    def getCompany(self):
        return self.empresa
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        db_table = 'usuario'
    
    class Admin:
        pass
