from django import forms

#Formulario con los datos para cargar una parada
class FormularioParada(forms.Form):
    linea = forms.CharField()
    orden = forms.IntegerField()
    latitud = forms.FloatField()
    longitud = forms.FloatField()
    calle1 = forms.CharField()
    calle2 = forms.CharField()
    
    def aumentarOrden(self):
        orden = orden +1

#Formulario con los datos para cargar una linea
class FormularioRecorrido(forms.Form):
    linea = forms.CharField()
    frecuencia = forms.IntegerField()
    empresa = forms.CharField()
    masivo = forms.FileField(required=False)
    
#Formulario con los datos para cargar una unidad de colectivo
class FormularioUnidad(forms.Form):
    linea = forms.CharField()
    aptoMovilidadReducida = forms.BooleanField(required=False)
    id_unidad_linea = forms.IntegerField()

class FormularioPrediccion(forms.Form):
    linea = forms.CharField()
    orden = forms.IntegerField()
    
class FormularioEmpresa(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    
class FormularioUsuario(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    categoria = forms.CharField()
    empresa = forms.CharField()
    password = forms.CharField()
    confirmacion = forms.CharField()
