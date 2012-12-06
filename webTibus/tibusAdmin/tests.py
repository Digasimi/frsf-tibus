"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from django.utils.unittest import TestCase
from tibusAdmin.models import Usuario
from tibus.models import Empresa

class UsuarioTest(TestCase):
    def nameEmtpyTest(self):
        """
        Tests que prueba que nombre vacio de error
        """
        usuarioPrueba = Usuario(nombre='', mail='sf@google.com', categoria ='Administrador')
        self.assertFalse(usuarioPrueba.validate(), "Nombre Vacio")

    def userValidTest(self):
        """
        Tests que prueba que nombre no vacio de error
        """
        usuarioPrueba = Usuario(nombre='Luka', mail='sf@google.com', categoria ='Administrador')
        empresaTemp = Empresa(nombre = 'prueba', mail='prueba@prueba.com')
        usuarioPrueba2 = Usuario(nombre='diegoluka', mail='sf@google.com', categoria ='Empresa', empresa=empresaTemp)
        self.assertTrue(usuarioPrueba.validate(), "usuario Administrador valido")
        self.assertTrue(usuarioPrueba2.validate(), "usuario Empresa valido")
        
    def nameNotValidTest(self):
        """
        Tests que prueba que nombre no valido con espacio de error
        """
        usuarioPrueba = Usuario(nombre='diego luka', mail='sf@google.com', categoria ='Administrador')
        self.assertFalse(usuarioPrueba.validate(), "nombre no valido")
        
    def mailEmtpyTest(self):
        """
        Tests que prueba que nombre no vacio de error
        """
        usuarioPrueba = Usuario(nombre='Luka', mail='', categoria ='Administrador')
        self.assertFalse(usuarioPrueba.validate(), "mail vacio")
        
    def companyEmptyTest(self):
        """
        Tests que prueba que nombre no valido con espacio de error
        """
        usuarioPrueba = Usuario(nombre='diegoluka', mail='sf@google.com', categoria ='Empresa')
        self.assertFalse(usuarioPrueba.validate(), "nombre empresa vacio")