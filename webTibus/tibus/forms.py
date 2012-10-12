from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from tibus.models import Recorrido, Parada

class PredictionForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None, label='Linea', help_text='Nombre de la linea')
    orden = forms.ModelChoiceField(queryset=Parada.objects.all(), empty_label=None, label='Parada', help_text='Ubicacion de la parada')
    apto = forms.BooleanField(required=False, label='Vehiculo Especial', help_text='Vehiculo con Rampa')
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-predictionForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('action', 'prediction'))
        super(PredictionForm, self).__init__(*args, **kwargs)