# Create your views here.
import logging

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max
from tibusAdmin.forms import StopForm,  RouteForm,  BusForm, CompanyForm,  UserForm,\
    PassworForm
from tibus.models import Parada, Recorrido, Unidad, Empresa
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from tibusAdmin.models import Usuario 

@login_required
def tadmin(request):#pagina de ABM de lineas
    return HttpResponseRedirect('linea')

@login_required
def route(request):#pagina de ABM de lineas
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    routeList = []
    companyList = []
    logger = logging.getLogger(__name__)
    
    if (userData.categoria == 'Administrador'):
        companyList = Empresa.objects.all()        
        routeList = Recorrido.objects.all().order_by('linea')
    elif (userData.categoria == 'Empresa'):
        companyList = Empresa.objects.filter(nombre = userData.empresa)   
        routeList = Recorrido.objects.filter(company = userData.empresa).order_by('linea')
    superadmin = (userData.categoria == 'Administrador')
    
    #logica
    if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                form = RouteForm(request.POST, request.FILES)
                routeName=request.POST.get('linea').upper()
                if request.POST.get('action') == 'viewCompany':
                    routeList = Recorrido.objects.filter(empresa__nombre =request.POST.get('empresa').upper()).order_by('linea')
                elif routeName == '': #comprueba que se ingresa route
                    errorDescription = "No ingreso la linea"
                elif request.POST.get('action') == 'viewRoute':          #no necesitaria el is_valid, solo que exista route
                    return HttpResponseRedirect('recorrido' + routeName)
                elif form.is_valid():
                    if request.POST.get('action') == 'addRoute':
                        newFrecuency = request.POST.get('frecuencia')
                        companyName = request.POST.get('empresa').upper()
                        if int(newFrecuency) > 0: #compueba que la frecuencia sea un entero mayor a 0
                            temporaryRoute = Recorrido(linea = routeName,  frecuencia = newFrecuency, company = Empresa.objects.get(nombre=companyName)) 
                            if temporaryRoute.validate(): #comprobacion de datos de route
                                try:
                                    temporaryRoute = Recorrido.objects.get(linea = routeName) #da verdadero si la route existe ya.
                                    errorDescription = "Linea ya existente"
                                except Recorrido.DoesNotExist:
                                    temporaryRoute.save()
                                    try:
                                        if (request.FILES['masivo'] != ''):
                                            fileName = request.FILES['masivo']
                                            tempOrder = 0
                                            errors = 0
                                            for route in fileName:
                                                values = route.split(';') #aca se debe hacer la carga de archivos masivos
                                                stopName1=''
                                                stopName2=''
                                                try:
                                                    tempLat = float(values[0])
                                                    tempLon = float(values[1])
                                                    stopName1 = values[2]
                                                    stopName2 = values[3]
                                                    tempOrder = tempOrder + 1
                                                    newParada = Parada(orden = tempOrder,  latitud = tempLat, longitud = tempLon, linea = temporaryRoute, calle1 = stopName1, calle2 = stopName2)  
                                                    newParada.save()
                                                except:
                                                    errors = errors + 1
                                                    errorDescription = "se encontraron " + str(errors) + " errors de datos"
                                            print tempOrder
                                    except MultiValueDictKeyError:
                                        errorDescription = "Faltan cargar paradas"
                            else:
                                errorDescription = "Identificador no valido"
                        else:
                            errorDescription = "La frecuencia debe ser un numero entero mayor a 0"
                    elif request.POST.get('action') == 'editRoute':  #edicion de route.
                        fileName = request.FILES['file']
                        temporaryRoute = Recorrido.objects.get(linea = routeName)
                        temporaryRoute.frecuencia = int(request.POST.get('frecuencia'))
                        temporaryRoute.save()
                    else: #if request.POST.get('action') == 'delRoute': Asume que la accion por omision es borrar
                        #La confirmacion de la eliminacion es en el codigo html
                        temporaryRoute = Recorrido.objects.get(linea = routeName)
                        temporaryRoute.delete() #el delete de django borra en cascada por defecto
                    #else:
                        #errorDescription = "Accion no valida"
                else:
                    errorDescription = "Falta algun dato o tipo de dato invalido"
            #empiezan las excepciones
            except Recorrido.DoesNotExist:
                errorDescription = "La linea ingresada no existe"
            except Empresa.DoesNotExist:
                errorDescription = "La empresa ingresada no existe"
            logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + routeName + " Error:" + errorDescription)
        else:
            form = RouteForm()
    else:
        errorDescription = "No posee permisos para ejecutar esta accion"
    logger.info("Usuario: " + userData.nombre +" in Route Error:" + errorDescription)
    return render_to_response('linea.html',  {'user': request.user,'form':form, 'error':errorDescription , 'companyList': companyList, 'routeList': routeList, 'admin': True, 'superadmin':superadmin },  context_instance=RequestContext(request))

