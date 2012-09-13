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
    return render_to_response('index.html',{'admin': False})
    
def model(request): #pagina que explica el funcionamiento del modelo
    return render_to_response('modelo.html',  {'admin': False})
    
def prediction(request): #pagina que mostrara las predicciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    parser = PresponseHandler()
    
    routeList = Recorrido.objects.all().order_by('route')
    stopList = Parada.objects.all()
    
    #logica
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        routeName = request.POST.get('route').upper()
        try:
            if request.POST.get('action')=="prediction":
                if routeName == '':
                    errorDescription = "No ingreso la linea"
                elif request.POST.get('orden')=='':
                    errorDescription = "No ingreso la parada"
                else:
                    temporaryRoute= Recorrido.objects.get(route = routeName.upper())
                    destinyStop = Parada.objects.get(route = temporaryRoute, orden = request.POST.get('orden'))
                    
                    #formato nuevo
                    conn = stomp.Connection([('127.0.0.1',61613)]) #Aca hay que definir el conector externo
                    conn.start()
                    conn.connect()
                    responseQueue = '/temp-queue/responseQueue'
                    msg = createMessage(temporaryRoute.getId(),  destinyStop.getId())
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
    return render_to_response('prediccion.html',  {'form':form, 'listaParada': stopList, 'predicciones':predictionList,  'error': errorDescription,  'admin': False,  'listaLinea':routeList, 'timeStamp': timeStampPrediction},  context_instance=RequestContext(request))
    
def tibushelp(request):#pagina de ayuda
    return render_to_response('ayuda.html',  {'admin': False})

def createMessage(route,  order):
    return '<prediction-request><route>' + str(route) + '</route><parada>' + str(order) + '</parada></prediction-request>'
