# Create your views here.
import logging

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max
from tibusAdmin.forms import StopForm,  RouteForm,  BusForm, CompanyForm,  UserForm, PassworForm, RoutesForm
from tibus.models import Parada, Recorrido, Unidad, Empresa
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
    form = RoutesForm()
    
    if (userData.categoria == 'Administrador'):
        companyList = Empresa.objects.all()        
        routeList = Recorrido.objects.all().order_by('linea')
    elif (userData.categoria == 'Empresa'):
        companyList = Empresa.objects.filter(nombre = userData.empresa)   
        routeList = Recorrido.objects.filter(empresa = userData.empresa).order_by('linea')
    superadmin = (userData.categoria == 'Administrador')
    
    #logica
    if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                form = RoutesForm(request.POST)
                routeName=request.POST.get('linea').upper()
                if request.POST.get('action') == 'viewCompany':
                    if request.POST.get('empresa') == 'all':
                        routeList = Recorrido.objects.all().order_by('linea')
                    else:
                        routeList = Recorrido.objects.filter(empresa__nombre =request.POST.get('empresa').upper()).order_by('linea')
                elif request.POST.get('action') == 'addRoute':
                    return HttpResponseRedirect('recorrido0?add')
                elif request.POST.get('action') == 'editRoute':  #edicion de route.
                    temporaryRoute = Recorrido.objects.get(linea = routeName)
                    return HttpResponseRedirect('recorrido' + temporaryRoute.getLinea() +'?edit')
                elif request.POST.get('action') == 'delRoute':  #edicion de route.
                    temporaryRoute = Recorrido.objects.get(linea = routeName)
                    return HttpResponseRedirect('recorrido' + temporaryRoute.getLinea() +'?delete')
                else:
                    errorDescription = "Accion no Valida"
            #empiezan las excepciones
            except Recorrido.DoesNotExist:
                errorDescription = "La linea ingresada no existe"
            except Empresa.DoesNotExist:
                errorDescription = "La empresa ingresada no existe"
            logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + routeName + " Error:" + errorDescription)
    else:
        errorDescription = "No posee permisos para ejecutar esta accion"
    logger.info("Usuario: " + userData.nombre +" in Route Error:" + errorDescription)
    return render_to_response('linea.html',  {'user': request.user,'form':form, 'error':errorDescription , 'companyList': companyList, 'routeList': routeList, 'admin': True, 'superadmin':superadmin },  context_instance=RequestContext(request))

