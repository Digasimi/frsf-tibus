from django import forms
from tibus.models import Empresa, Recorrido

#Formulario con los datos para cargar una parada
class StopForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None)
    orden = forms.IntegerField(required=False)
    latitud = forms.FloatField(required=False)
    longitud = forms.FloatField(required=False)
    calle1 = forms.CharField(required=False)
    calle2 = forms.CharField(required=False)
    paradaactiva = forms.BooleanField(required=False)
    action = forms.CharField(widget=forms.HiddenInput)
    
    def upOneOrder(self):
        self.orden = self.orden +1

#Formulario con los datos para cargar una route
class RoutesForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label=None)
    
class RouteForm(forms.Form):
    linea = forms.CharField()
    frecuencia = forms.IntegerField()
    orden = forms.IntegerField(required=False, widget=forms.HiddenInput)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label=None)
    masivo = forms.FileField(required=False, help_text = "Las paradas deben estan en orden y una por linea con el formato: Latitud; Longitud;Calle;Interseccion")
    action = forms.CharField(widget=forms.HiddenInput)
    
#Formulario con los datos para cargar una unidad de colectivo
class BusForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None)
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
    email = forms.EmailField(required=False)
    categoria = forms.CharField(widget=forms.HiddenInput, required=False)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label="Todas")
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirmacion = forms.CharField(widget=forms.PasswordInput, required=False)
    action = forms.CharField(widget=forms.HiddenInput)
    
class PassworForm(forms.Form):
    nombre = forms.CharField(widget=forms.HiddenInput)
    oldPassword = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(widget=forms.PasswordInput)
    confirmacion = forms.CharField(widget=forms.PasswordInput)
