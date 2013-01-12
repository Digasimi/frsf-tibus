from django import forms
from tibus.models import Empresa, Recorrido, Parada, DIASSEMANA
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import FormActions

#Formulario para la cara masiva y seleccion de paradas
class StopsForm(forms.Form):
    identificador = forms.IntegerField(required=False, widget=forms.HiddenInput)
    masivo = forms.FileField(required=False, help_text = "Las paradas deben estan en orden y una por linea con el formato: Latitud; Longitud;Calle;Interseccion",label='Archivo con lista de paradas')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-StopListForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Lista de paradas',
                'identificador',
                'masivo',
                'action',                            
            ),
            FormActions(
                Submit('action', 'Carga Masiva', css_class="btn-primary btn-block"),
                Submit('action', 'Agregar', css_class="btn-primary btn-block"),
                Submit('action', 'Modificar', css_class="btn-primary btn-block"),
                Submit('action', 'Eliminar', css_class="btn-primary btn-block"),
                Submit('action', 'Volver', css_class="btn-primary btn-block")
            ),
        )
        super(StopsForm, self).__init__(*args, **kwargs)
        
#Formulario para la carga de paradas
class StopForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None, widget=forms.HiddenInput)
    orden = forms.ModelChoiceField(queryset=Parada.objects.all(), required=False, empty_label='Parada Inicial', label='Insertar despues de')
    latitud = forms.FloatField(required=False, label='Latitud',widget=forms.HiddenInput)
    longitud = forms.FloatField(required=False, label='Longitud',widget=forms.HiddenInput)
    calle1 = forms.CharField(label='Nombre de la Calle')
    calle2 = forms.CharField(required=False, label='Nombre de la Interseccion')
    paradaactiva = forms.BooleanField(required=False, label='Parada Activa')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def upOneOrder(self):
        self.orden = self.orden +1
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-StopForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Datos de la parada',
                'linea',
                'orden',
                'latitud',
                'longitud',
                'calle1',
                'calle2',
                'paradaactiva',
                'action'                
            ),
            ButtonHolder(
                Submit('save', 'Guardar', css_class='button white'),
                Submit('save', 'Volver', css_class='button white')
            )
        )
        super(StopForm, self).__init__(*args, **kwargs)
        
    def setStopList(self, lineaId): #funcion que actualiza la lista de paradas al cambiar la seleccion de la linea
        self.fields['orden'].queryset = Parada.objects.filter(linea = lineaId).order_by('orden')
        
    def setEditOption(self):
        self.fields['orden'].widget.attrs["disabled"]="disabled"

#Formulario para la lista de route
class RoutesForm(forms.Form):
    identificador = forms.CharField(label='Nombre/identificador de la linea',initial='0', widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-RoutesForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Acciones',
                'identificador',                                
            ),
            FormActions(
                Submit('action','Agregar', css_class="btn-primary btn-block"),
                Submit('action','Modificar', css_class="btn-primary btn-block"),
                Submit('action','Eliminar', css_class="btn-primary btn-block")
            ),
        )
        super(RoutesForm, self).__init__(*args, **kwargs)

#Formulario para la carga de route    
class RouteForm(forms.Form):
    linea = forms.CharField(label='Nombre/identificador de la linea')
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label=None,label='Empresa asociada')
    predictable = forms.BooleanField(required=False, label='Permitir Prediccion')
    action = forms.CharField(widget=forms.HiddenInput)
    
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-RouteForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Datos de la linea',
                'linea',
                'empresa',
                'predictable',
                'action',
            ),
            ButtonHolder(
                Submit('save', 'Guardar', css_class='button white'),
                Submit('stops', 'Paradas', css_class='button white'),
                Submit('frecuency', 'Frecuencias', css_class='button white')
            )
        )
        super(RouteForm, self).__init__(*args, **kwargs)
        
    def filtrarEmpresa(self, companyUser):
        self.fields['empresa'].queryset = Empresa.objects.filter(nombre = companyUser.getName())
    
#Formulario para la lista de unidades
class BussForm(forms.Form):
    identificador = forms.CharField(label='Nombre/identificador de la unidad',initial='0', widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-BussForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Acciones',
                'identificador',                                
            ),
            FormActions(
                Submit('action','Agregar', css_class="btn-primary btn-block"),
                Submit('action','Modificar', css_class="btn-primary btn-block"),
                Submit('action','Eliminar', css_class="btn-primary btn-block")
            ),
        )
        super(BussForm, self).__init__(*args, **kwargs)
        
#Formulario con los datos para cargar una unidad de colectivo
class BusForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all().order_by('linea'), empty_label=None, label='Linea la que pertenece la unidad')
    apto_movilidad_reducida = forms.BooleanField(required=False, label ='Unidad con rampa')
    id_unidad_linea = forms.IntegerField(label='Identificador interno de la empresa')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-BusForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Unidad',
                'linea',
                'apto_movilidad_reducida',
                'id_unidad_linea',
                'action'                                
            ),
            FormActions(
                Submit('save', 'Guardar', css_class="btn-primary")                
            ),
        )
        super(BusForm, self).__init__(*args, **kwargs)
        
    def filtrarEmpresa(self, companyUser):
        self.fields['linea'].queryset = Recorrido.objects.filter(empresa__nombre = companyUser).order_by('linea')
        
    def setEditOption(self):
        self.fields['linea'].widget.attrs["disabled"]="disabled"

