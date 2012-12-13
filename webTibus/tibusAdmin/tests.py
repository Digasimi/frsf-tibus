"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from django.utils.unittest import TestCase
from tibusAdmin.models import Usuario
from tibus.models import Empresa, Parada, Recorrido
from tibusAdmin.views import orderStopList

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
        
class OrderStopListTest(TestCase):
    def oneStopTest(self):
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp = Parada(orden = 3, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        stopsList = [stopTemp]
        orderStopList(stopsList)
        self.assertEqual(stopsList[0].getOrder(), 1, "Falla")
        
    def twoStopTest(self):
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp1 = Parada(orden = 2, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        stopTemp2 = Parada(orden = 3, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        stopsList = [stopTemp1, stopTemp2]
        orderStopList(stopsList)
        self.assertEqual(stopsList[1].getOrder(), 2, "Falla")
        
    def fourStopTest(self):
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp1 = Parada(orden = 2, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        stopTemp2 = Parada(orden = 3, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        stopTemp3 = Parada(orden = 8, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        stopTemp4 = Parada(orden = 53, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        stopsList = [stopTemp1, stopTemp2,stopTemp3, stopTemp4]
        orderStopList(stopsList)
        self.assertEqual(stopsList[3].getOrder(), 4, "Falla")                