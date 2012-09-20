# Create your views here.

import stomp, time
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.utils import DatabaseError
from tibus.forms import PredictionForm
from tibus.models import Parada, Recorrido, Unidad, TiempoRecorrido, MyListener, PresponseHandler
from xml.sax import parseString,  SAXParseException

def index(request): #pagina principal
    c={}
    c.update(csrf(request))
    return render_to_response('index.html',{'admin': False},  context_instance=RequestContext(request))
    
def model(request): #pagina que explica el funcionamiento del modelo
    c={}
    c.update(csrf(request))
    return render_to_response('modelo.html',  {'admin': False},  context_instance=RequestContext(request))
    
def prediction(request): #pagina que mostrara las predicciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    parser = PresponseHandler()
    routeName = ""
    routeList = Recorrido.objects.all().order_by('linea')
    stopList = Parada.objects.all()
    
    #logica
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        routeName = request.POST.get('linea').upper()
        try:
            if request.POST.get('action')=="prediction":
                if routeName == '':
                    errorDescription = "No ingreso la linea"
                elif request.POST.get('orden')=='':
                    errorDescription = "No ingreso la parada"
                else:
                    temporaryRoute= Recorrido.objects.get(linea = routeName.upper())
                    stopList = Parada.objects.filter(linea = temporaryRoute)
                    destinyStop = Parada.objects.get(linea = temporaryRoute, orden = request.POST.get('orden'))
                    
                    #formato nuevo
                    conn = stomp.Connection([('127.0.0.1',61613)]) #Aca hay que definir el conector externo
                    conn.start()
                    conn.connect()
                    responseQueue = '/temp-queue/responseQueue'
                    msg = createMessage(temporaryRoute.getLinea(),  destinyStop.getId())
                    conn.set_listener('list', MyListener())
                    conn.send(msg, destination='/queue/predictions.requests',headers={'reply-to':responseQueue})
                    conn.subscribe(destination=responseQueue, ack='auto')
                    predictionXml = ""
                    lis1 = conn.get_listener('list')
                    timer = 0
                    while (predictionXml == '' and timer <= 15):
                        time.sleep(1)
                        timer=timer+1
                        predictionXml = lis1.getMessage()
                    if (timer == 15):
                        errorDescription = 'Tiempo de espera agotado'
                    else:
                        parseString(predictionXml, parser)
                        predictionList = parser.getLista()
                        timeStampPrediction = parser.getTimeStamp()
                    conn.unsubscribe(destination=responseQueue)
                    conn.disconnect()
                    errorDescription = parser.getError()
            else:
                if routeName != '':
                    stopList = Parada.objects.filter(linea__linea = routeName.upper())
            #empiezan las excepciones
        except SAXParseException:
            errorDescription = "Datos en formato incorrecto - Error de conexion con servidor"
        except ValueError:
            errorDescription = "Datos en formato incorrecto - Valor de datos"
        except DatabaseError:
            errorDescription = "Error de no se que" #Ver cuando salta este error. posible error de asociacion route-parada
        except stomp.exception.ConnectFailedException:
            errorDescription = "No hay conexion con el servidor"
        except Recorrido.DoesNotExist:
            errorDescription = "No existe la route"
        except Parada.DoesNotExist:
            errorDescription = "No existe la parada"
        except Unidad.DoesNotExist:
            errorDescription = "No hay unidades existentes"
        except TiempoRecorrido.DoesNotExist:
            errorDescription = "No hay estimaciones"
    else:
        form = PredictionForm()
        routeName = None
    return render_to_response('prediccion.html',  {'route': routeName ,'form':form, 'stopList': stopList, 'predicciones':predictionList,  'error': errorDescription,  'admin': False,  'routeList':routeList, 'timeStamp': timeStampPrediction},  context_instance=RequestContext(request))
    
def tibushelp(request):#pagina de ayuda
    c={}
    c.update(csrf(request))
    return render_to_response('ayuda.html',  {'admin': False},  context_instance=RequestContext(request))

def createMessage(route,  order):
    return '<prediction-request><linea>' + str(route) + '</linea><parada>' + str(order) + '</parada></prediction-request>'