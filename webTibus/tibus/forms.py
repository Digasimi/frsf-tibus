from django import forms
from tibus.models import Recorrido, Parada

class PredictionForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Recorrido.objects.all(), empty_label=None)
    orden = forms.ModelChoiceField(queryset=Parada.objects.all(), empty_label=None)
    apto = forms.BooleanField(required=False)