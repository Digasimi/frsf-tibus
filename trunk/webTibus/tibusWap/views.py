# Create your views here.
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from tibus.models import Empresa, Recorrido, Parada
from tibus.predictor import predictor
from timetobus.parameters import MOBILEPREDICTIONSNUMBERS

def index(request): #pagina principal
    c={}
    c.update(csrf(request))
    companyList = Empresa.objects.all().order_by('nombre')
    return render_to_response('index.wml',{'companyList': companyList,'admin': False},  context_instance=RequestContext(request))

def company(request, companyId): #pagina principal
    c={}
    c.update(csrf(request))
    routeList = Recorrido.objects.filter(empresa = companyId).order_by('linea')
    return render_to_response('company.wml',{'routeList': routeList,'admin': False},  context_instance=RequestContext(request))

def route(request, routeId): #pagina principal
    c={}
    c.update(csrf(request))
    stopList = Parada.objects.filter(linea = routeId, paradaactiva = True).order_by('orden')
    return render_to_response('route.wml',{'stopList': stopList,'admin': False},  context_instance=RequestContext(request))

def result(request, stopId): #pagina principal
    #carga inicial
    c = {}
    c.update(csrf(request))
    predictionList = []
    errorDescription = ""
    timeStampPrediction = ""
    
    #logica
    try:
        temporaryRoute= Parada.objects.get(idparada = stopId).getLinea().getLinea()
        predictorTemp = predictor()
        predictorTemp.doPrediction(temporaryRoute, stopId, False)
        errorDescription = predictorTemp.getError()
        predictionList = predictorTemp.getPredictionList()
        timeStampPrediction = predictorTemp.getTimeStamp()
        #empiezan las excepciones
    except Recorrido.DoesNotExist:
        errorDescription = "No existe la route"
    except Parada.DoesNotExist:
        errorDescription = "No existe la parada"
    return render_to_response('result.wml',{'timeStamp':timeStampPrediction,'error': errorDescription, 'predictionList': predictionList[0:MOBILEPREDICTIONSNUMBERS],'admin': False},  context_instance=RequestContext(request))