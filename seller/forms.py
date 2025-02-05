from django import forms
from . import models

class StoreForm(forms.ModelForm):
    class Meta:
        model = models.Seller
        fields = '__all__'
        exclude = ['user']