"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

from django.test import TestCase
from tibus.views import createMessage
from tibus.models import Empresa, Recorrido, Parada, Unidad, Frecuencia, DIASSEMANA
        
class MessageTest(TestCase):
    def getValidMessageTest(self):
        """
        Prueba que valida mensaje valido
        """
        messageValid = '<prediction-request><linea>1</linea><parada>1</parada></prediction-request>'
        self.assertEqual(createMessage(1,1), messageValid)

    def getNotRouteMessageTest(self):
        """
        Prueba que valida mensaje valido
        """
        self.assertEqual(createMessage('',1), None)
        
    def getNotStopMessageTest(self):
        """
        Prueba que valida mensaje valido
        """
        self.assertEqual(createMessage(1,''), None)
        
class CompanyTest(TestCase):
    def getValidCompanyTest(self):
        """
        Prueba que valida compania
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        self.assertTrue(companyTemp.validate())
    
class RouteTest(TestCase):
    def getValidRouteTest(self):
        """
        Prueba que valida recorrido
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        self.assertTrue(routeTemp.validate())
            
class StopTest(TestCase):
    def getValidStopTest(self):
        """
        Prueba que valida parada
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp = Parada(orden = 1, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        self.assertTrue(stopTemp.getActive())
            
class BusTest(TestCase):
    def getValidBusTest(self):
        """
        Prueba que valida unidad
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        busTemp = Unidad(linea = routeTemp, id_unidad_linea = 1234, apto_movilidad_reducida = True)
        self.assertTrue(busTemp.getApto())
            
class FrecuencyTest(TestCase):
    def getValidFrecuencyTest(self):
        """
        Prueba que valida frecuencia
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        frecuencyTemp = Frecuencia(linea = routeTemp, dia_semana = 'MARTES', hora = "00:00:00")
        self.assertTrue(frecuencyTemp.getDiaSemana()== 'MARTES')