@login_required    
def bus(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    routeList = []
    busList=[]
    logger = logging.getLogger(__name__)
    form = BusForm()
    
    if (userData.categoria == 'Administrador'):
        routeList = Recorrido.objects.all().order_by('linea')
        busList = Unidad.objects.all().order_by('id_unidad_linea')
    elif (userData.categoria == 'Empresa'):
        routeList = Recorrido.objects.filter(empresa=userData.empresa).order_by('linea')
        busList = Unidad.objects.filter(linea__empresa=userData.empresa).order_by('id_unidad_linea')
    superadmin = (userData.categoria == 'Administrador')
    
    #logica
    if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                form = BusForm(request.POST)
                if request.POST.get('action') == 'addBus':
                        return HttpResponseRedirect('unidaddata0?add')
                elif form.is_valid():
                    routeName=form.cleaned_data['linea']
                    busId=form.cleaned_data['id_unidad_linea']
                    if request.POST.get('action') == 'editBus':
                        temporaryBus = Unidad.objects.get(linea = routeName,  id_unidad_linea = busId)
                        return HttpResponseRedirect('unidaddata'+ str(temporaryBus.getId()) +'?edit')
                    elif request.POST.get('action') == 'delBus': 
                        temporaryBus = Unidad.objects.get(linea = routeName,  id_unidad_linea = busId)
                        return HttpResponseRedirect('unidaddata'+ str(temporaryBus.getId()) +'?delete')
                else:
                    if request.POST.get('id_unidad_linea')=='':
                        errorDescription = "No ingreso identificador de linea"
            #empiezan las excepciones
            except Recorrido.DoesNotExist:
                errorDescription = "No existe la linea"
            except Unidad.DoesNotExist:
                errorDescription = "No existe/n unidad/es"
    else:
        form = BusForm()
        form.initial = {'id_unidad_linea':0}
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
    form = CompanyForm()
    
        #logica
    if (userData.categoria == 'Administrador'):
        companyList = Empresa.objects.all().order_by('nombre')        
        superadmin = True
        if request.method == 'POST':
            try:
                if request.POST.get('action') == 'addCompany':
                    return HttpResponseRedirect('empresadata0?add')
                elif request.POST.get('action') == 'editCompany':
                    temporaryCompany = Empresa.objects.get(nombre = request.POST.get('nombre'))                    
                    return HttpResponseRedirect('empresadata'+ str(temporaryCompany.getId()) +'?edit')                #else:
                elif request.POST.get('action') == 'delCompany':
                    temporaryCompany = Empresa.objects.get(nombre = request.POST.get('nombre'))                    
                    return HttpResponseRedirect('empresadata'+ str(temporaryCompany.getId()) +'?delete')                #else:
            #empiezan las excepciones
            except Empresa.DoesNotExist:
                errorDescription = "No existe la empresa"
    else:
        superadmin = False
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
    logger = logging.getLogger(__name__)
    form = UserForm()
    
    if (userData.categoria == 'Administrador'):
        userList=Usuario.objects.filter(is_active = True).order_by('nombre')
        superadmin = True
        if request.method == 'POST':
            try:
                userName=request.POST.get('nombre').upper()
                if request.POST.get('action') == 'addUser':
                    return HttpResponseRedirect('usuariodata0?add')
                elif request.POST.get('action') == 'editUser':
                    temporaryUser = Usuario.objects.get(nombre = request.POST.get('nombre'))                    
                    return HttpResponseRedirect('usuariodata'+ temporaryUser.getName() +'?edit')
                elif request.POST.get('action') == 'rehabUser':
                    temporaryUser = Usuario.objects.get(nombre = request.POST.get('nombre'))                    
                    return HttpResponseRedirect('usuariodata'+ temporaryUser.getName() +'?rehab')
                elif request.POST.get('action') == 'delUser':
                    temporaryUser = Usuario.objects.get(nombre = request.POST.get('nombre'))                    
                    return HttpResponseRedirect('usuariodata'+ temporaryUser.getName() +'?delete')
            #empiezan las excepciones
            except Usuario.DoesNotExist:
                errorDescription = "No existe el usuario"
            logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Nombre_Usuario: " + userName + " Error:" + errorDescription)
    else:
        superadmin = False
        errorDescription = "No posee permisos para ejecutar esta accion"
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
    if userData.categoria == 'Administrador':
        companyList = Empresa.objects.all()
    elif userData.categoria == 'Empresa':
        companyList = [userData.empresa] 
        
    #logica
    try:
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                form = RouteForm(request.POST)
                temporaryOrder = request.POST.get('orden')
                if temporaryOrder == None or temporaryOrder == '':
                    temporaryOrder = 0
                if request.POST.get('action') == 'addStop': 
                    try:
                        temporaryRoute = Recorrido.objects.get(linea = routeId)
                        return HttpResponseRedirect('stopdata'+temporaryRoute.getLinea()+'?add')                    
                    except Recorrido.DoesNotExist:
                        if form.is_valid():
                            routeName = form.cleaned_data['linea']
                            routeFrecuency = form.cleaned_data['frecuencia']
                            routeCompany = form.cleaned_data['empresa']
                            if routeFrecuency > 0:
                                temporaryRoute = Recorrido(linea = routeName, frecuencia = request.POST.get('frecuencia'), empresa = Empresa.objects.get(nombre = request.POST.get('empresa')))
                                temporaryRoute.save();
                                return HttpResponseRedirect('stopdata'+temporaryRoute.getLinea()+'?add')
                            else:
                                errorDescription = "La frecuencia debe ser mayor que 0"
                        else:
                            if routeName == '':
                                errorDescription = "El nombre no puede ser vacio"
                            routeFrecuency = validateFrecuency(request.POST.get('frecuencia')) 
                            if routeFrecuency != '':
                                errorDescription = routeFrecuency 
                elif request.POST.get('action') == 'editStop': 
                    temporaryStop = Parada.objects.get(linea = (Recorrido.objects.get(linea = routeId)).getId(), orden = temporaryOrder)
                    return HttpResponseRedirect('stopdata'+str(temporaryStop.getId())+'?edit')
                elif request.POST.get('action') == 'delStop': 
                    temporaryStop = Parada.objects.get(linea = (Recorrido.objects.get(linea = routeId)).getId(), orden = temporaryOrder)
                    return HttpResponseRedirect('stopdata'+str(temporaryStop.getId())+'?delete')
                elif request.POST.get('action') == 'addMasiveStop': #Falta implementar carga masiva
                    try:
                        temporaryRoute = Recorrido.objects.get(linea = routeId)
                    except Recorrido.DoesNotExist:
                        if form.is_valid():
                            routeName = form.cleaned_data['linea']
                            routeFrecuency = form.cleaned_data['frecuencia']
                            routeCompany = form.cleaned_data['empresa']
                            if routeFrecuency > 0:
                                temporaryRoute = Recorrido(linea = routeName, frecuencia = request.POST.get('frecuencia'), empresa = Empresa.objects.get(nombre = request.POST.get('empresa')))
                                temporaryRoute.save();
                            else:
                                errorDescription = "La frecuencia debe ser mayor que 0"
                                return HttpResponseRedirect('recorrido0?add')
                        else:
                            if routeName == '':
                                errorDescription = "El nombre no puede ser vacio"
                            routeFrecuency = validateFrecuency(request.POST.get('frecuencia')) 
                            if routeFrecuency != '':
                                errorDescription = routeFrecuency 
                            return HttpResponseRedirect('recorrido0?add')
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
                                temporaryOrder = temporaryOrder + 1
                                newParada = Parada(orden = temporaryOrder,  latitud = tempLat, longitud = tempLon, linea = temporaryRoute.getId(), calle1 = stopName1, calle2 = stopName2)  
                                newParada.save()
                            except:
                                errors = errors + 1
                                errorDescription = "se encontraron " + str(errors) + " errors de datos"
                    else:
                        errorDescription = "No selecciono ningun archivo"
                elif request.POST.get('action') == 'save': 
                    if form.is_valid():
                        routeName = form.cleaned_data['linea']
                        routeFrecuency = form.cleaned_data['frecuencia']
                        routeCompany = form.cleaned_data['empresa']
                        action = form.cleaned_data['action'].lower()
                        if routeName == '':
                            errorDescription = "El nombre no puede ser vacio"
                        else:
                            routeFrecuency = validateFrecuency(request.POST.get('frecuencia')) 
                            if routeFrecuency != '':
                                errorDescription = routeFrecuency
                            else:
                                if action == 'add':  
                                    temporaryRoute = Recorrido(linea = routeName, frecuencia = routeFrecuency, empresa = Empresa.objects.get(nombre = routeCompany))
                                    temporaryRoute.save();
                                elif action == 'edit':
                                    temporaryRoute = Recorrido.objects.get(linea = routeName)
                                    temporaryRoute.frecuencia = routeFrecuency
                                    temporaryRoute.empresa = Empresa.objects.get(nombre = routeCompany)
                                    if validateFrecuency(routeFrecuency) == '':
                                        temporaryRoute.save();
                                    else:
                                        errorDescription = validateFrecuency(routeFrecuency)
                                elif action == 'delete':
                                    temporaryRoute = Recorrido.objects.get(linea = routeName)
                                    temporaryRoute.delete()
                                return HttpResponseRedirect('linea')
                    else:
                        if request.POST.get('linea') == '':
                            errorDescription = "El nombre no puede ser vacio"
                        elif request.POST.get('frecuencia') == '':
                            errorDescription = "La frecuencia no puede ser vacia"
                        elif request.POST.get('empresa') == '':
                            errorDescription = "La empresa ingresada no es valida"
                        else:    
                            errorDescription = "Los datos son incorrectos"
                else: 
                    errorDescription = "Accion no valida"
                logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + str(routeId) + " Parada: " + str(temporaryOrder) + " Error:" + str(errorDescription))
            else:
                if request.GET.get('add') == None:
                    temporaryRoute = Recorrido.objects.get(linea = routeId)
                    form.initial = {'linea': temporaryRoute.getLinea(), 'frecuencia' : temporaryRoute.getFrecuency(), 'empresa': temporaryRoute.getCompany()}
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
    return render_to_response('recorrido.html', {'user': request.user,'form': form,  'route': routeId, 'stopList': stopList ,  'error': errorDescription,  'admin': True, 'superadmin':superadmin, 'mensaje': mensaje, 'temporaryRoute':temporaryRoute, 'companyList':companyList}, context_instance=RequestContext(request))

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

