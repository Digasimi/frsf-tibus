import logging

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max
from tibusAdmin.forms import StopForm, RouteForm, BusForm, CompanyForm, UserForm, PasswordForm, RoutesForm,\
    StopsForm, BussForm, UsersForm, CompaniesForm, EliminarForm, FrecuenciesForm,\
    FrecuencyForm
from tibus.models import Parada, Recorrido, Unidad, Empresa, Frecuencia
from django.contrib.auth.decorators import login_required
from tibusAdmin.models import Usuario 
from django.utils.datastructures import MultiValueDictKeyError

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
    logger = logging.getLogger(__name__)
    form = RoutesForm()
    superadmin = (userData.categoria == 'Administrador')
    routeList = Recorrido.objects.all().order_by('linea','empresa')
    
    #logica
    try:
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                form = RoutesForm(request.POST)
                if request.POST.get('action') == 'Agregar':
                    return HttpResponseRedirect('recorrido0?add')
                else:
                    if form.is_valid():
                        routeName = form.cleaned_data['identificador']
                        temporaryRoute = Recorrido.objects.get(linea = routeName)
                        if request.POST.get('action') == 'Modificar':  #edicion de route.
                            return HttpResponseRedirect('recorrido' + temporaryRoute.getLinea() +'?edit')
                        elif request.POST.get('action') == 'Eliminar':  #edicion de route.
                            return HttpResponseRedirect('eliminar?type=linea&id='+ temporaryRoute.getLinea())
                    else:
                        errorDescription = "Accion no Valida"
                    logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + temporaryRoute.getLinea() + " Error:" + errorDescription)
        else:
            errorDescription = "No posee permisos para ejecutar esta accion"
    except Recorrido.DoesNotExist:
        errorDescription = "No selecciono ninguna linea/Linea no existente"
    logger.info("Usuario: " + userData.nombre +" in Route Error:" + errorDescription)
    return render_to_response('linea.html',  {'user': request.user,'routeList':routeList,'form':form, 'error':errorDescription , 'admin': True, 'superadmin':superadmin },  context_instance=RequestContext(request))

