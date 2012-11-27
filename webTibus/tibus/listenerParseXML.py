from xml.sax.handler import ContentHandler
from tibus.models import Presponse

#Clase que define un objeto que reenvia y recibe mensajes via stomp al servidor JMS
class MyListener(object):
    message = ''
  
    def on_error(self, headers, message):
        print ('received an error %s' % message)

    def on_message(self, headers, message):
        print ('received a message %s' % message)
        self.message = message
        
    def getMessage(self):
        return self.message

#Clase que maneja el xml respuesta y lo transforma en un lista de datos de Presponse    
class PresponseHandler(ContentHandler):
    list = []
    isColeElement= 0
    isTimeElement = 0
    islatElement = 0
    islonElement = 0
    isTimeStampElement = 0
    isErrorElemet = 0
    bus = ""
    time = ""
    lat = ""
    lon = "" 
    timestamp = ""
    error = ""
    
    def __init__ (self):
        self.list = []
        self.isColeElement= 0
        self.isTimeElement = 0
        self.islatElement = 0
        self.islonElement = 0
        self.isTimeStampElement = 0
        self.isErrorElemet = 0
        self.bus = ""
        self.time = ""
        self.lat = ""
        self.lon = ""
        self.timestamp = ""
        self.error = ""
    
    def startElement(self, name, attrs):
        if name == 'busId':
            self.isColeElement= 1
            self.bus = ""
        elif name == 'timeSec':
            self.isTimeElement = 1
            self.time = ""
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
            self.bus += ch
        if self.isTimeElement == 1:
            self.time += ch
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
            self.isTimeElement = 0
        if name == 'lat':
            self.islatElement = 0
        if name == 'lon':
            self.islonElement = 0
        if name == 'prediction':
            prediction = int(self.bus)/60
            self.list = self.list + [Presponse(self.bus, prediction)]
        if name == 'timestamp':
            self.isTimeStampElement = 0
        if name == "error":
            self.isErrorElemet = 0
        if name == 'prediction-response':
            print self.list
    
    def getLista(self):
        return self.list
    
    def getTimeStamp(self):
        return self.timestamp
    
    def getError(self):
        return self.error