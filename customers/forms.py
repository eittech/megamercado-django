from django import forms
from .models import Customer


class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('image',) 