@login_required    
def bus(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    busList=[]
    logger = logging.getLogger(__name__)
    form = BussForm()
    try:
        if (userData.categoria == 'Administrador'):
            busList = Unidad.objects.all().order_by('linea','id_unidad_linea')
        elif (userData.categoria == 'Empresa'):
            busList = Unidad.objects.filter(linea__empresa=userData.empresa).order_by('linea','id_unidad_linea')
        superadmin = (userData.categoria == 'Administrador')
        
        #logica
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                form = BussForm(request.POST)
                if request.POST.get('action') == 'Agregar':
                        return HttpResponseRedirect('unidaddata0?add')
                elif form.is_valid():
                    busId=form.cleaned_data['identificador']
                    if request.POST.get('action') == 'Modificar':
                        temporaryBus = Unidad.objects.get(idunidad = busId)
                        return HttpResponseRedirect('unidaddata'+ str(temporaryBus.getId()) +'?edit')
                    elif request.POST.get('action') == 'Eliminar': 
                        temporaryBus = Unidad.objects.get(idunidad = busId)
                        return HttpResponseRedirect('eliminar?type=unidad&id='+ str(temporaryBus.getId()))
                else:
                    if request.POST.get('id_unidad_linea')=='':
                        errorDescription = "No ingreso identificador de linea"
            #empiezan las excepciones
        else:
            form.initial = {'id_unidad_linea':0}
            errorDescription = "No posee permisos para ejecutar esta accion"
    except Recorrido.DoesNotExist:
        errorDescription = "No existe la linea"
    except Unidad.DoesNotExist:
        errorDescription = "No existe/n unidad/es"
    logger.info("Usuario: " + userData.nombre +" in Bus Error:" + errorDescription)
    return render_to_response('unidad.html',  {'user': request.user,'form':form,  'error': errorDescription,  'busList':busList,  'admin': True, 'superadmin':superadmin},  context_instance=RequestContext(request))

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
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    form = CompaniesForm()
    companyList = []
    
    #logica
    try:
        if (userData.categoria == 'Administrador'):
            superadmin = True
            companyList = Empresa.objects.all()
            if request.method == 'POST':
                companyName = request.POST.get('identificador')
                if request.POST.get('action') == 'Agregar':
                    return HttpResponseRedirect('empresadata0?add')
                elif request.POST.get('action') == 'Modificar':
                    temporaryCompany = Empresa.objects.get(nombre = companyName)                    
                    return HttpResponseRedirect('empresadata'+ str(temporaryCompany.getId()) +'?edit')                #else:
                elif request.POST.get('action') == 'Eliminar':
                    temporaryCompany = Empresa.objects.get(nombre = companyName)                    
                    return HttpResponseRedirect('eliminar?type=empresa&id='+ str(temporaryCompany.getId()))
        else:
            superadmin = False
            errorDescription = "No posee permisos para ejecutar esta accion"
    #empiezan las excepciones
    except Empresa.DoesNotExist:
        errorDescription = "No existe la empresa"
    logger.info("Usuario: " + userData.nombre +" in Company Error:" + errorDescription)        
    return render_to_response('empresa.html',  {'user': request.user, 'companyList':companyList, 'admin': True,'form':form,  'error': errorDescription, 'superadmin':superadmin},  context_instance=RequestContext(request))

@login_required    
def user(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    userList = []
    logger = logging.getLogger(__name__)
    form = UsersForm()
    
    try:
        if (userData.categoria == 'Administrador'):
            userList=Usuario.objects.filter(is_active = True).order_by('nombre')
            superadmin = True
            if request.method == 'POST':
                userName=request.POST.get('identificador')
                if userName == None:
                    userName = ''
                if request.POST.get('action') == 'Agregar':
                    return HttpResponseRedirect('usuariodata0?add')
                elif request.POST.get('action') == 'Modificar':
                    temporaryUser = Usuario.objects.get(nombre = userName)                    
                    return HttpResponseRedirect('usuariodata'+ temporaryUser.getName() +'?edit')
                elif request.POST.get('action') == 'Eliminar':
                    temporaryUser = Usuario.objects.get(nombre = userName)                    
                    return HttpResponseRedirect('eliminar?type=usuario&id='+ str(temporaryUser.getId()))
                logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Nombre_Usuario: " + userName + " Error:" + errorDescription)
        else:
            superadmin = False
            errorDescription = "No posee permisos para ejecutar esta accion"
    #empiezan las excepciones
    except Usuario.DoesNotExist:
        errorDescription = "No existe el usuario"
    logger.info("Usuario: " + userData.nombre +" in User Error:" + errorDescription)        
    return render_to_response('usuario.html',  {'user': request.user,'form':form,  'error': errorDescription,  'userList':userList,  'admin': True,  'superadmin':superadmin},  context_instance=RequestContext(request))

@login_required
def stop(request, routeId): #Pagina de ABM de paradas
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)  
    superadmin = (userData.categoria == 'Administrador')
    form = RouteForm()
    stopList = []
    mensaje = ''
    temporaryRoute = None
        
    #logica
    try:
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                form = RouteForm(request.POST)
                if form.is_valid():
                    routeName = form.cleaned_data['linea']
                    routeCompany = form.cleaned_data['empresa']
                    routePredictable = form.cleaned_data['predictable']
                    if routePredictable == None:
                        routePredictable = False
                    action = form.cleaned_data['action'].lower()
                    if action == 'delete':
                        temporaryRoute = Recorrido.objects.get(linea = routeId)
                        temporaryRoute.delete()
                        return HttpResponseRedirect('linea')
                    elif request.POST.get('stops') == 'Paradas':
                        try:
                            temporaryRoute = Recorrido.objects.get(linea = routeName)
                            return HttpResponseRedirect('stops' + temporaryRoute.getLinea())
                        except Recorrido.DoesNotExist:
                            errorDescription = "Primero debe guardar datos del recorrido"
                    elif request.POST.get('frecuency') == 'Frecuencias':
                        try:
                            temporaryRoute = Recorrido.objects.get(linea = routeId)
                            return HttpResponseRedirect('frecuency' + temporaryRoute.getLinea())
                        except Recorrido.DoesNotExist:
                            errorDescription = "Primero debe guardar datos del recorrido"
                    elif action == 'edit' or action == 'add':
                        if action == 'add':
                            temporaryRoute = Recorrido(linea = routeName, empresa = routeCompany, predictable = routePredictable)
                            if temporaryRoute.validate():
                                temporaryRoute.save();
                            else:
                                errorDescription = "Nombre no valido"
                        elif action == 'edit':
                            temporaryRoute = Recorrido.objects.get(linea = routeId)
                            temporaryRoute.linea = routeName
                            temporaryRoute.empresa = routeCompany
                            temporaryRoute.predictable = routePredictable
                            if temporaryRoute.validate():
                                temporaryRoute.save()
                            else:
                                errorDescription = "Nombre no valido"
                        return HttpResponseRedirect('linea')
                    else:
                        errorDescription = "Accion no valida"
                    logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + str(routeId) + " Error:" + str(errorDescription))
                else:
                    if request.POST.get('linea') == '':
                        errorDescription = "El nombre no puede ser vacio"
                    elif request.POST.get('empresa') == '':
                        errorDescription = "La empresa ingresada no es valida"
                    else:    
                        errorDescription = "Los datos son incorrectos"
            else:
                if request.GET.get('add') == None:
                    temporaryRoute = Recorrido.objects.get(linea = routeId)
                    form.initial = {'linea': temporaryRoute.getLinea(), 'empresa': temporaryRoute.getCompany(), 'predictable': temporaryRoute.getPredictable()}
                    stopList = Parada.objects.filter(linea = temporaryRoute.getId()).order_by('orden')
                    if request.GET.get('edit') == '':
                        mensaje = 'Modificacion de Linea Existente'
                    elif request.GET.get('delete') == '':
                        mensaje = 'Confirmacion de Eliminacion de Linea'
                else:
                    mensaje = 'Alta de Nueva Linea'
        else:
            errorDescription = "No posee permisos para ejecutar esta accion"
    #empiezan las excepciones
    except Recorrido.DoesNotExist:
        errorDescription = "La linea no existe"
        return HttpResponseRedirect('linea')
    except Parada.DoesNotExist:
        errorDescription = "No existen paradas"
    except ValueError:
        errorDescription = "El orden debe ser un numero entero"
    except Empresa.DoesNotExist:
        errorDescription = "La empresa ingresada no existe"
    logger.info("Usuario: " + userData.nombre +" in Stop Error:" + errorDescription)
    return render_to_response('recorrido.html', {'user': request.user,'form': form,  'route': routeId, 'stopList': stopList ,  'error': errorDescription,  'admin': True, 'superadmin':superadmin, 'mensaje': mensaje, 'temporaryRoute':temporaryRoute}, context_instance=RequestContext(request))