#Formulario para la lista de empresas
class CompaniesForm(forms.Form):
    identificador = forms.CharField(label='Nombre/identificador de la empresa',initial='', widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-CompaniesForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Acciones',
                'identificador',                                
            ),
            FormActions(
                Submit('action','Agregar', css_class="btn-primary btn-block"),
                Submit('action','Modificar', css_class="btn-primary btn-block"),
                Submit('action','Eliminar', css_class="btn-primary btn-block")
            ),
        )
        super(CompaniesForm, self).__init__(*args, **kwargs)
        
#Formulario para la carga de company
class CompanyForm(forms.Form):
    nombre = forms.CharField(label='Nombre de la empresa')
    email = forms.EmailField(required=False, label='Email de contacto')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-CompanyForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Datos de la empresa',
                'nombre',
                'email',
                'action',                            
            ),
            FormActions(
                Submit('save', 'Guardar', css_class="btn-primary")                
            ),
        )
        super(CompanyForm, self).__init__(*args, **kwargs)

#Formulario para la lista de usuarios
class UsersForm(forms.Form):
    identificador = forms.CharField(label='Nombre del Usuario',initial='', widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-UsersForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Acciones',
                'identificador',                               
            ),
            FormActions(
                Submit('action','Agregar', css_class="btn-primary btn-block"),
                Submit('action','Modificar', css_class="btn-primary btn-block"),
                Submit('action','Eliminar', css_class="btn-primary btn-block")
            ),
        )
        super(UsersForm, self).__init__(*args, **kwargs)
            
#Formulario para la carga de user            
class UserForm(forms.Form):
    nombre = forms.CharField(label='Nombre')
    email = forms.EmailField(required=False,label='email')
    categoria = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Administrador','Administrador'),('Empresa','Empresa')], label='Categoria')
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label="Todas", label='Empresa',required=False)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirmacion = forms.CharField(widget=forms.PasswordInput, label='Confirmar Password')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-UserForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Datos de usuario',
                'nombre',
                'email',
                'categoria',
                'empresa',
                'password',
                'confirmacion',
                'action',                            
            ),
            FormActions(
                Submit('save', 'Guardar', css_class="btn-primary")                
            ),
        )
        super(UserForm, self).__init__(*args, **kwargs)
        
    def setEditOption(self):
        self.fields['categoria'].widget.attrs["disabled"]="disabled"
        self.fields['empresa'].widget.attrs["disabled"]="disabled"

#Formulario para el cambio de password    
class PasswordForm(forms.Form):
    nombre = forms.CharField(widget=forms.HiddenInput)
    oldPassword = forms.CharField(widget=forms.PasswordInput, label='Password anterior')
    newPassword = forms.CharField(widget=forms.PasswordInput, label='Password nueva')
    confirmacion = forms.CharField(widget=forms.PasswordInput, label='Confirmar password anterior')
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-PasswordForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Cambio de password',
                'nombre',
                'oldPassword',
                'newPassword',
                'confirmacion',
            ),
            FormActions(
                Submit('save', 'Guardar', css_class="btn-primary")                
            ),
        )
        super(PasswordForm, self).__init__(*args, **kwargs)

#Formulario generico para la confirmacion de la eliminacion        
class EliminarForm(forms.Form):
    identificador = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-EliminarForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Confirmacion de Eliminacion'
            ),
            FormActions(
                Submit('eliminar', 'Eliminar', css_class="btn-primary")                
            ),
        )
        super(EliminarForm, self).__init__(*args, **kwargs)      

#Formulario para la lista de frecuencie        
class FrecuenciesForm(forms.Form):
    identificador = forms.CharField(label='Frecuencia de Linea',initial='', widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-FrecuenciesForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Acciones',
                'identificador',                               
            ),
            FormActions(
                Submit('action','Agregar', css_class="btn-primary btn-block"),
                Submit('action','Eliminar', css_class="btn-primary btn-block")
            ),
        )
        super(FrecuenciesForm, self).__init__(*args, **kwargs)
            
#Formulario para la carga de frecuenia            
class FrecuencyForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None, label='Linea')
    dia = forms.CharField(label='Dia de la semana', widget=forms.Select(choices=DIASSEMANA))
    hora = forms.TimeField(label='Hora de salida de la unidad')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-FrecuencyForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Frecuencias de Recorrido',
                'linea',
                'dia',
                'hora',
                'action',                            
            ),
            FormActions(
                Submit('save', 'Guardar', css_class="btn-primary")                
            ),
        )
        super(FrecuencyForm, self).__init__(*args, **kwargs)