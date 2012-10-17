from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from tibus.models import Recorrido, Parada

class PredictionForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None, label='Linea')
    orden = forms.ModelChoiceField(queryset=Parada.objects.all(), empty_label=None, label='Parada')
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

        self.helper.add_input(Submit('action', 'resultado'))
        super(PredictionForm, self).__init__(*args, **kwargs)