@login_required
def changepassword(request):
    errorDescription = ""
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
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
        form = PasswordForm()
    logger.info("Usuario: " + str(request.user) +" Accion: ChangePassword Error:" + errorDescription)
    return render_to_response('change_password.html', {'temporaryUser': request.user, 'form': form, 'error': errorDescription,  'admin': True}, context_instance=RequestContext(request))

@login_required    
def companydata(request, companyId): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    form = CompanyForm()
    mensaje = ''

    #logica
    try:
        if (userData.categoria == 'Administrador'):
            if request.method == 'POST':
                form = CompanyForm(request.POST)
                if form.is_valid():
                    action = form.cleaned_data['action'].lower()
                    if action == 'delete':
                        temporaryCompany = Empresa.objects.get(idempresa = companyId)
                        temporaryCompany.delete()
                        return HttpResponseRedirect('empresa')
                    else:
                        companyEmail = form.cleaned_data['email'].lower()
                        companyName = form.cleaned_data['nombre']
                        if companyName == '':
                            errorDescription = "El nombre no puede ser vacio"
                        elif companyEmail == '':
                            errorDescription = "El email no puede ser vacio"
                        else:
                            if action == 'add':
                                temporaryCompany = Empresa(nombre = companyName,  mail = companyEmail)
                                temporaryCompany.save();
                            elif action == 'edit':
                                temporaryCompany = Empresa.objects.get(idempresa = companyId)
                                temporaryCompany.nombre = companyName
                                temporaryCompany.mail = companyEmail
                                temporaryCompany.save();
                            else:
                                errorDescription = "Accion no valida"
                            logger.info("Usuario: " + userData.nombre +" Accion: " + action + " company Empresa: " + companyName + " Error:" + errorDescription)
                        return HttpResponseRedirect('empresa')
                #empiezan las excepciones
                else:
                    errorDescription = "Datos Incompletos o Invalidos"
            else:
                if request.GET.get('add') == None:
                    temporaryCompany = Empresa.objects.get(idempresa = companyId)
                    form.initial = {'nombre': temporaryCompany.getName(), 'email' : temporaryCompany.getMail()}
                    if request.GET.get('edit') == '':
                        mensaje = 'Modificacion de Empresa Existente'
                    elif request.GET.get('delete') == '':
                        mensaje = 'Confirmacion de Eliminacion de Empresa'
                else:
                    mensaje = 'Alta de Nueva Empresa'
        else:
            errorDescription = "No posee permisos para ejecutar esta accion"
    except Empresa.DoesNotExist:
        errorDescription = "No existe la empresa"
    logger.info("Usuario: " + userData.nombre +" in CompanyData Error:" + errorDescription)        
    return render_to_response('data.html',  {'user': request.user, 'admin': True,'form':form,  'error': errorDescription, 'superadmin': True, 'mensaje': mensaje },  context_instance=RequestContext(request))

