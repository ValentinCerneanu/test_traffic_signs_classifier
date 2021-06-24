
from django import forms
from .models import *

class MyForm(forms.ModelForm):
    class Meta:
        model = TrafficSign
        fields = ['image']