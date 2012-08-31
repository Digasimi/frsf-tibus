# Create your views here.

import stomp, time
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.utils import DatabaseError
from tibus.forms import FormularioPrediccion
from tibus.models import Parada, Recorrido, Unidad, TiempoRecorrido, MyListener, PresponseHandler
from xml.sax import parseString,  SAXParseException

def index(request): #pagina principal
    return render_to_response('index.html',{'admin': False})
    
def modelo(request): #pagina que explica el funcionamiento del modelo
    return render_to_response('modelo.html',  {'admin': False})
    
def prediccion(request): #pagina que mostrara las predicciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    listaPrediccion = []
    descripcionError = ""
    prediccionTimeStamp = ""
    parser = PresponseHandler()
    
    listaLineas = Recorrido.objects.all().order_by('linea')
    listaParadas = Parada.objects.all()
    
    #logica
    if request.method == 'POST':
        form = FormularioPrediccion(request.POST)
        idLinea = request.POST.get('linea').upper()
        try:
            if request.POST.get('accion')=="predecir":
                if idLinea == '':
                    descripcionError = "No ingreso la linea"
                elif request.POST.get('orden')=='':
                    descripcionError = "No ingreso la parada"
                else:
                    newId= Recorrido.objects.get(linea = idLinea.upper())
                    listaParadas = Parada.objects.filter(linea = newId)
                    
                    #formato nuevo
                    conn = stomp.Connection([('127.0.0.1',61613)]) #Aca hay que definir el conector externo
                    conn.start()
                    conn.connect()
                    respuesta = '/temp-queue/respuesta'
                    mensaje = crearMensaje(idLinea,  request.POST.get('orden'))
                    conn.set_listener('list', MyListener())
                    conn.send(mensaje, destination='/queue/predictions.requests',headers={'reply-to':respuesta})
                    conn.subscribe(destination=respuesta, ack='auto')
                    mens = ""
                    lis1 = conn.get_listener('list')
                    timer = 0
                    while (mens == '' and timer < 6):
                        time.sleep(1)
                        timer=timer+1
                        mens = lis1.getMensaje()
                    if (timer == 6):
                        descripcionError = 'Tiempo de espera agotado'
                    else:
                        parseString(mens, parser)
                        listaPrediccion = parser.obtenerLista()
                        prediccionTimeStamp = parser.obtenerTimeStamp()
                    conn.unsubscribe(destination=respuesta)
                    conn.disconnect()
            else:
                if idLinea != '':
                    listaParadas = Parada.objects.filter(linea__linea = idLinea.upper())
            #empiezan las excepciones
        except SAXParseException:
            descripcionError = "Datos en formato incorrecto - Error de conexion con servidor"
        except ValueError:
            descripcionError = "Datos en formato incorrecto - Valor de datos"
        except DatabaseError:
            descripcionError = "Error de no se que" #Ver cuando salta este error. posible error de asociacion linea-parada
        except stomp.exception.ConnectFailedException:
            descripcionError = "No hay conexion con el servidor"
        except Recorrido.DoesNotExist:
            descripcionError = "No existe la linea"
        except Parada.DoesNotExist:
            descripcionError = "No existe la parada"
        except Unidad.DoesNotExist:
            descripcionError = "No hay unidades existentes"
        except TiempoRecorrido.DoesNotExist:
            descripcionError = "No hay estimaciones"
    else:
        form = FormularioPrediccion()
    return render_to_response('prediccion.html',  {'form':form, 'listaParadas': listaParadas, 'predicciones':listaPrediccion,  'error': descripcionError,  'admin': False,  'listaLineas':listaLineas, 'timeStamp': prediccionTimeStamp},  context_instance=RequestContext(request))
    
def ayuda(request):#pagina de ayuda
    return render_to_response('ayuda.html',  {'admin': False})

def crearMensaje(linea,  orden):
    return '<prediction-request><linea>'+linea+'</linea><parada>'+orden+'</parada></prediction-request>'