@login_required    
def userdata(request, userId): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    categoryList = []
    form = UserForm()
    logger = logging.getLogger(__name__)
    temporaryUser = None
    mensaje = ''
    
    try:
        if (userData.categoria == 'Administrador'):
            categoryList = ['Administrador', 'Empresa']
            superadmin = True
            if request.method == 'POST':
                form = UserForm(request.POST)
                if form.is_valid():
                    userName = form.cleaned_data['nombre']
                    action = form.cleaned_data['action'].lower()
                    if action == 'delete': #Asume que la accion por omision es borrar
                        if userName == '':
                            errorDescription = "No ingreso el nombre de Usuario"
                        elif (Usuario.objects.filter(categoria = "Administrador").count() == 1):
                            errorDescription = "No se puede eliminar el ultimo usuario Administrador"
                        else:
                            temporaryUser = Usuario.objects.get(nombre = userName)
                            temporaryUser.delete()
                    else:                                
                        userEmail = form.cleaned_data['email']
                        userCategory = form.cleaned_data['categoria']
                        userCompany= form.cleaned_data['empresa']
                        userPassword = form.cleaned_data['password']
                        userConfirmation = form.cleaned_data['confirmacion']
                        if action == 'add':
                            if (userCompany != "" and userCategory =='Empresa'):
                                company = Empresa.objects.get(nombre = userCompany)
                            else:
                                company = None
                            try:
                                temporaryUser = Usuario.objects.get(nombre = userName) #da verdadero si la route ya existe.
                                errorDescription = "Usuario ya existente"
                            except:
                                if (userPassword == userConfirmation):
                                    temporaryUser = Usuario(username = userName, nombre = userName,  mail = userEmail,  categoria=userCategory,  empresa=company)
                                    temporaryUser.set_password(userPassword)
                                    if (userCategory =='Administrador'):
                                        temporaryUser.is_superuser = True
                                    temporaryUser.save()
                                else:
                                    errorDescription = "Las passwords no coinciden"

                        elif action == 'edit':
                            if(userName.lower() != ''): 
                                temporaryUser = Usuario.objects.get(nombre = userName)
                                temporaryUser.mail= userEmail
                                if (userPassword != None and userPassword == userConfirmation):
                                    temporaryUser.set_password(userPassword)
                                else:
                                    errorDescription = "Las passwords no coinciden"
                                if (userCategory =='Administrador'):
                                    temporaryUser.is_superuser = True
                                else:
                                    temporaryUser.is_superuser = False
                                temporaryUser.save();
                        else:
                            errorDescription = "Accion no valida: " + action
                    logger.info("Usuario: " + userData.nombre +" Accion: " + action + " Nombre_Usuario: " + userName + " Error:" + errorDescription)
                    return HttpResponseRedirect('usuario')
                else:
                    errorDescription = "Los datos ingresados no son validos" 
            else:
                if request.GET.get('add') == None:
                    temporaryUser = Usuario.objects.get(nombre = userId)
                    form.initial = {'nombre': temporaryUser.getName(), 'email' : temporaryUser.getMail(), 'categoria' : temporaryUser.getCategory(), 'empresa': temporaryUser.getCompany(), 'password':'nuevo','confirmacion':'nuevo'}
                    if request.GET.get('edit') == '':
                        mensaje = 'Modificacion de Usuario Existente'
                    elif request.GET.get('delete') == '':
                        mensaje = 'Confirmacion de Eliminacion de Usuario'
                else:
                    mensaje = 'Alta de Nuevo Usuario'
        else:
            superadmin = False
            errorDescription = "No posee permisos para ejecutar esta accion"
    #empiezan las excepciones
    except Usuario.DoesNotExist:
        errorDescription = "No existe el usuario"
    except Empresa.DoesNotExist:
        errorDescription = "No existe la compania"
    logger.info("Usuario: " + userData.nombre +" in User Error:" + errorDescription)        
    return render_to_response('data.html',  {'user': request.user,'form':form,  'error': errorDescription,  'admin': True, 'categoryList':categoryList, 'superadmin':superadmin, 'mensaje':mensaje, 'temporaryUser':temporaryUser},  context_instance=RequestContext(request))

