# Create your views here.

import stomp, time
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.utils import DatabaseError
from django.http import HttpResponseRedirect
from tibus.forms import PredictionForm, ItineraryForm, TravelForm
from tibus.models import Parada, Recorrido, Unidad, Frecuencia
from tibus.listenerParseXML import MyListener, PresponseHandler, Presponse
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
        
    #logica
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        try:
            if request.POST.get('action')=='resultado':
                routePrediction = Recorrido.objects.get(idrecorrido=request.POST.get('linea'))
                stopPrediction = Parada.objects.get(idparada = request.POST.get('orden'))
                aptoPrediction = request.POST.get('apto')
                if aptoPrediction == None:
                    aptoPrediction = False
                return HttpResponseRedirect('resultado?linea=' + str(routePrediction.getId()) + '&parada='+ str(stopPrediction.getId())+'&apto='+str(aptoPrediction))
            else:
                form.setQueryOrden(request.POST.get('linea'))
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
    return render_to_response('prediccion.html',  {'form':form, 'error': errorDescription,  'admin': False},  context_instance=RequestContext(request))
    
def contact(request):#pagina de ayuda
    c={}
    c.update(csrf(request))
    return render_to_response('contact.html',  {'admin': False},  context_instance=RequestContext(request))

#Funcino que crea el mensaje xml dados los id de route y de unidad
def createMessage(route,  order):
    if route == None or order == None or route == '' or order == '':
        return None
    else: 
        return '<prediction-request><linea>' + str(route) + '</linea><parada>' + str(order) + '</parada></prediction-request>'

def arriveResult(request): #pagina que mostrara las predicciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    parser = PresponseHandler()
    stopList = Parada.objects.all()
    
    #logica
    routeName = request.GET.get('linea')
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
            temporaryRoute= Recorrido.objects.get(idrecorrido = routeName)
            stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
            destinyStop = Parada.objects.get(idparada = destinyStopId)
            
            #formato nuevo
            conn = stomp.Connection([('127.0.0.1',61613)]) #Aca hay que definir el conector externo
            conn.start()
            conn.connect()
            responseQueue = '/temp-queue/responseQueue'
            msg = createMessage(temporaryRoute.getLinea(),  destinyStop.getId())
            if msg == None:
                errorDescription = "Datos incompletos"
            else:
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
        errorDescription = "Error de conexion con servidor"
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
    return render_to_response('resultado.html',  {'route': temporaryRoute, 'stopList': stopList, 'predicciones':predictionList[0:6],  'error': errorDescription,  'admin': False,  'timeStamp': timeStampPrediction, 'linea': temporaryRoute.getLinea(), 'parada': destinyStop},  context_instance=RequestContext(request))

def itinerary(request): #pagina que muestra las recorridos de las distintas unidades
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    form = ItineraryForm()
    if request.method == 'POST':
        temporaryRoute = Recorrido.objects.get(idrecorrido = request.POST.get('linea'))
        stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
        frecuencyList = Frecuencia.objects.filter(linea = temporaryRoute)
        form.quitEmptyOption()
        form.initial = {'linea':request.POST.get('linea')}
    else:
        temporaryRoute = None
        stopList = []
        frecuencyList = []
    
    return render_to_response('itinerario.html',  {'stopList':stopList, 'frecuencyList':frecuencyList, 'error': errorDescription, 'form': form},  context_instance=RequestContext(request))

def travelPrediction(request): #pagina que mostrara el formulario de datos para las predicciones de tiempos de viaje
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
        
    #logica
    if request.method == 'POST':
        form = TravelForm(request.POST)
        try:
            if request.POST.get('action')=='resultado':
                routePrediction = Recorrido.objects.get(idrecorrido=request.POST.get('linea'))
                origenStopPrediction = Parada.objects.get(idparada = request.POST.get('origen'))
                destinyStopPrediction = Parada.objects.get(idparada = request.POST.get('destino'))
                if (destinyStopPrediction.getOrder() >= origenStopPrediction.getOrder()):
                    return HttpResponseRedirect('rViaje?linea=' + str(routePrediction.getId()) + '&origen='+ str(origenStopPrediction.getId())+'&destino='+ str(destinyStopPrediction.getId()))
                else:
                    errorDescription = "La parada destino debe ser posterior a la parada origen"
                    form.setQueryOrden(request.POST.get('linea'))
            else:
                form.setQueryOrden(request.POST.get('linea'))
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
        form = TravelForm()
    return render_to_response('prediccion.html',  {'form':form, 'error': errorDescription,  'admin': False},  context_instance=RequestContext(request))

def travelResult(request): #pagina que mostrara los resultados de las estimaciones de tiempos de viaje 
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    parser = PresponseHandler()
    stopList = Parada.objects.all()
    
    #logica
    routeName = request.GET.get('linea')
    origenStopId= request.GET.get('origen')
    destinyStopId= request.GET.get('destino')
    if request.POST.get('action') == 'prediction':
        return HttpResponseRedirect('viaje')
    try:
        if routeName == '':
            errorDescription = "No ingreso la linea"
        elif destinyStopId == '' or origenStopId == '':
            errorDescription = "No ingreso la parada"
        else:
            temporaryRoute= Recorrido.objects.get(idrecorrido = routeName)
            stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
            origenStop = Parada.objects.get(idparada = origenStopId)
            destinyStop = Parada.objects.get(idparada = destinyStopId)
            
            #formato nuevo
            conn = stomp.Connection([('127.0.0.1',61613)]) #Aca hay que definir el conector externo
            conn.start()
            conn.connect()
            responseQueue = '/temp-queue/responseQueue'
            conn.set_listener('list', MyListener())
            #Estimacion origen
            msg = createMessage(temporaryRoute.getLinea(),  origenStop.getId())
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
                predictionList1 = parser.getLista()
                errorDescription = parser.getError()
                timeStampPrediction = parser.getTimeStamp()
            if errorDescription == "":
                #Estimacion destino
                msg = createMessage(temporaryRoute.getLinea(),  destinyStop.getId())
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
                    predictionList2 = parser.getLista()
                    errorDescription = parser.getError()
                if errorDescription == "":
                    if predictionList1 == [] or predictionList2 == []:
                        errorDescription = "No hay predicciones disponibles"
                    else:
                        for prediccion1 in predictionList1:
                            for prediccion2 in predictionList2:
                                if prediccion1.bus == prediccion2.bus:
                                    if (prediccion2.timeseg >= prediccion1.timeseg):
                                        predictionMinute = (prediccion2.time - prediccion1.time)
                                        predictionSecond = (prediccion2.timeseg - prediccion1.timeseg)
                                    else:
                                        predictionMinute = (prediccion2.time - 1 - prediccion1.time)
                                        predictionSecond = (prediccion2.timeseg + 60 - prediccion1.timeseg)
                                    predictionList = [Presponse(prediccion1.bus, predictionMinute, predictionSecond,0,0)]
                        if predictionList == []:
                            errorDescription = "No hay predicciones disponibles"
            conn.unsubscribe(destination=responseQueue)
            conn.disconnect()
        #empiezan las excepciones
    except SAXParseException:
        errorDescription = "Error de conexion con servidor"
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
    return render_to_response('vResultado.html',  {'route': temporaryRoute, 'stopList': stopList, 'predicciones':predictionList[0:6],  'error': errorDescription,  'admin': False,  'timeStamp': timeStampPrediction, 'linea': temporaryRoute.getLinea(), 'origen': origenStop,'destino': destinyStop},  context_instance=RequestContext(request))