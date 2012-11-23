from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from tibus.models import Recorrido, Parada

class PredictionForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.filter(predictable = True), empty_label='Seleccione una linea', label='Linea')
    linea.widget.attrs["onchange"]="this.form.submit()"
    orden = forms.ModelChoiceField(queryset=Parada.objects.none(), empty_label='Debe Seleccionar la linea primero', label='Parada', required=False)
    apto = forms.BooleanField(required=False, label='Vehiculo con Rampa')
    
    def __init__(self, *args, **kwargs):
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
        
    def setQueryOrden(self, lineaId):
        self.fields['orden'].queryset = Parada.objects.filter(linea = lineaId)
        self.fields['orden'].empty_label = None
        self._errors = {}
        self.helper.add_input(Submit('action', 'resultado'))
        
class ItineraryForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label='Seleccione una linea', label='Linea')
    linea.widget.attrs["onchange"]="this.form.submit()"
    
    def __init__(self, *args, **kwargs):
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
        
    def quitEmptyOption(self):
        self.fields['linea'].empty_label = None