@login_required    
def busdata(request, busId): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    form = BusForm()
    temporaryBus = None
    mensaje = ''
    
    try:
        superadmin = (userData.categoria == 'Administrador')
        #logica
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                form = BusForm(request.POST)
                if form.is_valid():
                    action = form.cleaned_data['action'].lower()
                    routeName = form.cleaned_data['linea']
                    busIdLinea = form.cleaned_data['id_unidad_linea']
                    if action == 'delete': 
                        temporaryBus = Unidad.objects.get(idunidad = busId)
                        temporaryBus.delete()
                    else:
                        if busIdLinea == None:
                            errorDescription = "No ingreso el identificador de la unidad"
                        else:
                            busAble= form.cleaned_data['apto_movilidad_reducida']
                            if action == 'add':
                                try:
                                    temporaryBus = Unidad.objects.get(idunidad = busId) #da verdadero si la bus ya existe
                                    errorDescription = "Unidad ya existente"
                                except Unidad.DoesNotExist:
                                    temporaryBus = Unidad(linea = routeName,  apto_movilidad_reducida = busAble, id_unidad_linea = busIdLinea)
                                    temporaryBus.save()
                            elif action == 'edit': 
                                temporaryBus = Unidad.objects.get(idunidad = busId)
                                temporaryBus.id_unidad_linea = busIdLinea
                                temporaryBus.apto_movilidad_reducida = busAble
                                temporaryBus.save()
                            else: 
                                errorDescription = "Accion no permitida"
                    logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + routeName.getLinea() + " Unidad: " + str(busId) + " Error:" + errorDescription)
                    return HttpResponseRedirect('unidad')
                else:
                    if request.POST.get('id_unidad_linea') == '':
                        errorDescription = "No ingreso el identificador de la unidad"
                    else:
                        try:
                            int(request.POST.get('id_unidad_linea') =='')
                            Recorrido.objects.get(idrecorrido = request.POST.get('linea'))
                        except ValueError:
                            errorDescription = "El identificador de la linea debe ser un numero entero"
            else:
                if request.GET.get('add') == None:
                    temporaryBus = Unidad.objects.get(idunidad = busId)
                    form.initial = {'linea': temporaryBus.getLinea(), 'apto_movilidad_reducida' : temporaryBus.getApto(), 'id_unidad_linea': temporaryBus.getIdByLinea()}
                    if request.GET.get('edit') == '':
                        mensaje = 'Modificacion de Unidad Existente'
                    elif request.GET.get('delete') == '':
                        mensaje = 'Confirmacion de Eliminacion de Unidad'
                else:
                    mensaje = 'Alta de Nueva Unidad'
        else:
            errorDescription = "No posee permisos para ejecutar esta accion"
    except Recorrido.DoesNotExist:
        errorDescription = "No existe la linea"
    except Unidad.DoesNotExist:
        errorDescription = "No existe/n unidad/es"  
    logger.info("Usuario: " + userData.nombre +" in Bus Error:" + errorDescription)
    return render_to_response('data.html',  {'user': request.user,'form':form,  'error': errorDescription, 'admin': True, 'superadmin':superadmin, 'mensaje':mensaje, 'temporaryBus':temporaryBus},  context_instance=RequestContext(request))

