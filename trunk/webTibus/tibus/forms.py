from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from tibus.models import Recorrido, Parada

#Formulario de datos de Prediccion de arribo de unidad a parada
class PredictionForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.filter(predictable = True).order_by('linea'), empty_label='Seleccione una linea', label='Linea')
    linea.widget.attrs["onchange"]="this.form.submit()"
    orden = forms.ModelChoiceField(queryset=Parada.objects.none(), empty_label='Debe Seleccionar la linea primero', label='Parada', required=False)
    apto = forms.BooleanField(required=False, label='Vehiculo con Rampa')
    
    def __init__(self, *args, **kwargs): #inicializacion
        self.helper = FormHelper()
        self.helper.form_id = 'id-predictionForm'
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            Fieldset(
                'Tiempos de arribo',
                'linea',
                'orden',
                'apto',
            ),
        )
        super(PredictionForm, self).__init__(*args, **kwargs)
        
    def setQueryOrden(self, lineaId): #funcion que actualiza la lista de paradas al cambiar la seleccion de la linea
        self.fields['orden'].queryset = Parada.objects.filter(linea = lineaId)
        self.fields['orden'].empty_label = None
        self._errors = {}
        self.helper.add_input(Submit('action', 'resultado'))

#Formulario de datos para mostrar recorridos a usuarios        
class ItineraryForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all().order_by('linea'), empty_label='Seleccione una linea', label='Linea')
    linea.widget.attrs["onchange"]="this.form.submit()"
    
    def __init__(self, *args, **kwargs): #inicializacion
        self.helper = FormHelper()
        self.helper.form_id = 'id-itineraryForm'
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            Fieldset(
                'Recorrido',
                'linea',
            ),
        )
        super(ItineraryForm, self).__init__(*args, **kwargs)
        
    def quitEmptyOption(self): #funcion que actualiza la lista de paradas al cambiar la seleccion de la linea
        self.fields['linea'].empty_label = None

#Formulario de datos de Prediccion de viaje        
class TravelForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.filter(predictable = True).order_by('linea'), empty_label='Seleccione una linea', label='Linea')
    linea.widget.attrs["onchange"]="this.form.submit()"
    origen = forms.ModelChoiceField(queryset=Parada.objects.none(), empty_label='Debe Seleccionar la linea primero', label='Parada origen', required=False)
    destino = forms.ModelChoiceField(queryset=Parada.objects.none(), empty_label='Debe Seleccionar la linea primero', label='Parada destino', required=False)
    
    def __init__(self, *args, **kwargs): #inicializacion
        self.helper = FormHelper()
        self.helper.form_id = 'id-travelForm'
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            Fieldset(
                'Tiempos de viaje',
                'linea',
                'origen',
                'destino',
            ),
        )
        super(TravelForm, self).__init__(*args, **kwargs)
        
    def setQueryOrden(self, lineaId): #funcion que actualiza la lista de paradas al cambiar la seleccion de la linea
        self.fields['origen'].queryset = Parada.objects.filter(linea = lineaId).order_by('orden')
        self.fields['origen'].empty_label = None
        self.fields['destino'].queryset = Parada.objects.filter(linea = lineaId).order_by('orden')
        self.fields['destino'].empty_label = None
        self._errors = {}
        self.helper.add_input(Submit('action', 'resultado'))