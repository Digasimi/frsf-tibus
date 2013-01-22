from xml.sax.handler import ContentHandler

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
            prediction = int(self.time)/60
            predictionSeg = int(self.time) % 60
            self.list = self.list + [Presponse(self.bus, prediction, predictionSeg, self.lat, self.lon)]
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
    
    #Clase que guarda una estimacion de tiempo
class Presponse(object):
    bus = ''
    time = 0
    lat = 0
    lon = 0
    timeseg = 0
    
    def __init__ (self, c, t, ts, la, lo):
        self.bus = c
        self.time = t
        self.timeseg = ts
        self.lat = la
        self.lon = lo

    def __unicode__(self):
        return self.bus
    
    def getBus(self):
        return self.bus
    
    def getTime(self):
        return self.time
    
    def getLat(self):
        return self.lat
    
    def getLon(self):
        return self.lon
    
    def setLatLon(self, nuevaLat, nuevaLon):
        self.lat = nuevaLat
        self.lon = nuevaLon
        
    def setTimeSeg(self, newTimeSeg):
        self.timeseg = newTimeSeg