@login_required    
def stopdata(request, stopId): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)  
    superadmin = (userData.categoria == 'Administrador')
    form = StopForm()
    temporaryStop = None
    mensaje = ''
    stopList=[]
    
    #logica
    try:
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                try:
                    form = StopForm(request.POST)
                    if request.POST.get('save')=="Volver":
                        temporaryRoute = Recorrido.objects.get(idrecorrido = request.POST.get('linea'))
                        return HttpResponseRedirect('stops' + temporaryRoute.getLinea())
                    if form.is_valid():
                        action = form.cleaned_data['action']
                        temporaryStopPrevious = form.cleaned_data['orden']
                        if temporaryStopPrevious == None:
                            stopOrder = 0
                        else:  
                            stopOrder = temporaryStopPrevious.getOrder()
                        temporaryRoute= form.cleaned_data['linea']
                        if action == 'delete':
                            temporaryStop = Parada.objects.get(idparada = stopId)  
                            temporaryStop.delete()
                            #!reacomodar paradas                
                            for temporaryStop in stopList: 
                                if temporaryStop.getOrder() > int(stopOrder): 
                                    temporaryStop.downOneOrder()
                                    temporaryStop.save()
                            stopList = orderStopList(Parada.objects.filter(linea = temporaryRoute).order_by('orden'))
                        else:
                            stopLat = form.cleaned_data['latitud']
                            stopLon = form.cleaned_data['longitud']
                            stopStreet1 = form.cleaned_data['calle1']
                            if stopLat == '' or stopLon == '':
                                errorDescription = "Las coordenadas no pueden ser vacias"
                            elif stopStreet1 == '':
                                errorDescription = "La descripcion de la calle 1 de la parada no pueden ser vacias"
                            else:
                                stopStreet2 = form.cleaned_data['calle2']
                                stopActive = form.cleaned_data['paradaactiva']
                                stopList = Parada.objects.filter(linea = temporaryRoute).order_by('orden')
                                if stopOrder == None or stopOrder == '':
                                    stopOrder = 0
                                if int(stopOrder) >= 0:  #comprueba que el orden sea un entero mayor que 0
                                    if action == 'edit': #sin revisar - Falta ver que pasa si se cambia el orden.
                                        temporaryStop = Parada.objects.get(idparada = stopId)  
                                        temporaryStop.latitud = stopLat
                                        temporaryStop.longitud = stopLon
                                        temporaryStop.calle1 = stopStreet1
                                        temporaryStop.calle2 = stopStreet2
                                        temporaryStop.paradaactiva = stopActive
                                        temporaryStop.save()
                                    elif action == 'add':
                                        if len(stopList) == 0: #comprueba que no sea la primer parada
                                            stopOrder = 1
                                        elif stopOrder != 0: #agrega la parada en una posicion especifica
                                            for temporaryStop in stopList: 
                                                if temporaryStop.getOrder() >= int(stopOrder): 
                                                    temporaryStop.upOneOrder()
                                                    temporaryStop.save()
                                            stopList = orderStopList(Parada.objects.filter(linea = temporaryRoute).order_by('orden'))
                                        else: #agrega la parada al final del recorrido
                                            stopOrder = stopList.aggregate(orden=Max('orden')).get('orden') + 1
                                        temporaryStop = Parada(orden = stopOrder,  latitud = stopLat, longitud = stopLon, linea = temporaryRoute, calle1 = stopStreet1,calle2 = stopStreet2,paradaactiva = stopActive)  
                                        temporaryStop.save()
                                    else:
                                        errorDescription = "La accion no es valida"
                                else:
                                    errorDescription = "El orden debe ser un numero entero mayor a 0"
                                logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + str(temporaryRoute) + " Parada: " + str(stopOrder) + " Error:" + errorDescription)
                                return HttpResponseRedirect('recorrido' + str(temporaryRoute))
                    else:
                        errorDescription = "Los datos no son validos"
                except ValueError:
                    errorDescription = "El orden debe ser un numero entero"
                except TypeError:
                    errorDescription = "Las coordenadas no pueden ser vacias"
            else:
                if request.GET.get('add') == '':
                    temporaryRoute = Recorrido.objects.get(linea = stopId)
                    form.initial = {'linea': temporaryRoute.getId()}
                    mensaje = 'Alta de Nueva Parada'
                else:
                    temporaryStop = Parada.objects.get(idparada = stopId)
                    temporaryRoute= Recorrido.objects.get(linea = temporaryStop.getLinea())
                    form.initial = {'linea': temporaryRoute.getId(),'orden': temporaryStop.getOrder(), 'latitud': temporaryStop.getLat(), 'longitud': temporaryStop.getLon(), 'calle1': temporaryStop.getStreetName1(), 'calle2': temporaryStop.getStreetName2(), 'paradaactiva': temporaryStop.getActive()}
                    if request.GET.get('edit') == '':
                        mensaje = 'Modificacion de Parada Existente'
                    elif request.GET.get('delete') == '':
                        mensaje = 'Confirmacion de Eliminacion de Parada'
                stopList = Parada.objects.filter(linea = temporaryRoute.getId()) 
        else:
            errorDescription = "No posee permisos para ejecutar esta accion"
    #empiezan las excepciones
    except Recorrido.DoesNotExist:
        return HttpResponseRedirect('linea')
    except Parada.DoesNotExist:
        errorDescription = "No existen paradas"
    logger.info("Usuario: " + userData.nombre +" in Stop Error:" + errorDescription)
    return render_to_response('stopdata.html',  {'user': request.user,'form':form,  'error': errorDescription, 'admin': True, 'superadmin':superadmin, 'stopList': stopList, 'mensaje':mensaje, 'temporaryStop':temporaryStop},  context_instance=RequestContext(request))

