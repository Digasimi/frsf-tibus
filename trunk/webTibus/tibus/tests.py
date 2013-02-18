"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

from django.test import TestCase
from tibus.models import Empresa, Recorrido, Parada, Unidad, Frecuencia
from tibus.predictor import Predictor
        
class CompanyTest(TestCase):
    def validCompanyTest(self):
        """
        Prueba que valida compania
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        self.assertTrue(companyTemp.validate())
        
    def emptyMailCompanyTest(self):
        """
        Prueba que valida mail vacio de compania
        """
        companyTemp = Empresa(nombre = "company", mail = "")
        self.assertFalse(companyTemp.validate())
        
    def emptyNameCompanyTest(self):
        """
        Prueba que valida nombre vacio de compania
        """
        companyTemp = Empresa(nombre = "", mail = "company@gmail.com")
        self.assertFalse(companyTemp.validate())
    
class RouteTest(TestCase):
    def ValidRouteTest(self):
        """
        Prueba que valida recorrido
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        self.assertTrue(routeTemp.validate())
        
    def notNameRouteTest(self):
        """
        Prueba que valida recorrido
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "", empresa = companyTemp, predictable = True)
        self.assertFalse(routeTemp.validate())
            
class StopTest(TestCase):
    def validStopTest(self):
        """
        Prueba que valida parada
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp = Parada(orden = 1, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2")
        self.assertTrue(stopTemp.validate())
        
    def notValidLatStopTest(self):
        """
        Prueba que verifica parada latitud no valida
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp = Parada(orden = 1, latitud = 97.2, longitud = 30.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        self.assertFalse(stopTemp.validate())
        
    def notValidLonStopTest(self):
        """
        Prueba que verifica parada longitud no valida
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp = Parada(orden = 1, latitud = 37.2, longitud = 230.1, linea = routeTemp, calle1 = "calle1", calle2="calle2", paradaactiva = True)
        self.assertFalse(stopTemp.validate())
        
    def notStreetStopTest(self):
        """
        Prueba que verifica descripcion de parada no existente
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp = Parada(orden = 1, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = None, calle2="calle2", paradaactiva = True)
        self.assertFalse(stopTemp.validate())
        
    def emptyStreetStopTest2(self):
        """
        Prueba que verifica descripcion de parada vacia
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        stopTemp = Parada(orden = 1, latitud = 37.2, longitud = 30.1, linea = routeTemp, calle1 = '', calle2="calle2", paradaactiva = True)
        self.assertFalse(stopTemp.validate())
            
class BusTest(TestCase):
    def validBusTest(self):
        """
        Prueba que valida unidad
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        busTemp = Unidad(linea = routeTemp, id_unidad_linea = 1234, apto_movilidad_reducida = True)
        self.assertTrue(busTemp.getApto())
        
    def validAptoBusTest(self):
        """
        Prueba que valida frecuencia
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        busTemp = Unidad(linea = routeTemp, id_unidad_linea = 1234, apto_movilidad_reducida = "False")
        try:
            busTemp.save()
            self.assertTrue(False)
        except:
            self.assertTrue(True)        
            
class FrecuencyTest(TestCase):
    def validFrecuencyTest(self):
        """
        Prueba que valida frecuencia
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        frecuencyTemp = Frecuencia(linea = routeTemp, dia_semana = 'MARTES', hora = "00:00:00")
        self.assertTrue(frecuencyTemp.getDiaSemana()== 'MARTES')
        
    def notValidHourFrecuencyTest(self):
        """
        Prueba que valida frecuencia
        """
        companyTemp = Empresa(nombre = "company", mail = "company@gmail.com")
        routeTemp = Recorrido(linea = "route1", empresa = companyTemp, predictable = True)
        frecuencyTemp = Frecuencia(linea = routeTemp, dia_semana = 'MARTES', hora = "27:00:00")
        try:
            frecuencyTemp.save()
            self.assertTrue(False)
        except:
            self.assertTrue(True)
            
class PredictorTest(TestCase):
    testPredictor = Predictor()
     
    def emptyMessage(self):
        msg = self.testPredictor.createMessage("", "")
        self.assertIsNone(msg, "Mensaje Vacio")
        
    def notRouteMessage(self):
        msg = self.testPredictor.createMessage(13, "")
        self.assertIsNone(msg, "Mensaje Vacio")
        
    def notStopMessage(self):
        msg = self.testPredictor.createMessage("", 12)
        self.assertIsNone(msg, "Mensaje Vacio")
        
    def correctMessage(self):
        messageValid = '<prediction-request><linea>1</linea><parada>1</parada></prediction-request>'
        msg = self.testPredictor.createMessage(1, 1)
        self.assertEqual(msg, messageValid)
        
    def emptyPrediction(self):
        self.testPredictor.doPrediction("", "", "")
        self.assertNotEqual("", self.testPredictor.getError(), "Error de prueba")
        
    def notRoutePrediction(self):
        self.testPredictor.doPrediction("", 13, None)
        self.assertNotEqual("", self.testPredictor.getError(), "Error de prueba")
    
    def notStopPrediction(self):
        self.testPredictor.doPrediction(12, "", None)
        self.assertNotEqual("", self.testPredictor.getError(), "Error de prueba")
        
    def notAptoPrediction(self):
        self.testPredictor.doPrediction(1, 1, "")
        self.assertNotEqual("Datos incompletos", self.testPredictor.getError(), "Error de prueba")

    def falseAptoPrediction(self):
        self.testPredictor.doPrediction(1, 1, False)
        self.assertNotEqual("Datos incompletos", self.testPredictor.getError(), "Error de prueba")
        
    def trueAptoPrediction(self):
        self.testPredictor.doPrediction(1, 1, True)
        self.assertNotEqual("Datos incompletos", self.testPredictor.getError(), "Error de prueba")