@login_required    
def companydata(request, companyId): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    form = CompanyForm()

    #logica
    if (userData.categoria == 'Administrador'):
        if request.method == 'POST' or companyId == 0:
            try:
                form = CompanyForm(request.POST)
                if form.is_valid():
                    companyName = form.cleaned_data['nombre'].upper()
                    companyEmail = form.cleaned_data['email'].lower()
                    action = form.cleaned_data['action'].lower()
                    if action == 'add':
                        temporaryCompany = Empresa(nombre = companyName,  mail = companyEmail)
                        temporaryCompany.save();
                    elif action == 'edit':
                        temporaryCompany = Empresa.objects.get(idempresa = companyId)
                        temporaryCompany.nombre = companyName
                        temporaryCompany.mail = companyEmail
                        temporaryCompany.save();
                    elif action == 'delete':
                        temporaryCompany = Empresa.objects.get(idempresa = companyId)
                        temporaryCompany.delete()
                    else:
                        errorDescription = "Accion no valida"
                    logger.info("Usuario: " + userData.nombre +" Accion: " + action + "company Empresa: " + companyName + " Error:" + errorDescription)
                    return HttpResponseRedirect('empresa')
                #empiezan las excepciones
                else:
                    errorDescription = "Datos Incompletos o Invalidos"
            except Empresa.DoesNotExist:
                errorDescription = "No existe la empresa"
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
    logger.info("Usuario: " + userData.nombre +" in CompanyData Error:" + errorDescription)        
    return render_to_response('empresadata.html',  {'user': request.user, 'admin': True,'form':form,  'error': errorDescription, 'superadmin': True, 'mensaje': mensaje },  context_instance=RequestContext(request))

