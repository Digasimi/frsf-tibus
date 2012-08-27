# Create your views here.

from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max
from tibusAdmin.forms import FormularioParada,  FormularioRecorrido,  FormularioUnidad, FormularioEmpresa,  FormularioUsuario,\
    FormularioPassword
from tibus.models import Parada,  Recorrido,  Unidad, Empresa, Usuario
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

@login_required
def tadmin(request):#pagina de ABM de lineas
    return HttpResponseRedirect('linea')

@login_required
def linea(request):#pagina de ABM de lineas
    #carga inicial
    c = {}
    c.update(csrf(request))
    descripcionError = ""
    datosUsuario = Usuario.objects.get(nombre = request.user)
    listaLinea = []
    listaEmpresa = []
    
    if (datosUsuario.categoria == 'Administrador'):
        listaEmpresa = Empresa.objects.all()        
        listaLinea = Recorrido.objects.all().order_by('linea')
    elif (datosUsuario.categoria == 'Empresa'):
        listaEmpresa = Empresa.objects.filter(nombre = datosUsuario.empresa)   
        listaLinea = Recorrido.objects.filter(empresa = datosUsuario.empresa).order_by('linea')
    
    #logica
    if (datosUsuario.categoria == 'Administrador' or datosUsuario.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                form = FormularioRecorrido(request.POST, request.FILES)
                idLinea=request.POST.get('linea').upper()
                if request.POST.get('accion') == 'viewEmpresa':
                    listaLinea = Recorrido.objects.filter(empresa__nombre =request.POST.get('empresa').upper()).order_by('linea')
                elif idLinea == '': #comprueba que se ingresa linea
                    descripcionError = "No ingreso la linea"
                elif request.POST.get('accion') == 'viewLinea':          #no necesitaria el is_valid, solo que exista linea
                    direccion = 'recorrido/' + idLinea #carga la pagina de edicion de paradas asociadas a la linea ingresada
                    return HttpResponseRedirect(direccion)
                elif form.is_valid():
                    if request.POST.get('accion') == 'addLinea':
                        newFrec = request.POST.get('frecuencia')
                        newEmpresa = request.POST.get('empresa').upper()
                        if int(newFrec) > 0: #compueba que la frecuencia sea un entero mayor a 0
                            newLinea = Recorrido(linea = idLinea,  frecuencia = newFrec, empresa = Empresa.objects.get(nombre=newEmpresa)) 
                            if newLinea.validar(): #comprobacion de datos de linea
                                try:
                                    newLinea = Recorrido.objects.get(linea = idLinea) #da verdadero si la linea existe ya.
                                    descripcionError = "Linea ya existente"
                                except Recorrido.DoesNotExist:
                                    newLinea.save()
                                    try:
                                        if (request.FILES['masivo'] != ''):
                                            nombreArchivo = request.FILES['masivo']
                                            ordenTemp = 0
                                            errores = 0
                                            for linea in nombreArchivo:
                                                valores = linea.split(';') #aca se debe hacer la carga de archivos masivos
                                                calleTemp1=''
                                                calleTemp2=''
                                                try:
                                                    parLat = float(valores[0])
                                                    parLon = float(valores[1])
                                                    calleTemp1 = valores[2]
                                                    calleTemp2 = valores[3]
                                                    ordenTemp = ordenTemp + 1
                                                    newParada = Parada(orden = ordenTemp,  latitud = parLat, longitud = parLon, linea = newLinea, calle1 = calleTemp1, calle2 = calleTemp2)  
                                                    newParada.save()
                                                except:
                                                    errores = errores + 1
                                                    descripcionError = "se encontraron " + str(errores) + " errores de datos"
                                            print ordenTemp
                                    except MultiValueDictKeyError:
                                        descripcionError = "Faltan cargar paradas"
                            else:
                                descripcionError = "Identificador no valido"
                        else:
                            descripcionError = "La frecuencia debe ser un numero entero mayor a 0"
                    elif request.POST.get('accion') == 'editLinea':  #edicion de linea.
                        nombreArchivo = request.FILES['file']
                        newLinea = Recorrido.objects.get(linea = idLinea)
                        newLinea.frecuencia = int(request.POST.get('frecuencia'))
                        newLinea.save()
                    else: #if request.POST.get('accion') == 'delLinea': Asume que la accion por omision es borrar
                        #La confirmacion de la eliminacion es en el codigo html
                        newLinea = Recorrido.objects.get(linea = idLinea)
                        newLinea.delete() #el delete de django borra en cascada por defecto
                    #else:
                        #descripcionError = "Accion no valida"
                else:
                    descripcionError = "Falta algun dato o tipo de dato invalido"
            #empiezan las excepciones
            except Recorrido.DoesNotExist:
                descripcionError = "La linea ingresada no existe"
            except Empresa.DoesNotExist:
                descripcionError = "La empresa ingresada no existe"
        else:
            form = FormularioRecorrido()
    else:
        descripcionError = "No posee permisos para ejecutar esta accion"
    return render_to_response('linea.html',  {'usuario': request.user,'form':form,  'error':descripcionError , 'listaEmpresa': listaEmpresa, 'listaLinea': listaLinea,  'admin': True},  context_instance=RequestContext(request))

@login_required    
def unidad(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    listaUnidad=[]
    descripcionError = ""
    datosUsuario = Usuario.objects.get(nombre = request.user)
    listaLinea = []
    
    if (datosUsuario.categoria == 'Administrador'):
        listaLinea = Recorrido.objects.all().order_by('linea')
    elif (datosUsuario.categoria == 'Empresa'):
        listaLinea = Recorrido.objects.filter(empresa=datosUsuario.empresa).order_by('linea')
        
    #logica
    if (datosUsuario.categoria == 'Administrador' or datosUsuario.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                idLinea=request.POST.get('linea').upper()
                if request.POST.get('accion') == 'viewUnidad':
                    if idLinea == '': 
                        listaUnidad = Unidad.objects.all().order_by('id_unidad_linea')
                    else:
                        listaUnidad = Unidad.objects.filter(linea = Recorrido.objects.get(linea = idLinea)).order_by('id_unidad_linea')
                elif idLinea == '': #comprueba que se ingresa linea
                    descripcionError = "No ingreso la linea"
                    form = FormularioUnidad(request.POST)
                else:
                    newLinea = Recorrido.objects.get(linea = idLinea) #carga la linea.
                    newId=request.POST.get('id_unidad_linea').upper()
                    if form.is_valid():
                        if request.POST.get('accion') == 'addUnidad':
                            newApto = request.POST.get('aptoMovilidadReducida') 
                            if not(newApto):
                                newApto = 0;
                            try:
                                newUnidad = Unidad.objects.get(linea = newLinea, id_unidad_linea = newId) #da verdadero si la unidad ya existe
                                descripcionError = "Unidad ya existente"
                            except Unidad.DoesNotExist:
                                newUnidad = Unidad(linea = newLinea,  aptoMovilidadReducida = newApto,  idunidad = idLinea + "_" + newId, id_unidad_linea = newId)
                                newUnidad.save()
                        elif request.POST.get('accion') == 'editUnidad': 
                            newUnidad = Unidad.objects.get(linea = newLinea,  id_unidad_linea = newId)
                            newApto = request.POST.get('aptoMovilidadReducida') 
                            if newApto:
                                newUnidad.aptoMovilidadReducida = 1;
                            else:
                                newUnidad.aptoMovilidadReducida = 0;
                            newUnidad.save()
                        else: #if request.POST.get('accion') == 'delUnidad': Asume que la accion por omision es borrar
                            #La confirmacion de la eliminacion es en el codigo html
                            newUnidad = Unidad.objects.get(linea = newLinea,  id_unidad_linea = newId)
                            newUnidad.delete()
                        #else:
                            #descripcionError = "Accion no valida: " + str(request.POST.get('accion'))
                    else:
                        descripcionError = "Falta ingresar algun dato"
                    listaUnidad = Unidad.objects.filter(linea = newLinea).order_by('id_unidad_linea')
            #empiezan las excepciones
            except Recorrido.DoesNotExist:
                descripcionError = "No existe la linea"
            except Unidad.DoesNotExist:
                descripcionError = "No existe/n unidad/es"
            form = FormularioUnidad()
        else:
            form = FormularioUnidad()
            listaUnidad = Unidad.objects.all().order_by('id_unidad_linea')
    else:
        descripcionError = "No posee permisos para ejecutar esta accion"
    return render_to_response('unidad.html',  {'usuario': request.user,'form':form,  'error': descripcionError,  'listaUnidad':listaUnidad,  'admin': True,  'listaLinea': listaLinea},  context_instance=RequestContext(request))

@login_required    
def recorrido(request): #Pagina de ABM de paradas
    c = {}
    c.update(csrf(request))
    idLinea = request.POST.get('linea')
    descripcionError = ""
    datosUsuario = Usuario.objects.get(nombre = request.user)    
    
    if (datosUsuario.categoria == 'Administrador'):
        listaLineas = Recorrido.objects.all().order_by('linea')
        listaParadas = Parada.objects.all()
    elif (datosUsuario.categoria == 'Empresa'):
        listaLineas = Recorrido.objects.filter(empresa=datosUsuario.empresa).order_by('linea')
        if idLinea == '' or idLinea == None:
            listaParadas = Parada.objects.filter(linea__empresa = datosUsuario.empresa)
        else:
            listaParadas = Parada.objects.filter(linea__empresa = datosUsuario.empresa,  linea__linea = idLinea)
    
    #logica
    if (datosUsuario.categoria == 'Administrador' or datosUsuario.categoria == 'Empresa'):
        try:
            #if request.method == 'POST':
                form = FormularioParada()
                if idLinea == '' or idLinea == None:
                    form = FormularioParada()
                    descripcionError = "No ingreso la linea"
                else:
                    idLinea = idLinea.upper()
                    newId= Recorrido.objects.get(linea = idLinea)
                    listaParadas = Parada.objects.filter(linea = newId).order_by('orden')
                    if request.POST.get('accion') == 'viewLinea':
                        form = FormularioParada()
                        return render_to_response('recorrido.html', {'form': form,  'linea': idLinea, 'listaLineas': listaLineas, 'listaParadas': listaParadas,  'admin': True}, context_instance=RequestContext(request))
                    else:
                        parOrden = request.POST.get('orden')
                        if parOrden == None or parOrden == '':
                            parOrden = 0
                        try:
                            if int(parOrden) >= 0:  #comprueba que el orden sea un entero mayor que 0
                                if request.POST.get('accion') == 'viewParada':
                                    parada = Parada.objects.filter(linea = newId,  orden = int(parOrden))
                                elif request.POST.get('accion') == 'addParada':
                                    parLat = float(request.POST.get('newlatitud'))
                                    parLon = float(request.POST.get('newlongitud'))
                                    calleT1 = request.POST.get('calle1')
                                    calleT2 = request.POST.get('calle2')
                                    activa = request.POST.get('paradaActiva')
                                    if not(activa):
                                        activa = 0
                                    if len(listaParadas) == 0: #comprueba que no sea la primer parada
                                        parOrden = 1
                                    elif parOrden != 0: #agrega la parada en una posicion especifica
                                        for paradaTemp in listaParadas: 
                                            if paradaTemp.ordenParada() > int(parOrden): 
                                                paradaTemp.aumentarOrden()
                                                paradaTemp.save()
                                        listaParadas = ordenarListaParadas(Parada.objects.filter(linea = newId).order_by('orden'))
                                    else: #agrega la parada al final del recorrido
                                        parOrden = listaParadas.aggregate(orden=Max('orden')).get('orden') + 1
                                    newParada = Parada(orden = parOrden,  latitud = parLat, longitud = parLon, linea = newId, calle1 = calleT1,calle2 = calleT2,paradaActiva = activa)  
                                    newParada.save()
                                elif request.POST.get('accion') == 'editParada': #sin revisar - Falta ver que pasa si se cambia el orden.
                                    newParada = Parada.objects.get(orden = int(parOrden),  linea = newId)  
                                    newParada.latitud = float(request.POST.get('newlatitud'))
                                    newParada.longitud = float(request.POST.get('newlongitud'))
                                    newParada.calle1 = request.POST.get('calle1')
                                    newParada.calle2 = request.POST.get('calle2')
                                    if request.POST.get('paradaActiva'):
                                        newParada.paradaActiva = True
                                    else:
                                        newParada.paradaActiva = False  
                                    newParada.save()
                                else: #if request.POST.get('accion') == 'delParada':  Asume que la accion por omision es borrar
                                    #La confirmacion de la eliminacion es en el codigo html
                                    newParada = Parada.objects.get(orden = parOrden,  linea = newId)  
                                    newParada.delete()
                                    #!reacomodar paradas                
                                    for paradaTemp in listaParadas: 
                                        if paradaTemp.ordenParada() > int(parOrden): 
                                            paradaTemp.disminuirOrden()
                                            paradaTemp.save()
                                    listaParadas = ordenarListaParadas(Parada.objects.filter(linea = newId).order_by('orden'))
                                #else:
                                    #descripcionError = "Accion no valida"
                            else:
                                descripcionError = "El orden debe ser un numero entero mayor a 0"
                        except ValueError:
                            descripcionError = "El orden debe ser un numero entero"
                        except TypeError:
                            descripcionError = "Las coordenadas no pueden ser vacias"
                    listaParadas = Parada.objects.filter(linea__linea = idLinea).order_by('orden') # para actualizar cambios en la lista de paradas
        #empiezan las excepciones
        except Recorrido.DoesNotExist:
            listaLinea = Recorrido.objects.all()
            return render_to_response('linea.html',  {'usuario': request.user,'form':FormularioRecorrido(),  'error': "No ingreso una linea valida" , 'listaLinea': listaLinea,  'admin': True},  context_instance=RequestContext(request))
        except Parada.DoesNotExist:
            form = FormularioParada()
            descripcionError = "No existen paradas"
    else:
        descripcionError = "No posee permisos para ejecutar esta accion"
    return render_to_response('recorrido.html', {'usuario': request.user,'form': form,  'linea': idLinea, 'listaLineas': listaLineas, 'listaParadas': listaParadas ,  'error': descripcionError,  'admin': True}, context_instance=RequestContext(request))

def ordenarListaParadas(listaParadas): #metodo para ordenar las paradas e evitar saltar el orden
    i=1
    for paradaTemp in listaParadas:
        if paradaTemp.ordenParada() > i:
            while paradaTemp.ordenParada() > i:
                paradaTemp.disminuirOrden()
            paradaTemp.save()
        i = i +1
    return listaParadas

@login_required    
def empresa(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    listaEmpresa=Empresa.objects.all().order_by('nombre')
    descripcionError = ""
    datosUsuario = Usuario.objects.get(nombre = request.user)
    
    if (datosUsuario.categoria == 'Administrador'):
        listaEmpresa = Empresa.objects.all()        
    elif (datosUsuario.categoria == 'Empresa'):
        listaEmpresa = Empresa.objects.filter(nombre = datosUsuario.empresa)   
        
    #logica
    if (datosUsuario.categoria == 'Administrador' or datosUsuario.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                idEmpresa=request.POST.get('nombre').upper()
                email=request.POST.get('email').lower()
                form = FormularioEmpresa(request.POST)
                if idEmpresa == '': #comprueba que el nombre no sea vacia.
                    descripcionError = "No ingreso la empresa"
                elif request.POST.get('accion') == 'addEmpresa':
                    if email == "": #comprobar direccion de mail, no comprueba formato.
                        descripcionError = "No ingreso datos validos"
                    else:
                        try:
                            newEmpresa = Empresa.objects.get(nombre = idEmpresa) #da verdadero si la linea ya existe.
                            descripcionError = "Empresa ya existente"
                        except:
                            newEmpresa = Empresa(nombre = idEmpresa,  mail = email)
                            newEmpresa.save()
                else:
                    newEmpresa = Empresa.objects.get(nombre = idEmpresa)
                    if request.POST.get('accion') == 'viewEmpresa':
                        newApto = 0; #aca falta hacer algo
                    elif request.POST.get('accion') == 'editEmpresa': 
                        newEmpresa.mail = email;
                        newEmpresa.save();
                    else: #if request.POST.get('accion') == 'delEmpresa': Asume que la accion por omision es borrar
                        #La confirmacion de la eliminacion es en el codigo html
                        newEmpresa.delete()
                #else:
                    #descripcionError = "Accion no valida: " + str(request.POST.get('accion'))
                listaEmpresa=Empresa.objects.all().order_by('nombre')
            #empiezan las excepciones
            except Empresa.DoesNotExist:
                descripcionError = "No existe la empresa"
        else:
            form = FormularioEmpresa()
    else:
        descripcionError = "No posee permisos para ejecutar esta accion"        
    return render_to_response('empresa.html',  {'usuario': request.user,  'admin': True,'form':form,  'error': descripcionError,  'listaEmpresa':listaEmpresa},  context_instance=RequestContext(request))

@login_required    
def usuario(request): #pagina de ABM de unidades - faltan excepciones
    #carga inicial
    c = {}
    c.update(csrf(request))
    descripcionError = ""
    datosUsuario = Usuario.objects.get(nombre = request.user)
    listaUsuario = []
    listaEmpresa = []
    listaCategoria = []
    
    if (datosUsuario.categoria == 'Administrador'):
        listaUsuario=Usuario.objects.filter(is_active = True ).order_by('nombre')
        listaEmpresa = Empresa.objects.all()        
        listaCategoria = ['Administrador', 'Empresa']
    elif (datosUsuario.categoria == 'Empresa'):
        listaUsuario=Usuario.objects.filter(is_active = True,  empresa = datosUsuario.empresa).order_by('nombre')
        listaEmpresa = Empresa.objects.filter(nombre = datosUsuario.empresa)   
        listaCategoria = ['Empresa']
        
    #logica
    if (datosUsuario.categoria == 'Administrador' or datosUsuario.categoria == 'Empresa'):
        if request.method == 'POST':
            try:
                form = FormularioUsuario(request.POST)
                idUsuario=request.POST.get('nombre').upper()
                if idUsuario == '': #comprueba que el nombre no sea vacia.
                    descripcionError = "No ingreso el nombre del usuario"
                elif request.POST.get('accion') == 'addUsuario':
                    if form.is_valid(): #comprobar direccion de mail, no comprueba formato.
                        email=request.POST.get('email').lower()
                        categoria=request.POST.get('categoria')
                        if (request.POST.get('empresa') != ""):
                            empresa = Empresa.objects.get(nombre = request.POST.get('empresa'))
                        else:
                            empresa = None
                        password=request.POST.get('password')
                        try:
                            newUsuario = Usuario.objects.get(nombre = idUsuario) #da verdadero si la linea ya existe.
                            descripcionError = "Usuario ya existente"
                        except:
                            if (password == request.POST.get('confirmacion')):
                                newUsuario = Usuario(username = idUsuario, nombre = idUsuario,  mail = email,  categoria=categoria,  empresa=empresa)
                                newUsuario.set_password(password)
                                if (categoria =='Administrador'):
                                    newUsuario.is_superuser = True
                                newUsuario.save()
                            else:
                                descripcionError = "Las passwords no coinciden"
                    else:
                        descripcionError = "No ingreso datos validos"
                else:
                    newUsuario = Usuario.objects.get(nombre = idUsuario)
                    if request.POST.get('accion') == 'viewUsuario': #No se usa
                        form = FormularioUsuario(email = request.POST.get('email').lower())
                    elif request.POST.get('accion') == 'rehabUsuario':
                        newUsuario.is_active = True
                        newUsuario.save()
                    elif request.POST.get('accion') == 'editUsuario': 
                        if(request.POST.get('email').lower() != ''):
                            newUsuario.mail=request.POST.get('email').lower()
                        if (password == request.POST.get('confirmacion')):
                            newUsuario.set_password(password)
                        else:
                            descripcionError = "Las passwords no coinciden"
                        newUsuario.save();
                    elif request.POST.get('accion') == 'delUsuario': #Asume que la accion por omision es borrar
                        #La confirmacion de la eliminacion es en el codigo html
                        if ((newUsuario.categoria == "Administrador") and (Usuario.objects.filter(categoria = "Administrador").count() > 1)):
                            descripcionError = "No se puede eliminar el ultimo usuario Administrador"
                        elif ((newUsuario.categoria == "Empresa")and(newUsuario.nombre != datosUsuario.nombre)):
                            descripcionError = "No se puede eliminar otro usuario de igual Jerarquia"
                        elif((newUsuario.categoria == "Empresa")and(newUsuario.categoria == "Administrador")):
                            descripcionError = "No se puede eliminar otro usuario de mayor Jerarquia"
                        else:
                            newUsuario.is_active = False
                            newUsuario.save()
                #else:
                    #descripcionError = "Accion no valida: " + str(request.POST.get('accion'))
                listaUsuario=Usuario.objects.filter(is_active = True ).order_by('nombre')
            #empiezan las excepciones
            except Usuario.DoesNotExist:
                descripcionError = "No existe el usuario"
            except Empresa.DoesNotExist:
                descripcionError = "No existe la empresa"
        else:
            form = FormularioUsuario()
    else:
        descripcionError = "No posee permisos para ejecutar esta accion"        
    return render_to_response('usuario.html',  {'usuario': request.user,'form':form,  'error': descripcionError,  'listaUsuarios':listaUsuario,  'admin': True,  'listaEmpresa' : listaEmpresa,  'listaCategoria':listaCategoria},  context_instance=RequestContext(request))

@login_required
def recorridoLinea(request, idLinea): #Pagina de ABM de paradas
    #carga inicial
    c = {}
    c.update(csrf(request))
    descripcionError = ""
    datosUsuario = Usuario.objects.get(nombre = request.user)    
    
    if (datosUsuario.categoria == 'Administrador'):
        listaLineas = Recorrido.objects.all().order_by('linea')
        listaParadas = Parada.objects.all()
    elif (datosUsuario.categoria == 'Empresa'):
        listaLineas = Recorrido.objects.filter(empresa=datosUsuario.empresa).order_by('linea')
        if idLinea == '' or idLinea == None:
            listaParadas = Parada.objects.filter(linea__empresa = datosUsuario.empresa)
        else:
            listaParadas = Parada.objects.filter(linea__empresa = datosUsuario.empresa,  linea__linea = idLinea)
    
    #logica
    if (datosUsuario.categoria == 'Administrador' or datosUsuario.categoria == 'Empresa'):
        try:
            #if request.method == 'POST':
                form = FormularioParada()
                if idLinea == '' or idLinea == None:
                    form = FormularioParada()
                    descripcionError = "No ingreso la linea"
                else:
                    idLinea = idLinea.upper()
                    newId= Recorrido.objects.get(linea = idLinea)
                    listaParadas = Parada.objects.filter(linea = newId).order_by('orden')
                    if request.POST.get('accion') == 'viewLinea':
                        form = FormularioParada()
                        return render_to_response('recorrido.html', {'form': form,  'linea': idLinea, 'listaLineas': listaLineas, 'listaParadas': listaParadas,  'admin': True}, context_instance=RequestContext(request))
                    else:
                        parOrden = request.POST.get('orden')
                        if parOrden == None or parOrden == '':
                            parOrden = 0
                        try:
                            if int(parOrden) >= 0:  #comprueba que el orden sea un entero mayor que 0
                                if request.POST.get('accion') == 'viewParada':
                                    parada = Parada.objects.filter(linea = newId,  orden = int(parOrden))
                                elif request.POST.get('accion') == 'addParada':
                                    parLat = float(request.POST.get('newlatitud'))
                                    parLon = float(request.POST.get('newlongitud'))
                                    calleT1 = request.POST.get('calle1')
                                    calleT2 = request.POST.get('calle2')
                                    activa = request.POST.get('paradaActiva')
                                    if not(activa):
                                        activa = 0
                                    if len(listaParadas) == 0: #comprueba que no sea la primer parada
                                        parOrden = 1
                                    elif parOrden != 0: #agrega la parada en una posicion especifica
                                        for paradaTemp in listaParadas: 
                                            if paradaTemp.ordenParada() > int(parOrden): 
                                                paradaTemp.aumentarOrden()
                                                paradaTemp.save()
                                        listaParadas = ordenarListaParadas(Parada.objects.filter(linea = newId).order_by('orden'))
                                    else: #agrega la parada al final del recorrido
                                        parOrden = listaParadas.aggregate(orden=Max('orden')).get('orden') + 1
                                    newParada = Parada(orden = parOrden,  latitud = parLat, longitud = parLon, linea = newId, calle1 = calleT1,calle2 = calleT2,paradaActiva = activa)  
                                    newParada.save()
                                elif request.POST.get('accion') == 'editParada': #sin revisar - Falta ver que pasa si se cambia el orden.
                                    newParada = Parada.objects.get(orden = int(parOrden),  linea = newId)  
                                    newParada.latitud = float(request.POST.get('newlatitud'))
                                    newParada.longitud = float(request.POST.get('newlongitud'))
                                    newParada.calle1 = request.POST.get('calle1')
                                    newParada.calle2 = request.POST.get('calle2')
                                    if request.POST.get('paradaActiva'):
                                        newParada.paradaActiva = True
                                    else:
                                        newParada.paradaActiva = False 
                                    newParada.save()
                                else: #if request.POST.get('accion') == 'delParada':  Asume que la accion por omision es borrar
                                    #La confirmacion de la eliminacion es en el codigo html
                                    newParada = Parada.objects.get(orden = parOrden,  linea = newId)  
                                    newParada.delete()
                                    #!reacomodar paradas                
                                    for paradaTemp in listaParadas: 
                                        if paradaTemp.ordenParada() > int(parOrden): 
                                            paradaTemp.disminuirOrden()
                                            paradaTemp.save()
                                    listaParadas = ordenarListaParadas(Parada.objects.filter(linea = newId).order_by('orden'))
                                #else:
                                    #descripcionError = "Accion no valida"
                            else:
                                descripcionError = "El orden debe ser un numero entero mayor a 0"
                        except ValueError:
                            descripcionError = "El orden debe ser un numero entero"
                        except TypeError:
                            descripcionError = "Las coordenadas no pueden ser vacias"
                    listaParadas = Parada.objects.filter(linea__linea = idLinea).order_by('orden') # para actualizar cambios en la lista de paradas
        #empiezan las excepciones
        except Recorrido.DoesNotExist:
            listaLinea = Recorrido.objects.all()
            return render_to_response('linea.html',  {'usuario': request.user,'form':FormularioRecorrido(),  'error': "No ingreso una linea valida" , 'listaLinea': listaLinea,  'admin': True},  context_instance=RequestContext(request))
        except Parada.DoesNotExist:
            form = FormularioParada()
            descripcionError = "No existen paradas"
    else:
        descripcionError = "No posee permisos para ejecutar esta accion"
    return render_to_response('recorrido.html', {'usuario': request.user,'form': form,  'linea': idLinea, 'listaLineas': listaLineas, 'listaParadas': listaParadas ,  'error': descripcionError,  'admin': True}, context_instance=RequestContext(request))

@login_required
def cambiarpassword(request):
    descripcionError = ""
    if request.method == 'POST':
        form = FormularioPassword(request.POST)
        usuario = Usuario.objects.get(nombre = request.user)
        if(request.POST.get('newPassword')==request.POST.get('confirmacion')):
            if(usuario.check_password(request.POST.get('oldPassword'))):
                usuario.set_password(request.POST.get('newPassword'))
                usuario.save()
                descripcionError = 'La password se cambio con exito'
            else:
                descripcionError = 'El password ingresada no es la correcta'
        else:
            descripcionError = 'Los passwords no coinciden'
    else:
        form = FormularioPassword()
    return render_to_response('change_password.html', {'usuario': request.user, 'form': form, 'error': descripcionError,  'admin': True}, context_instance=RequestContext(request))