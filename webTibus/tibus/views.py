# Create your views here.

import stomp
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.utils import DatabaseError
from django.http import HttpResponseRedirect
from tibus.forms import PredictionForm, ItineraryForm, TravelForm
from tibus.models import Parada, Recorrido, Unidad, Frecuencia
from tibus.listenerParseXML import Presponse
from tibus.predictor import Predictor
from timetobus.parameters import PREDICTIONSNUMBERS

def index(request): 
    '''
    pagina principal que redirecciona a la aplicacion acorde al dispositivo desde el que se accede
    '''
    c={}
    c.update(csrf(request))
    if request.is_mobile:
        if not request.is_http_mobile:
            return HttpResponseRedirect('windex')
        else:
            return HttpResponseRedirect('sindex')
    else:
        return render_to_response('index.html',{'admin': False},  context_instance=RequestContext(request))
    
def model(request): 
    '''
    pagina que explica el funcionamiento del modelo
    Actualmente fuera de uso
    '''
    c={}
    c.update(csrf(request))
    return render_to_response('modelo.html',  {'admin': False},  context_instance=RequestContext(request))
    
def prediction(request): 
    '''
    Pagina que mostrara el formulario para la carga de datos para la prediccion de tiempos de arribo
    '''
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
        except Recorrido.DoesNotExist:
            errorDescription = "No existe la route"
        except Parada.DoesNotExist:
            errorDescription = "No existe la parada"
    else:
        form = PredictionForm()
    return render_to_response('prediccion.html',  {'form':form, 'error': errorDescription,  'admin': False},  context_instance=RequestContext(request))
    
def contact(request):#pagina de ayuda
    '''
    Pagina que muestra los datos de contacto
    '''
    c={}
    c.update(csrf(request))
    return render_to_response('contact.html',  {'admin': False},  context_instance=RequestContext(request))

def arriveResult(request): 
    '''
    Pagina que mostrara los resultados de la prediccion de tiempos de arribo
    '''
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    stopList = []
    temporaryRoute = None
    nameTemporaryRoute = ""
    destinyStop = None
    
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
            nameTemporaryRoute = temporaryRoute.getLinea()
            stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
            destinyStop = Parada.objects.get(idparada = destinyStopId)
            predictorTemp = Predictor()
            predictorTemp.doPrediction(nameTemporaryRoute, destinyStopId, aptoPrediction)
            errorDescription = predictorTemp.getError()
            predictionList = predictorTemp.getPredictionList()
            timeStampPrediction = predictorTemp.getTimeStamp()
        #empiezan las excepciones
    except Recorrido.DoesNotExist:
        errorDescription = "No existe la route"
    except Parada.DoesNotExist:
        errorDescription = "No existe la parada"
    except Unidad.DoesNotExist:
        errorDescription = "No hay unidades existentes"
    return render_to_response('resultado.html',  {'route': temporaryRoute, 'stopList': stopList, 'predicciones':predictionList[0:PREDICTIONSNUMBERS],  'error': errorDescription,  'admin': False,  'timeStamp': timeStampPrediction, 'linea': nameTemporaryRoute, 'parada': destinyStop},  context_instance=RequestContext(request))

def itinerary(request): 
    '''
    Pagina que muestra el formulario y los datos de los recorridos de las lineas
    '''
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

def travelPrediction(request): 
    '''
    Pagina que mostrara el formulario de datos para las predicciones de tiempos de viaje
    '''
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

def travelResult(request): 
    '''pagina que mostrara los resultados de las estimaciones de tiempos de viaje
    ''' 
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    stopList = []
    temporaryRoute = None
    nameTemporaryRoute = ""
    destinyStop = None
    origenStop = None
    
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
            nameTemporaryRoute = temporaryRoute.getLinea()
            stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
            origenStop = Parada.objects.get(idparada = origenStopId)
            destinyStop = Parada.objects.get(idparada = destinyStopId)
            
            predictorTemp = Predictor()
            predictorTemp.doPrediction(nameTemporaryRoute, origenStopId, False)
            errorDescription = predictorTemp.getError()
            predictionList1 = predictorTemp.getPredictionList()
            if errorDescription == "":
                predictorTemp.doPrediction(nameTemporaryRoute, destinyStopId, False)
                errorDescription = predictorTemp.getError()
                predictionList2 = predictorTemp.getPredictionList()
                timeStampPrediction = predictorTemp.getTimeStamp()
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
        #empiezan las excepciones
    except Recorrido.DoesNotExist:
        errorDescription = "No existe la route"
    except Parada.DoesNotExist:
        errorDescription = "No existe la parada"
    except Unidad.DoesNotExist:
        errorDescription = "No hay unidades existentes"
    return render_to_response('vResultado.html',  {'route': temporaryRoute, 'stopList': stopList, 'predicciones':predictionList[0:PREDICTIONSNUMBERS],  'error': errorDescription,  'admin': False,  'timeStamp': timeStampPrediction, 'linea': nameTemporaryRoute, 'origen': origenStop,'destino': destinyStop},  context_instance=RequestContext(request))