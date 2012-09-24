from django import forms

#Formulario con los datos para cargar una parada
class StopForm(forms.Form):
    linea = forms.CharField(widget=forms.HiddenInput)
    orden = forms.IntegerField(required=False)
    latitud = forms.FloatField()
    longitud = forms.FloatField()
    calle1 = forms.CharField()
    calle2 = forms.CharField()
    paradaactiva = forms.BooleanField(required=False)
    
    def upOneOrder(self):
        self.orden = self.orden +1

#Formulario con los datos para cargar una route
class RouteForm(forms.Form):
    linea = forms.CharField()
    frecuencia = forms.IntegerField()
    empresa = forms.CharField(widget=forms.HiddenInput)
    masivo = forms.FileField(required=False)
    
#Formulario con los datos para cargar una unidad de colectivo
class BusForm(forms.Form):
    linea = forms.CharField(widget=forms.HiddenInput)
    apto_movilidad_reducida = forms.BooleanField(required=False)
    id_unidad_linea = forms.IntegerField()
    action = forms.CharField(widget=forms.HiddenInput)

class CompanyForm(forms.Form):
    idcompany = forms.IntegerField(widget=forms.HiddenInput, required=False)
    nombre = forms.CharField()
    email = forms.EmailField()
    action = forms.CharField(widget=forms.HiddenInput)
    
class UserForm(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    categoria = forms.CharField(widget=forms.HiddenInput)
    empresa = forms.CharField(required=False, widget=forms.HiddenInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirmacion = forms.CharField(widget=forms.PasswordInput)
    action = forms.CharField(widget=forms.HiddenInput)
    
class PassworForm(forms.Form):
    nombre = forms.CharField(widget=forms.HiddenInput)
    oldPassword = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(widget=forms.PasswordInput)
    confirmacion = forms.CharField(widget=forms.PasswordInput)
