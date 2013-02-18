'''
Created on 15/02/2013

@author: diego
'''
import stomp, time
from tibus.models import Unidad
from tibus.listenerParseXML import MyListener, PresponseHandler
from xml.sax import parseString,  SAXParseException
from timetobus.parameters import REQUESTSERVER, REQUESTQUEUENAME, RESPONSEQUEUENAME, REQUESTTIMEOUT 
from django.db.utils import DatabaseError

class Predictor():
    errorDescription = ''
    timeStampPrediction = ''
    predictionList = []
    parser = PresponseHandler()
    
    def getError(self):
        return self.errorDescription
    
    def getTimeStamp(self):
        return self.timeStampPrediction
    
    def getPredictionList(self):
        return self.predictionList
    
    #Funcino que crea el mensaje xml dados los id de route y de unidad
    def createMessage(self, route,  order):
        if route == None or order == None or route == '' or order == '':
            return None
        else: 
            return '<prediction-request><linea>' + str(route) + '</linea><parada>' + str(order) + '</parada></prediction-request>'
    
    def doPrediction(self, routeId, stopId, aptoPrediction):
        try:
            conn = stomp.Connection(REQUESTSERVER) #Aca hay que definir el conector externo
            conn.start()
            conn.connect()
            msg = self.createMessage(routeId, stopId)
            if aptoPrediction == None or aptoPrediction == "":
                aptoPrediction = False
            if msg == None:
                self.errorDescription = "Datos incompletos"
            else:
                conn.set_listener('list', MyListener())
                conn.send(msg, destination = REQUESTQUEUENAME,headers={'reply-to':RESPONSEQUEUENAME})
                conn.subscribe(destination = RESPONSEQUEUENAME, ack='auto')
                predictionXml = ""
                lis1 = conn.get_listener('list')
                timer = 0
                while (predictionXml == '' and timer <= REQUESTTIMEOUT):
                    time.sleep(1)
                    timer=timer+1
                    predictionXml = lis1.getMessage()
                if (timer == REQUESTTIMEOUT):
                    self.errorDescription = 'Tiempo de espera agotado'
                else:
                    parseString(predictionXml, self.parser)
                    tempPredictionList = self.parser.getLista()
                    self.errorDescription = self.parser.getError()
                    if (aptoPrediction == 'True'):#filtrar lista con colec aptos
                        for prediction in tempPredictionList:
                            try:
                                temporaryBus = Unidad.objects.get(id_unidad_linea = prediction.bus, linea = routeId)
                                if (temporaryBus.getApto() == True):
                                    self.predictionList = self.predictionList + [prediction]
                            except Unidad.DoesNotExist:
                                self.predictionList = self.predictionList
                        if len(self.predictionList) == 0:
                            self.errorDescription = "No hay estimaciones disponibles"
                    else:
                        self.predictionList = tempPredictionList
                    self.timeStampPrediction = self.parser.getTimeStamp()
                conn.unsubscribe(destination=RESPONSEQUEUENAME)
                conn.disconnect()
                self.errorDescription = self.parser.getError()
                    #empiezan las excepciones
        except SAXParseException:
            self.errorDescription = "Error de conexion con servidor"
            #Ver posibilidad de no estimacion
        except ValueError:
            self.errorDescription = "Datos en formato incorrecto - Valor de datos"
        except DatabaseError:
            self.errorDescription = "Error de base de datos"
        except stomp.exception.ConnectFailedException:
            self.errorDescription = "No hay conexion con el servidor"