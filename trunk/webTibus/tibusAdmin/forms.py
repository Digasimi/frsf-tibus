from django import forms
from tibus.models import Empresa, Recorrido, Parada
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import FormActions

#Formulario con los datos para cargar una parada
class StopForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None, widget=forms.HiddenInput)
    orden = forms.ModelChoiceField(queryset=Parada.objects.all(), required=False, empty_label='Parada Inicial')
    latitud = forms.FloatField(required=False, label='Latitud')
    longitud = forms.FloatField(required=False, label='Longitud')
    calle1 = forms.CharField(label='Nombre de la Calle')
    calle2 = forms.CharField(required=False, label='Nombre de la Interseccion')
    paradaactiva = forms.BooleanField(required=False, label='Parada Activa')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def upOneOrder(self):
        self.orden = self.orden +1
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-StopForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        
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
            ),
            ButtonHolder(
                Submit('save', 'Guardar', css_class='button white')
            )
        )

        #self.helper.add_input(Submit('save', 'Guardar'))
        super(StopForm, self).__init__(*args, **kwargs)

#Formulario con los datos para cargar una route
class RoutesForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label=None)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-RoutesForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        
        self.helper.layout = Layout(
            Fieldset(
                'Datos de la parada',
                'linea',
                'empresa',                                
            ),
            FormActions(
                Submit('action', 'addRoute', css_class="btn-primary"),
                Submit('action','editRoute', css_class="btn-primary"),
                Submit('action','delRoute')
            ),
        )
        #self.helper.add_input(Submit('save', 'Guardar'))
        super(RoutesForm, self).__init__(*args, **kwargs)

    
class RouteForm(forms.Form):
    linea = forms.CharField(label='Nombre/identificador de la linea')
    frecuencia = forms.IntegerField(required=False,label='Frecuencia de salida')
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label=None,label='Empresa asociada')
    masivo = forms.FileField(required=False, help_text = "Las paradas deben estan en orden y una por linea con el formato: Latitud; Longitud;Calle;Interseccion",label='Archivo con lista de paradas')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-RouteForm'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('save', 'Guardar'))
        self.helper.add_input(Submit('stops', 'Paradas'))
        self.helper.add_input(Submit('frecuency', 'Frecuencias'))
        super(RouteForm, self).__init__(*args, **kwargs)
    
#Formulario con los datos para cargar una unidad de colectivo
class BusForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None, label='Linea la que pertenece la unidad')
    apto_movilidad_reducida = forms.BooleanField(required=False, label ='Unidad con rampa')
    id_unidad_linea = forms.IntegerField(label='Identificador interno de la empresa')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-BusForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        
        self.helper.layout = Layout(
            Fieldset(
                'Unidad',
                'linea',
                'apto_movilidad_reducida',
                'id_unidad_linea',                                
            ),
            FormActions(
                Submit('save', 'Guardar', css_class="btn-primary")                
            ),
        )

        #self.helper.add_input(Submit('save', 'Guardar'))
        super(BusForm, self).__init__(*args, **kwargs)

class CompanyForm(forms.Form):
    nombre = forms.CharField(label='Nombre de la empresa')
    email = forms.EmailField(required=False, label='Email de contacto')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-CompanyForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('save', 'Guardar'))
        super(CompanyForm, self).__init__(*args, **kwargs)
    
class UserForm(forms.Form):
    nombre = forms.CharField(label='Nombre')
    email = forms.EmailField(required=False,label='email')
    categoria = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Administrador','Administrador'),('Empresa','Empresa')], label='Categoria')
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label="Todas", label='Empresa')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirmacion = forms.CharField(widget=forms.PasswordInput, label='Confirmar Password')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-UserForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        
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

        #self.helper.add_input(Submit('save', 'Guardar'))
        super(UserForm, self).__init__(*args, **kwargs)
    
class PasswordForm(forms.Form):
    nombre = forms.CharField(widget=forms.HiddenInput)
    oldPassword = forms.CharField(widget=forms.PasswordInput, label='Password anterior')
    newPassword = forms.CharField(widget=forms.PasswordInput, label='Password nueva')
    confirmacion = forms.CharField(widget=forms.PasswordInput, label='Confirmar password anterior')
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-PasswordForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('save', 'Guardar'))
        super(PasswordForm, self).__init__(*args, **kwargs)

class StopsForm(forms.Form):
    orden = forms.IntegerField(required=False, label='Orden de la parada seleccionada')
    masivo = forms.FileField(required=False, help_text = "Las paradas deben estan en orden y una por linea con el formato: Latitud; Longitud;Calle;Interseccion",label='Archivo con lista de paradas')
    action = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-StopListForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('action', 'addMasiveStop'))
        self.helper.add_input(Submit('action', 'addStop'))
        self.helper.add_input(Submit('action', 'editStop'))
        self.helper.add_input(Submit('action', 'delStop'))
        super(StopsForm, self).__init__(*args, **kwargs)