@login_required
def stopList(request, routeId):
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    form = StopsForm()
    superadmin = (userData.categoria == 'Administrador')
    stopList = []
    
    #logica
    if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
        try:
            if request.method == 'POST':
                form = StopsForm(request.POST, request.FILES)
                if form.is_valid():
                    temporaryOrden = form.cleaned_data['identificador']
                    temporaryRoute = Recorrido.objects.get(linea = routeId)
                    if request.POST.get('action') == 'Volver':
                        return HttpResponseRedirect('recorrido'+routeId+'?edit')
                    elif request.POST.get('action') == 'Agregar':
                        return HttpResponseRedirect('stopdata'+routeId+'?add')
                    elif request.POST.get('action') == 'Modificar':
                        temporaryStop = Parada.objects.get(linea = temporaryRoute, orden = temporaryOrden)                    
                        return HttpResponseRedirect('stopdata'+ str(temporaryStop.getId()) +'?edit')
                    elif request.POST.get('action') == 'Eliminar':
                        temporaryStop = Parada.objects.get(linea = temporaryRoute, orden = temporaryOrden)
                        return HttpResponseRedirect('eliminar?type=parada&id='+ str(temporaryStop.getId()))
                    elif request.POST.get('action') == 'Carga Masiva': #Falta implementar carga masiva
                        if (request.FILES['masivo'] != ''):
                            fileName = request.FILES['masivo']
                            temporaryOrder = int(Parada.objects.filter(linea = (Recorrido.objects.get(linea = routeId)).getId()).count())
                            errors = 0
                            for route in fileName:
                                values = route.split(';') 
                                try:
                                    tempLat = float(values[0])
                                    tempLon = float(values[1])
                                    stopName1 = values[2]
                                    stopName2 = values[3]
                                    if stopName2 == None or stopName2 == '\n':
                                        stopName2 = ''
                                    if stopName1 != None:
                                        temporaryOrder = temporaryOrder + 1
                                        newParada = Parada(orden = temporaryOrder,  latitud = tempLat, longitud = tempLon, linea = Recorrido.objects.get(linea = routeId), calle1 = stopName1, calle2 = stopName2)  
                                        newParada.save()
                                    else:
                                        errors = errors + 1
                                except:
                                    errors = errors + 1
                                    errorDescription = "se encontraron " + str(errors) + " errors de datos"
                            return HttpResponseRedirect('recorrido' + temporaryRoute.getLinea() +'?edit')
                        else:
                            errorDescription = "No selecciono ningun archivo"
                    else:
                        errorDescription = "Accion no Valida"
                    logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Stops: " + routeId + " Error:" + errorDescription)
            else:
                stopList = Parada.objects.filter(linea = Recorrido.objects.get(linea = routeId)).order_by('orden')
        except Recorrido.DoesNotExist:
            return HttpResponseRedirect('linea')
        except Parada.DoesNotExist:
            errorDescription = "No selecciono ninguna parada/Parada no existente"
            stopList = Parada.objects.filter(linea = Recorrido.objects.get(linea = routeId)).order_by('orden')
        except MultiValueDictKeyError:
            errorDescription = "No selecciono ninguno ningun archivo"
            stopList = Parada.objects.filter(linea = Recorrido.objects.get(linea = routeId)).order_by('orden')
    else:
        errorDescription = "No posee permisos para ejecutar esta accion"
    logger.info("Usuario: " + userData.nombre +" in Stops Error:" + errorDescription)
    return render_to_response('stopslist.html',  {'form':form, 'stopList':stopList, 'superadmin':superadmin, 'error':errorDescription},  context_instance=RequestContext(request))

@login_required
def frecuency(request, routeId):
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    FrecuenciesList = []
    logger = logging.getLogger(__name__)
    form = FrecuenciesForm()
    
    try:
        if (userData.categoria == 'Administrador'):
            temporaryRoute = Recorrido.objects.get(linea = routeId)
            FrecuenciesList = Frecuencia.objects.filter(linea = temporaryRoute)
            superadmin = True
            if request.method == 'POST':
                form = FrecuenciesForm(request.POST)
                idFrecuencia = request.POST.get('identificador')
                if request.POST.get('action') == 'Agregar':
                    return HttpResponseRedirect('frecuencydata'+routeId+'?add')
                elif request.POST.get('action') == 'Eliminar':
                    temporaryFrecuency = Frecuencia.objects.get(idfrecuencia = idFrecuencia)                    
                    return HttpResponseRedirect('eliminar?type=frecuencia&id='+ str(temporaryFrecuency.getId()))
                logger.info("Frecuencia: " + userData.nombre +" Accion: " + request.POST.get('action') + " Frecuencia: " + str(temporaryFrecuency.getId()) + " Error:" + errorDescription)
            #empiezan las excepciones
        else:
            superadmin = False
            errorDescription = "No posee permisos para ejecutar esta accion"
    except Frecuencia.DoesNotExist:
        errorDescription = "Frecuencia no existente"
    except Recorrido.DoesNotExist:
        errorDescription = "Linea no Existente"
    logger.info("Usuario: " + userData.nombre +" in Frecuency Error:" + errorDescription)        
    return render_to_response('frecuency.html',  {'user': request.user,'form':form,  'error': errorDescription,  'list':FrecuenciesList,  'admin': True,  'superadmin':superadmin},  context_instance=RequestContext(request))