@login_required    
def bus(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    busList=[]
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    routeList = []
    logger = logging.getLogger(__name__)
    
    if (userData.categoria == 'Administrador'):
        routeList = Recorrido.objects.all().order_by('linea')
    elif (userData.categoria == 'Empresa'):
        routeList = Recorrido.objects.filter(company=userData.empresa).order_by('linea')
    superadmin = (userData.categoria == 'Administrador')
    #logica
    if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                routeName=request.POST.get('linea').upper()
                form = BusForm(request.POST)
                if routeName == '': #comprueba que se ingresa route
                    errorDescription = "No ingreso la linea"
                else:
                    route = Recorrido.objects.get(linea = routeName) #carga la route.
                    busId=request.POST.get('id_unidad_linea').upper()
                    if form.is_valid():
                        if request.POST.get('action') == 'addBus':
                            busApto = request.POST.get('aptoMovilidadReducida') 
                            if not(busApto):
                                busApto = 0;
                            try:
                                temporaryBus = Unidad.objects.get(linea = route, id_unidad_linea = busId) #da verdadero si la bus ya existe
                                errorDescription = "Unidad ya existente"
                            except Unidad.DoesNotExist:
                                temporaryBus = Unidad(linea = route,  aptoMovilidadReducida = busApto,  idunidad = routeName + "_" + busId, id_unidad_linea = busId)
                                temporaryBus.save()
                        elif request.POST.get('action') == 'editBus': 
                            temporaryBus = Unidad.objects.get(linea = route,  id_unidad_linea = busId)
                            busApto = request.POST.get('aptoMovilidadReducida') 
                            if busApto:
                                temporaryBus.aptoMovilidadReducida = 1;
                            else:
                                temporaryBus.aptoMovilidadReducida = 0;
                            temporaryBus.save()
                        else: #if request.POST.get('action') == 'delBus': Asume que la accion por omision es borrar
                            #La confirmacion de la eliminacion es en el codigo html
                            temporaryBus = Unidad.objects.get(linea = route,  id_unidad_linea = busId)
                            temporaryBus.delete()
                        #else:
                            #errorDescription = "Accion no valida: " + str(request.POST.get('action'))
                    else:
                        errorDescription = "Falta ingresar algun dato"
                    busList = Unidad.objects.filter(linea = route).order_by('id_unidad_linea')
            #empiezan las excepciones
            except Recorrido.DoesNotExist:
                errorDescription = "No existe la linea"
            except Unidad.DoesNotExist:
                errorDescription = "No existe/n unidad/es"
            form = BusForm()
            logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + routeName + " Unidad: " + busId + " Error:" + errorDescription)
        else:
            form = BusForm()
            busList = Unidad.objects.all().order_by('id_unidad_linea')
    else:
        form = BusForm()
        errorDescription = "No posee permisos para ejecutar esta accion"
    logger.info("Usuario: " + userData.nombre +" in Bus Error:" + errorDescription)
    return render_to_response('unidad.html',  {'user': request.user,'form':form,  'error': errorDescription,  'busList':busList,  'admin': True,  'routeList': routeList,'superadmin':superadmin},  context_instance=RequestContext(request))

