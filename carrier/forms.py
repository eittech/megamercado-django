from django import forms
from .models import *

class CarrierShopForm(forms.ModelForm):
    '''
        Aqui se implementa el formulario para la creacion
        de nuevos carrier shop
    '''
    id_carrier = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=Carrier.objects.all())
    class Meta:
        '''
            Aqui se especifica que datos se tienen que incluir en
            el formulario
        '''
        model = CarrierShop
        fields=['id_carrier']