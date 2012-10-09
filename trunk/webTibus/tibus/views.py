# Create your views here.

import stomp, time
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.utils import DatabaseError
from django.http import HttpResponseRedirect
from tibus.forms import PredictionForm
from tibus.models import Parada, Recorrido, Unidad, MyListener, PresponseHandler
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
    errorDescription = ""
    timeStampPrediction = ""
    routeName = ""
    
    #logica
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        try:
            if request.POST.get('action')=="prediction":
                if form.is_valid():
                    routePrediction = form.cleaned_data['linea']
                    stopPrediction = form.cleaned_data['orden']
                    aptoPrediction = form.cleaned_data['apto']
                    if aptoPrediction == None:
                        aptoPrediction = False
                    return HttpResponseRedirect('resultado?linea=' + str(routePrediction.getLinea()) + '&parada='+ str(stopPrediction)+'&apto='+str(aptoPrediction))
                else:
                    if request.POST.get('linea') == None:
                        errorDescription = "No ingreso la linea"
                    elif request.POST.get('orden') == None:
                        errorDescription = "No ingreso la parada"
                    else:                    
                        errorDescription = "Datos en formato incorrecto"
            else:
                if routeName != '':
                    form.initial = {'linea': routeName}
                    form.orden.queryset = Parada.objects.filter(linea=routeName)
            #empiezan las excepciones
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
    else:
        form = PredictionForm()
        routeName = None
    return render_to_response('prediccion.html',  {'linea': routeName ,'form':form, 'error': errorDescription,  'admin': False, 'timeStamp': timeStampPrediction},  context_instance=RequestContext(request))
    
def tibushelp(request):#pagina de ayuda
    c={}
    c.update(csrf(request))
    return render_to_response('ayuda.html',  {'admin': False},  context_instance=RequestContext(request))

def createMessage(route,  order):
    return '<prediction-request><linea>' + str(route) + '</linea><parada>' + str(order) + '</parada></prediction-request>'

def result(request): #pagina que mostrara las predicciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    parser = PresponseHandler()
    stopList = Parada.objects.all()
    
    #logica
    routeName = request.GET.get('linea').upper()
    destinyStopId= request.GET.get('parada')
    aptoPrediction = request.GET.get('apto')
    if request.POST.get('action') == 'prediction':
        return HttpResponseRedirect('prediccion')
    try:
        if routeName == '':
            errorDescription = "No ingreso la linea"
        elif destinyStopId == '':
            errorDescription = "No ingreso la parada"
        else:
            temporaryRoute= Recorrido.objects.get(linea = routeName.upper())
            stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
            destinyStop = Parada.objects.get(linea = temporaryRoute, orden = destinyStopId)
            
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
                tempPredictionList = parser.getLista()
                errorDescription = parser.getError()
                if (aptoPrediction == 'True'):#filtrar lista con colec aptos
                    for prediction in tempPredictionList:
                        try:
                            temporaryBus = Unidad.objects.get(id_unidad_linea = prediction.bus, linea__linea = routeName)
                            if (temporaryBus.getApto() == True):
                                predictionList = predictionList + [prediction]
                        except Unidad.DoesNotExist:
                            predictionList = predictionList
                    if len(predictionList) == 0:
                        errorDescription = "No hay estimaciones disponibles"
                else:
                    predictionList = tempPredictionList
                timeStampPrediction = parser.getTimeStamp()
            conn.unsubscribe(destination=responseQueue)
            conn.disconnect()
            errorDescription = parser.getError()
        #empiezan las excepciones
    except SAXParseException:
        errorDescription = "Datos en formato incorrecto - Error de conexion con servidor"
        #Ver posibilidad de no estimacion
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
    return render_to_response('resultado.html',  {'route': routeName, 'stopList': stopList, 'predicciones':predictionList,  'error': errorDescription,  'admin': False,  'timeStamp': timeStampPrediction, 'linea': routeName, 'parada': destinyStopId},  context_instance=RequestContext(request))
