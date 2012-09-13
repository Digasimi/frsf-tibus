from django import forms

class PredictionForm(forms.Form):
    linea = forms.CharField(widget=forms.HiddenInput)
    orden = forms.IntegerField(widget=forms.HiddenInput)