def orderStopList(stopList): #metodo para ordenar las paradas e evitar saltar el orden
    i=1
    for tempStop in stopList:
        if tempStop.getOrder() > i:
            while tempStop.getOrder() > i:
                tempStop.downOneOrder()
            tempStop.save()
        i = i +1
    return stopList

@login_required    
def company(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    companyList=[]
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    
    if (userData.categoria == 'Administrador'):
        companyList = Empresa.objects.all().order_by('nombre')        
        superadmin = True
    else:
        superadmin = False
        
    #logica
    if (userData.categoria == 'Administrador'):
        if request.method == 'POST':
            try:
                companyName=request.POST.get('nombre').upper()
                companyEmail=request.POST.get('companyEmail').lower()
                form = CompanyForm(request.POST)
                if companyName == '': #comprueba que el nombre no sea vacia.
                    errorDescription = "No ingreso la empresa"
                elif request.POST.get('action') == 'addCompany':
                    if companyEmail == "": #comprobar direccion de mail, no comprueba formato.
                        errorDescription = "No ingreso datos validos"
                    else:
                        try:
                            temporaryCompany = Empresa.objects.get(nombre = companyName) #da verdadero si la route ya existe.
                            errorDescription = "Empresa ya existente"
                        except:
                            temporaryCompany = Empresa(nombre = companyName,  mail = companyEmail)
                            temporaryCompany.save()
                            logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Empresa: " + companyName + " Error:" + errorDescription)
                else:
                    temporaryCompany = Empresa.objects.get(nombre = companyName)
                    if request.POST.get('action') == 'editCompany': 
                        temporaryCompany.mail = companyEmail;
                        temporaryCompany.save();
                    else: #if request.POST.get('action') == 'delEmpresa': Asume que la accion por omision es borrar
                        #La confirmacion de la eliminacion es en el codigo html
                        temporaryCompany.delete()
                #else:
                    #errorDescription = "Accion no valida: " + str(request.POST.get('action'))
                companyList=Empresa.objects.all().order_by('nombre')
            #empiezan las excepciones
            except Empresa.DoesNotExist:
                errorDescription = "No existe la empresa"
            logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Empresa: " + companyName + " Error:" + errorDescription)
        else:
            form = CompanyForm()
    else:
        form = CompanyForm()
        errorDescription = "No posee permisos para ejecutar esta accion"
    logger.info("Usuario: " + userData.nombre +" in Company Error:" + errorDescription)        
    return render_to_response('empresa.html',  {'user': request.user, 'admin': True,'form':form,  'error': errorDescription,  'companyList':companyList, 'superadmin':superadmin},  context_instance=RequestContext(request))

@login_required    
def user(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    userList = []
    companyList = []
    categoryList = []
    logger = logging.getLogger(__name__)
    
    if (userData.categoria == 'Administrador'):
        userList=Usuario.objects.filter(is_active = True).order_by('nombre')
        companyList = Empresa.objects.all().order_by('nombre')        
        categoryList = ['Administrador', 'Empresa']
        superadmin = True
    else:
        superadmin = False
        
    #logica
    if (userData.categoria == 'Administrador'):
        if request.method == 'POST':
            try:
                form = UserForm(request.POST)
                userName=request.POST.get('nombre').upper()
                if userName == '': #comprueba que el nombre no sea vacia.
                    errorDescription = "No ingreso el nombre del user"
                elif request.POST.get('action') == 'addUser':
                    if form.is_valid(): #comprobar direccion de mail, no comprueba formato.
                        userName=request.POST.get('userName').lower()
                        userCategory=request.POST.get('userCategory')
                        if (request.POST.get('empresa') != ""):
                            company = Empresa.objects.get(nombre = request.POST.get('empresa'))
                        else:
                            company = None
                        password=request.POST.get('password')
                        try:
                            temporaryUser = Usuario.objects.get(nombre = userName) #da verdadero si la route ya existe.
                            errorDescription = "Usuario ya existente"
                        except:
                            if (password == request.POST.get('confirmacion')):
                                temporaryUser = Usuario(username = userName, nombre = userName,  mail = userName,  userCategory=userCategory,  company=company)
                                temporaryUser.set_password(password)
                                if (userCategory =='Administrador'):
                                    temporaryUser.is_superuser = True
                                temporaryUser.save()
                            else:
                                errorDescription = "Las passwords no coinciden"
                    else:
                        errorDescription = "No ingreso datos validos"
                else:
                    temporaryUser = Usuario.objects.get(nombre = userName)
                    if request.POST.get('action') == 'viewUser': #No se usa
                        form = UserForm(userName = request.POST.get('userName').lower())
                    elif request.POST.get('action') == 'rehabUser':
                        temporaryUser.is_active = True
                        temporaryUser.save()
                    elif request.POST.get('action') == 'editUser': 
                        if(request.POST.get('userName').lower() != ''):
                            temporaryUser.mail=request.POST.get('userName').lower()
                        if (password == request.POST.get('confirmacion')):
                            temporaryUser.set_password(password)
                        else:
                            errorDescription = "Las passwords no coinciden"
                        temporaryUser.save();
                    elif request.POST.get('action') == 'delUser': #Asume que la accion por omision es borrar
                        #La confirmacion de la eliminacion es en el codigo html
                        if ((temporaryUser.categoria == "Administrador") and (Usuario.objects.filter(userCategory = "Administrador").count() > 1)):
                            errorDescription = "No se puede eliminar el ultimo usuario Administrador"
                        elif ((temporaryUser.categoria == "Empresa")and(temporaryUser.nombre != userData.nombre)):
                            errorDescription = "No se puede eliminar otro usuario de igual Jerarquia"
                        elif((temporaryUser.categoria == "Empresa")and(temporaryUser.categoria == "Administrador")):
                            errorDescription = "No se puede eliminar otro usuario de mayor Jerarquia"
                        else:
                            temporaryUser.is_active = False
                            temporaryUser.save()
                #else:
                    #errorDescription = "Accion no valida: " + str(request.POST.get('action'))
                userList=Usuario.objects.filter(is_active = True ).order_by('nombre')
            #empiezan las excepciones
            except Usuario.DoesNotExist:
                errorDescription = "No existe el usuario"
            except Empresa.DoesNotExist:
                errorDescription = "No existe la compania"
            logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Nombre_Usuario: " + userName + " Error:" + errorDescription)
        else:
            form = UserForm()
    else:
        form = UserForm()
        errorDescription = "No posee permisos para ejecutar esta accion"
    logger.info("Usuario: " + userData.nombre +" in User Error:" + errorDescription)        
    return render_to_response('usuario.html',  {'user': request.user,'form':form,  'error': errorDescription,  'userList':userList,  'admin': True,  'companyList' : companyList,  'categoryList':categoryList, 'superadmin':superadmin},  context_instance=RequestContext(request))

@login_required
def stop(request, routeId): #Pagina de ABM de paradas
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)  
    superadmin = (userData.categoria == 'Administrador')
    form = StopForm()
    
    #logica
    try:
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            stopList = Parada.objects.filter(linea__linea = routeId).order_by('orden')
            form = StopForm()
            routeId = routeId.upper()
            temporaryRoute= Recorrido.objects.get(linea = routeId)
            stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
            if request.method == 'POST':
                temporaryOrder = request.POST.get('orden')
                if temporaryOrder == None or temporaryOrder == '':
                    temporaryOrder = 0
                try:
                    if int(temporaryOrder) >= 0:  #comprueba que el orden sea un entero mayor que 0
                        if request.POST.get('action') == 'addStop':
                            temporaryLat = float(request.POST.get('newlatitud'))
                            temporaryLon = float(request.POST.get('newlongitud'))
                            nameStop1 = request.POST.get('calle1')
                            nameStop2 = request.POST.get('calle2')
                            predectibleStop = request.POST.get('paradaactiva')
                            if not(predectibleStop):
                                predectibleStop = 0
                            if len(stopList) == 0: #comprueba que no sea la primer parada
                                temporaryOrder = 1
                            elif temporaryOrder != 0: #agrega la parada en una posicion especifica
                                for temporaryStop in stopList: 
                                    if temporaryStop.getOrder() > int(temporaryOrder): 
                                        temporaryStop.upOneOrder()
                                        temporaryStop.save()
                                stopList = orderStopList(Parada.objects.filter(linea = temporaryRoute).order_by('orden'))
                            else: #agrega la parada al final del recorrido
                                temporaryOrder = stopList.aggregate(orden=Max('orden')).get('orden') + 1
                            temporaryStop = Parada(orden = temporaryOrder,  latitud = temporaryLat, longitud = temporaryLon, linea = temporaryRoute, calle1 = nameStop1,calle2 = nameStop2,paradaactiva = predectibleStop)  
                            temporaryStop.save()
                        elif request.POST.get('action') == 'editStop': #sin revisar - Falta ver que pasa si se cambia el orden.
                            temporaryStop = Parada.objects.get(orden = int(temporaryOrder),  linea = temporaryRoute)  
                            temporaryStop.latitud = float(request.POST.get('newlatitud'))
                            temporaryStop.longitud = float(request.POST.get('newlongitud'))
                            temporaryStop.calle1 = request.POST.get('calle1')
                            temporaryStop.calle2 = request.POST.get('calle2')
                            if request.POST.get('paradaactiva'):
                                temporaryStop.paradaactiva = True
                            else:
                                temporaryStop.paradaactiva = False  
                            temporaryStop.save()
                        else: #if request.POST.get('action') == 'delParada':  Asume que la accion por omision es borrar
                            #La confirmacion de la eliminacion es en el codigo html
                            temporaryStop = Parada.objects.get(orden = temporaryOrder,  linea = temporaryRoute)  
                            temporaryStop.delete()
                            #!reacomodar paradas                
                            for temporaryStop in stopList: 
                                if temporaryStop.getOrder() > int(temporaryOrder): 
                                    temporaryStop.downOneOrder()
                                    temporaryStop.save()
                            stopList = orderStopList(Parada.objects.filter(linea = temporaryRoute).order_by('orden'))
                        #else:
                            #errorDescription = "Accion no valida"
                    else:
                        errorDescription = "El orden debe ser un numero entero mayor a 0"
                except ValueError:
                    errorDescription = "El orden debe ser un numero entero"
                except TypeError:
                    errorDescription = "Las coordenadas no pueden ser vacias"
                logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + routeId + " Parada: " + temporaryOrder + " Error:" + errorDescription)
            stopList = Parada.objects.filter(linea__linea = routeId).order_by('orden') # para actualizar cambios en la lista de paradas
        else:
            errorDescription = "No posee permisos para ejecutar esta accion"
    #empiezan las excepciones
    except Recorrido.DoesNotExist:
        return HttpResponseRedirect('linea')
    except Parada.DoesNotExist:
        form = StopForm()
        errorDescription = "No existen paradas"
    logger.info("Usuario: " + userData.nombre +" in Stop Error:" + errorDescription)
    return render_to_response('recorrido.html', {'user': request.user,'form': form,  'route': routeId, 'stopList': stopList ,  'error': errorDescription,  'admin': True, 'superadmin':superadmin}, context_instance=RequestContext(request))

@login_required
def changepassword(request):
    errorDescription = ""
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        form = PassworForm(request.POST)
        temporaryUser = Usuario.objects.get(nombre = request.user)
        if(request.POST.get('newPassword')==request.POST.get('confirmacion')):
            if(temporaryUser.check_password(request.POST.get('oldPassword'))):
                temporaryUser.set_password(request.POST.get('newPassword'))
                temporaryUser.save()
                errorDescription = 'La password se cambio con exito'
            else:
                errorDescription = 'El password ingresada no es la correcta'
        else:
            errorDescription = 'Los passwords no coinciden'
    else:
        form = PassworForm()
    logger.info("Usuario: " + request.user +" Accion: ChangePassword Error:" + errorDescription)
    return render_to_response('change_password.html', {'temporaryUser': request.user, 'form': form, 'error': errorDescription,  'admin': True}, context_instance=RequestContext(request))