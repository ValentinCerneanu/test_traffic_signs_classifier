
from django import forms
 
class MyForm(forms.Form):
    name = forms.CharField()
    image = forms.ImageField()