@login_required    
def userdata(request, userId): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    companyList = []
    categoryList = []
    form = UserForm()
    logger = logging.getLogger(__name__)
    temporaryUser = None
    
    try:
        if (userData.categoria == 'Administrador'):
            companyList = Empresa.objects.all().order_by('nombre')        
            categoryList = ['Administrador', 'Empresa']
            superadmin = True
            if request.method == 'POST':
                form = UserForm(request.POST)
                if form.is_valid():
                    userName = form.cleaned_data['nombre'].upper()
                    action = form.cleaned_data['action'].lower()
                    if action == 'delete': #Asume que la accion por omision es borrar
                        if userName == '':
                            errorDescription = "No ingreso el nombre de Usuario"
                        elif (Usuario.objects.filter(categoria = "Administrador").count() == 1):
                            errorDescription = "No se puede eliminar el ultimo usuario Administrador"
                        else:
                            temporaryUser = Usuario.objects.get(nombre = userName)
                            temporaryUser.is_active = False
                            temporaryUser.save()
                    elif action == 'rehab':
                        if userName == '':
                            errorDescription = "No ingreso el nombre de Usuario"
                        else:
                            temporaryUser = Usuario.objects.get(nombre = userName)
                            temporaryUser.is_active = True
                            temporaryUser.save()
                    else:                                
                        userEmail = form.cleaned_data['email'].lower()
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
                                    temporaryUser = Usuario(username = userName, nombre = userName,  mail = userName,  categoria=userCategory,  empresa=company)
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
                    form.initial = {'nombre': temporaryUser.getName(), 'email' : temporaryUser.getMail(), 'categoria' : temporaryUser.getCategory(), 'empresa': temporaryUser.getCompany()}
                    if request.GET.get('edit') == '':
                        mensaje = 'Modificacion de Usuario Existente'
                    elif request.GET.get('delete') == '':
                        mensaje = 'Confirmacion de Eliminacion de Usuario'
                    elif request.GET.get('rehab') == '':
                        mensaje = 'Confirmacion de Rehabilitacion de Usuario'
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
    return render_to_response('usuariodata.html',  {'user': request.user,'form':form,  'error': errorDescription,  'admin': True,  'companyList' : companyList,  'categoryList':categoryList, 'superadmin':superadmin, 'mensaje':mensaje, 'temporaryUser':temporaryUser},  context_instance=RequestContext(request))

