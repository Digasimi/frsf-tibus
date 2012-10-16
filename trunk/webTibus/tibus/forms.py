from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from tibus.models import Recorrido, Parada

class PredictionForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None, label='Linea')
    orden = forms.ModelChoiceField(queryset=Parada.objects.all(), empty_label=None, label='Parada')
    apto = forms.BooleanField(required=False, label='Vehiculo con Rampa')
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-predictionForm'
        #self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'resultado'
        
        self.helper.layout = Layout(
            Fieldset(
                'Tiempos de arribo',
                'linea',
                'orden',
                'apto',
            ),
#            ButtonHolder(
#                Submit('submit', 'Consultar', css_class='button white')
#            )
        )

        self.helper.add_input(Submit('action', 'resultado'))
        super(PredictionForm, self).__init__(*args, **kwargs)