@login_required
def eliminar(request):
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    form = EliminarForm()
    
    if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
        dataType = request.GET.get('type')
        identificador = request.GET.get('id')
        try:
            if dataType == 'usuario':
                temporary = Usuario.objects.get(id = identificador)
            elif dataType == 'empresa':
                temporary = Empresa.objects.get(idempresa = identificador)
            elif dataType == 'linea':
                temporary = Recorrido.objects.get(linea = identificador)
            elif dataType == 'parada':
                temporary = Parada.objects.get(idparada = identificador)
            elif dataType == 'unidad':
                temporary = Unidad.objects.get(idunidad = identificador)
            elif dataType == 'frecuencia':
                temporary = Frecuencia.objects.get(idfrecuencia = identificador)    
            if request.method == 'POST' and temporary != None:
                temporary.delete()
                return HttpResponseRedirect('index')
        except Usuario.DoesNotExist:
            errorDescription = "No existe usuario"
        except Empresa.DoesNotExist:
            errorDescription = "No existe empresa"
        except Recorrido.DoesNotExist:
            errorDescription = "No existe recorrido"
        except Parada.DoesNotExist:
            errorDescription = "No existe parada"
        except Unidad.DoesNotExist:
            errorDescription = "No existe unidad"   
        except Frecuencia.DoesNotExist:
            errorDescription = "No existe frecuencia"                    
        logger.info("Usuario: " + userData.nombre +" in Eliminar Type: " + dataType + " identificador "+ str(identificador) + "Error:" + errorDescription)
    else:
        errorDescription = "No posee permisos para ejecutar esta accion"
    logger.info("Usuario: " + userData.nombre +" in Eliminar Error:" + errorDescription)
    return render_to_response('eliminar.html',  {'form':form,'error':errorDescription},  context_instance=RequestContext(request))

@login_required
def frecuencydata(request, routeId):
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    superadmin = (userData.categoria == 'Administrador')
    form = FrecuencyForm()
    logger = logging.getLogger(__name__)
    temporaryFrecuency = None
    mensaje = ''
    
    try:
        #logica
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                form = FrecuencyForm(request.POST)
                if form.is_valid():
                    action = form.cleaned_data['action'].lower()
                    routeName = form.cleaned_data['linea']
                    dayFrecuency = form.cleaned_data['dia']
                    timeFrecuency = form.cleaned_data['hora']
                    if action == 'add':
                        try:
                            temporaryFrecuency = Frecuencia.objects.get(linea = routeName, dia_semana = dayFrecuency, hora = timeFrecuency) #da verdadero si la bus ya existe
                            errorDescription = "Frecuencia ya cargada"
                        except Frecuencia.DoesNotExist:
                            temporaryFrecuency = Frecuencia(linea = routeName, dia_semana = dayFrecuency, hora = timeFrecuency) #da verdadero si la bus ya existe
                            temporaryFrecuency.save()
                    else: 
                        errorDescription = "Accion no permitida"
                    logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + routeName.getLinea() + " Frecuencia: " + dayFrecuency +"-" + request.POST.get('hora') + " Error:" + errorDescription)
                    return HttpResponseRedirect('frecuency'+routeId)
                else:
                    if request.POST.get('hora') == '':
                        errorDescription = "No ingreso la hora"
        else:
            errorDescription = "No posee permisos para ejecutar esta accion"
    except Frecuencia.DoesNotExist:
        errorDescription = "Frecuencia no existe"
    logger.info("Usuario: " + userData.nombre +" in frecuencyData Error:" + errorDescription)
    return render_to_response('data.html',  {'user': request.user,'form':form,  'error': errorDescription,  'admin': True, 'superadmin':superadmin, 'mensaje':mensaje, 'temporaryFrecuency':temporaryFrecuency},  context_instance=RequestContext(request))