@login_required    
def busdata(request, busId): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    routeList = []
    errorDescription = ""
    userData = Usuario.objects.get(nombre = request.user)
    logger = logging.getLogger(__name__)
    form = BusForm()
    temporaryBus = None
    
    try:
        if (userData.categoria == 'Administrador'):
            routeList = Recorrido.objects.all().order_by('linea')
        elif (userData.categoria == 'Empresa'):
            routeList = Recorrido.objects.filter(company=userData.empresa).order_by('linea')
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
                    logger.info("Usuario: " + userData.nombre +" Accion: " + request.POST.get('action') + " Linea: " + routeName.getLinea() + " Unidad: " + busId + " Error:" + errorDescription)
                    return HttpResponseRedirect('unidad')
                else:
                    if request.POST.get('linea') =='':
                        errorDescription = "No ingreso la linea"
                    else:
                        try:
                            int(request.POST.get('id_unidad_linea') =='')
                            routeName = Recorrido.objects.get(linea = request.POST.get('linea') =='')
                        except ValueError:
                            errorDescription = "El identificador de la linea debe ser un numero entero"
            else:
                if request.GET.get('add') == None:
                    temporaryBus = Unidad.objects.get(idunidad = busId)
                    form.initial = {'linea': temporaryBus.getLinea(), 'aptoMovilidadReducida' : temporaryBus.getApto(), 'id_unidad_linea': temporaryBus.getIdByLinea()}
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
    return render_to_response('unidaddata.html',  {'user': request.user,'form':form,  'error': errorDescription, 'admin': True,  'routeList': routeList,'superadmin':superadmin, 'mensaje':mensaje, 'temporaryBus':temporaryBus},  context_instance=RequestContext(request))

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
    stopList = []
    temporaryStop = None
    mensaje = ''
    
    #logica
    try:
        if (userData.categoria == 'Administrador' or userData.categoria == 'Empresa'):
            if request.method == 'POST':
                try:
                    form = StopForm(request.POST)
                    if form.is_valid():
                        action = form.cleaned_data['action']
                        stopOrder = form.cleaned_data['orden']
                        temporaryRoute= Recorrido.objects.get(idrecorrido = form.cleaned_data['linea'])
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
        form = StopForm()
        errorDescription = "No existen paradas"
    logger.info("Usuario: " + userData.nombre +" in Stop Error:" + errorDescription)
    return render_to_response('stopdata.html',  {'user': request.user,'form':form,  'error': errorDescription, 'admin': True, 'superadmin':superadmin, 'stopList': stopList, 'mensaje':mensaje, 'temporaryStop':temporaryStop},  context_instance=RequestContext(request))

def validateFrecuency(frecuency):
    error = ''
    try:
        if frecuency == '':
            error = 'La frecuencia no puede ser nula/vacia'
        elif int(frecuency) <= 0:
            error = 'La frecuencia debe ser mayor que 0'
    except ValueError:
        error = "La frecuencia debe ser un numero entero"
    return error
