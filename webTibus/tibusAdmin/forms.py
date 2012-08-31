from django import forms

#Formulario con los datos para cargar una parada
class FormularioParada(forms.Form):
    linea = forms.CharField(widget=forms.HiddenInput)
    orden = forms.IntegerField(required=False)
    latitud = forms.FloatField()
    longitud = forms.FloatField()
    calle1 = forms.CharField()
    calle2 = forms.CharField()
    paradaactiva = forms.BooleanField(required=False)
    
    def aumentarOrden(self):
        self.orden = self.orden +1

#Formulario con los datos para cargar una linea
class FormularioRecorrido(forms.Form):
    linea = forms.CharField()
    frecuencia = forms.IntegerField()
    empresa = forms.CharField(widget=forms.HiddenInput)
    masivo = forms.FileField(required=False)
    
#Formulario con los datos para cargar una unidad de colectivo
class FormularioUnidad(forms.Form):
    linea = forms.CharField(widget=forms.HiddenInput)
    aptoMovilidadReducida = forms.BooleanField(required=False)
    id_unidad_linea = forms.IntegerField()

class FormularioEmpresa(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    
class FormularioUsuario(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    categoria = forms.CharField(widget=forms.HiddenInput)
    empresa = forms.CharField(required=False, widget=forms.HiddenInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirmacion = forms.CharField(widget=forms.PasswordInput)

class FormularioPassword(forms.Form):
    nombre = forms.CharField(widget=forms.HiddenInput)
    oldPassword = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(widget=forms.PasswordInput)
    confirmacion = forms.CharField(widget=forms.PasswordInput)
